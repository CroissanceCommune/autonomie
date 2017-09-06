# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
import datetime
import logging
import colander
import deform

from beaker.cache import cache_region
from sqlalchemy import (
    Column,
    Date,
    Integer,
    String,
    Enum,
    Text,
    Boolean,
    ForeignKey,
    distinct,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)

from autonomie_base.models.base import (
    DBBASE,
    DBSESSION,
    default_table_args,
)
from autonomie.models.expense.types import ExpenseType
from autonomie.models.expense.payment import ExpensePayment
from autonomie.utils import strings
from autonomie import forms
from autonomie.forms.custom_types import (
    AmountType,
)
from autonomie.compute.expense import (
    ExpenseCompute,
    ExpenseLineCompute,
    ExpenseKmLineCompute,
)
from autonomie.compute.math_utils import (
    integer_to_amount,
)

from autonomie_base.models.types import PersistentACLMixin
from autonomie.models.action_manager import (
    Action,
    ActionManager,
)
from autonomie.models.user import get_deferred_user_choice
from autonomie.models.node import Node


logger = logging.getLogger(__name__)


PAID_STATES = (
    ('waiting', u"En attente"),
    ("paid", u"Partiellement payée"),
    ('resulted', u"Payée"),
)
ALL_STATES = ('draft', 'wait', 'valid', 'invalid')


def get_available_years():
    """
    Return the available years for ExpenseSheet creation
    """
    from autonomie.models.expense import ExpenseSheet
    years = [i[0] for i in DBSESSION().query(distinct(ExpenseSheet.year))]
    today = datetime.date.today()
    for i in (today.year - 1, today.year, today.year + 1):
        if i not in years:
            years.append(i)

    years.sort()
    return years


def _build_action_manager():
    """
    Return a state machine that allows ExpenseSheet status handling
    """
    manager = ActionManager()
    for status, icon, label, title, css in (
        (
            'valid', "ok-sign",
            u"Valider",
            u"Valider ce document (il ne pourra plus être modifié)",
            "btn btn-primary primary-action",
        ),
        (
            'wait',
            'time',
            u"Demander la validation",
            u"Enregistrer ce document et en demander la validation",
            "btn btn-primary primary-action",
        ),
        (
            'invalid',
            'trash',
            u"Invalider",
            u"Invalider ce document afin que l'entrepreneur le corrige",
            "btn btn-default",
        ),
        (
            'draft',
            'save',
            u"Enregistrer",
            u'Enregistrer en brouillon afin de modifier ce document '
            u'ultérieurement',
            'btn btn-default',
        ),
    ):
        action = Action(
            status,
            '%s.expensesheet' % (status,),
            status_attr='status',
            userid_attr='status_person_id',
            icon=icon,
            label=label,
            title=title,
            css=css,
        )
        manager.add(action)

    return manager


def _build_justified_state_manager():
    """
    Return a state manager for setting the justified status attribute on
    ExpenseSheet objects
    """
    manager = ActionManager()
    for status, icon, label, title, css in (
        (
            False,
            'fa fa-clock-o',
            u"En attente",
            u"Aucun justificatif n'a été reçu",
            "btn btn-default",
        ),
        (
            True,
            'fa fa-check',
            u"Reçus",
            u"Les justificatifs ont bien été reçus",
            "btn btn-default",
        ),
    ):
        action = Action(
            status,
            'set_justified.expensesheet',
            status_attr='justified',
            icon=icon,
            label=label,
            title=title,
            css=css,
        )
        manager.add(action)
    return manager


@colander.deferred
def deferred_unique_expense(node, kw):
    """
    Return a validator to check if the expense is unique
    """
    from autonomie.models.expense import ExpenseSheet
    request = kw['request']
    if isinstance(request.context, ExpenseSheet):
        company_id = request.context.company_id
        user_id = request.context.user_id
    else:
        if 'uid' in request.matchdict:
            user_id = request.matchdict['uid']
        else:
            user_id = request.user.id

        company_id = request.context.id

    def validator(node, value):
        """
        The validator
        """
        month = value['month']
        year = value['year']

        query = ExpenseSheet.query().filter_by(month=month)
        query = query.filter_by(year=year)
        query = query.filter_by(user_id=user_id)
        query = query.filter_by(company_id=company_id)
        if query.count() > 0:
            exc = colander.Invalid(
                node,
                u"Une note de dépense pour la période {0} {1} existe "
                u"déjà".format(
                    strings.month_name(month),
                    year,
                )
            )
            exc['month'] = u"Une note de dépense existe"
            exc['year'] = u"Une note de dépense existe"
            raise exc
    return validator


class ExpenseSheet(Node, ExpenseCompute):
    """
        Model representing a whole ExpenseSheet
        An expensesheet is related to a company and an employee (one user may
        have multiple expense sheets if it has multiple companies)
        :param company_id: The user's company id
        :param user_id: The user's id
        :param year: The year the expense is related to
        :param month: The month the expense is related to
        :param status: Status of the sheet
        :param comments: Comments added to this expense sheet
        :param status_user: The user related to statuschange
        :param lines: expense lines of this sheet
    """
    __tablename__ = 'expense_sheet'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'expensesheet'}
    __colanderalchemy_config__ = {
        "validator": deferred_unique_expense
    }
    id = Column(
        ForeignKey('node.id'),
        primary_key=True,
        info={"colanderalchemy": forms.EXCLUDED},
    )
    month = Column(
        Integer,
        info={
            "colanderalchemy": {
                "title": u"Mois",
                "widget": forms.get_month_select_widget({}),
                "validator": colander.OneOf(range(1, 13)),
                "default": forms.default_month,
            }
        }
    )
    year = Column(
        Integer,
        info={
            'colanderalchemy': {
                "title": u"Année",
                "widget": forms.get_year_select_deferred(
                    query_func=get_available_years
                ),
                "validator": colander.Range(
                    min=0, min_err=u"Veuillez saisir une année valide"
                ),
                "default": forms.default_year,
            }
        }
    )
    paid_status = Column(
        String(10),
        default='waiting',
        info={
            'colanderalchemy': {
                "title": u"Statut du paiement de la note de dépense",
                'widget': deform.widget.SelectWidget(values=PAID_STATES),
                'validator': colander.OneOf(dict(PAID_STATES).keys())
            }
        }
    )

    justified = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Justificatifs reçus",
            }
        }
    )

    status = Column(
        String(10),
        default='draft',
        info={
            'colanderalchemy': {
                "title": u"Statut de la note de dépense",
                'validator': colander.OneOf(ALL_STATES),
                'widget': deform.widget.SelectWidget(
                    values=zip(ALL_STATES, ALL_STATES)
                ),
            }
        }
    )
    status_user_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        info={
            'colanderalchemy': {
                "title": u"Dernier utilisateur à avoir modifié le document",
                'widget': get_deferred_user_choice()
            },
            "export": forms.EXCLUDED,
        }
    )
    status_date = Column(
        Date(),
        default=datetime.date.today,
        onupdate=datetime.date.today,
        info={
            'colanderalchemy': {
                "title": u"Date du dernier changement de statut",
            },
        }
    )

    exported = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {'title': u"A déjà été exportée ?"},
        }
    )

    company_id = Column(
        Integer,
        ForeignKey("company.id", ondelete="cascade"),
        info={
            "colanderalchemy": forms.EXCLUDED
        }
    )

    user_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        info={
            "colanderalchemy": forms.EXCLUDED
        }
    )

    # Relationships
    lines = relationship(
        "ExpenseLine",
        back_populates="sheet",
        cascade="all, delete-orphan",
        order_by="ExpenseLine.date",
        info={
            "colanderalchemy": {"title": u"Dépenses"}
        }
    )
    kmlines = relationship(
        "ExpenseKmLine",
        back_populates="sheet",
        cascade="all, delete-orphan",
        order_by="ExpenseKmLine.date",
        info={
            "colanderalchemy": {"title": u"Dépenses kilométriques"}
        }
    )
    company = relationship(
        "Company",
        backref=backref(
            "expenses",
            order_by="ExpenseSheet.month",
            cascade="all, delete-orphan",
        )
    )
    user = relationship(
        "User",
        primaryjoin="ExpenseSheet.user_id==User.id",
        info={
            'colanderalchemy': forms.EXCLUDED,
        },
        backref=backref(
            "expenses",
            order_by="ExpenseSheet.month",
            info={
                'colanderalchemy': forms.EXCLUDED,
                'export': {'exclude': True},
            },
            cascade="all, delete-orphan"
        ),
    )
    status_user = relationship(
        "User",
        primaryjoin="ExpenseSheet.status_user_id==User.id",
        info={
            'colanderalchemy': forms.EXCLUDED,
        }
    )
    communications = relationship(
        "Communication",
        back_populates="expense_sheet",
        order_by="desc(Communication.date)",
        cascade="all, delete-orphan",
        info={
            'colanderalchemy': forms.EXCLUDED,
        }
    )
    state_manager = _build_action_manager()
    justified_state_manager = _build_justified_state_manager()

    def __json__(self, request):
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),

            company_id=self.company_id,
            user_id=self.user_id,
            paid_status=self.paid_status,
            justified=self.justified,
            status=self.status,
            status_user_id=self.status_user_id,
            status_date=self.status_date.isoformat(),

            lines=[line.__json__(request) for line in self.lines],
            kmlines=[line.__json__(request) for line in self.kmlines],
            month=self.month,
            month_label=strings.month_name(self.month),
            year=self.year,
            attachments=[
                f.__json__(request)for f in self.children if f.type_ == 'file'
            ]
        )

    def set_status(self, status, request, **kw):
        """
        set the status of a task through the state machine
        """
        return self.state_manager.process(
            status,
            self,
            request,
            **kw
        )

    def check_status_allowed(self, status, request, **kw):
        return self.state_manager.check_allowed(status, self, request)

    def set_justified_status(self, status, request, **kw):
        """
        set the signed status of a task through the state machine
        """
        return self.justified_state_manager.process(
            status,
            self,
            request,
            **kw
        )

    def check_justified_status_allowed(self, status, request, **kw):
        return self.justified_state_manager.check_allowed(status, self, request)

    def get_company_id(self):
        """
            Return the if of the company associated to this model
        """
        return self.company_id

    # Payment stuff
    def record_payment(self, **kw):
        """
        Record a payment for the current expense
        """
        logger.debug("Recording a payment")
        resulted = kw.pop('resulted', False)

        payment = ExpensePayment()
        for key, value in kw.iteritems():
            setattr(payment, key, value)
        logger.info(u"Amount : {0}".format(payment.amount))
        self.payments.append(payment)

        user_id = kw.get('user_id')
        return self.check_resulted(force_resulted=resulted, user_id=user_id)

    def check_resulted(self, force_resulted=False, user_id=None):
        """
        Check if the expense is resulted or not and set the appropriate status
        """
        logger.debug(u"-> There still to pay : %s" % self.topay())
        if self.topay() <= 0 or force_resulted:
            self.paid_status = 'resulted'
        elif len(self.payments) > 0:
            self.paid_status = 'paid'
        else:
            self.paid_status = "waiting"

        return self

    def duplicate(self, year, month):
        sheet = ExpenseSheet()
        sheet.month = month
        sheet.year = year

        sheet.user_id = self.user_id
        sheet.company_id = self.company_id

        sheet.lines = [line.duplicate() for line in self.lines]
        sheet.kmlines = [line.duplicate() for line in self.kmlines]

        return sheet


class BaseExpenseLine(DBBASE, PersistentACLMixin):
    """
        Base models for expense lines
        :param type: Column for polymorphic discrimination
        :param date: Date of the expense
        :param description: description of the expense
        :param code: analytic code related to this expense
        :param valid: validation status of the expense
        :param sheet_id: id of the expense sheet this expense is related to
    """
    __tablename__ = 'baseexpense_line'
    __table_args__ = default_table_args
    __mapper_args__ = dict(
        polymorphic_on="type",
        polymorphic_identity="line",
        with_polymorphic='*',
    )
    id = Column(
        Integer,
        primary_key=True,
        info={"colanderalchemy": forms.EXCLUDED},
    )
    type = Column(
        String(30),
        nullable=False,
        info={'colanderalchemy': forms.EXCLUDED},
    )
    date = Column(
        Date(),
        default=datetime.date.today,
        info={'colanderalchemy': {'title': u"Date"}},
    )
    description = Column(
        String(255),
        info={'colanderalchemy': {'title': u"Description"}},
        default="",
    )
    category = Column(Enum('1', '2', name='category'), default='1')
    valid = Column(
        Boolean(),
        default=True,
        info={"colanderalchemy": {"title": u"Valide ?"}}
    )

    type_id = Column(
        Integer,
        info={
            'colanderalchemy': {
                'validator': forms.get_deferred_select_validator(ExpenseType),
                'missing': colander.required,
                "title": u"Type de dépense",
            }
        }
    )

    sheet_id = Column(
        Integer,
        ForeignKey("expense_sheet.id", ondelete="cascade"),
        info={'colanderalchemy': forms.EXCLUDED}
    )

    type_object = relationship(
        "ExpenseType",
        primaryjoin='BaseExpenseLine.type_id==ExpenseType.id',
        uselist=False,
        foreign_keys=type_id,
        info={'colanderalchemy': forms.EXCLUDED}
    )

    def __json__(self, request):
        return dict(
            id=self.id,
            date=self.date,
            description=self.description,
            category=self.category,
            valid=self.valid,
            type_id=self.type_id,
            sheet_id=self.sheet_id,
        )


class ExpenseLine(BaseExpenseLine, ExpenseLineCompute):
    """
        Common Expense line
    """
    __tablename__ = "expense_line"
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expenseline')
    id = Column(
        Integer,
        ForeignKey('baseexpense_line.id'),
        primary_key=True,
        info={'colanderalchemy': forms.EXCLUDED}
    )
    ht = Column(
        Integer,
        info={
            'colanderalchemy': {
                'typ': AmountType(2),
                'title': 'Montant HT',
                'missing': colander.required,
            }
        },
    )
    tva = Column(
        Integer,
        info={
            'colanderalchemy': {
                'typ': AmountType(2),
                'title': 'Montant de la TVA',
                'missing': colander.required,
            }
        },
    )
    sheet = relationship(
        "ExpenseSheet",
        uselist=False,
        info={'colanderalchemy': forms.EXCLUDED}
    )

    def __json__(self, request):
        res = BaseExpenseLine.__json__(self, request)
        res.update(
            dict(
                ht=integer_to_amount(self.ht, 2),
                tva=integer_to_amount(self.tva, 2)
            )
        )
        return res

    def duplicate(self):
        line = ExpenseLine()
        line.description = self.description
        line.category = self.category
        line.type_id = self.type_id

        line.ht = self.ht
        line.tva = self.tva
        return line


class ExpenseKmLine(BaseExpenseLine, ExpenseKmLineCompute):
    """
        Model representing a specific expense related to kilometric fees
        :param start: starting point
        :param end: endpoint
        :param km: Number of kilometers
    """
    __tablename__ = "expensekm_line"
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expensekmline')
    id = Column(
        Integer,
        ForeignKey('baseexpense_line.id'),
        primary_key=True,
        info={'colanderalchemy': forms.EXCLUDED}
    )
    type_label = Column(String(50))
    start = Column(
        String(150),
        default="",
        info={"colanderalchemy": {"title": u"Point de départ"}}
    )
    end = Column(
        String(150),
        default="",
        info={"colanderalchemy": {"title": u"Point d'arrivée"}}
    )
    km = Column(
        Integer,
        info={
            'colanderalchemy': {
                'typ': AmountType(2),
                'title': 'Nombre de kilomètres',
                'missing': colander.required,
            }
        },
    )
    sheet = relationship(
        "ExpenseSheet",
        uselist=False,
        info={'colanderalchemy': forms.EXCLUDED}
    )

    def __json__(self, request):
        res = BaseExpenseLine.__json__(self, request)
        res.update(
            dict(
                type_label=self.type_label,
                km=integer_to_amount(self.km),
                start=self.start,
                end=self.end,
                vehicle=self.vehicle,
            )
        )
        return res

    @property
    def vehicle(self):
        return self.type_object.label

    def duplicate(self):
        line = ExpenseKmLine()
        line.description = self.description
        line.category = self.category
        line.type_id = self.type_id

        line.start = self.start
        line.end = self.end
        line.km = self.km
        return line


class Communication(DBBASE):
    """
        Communication Class, logs communications between the contractor and its
        CAE
    """
    __tablename__ = "communication"
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("accounts.id"))
    content = Column(Text)
    date = Column(
        Date(),
        default=datetime.date.today,
        onupdate=datetime.date.today
    )
    expense_sheet_id = Column(Integer, ForeignKey("expense_sheet.id"))

    expense_sheet = relationship("ExpenseSheet")

    user = relationship(
        "User",
        primaryjoin="Communication.user_id==User.id",
        backref=backref(
            "expense_communications",
            order_by="Communication.date",
            cascade="all, delete-orphan",
            info={
                'colanderalchemy': forms.EXCLUDED,
                'export': {'exclude': True},
            },
        )
    )


def get_expense_years():
    """
    Return the list of years that there were some expense configured
    """
    @cache_region("long_term", "expenseyears")
    def expenseyears():
        """
        return distinct expense years available in the database
        """
        query = DBSESSION().query(distinct(ExpenseSheet.year))
        query = query.order_by(ExpenseSheet.year)
        years = [year[0] for year in query]
        current = datetime.date.today().year
        if current not in years:
            years.append(current)
        return years
    return expenseyears()


def get_expense_sheet_name(month, year):
    """
    Return the name of an expensesheet
    """
    return u"expense_{0}_{1}".format(month, year)
