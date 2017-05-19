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

from beaker.cache import cache_region
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Integer,
    String,
    Float,
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

from autonomie.models.base import (
    DBBASE,
    DBSESSION,
    default_table_args,
)
from autonomie.forms import (
    get_hidden_field_conf,
    EXCLUDED,
)
from autonomie.compute.expense import (
    ExpenseCompute,
    ExpenseLineCompute,
    ExpenseKmLineCompute,
)

from autonomie.models.types import PersistentACLMixin
from autonomie.models.statemachine import StateMachine
from autonomie.models.node import Node


logger = logging.getLogger(__name__)


class ExpenseType(DBBASE):
    """
        Base Type for expenses
        :param label: Label of the expense type that will be used in the UI
        :param code: Analytic code related to this expense
        :param type: Column for polymorphic discrimination
    """
    __colanderalchemy_config__ = {
        'title': u"Configuration des types de dépenses",
        'validation_msg': u"Les types de dépenses ont bien été configurés",
        "help_msg": u"Configurer les types de dépenses utilisables dans \
les formulaires de saisie",
    }
    __tablename__ = 'expense_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_on="type",
                           polymorphic_identity="expense",
                           with_polymorphic='*')
    id = Column(
        Integer,
        primary_key=True,
        info={
            "colanderalchemy": get_hidden_field_conf()
        }
    )
    type = Column(
        String(30),
        nullable=False,
        info={'colanderalchemy': EXCLUDED}
    )
    active = Column(
        Boolean(),
        default=True,
        info={'colanderalchemy': EXCLUDED}
    )
    label = Column(
        String(50),
        info={
            'colanderalchemy': {
                'title': u"Libellé",
            }
        },
        nullable=False,
    )
    code = Column(
        String(15),
        info={
            'colanderalchemy': {
                'title': u"Compte de charge de la dépense",
            }
        },
        nullable=False,
    )

    code_tva = Column(
        String(15),
        default="",
        info={
            'colanderalchemy': {
                'title': u"Code TVA (si nécessaire)",
            }
        }
    )
    compte_tva = Column(
        String(15),
        default="",
        info={
            'colanderalchemy': {
                'title': u"Compte de TVA déductible (si nécessaire)",
            }
        }
    )
    contribution = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Inclue dans la contribution ?",
                'description': u"Ce type de dépense est-il intégré dans la \
contribution à la CAE ?"
            }
        }
    )

    def __json__(self, request=None):
        return {
            "id": self.id,
            "value": str(self.id),
            "active": self.active,
            "code": self.code,
            "label": u"{0} ({1})".format(self.label, self.code),
        }


class ExpenseKmType(ExpenseType):
    """
        Type of expenses related to kilometric fees
    """
    __colanderalchemy_config__ = {
        'title': u"type de dépenses kilométriques",
        'validation_msg': u"Les types de dépenses kilométriques ont bien été \
configurés",
        "help_msg": u"Configurer les types de dépenses kilométriques \
utilisables dans les notes de dépense",
    }
    __tablename__ = 'expensekm_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expensekm')
    id = Column(
        Integer,
        ForeignKey('expense_type.id'),
        primary_key=True,
        info={
            "colanderalchemy": get_hidden_field_conf()
        }
    )
    amount = Column(
        Float(precision=4),
        info={
            'colanderalchemy': {
                'title': u"Tarif au km",
            }
        },
        nullable=False,
    )

    def __json__(self, request=None):
        res = ExpenseType.__json__(self)
        res['amount'] = self.amount
        return res


class ExpenseTelType(ExpenseType):
    """
        Type of expenses related to telefonic fees
    """
    __colanderalchemy_config__ = {
        'title': u"type de dépenses téléphoniques",
        'validation_msg': u"Les types de dépenses téléphoniques ont bien été \
configurés",
        "help_msg": u"Configurer les types de dépenses téléphoniques \
utilisables dans les notes de dépense",
    }
    __tablename__ = 'expensetel_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expensetel')
    id = Column(
        Integer,
        ForeignKey('expense_type.id'),
        primary_key=True,
        info={
            "colanderalchemy": get_hidden_field_conf()
        }
    )
    percentage = Column(
        Integer,
        info={
            'colanderalchemy': {
                'title': u"Pourcentage remboursé",
                'missing': colander.required
            }
        },
        nullable=False,
    )
    initialize = Column(
        Boolean,
        default=True,
        info={
            'colanderalchemy': {
                'title': u"Créer une entrée par défaut ?",
                'description': u"Dans le formulaire de saisie des notes de \
dépense, une ligne sera automatiquement ajouté au Frais de l'entrepreneur."
            }
        }
    )

    def __json__(self, request=None):
        res = ExpenseType.__json__(self)
        res['percentage'] = self.percentage
        return res


def record_expense_payment(request, expense, **kw):
    """
    Record an expense payment using the datas provided in kw

    Caution : The kw args should be validated before being transmitted here

    :param obj expense: An ExpenseSheet instance
    :param dict kw: Form validated datas used to init an ExpensePayment object

    :returns: The ExpensePayment object
    """
    # Here we could register a service
    return expense.record_payment(**kw)


def build_state_machine():
    """
    Return a state machine that allows ExpenseSheet status handling
    """
    draft = ('draft', 'view_expense',)
    reset = ('reset', 'edit_expense', None, False)
    wait = ('wait', 'edit_expense', )
    valid = ('valid', "admin_expense", )
    invalid = ('invalid', "admin_expense",)
    # Partiellement payé
    paid = ('paid', "admin_expense", record_expense_payment, )
    resulted = ('resulted', "admin_expense", )  # Soldé
    states = {}
    states['draft'] = (wait, reset, valid,)
    states['invalid'] = (draft, wait,)
    states['wait'] = (valid, invalid, draft)
    states['valid'] = (resulted, paid,)
    states['paid'] = (paid, )
    return states


class ExpenseStates(StateMachine):
    """
        Expense state machine
    """
    status_attr = "status"
    userid_attr = "status_user_id"


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
    id = Column(ForeignKey('node.id'), primary_key=True)
    month = Column(Integer)
    year = Column(Integer)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="cascade"))
    user_id = Column(Integer, ForeignKey("accounts.id"))
    status = Column(String(10), default='draft')
    status_user_id = Column(Integer, ForeignKey("accounts.id"))
    status_date = Column(
        Date(),
        default=datetime.date.today,
        onupdate=datetime.date.today
    )
    exported = Column(Boolean(), default=False)
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
        backref=backref(
            "expenses",
            order_by="ExpenseSheet.month",
            info={
                'colanderalchemy': EXCLUDED,
                'export': {'exclude': True},
            },
            cascade="all, delete-orphan"
        ),
    )
    status_user = relationship(
        "User",
        primaryjoin="ExpenseSheet.status_user_id==User.id",
    )

    state_machine = ExpenseStates('draft', build_state_machine())
    valid_states = ('valid', 'resulted', 'paid')

    def __json__(self, request):
        return dict(
            id=self.id,
            lines=[line.__json__(request) for line in self.lines],
            kmlines=[line.__json__(request) for line in self.kmlines],
            month=self.month,
            year=self.year,
        )

    def set_status(self, status, request, user_id, **kw):
        """
            Set the status of a task through a state machine
        """
        return self.state_machine.process(self, request, user_id, status, **kw)

    def get_next_actions(self):
        """
            Return the next available actions regarding the current status
        """
        return self.state_machine.get_next_states(self.status)

    def is_allowed(self, request, statename):
        """
        Return True if the given state is allowed for the current request

        :param obj request: The pyramid request object
        :param str statename: The name of the state we want ('draft' ...)
        :returns: True if the given state is allowed
        :rtype: bool
        """
        result = False
        state_obj = self.state_machine.get_state(self.status, statename)
        if state_obj is not None:
            result = state_obj.allowed(self, request)
        return result

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
        resulted = kw.pop('resulted', False)

        payment = ExpensePayment()
        for key, value in kw.iteritems():
            setattr(payment, key, value)
        logger.info(u"Amount : {0}".format(payment.amount))
        self.payments.append(payment)
        return self.check_resulted(force_resulted=resulted)

    def check_resulted(self, force_resulted=False, user_id=None):
        """
        Check if the expense is resulted or not and set the appropriate status
        """
        old_status = self.status
        logger.debug(u"-> There still to pay : %s" % self.topay())
        if self.topay() == 0 or force_resulted:
            self.status = 'resulted'
        elif len(self.payments) > 0:
            self.status = 'paid'
        else:
            self.status = 'valid'
        # If the status has changed, we update the statusPerson
        if user_id is not None and old_status != self.status:
            self.status_user_id = user_id
        return self


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
    id = Column(Integer, primary_key=True)
    type = Column(String(30), nullable=False)
    date = Column(Date(), default=datetime.date.today)
    description = Column(String(255))
    category = Column(Enum('1', '2', name='category'), default='1')
    valid = Column(Boolean(), default=True)
    type_id = Column(Integer)
    sheet_id = Column(
        Integer,
        ForeignKey("expense_sheet.id", ondelete="cascade")
    )
    type_object = relationship(
        "ExpenseType",
        primaryjoin='BaseExpenseLine.type_id==ExpenseType.id',
        uselist=False,
        foreign_keys=type_id,
    )


class ExpenseLine(BaseExpenseLine, ExpenseLineCompute):
    """
        Common Expense line
    """
    __tablename__ = "expense_line"
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expenseline')
    id = Column(Integer, ForeignKey('baseexpense_line.id'), primary_key=True)
    ht = Column(Integer)
    tva = Column(Integer)
    sheet = relationship(
        "ExpenseSheet",
        backref=backref(
            "lines",
            order_by="ExpenseLine.date",
            cascade="all, delete-orphan"
        )
    )

    def __json__(self, request):
        return dict(
            id=self.id,
            date=self.date,
            valid=self.valid,
            category=self.category,
            description=self.description,
            ht=self.ht,
            tva=self.tva,
            type_id=self.type_id,
        )


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
    id = Column(Integer, ForeignKey('baseexpense_line.id'), primary_key=True)
    type_label = Column(String(50))
    start = Column(String(150), default="")
    end = Column(String(150), default="")
    km = Column(Integer)
    sheet = relationship(
        "ExpenseSheet",
        backref=backref(
            "kmlines",
            order_by="ExpenseLine.date",
            cascade="all, delete-orphan"
        )
    )

    def __json__(self, request):
        return dict(id=self.id,
                    date=self.date,
                    valid=self.valid,
                    category=self.category,
                    description=self.description,
                    type_label=self.type_label,
                    km=self.km,
                    start=self.start,
                    end=self.end,
                    type_id=self.type_id)

    @property
    def vehicle(self):
        return self.type_object.label


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

    expense_sheet = relationship(
        "ExpenseSheet",
        backref=backref(
            "communications",
            order_by="Communication.date",
            cascade="all, delete-orphan"
        )
    )

    user = relationship(
        "User",
        primaryjoin="Communication.user_id==User.id",
        backref=backref(
            "expense_communications",
            order_by="Communication.date",
            cascade="all, delete-orphan",
            info={
                'colanderalchemy': EXCLUDED,
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


class ExpensePayment(DBBASE, PersistentACLMixin):
    """
        Expense Payment entry
    """
    __tablename__ = 'expense_payment'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime(),
        info={
            'colanderalchemy': {
                'exclude': True, 'title': u"Créé(e) le",
            }
        },
        default=datetime.datetime.now,
    )

    updated_at = Column(
        DateTime(),
        info={
            'colanderalchemy': {
                'exclude': True, 'title': u"Mis(e) à jour le",
            }
        },
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    mode = Column(String(50))
    amount = Column(Integer)
    date = Column(DateTime(), default=datetime.datetime.now)
    # est-ce un abandon de créance
    waiver = Column(Boolean(), default=False)
    exported = Column(Boolean(), default=False)
    expense_sheet_id = Column(
        Integer,
        ForeignKey('expense_sheet.id', ondelete="cascade")
    )
    bank_id = Column(ForeignKey('bank_account.id'))
    bank = relationship(
        "BankAccount",
        backref=backref(
            'expense_payments',
            order_by="ExpensePayment.date",
            info={'colanderalchemy': {'exclude': True}},
        ),
    )
    expense = relationship(
        "ExpenseSheet",
        backref=backref(
            'payments',
            order_by="ExpensePayment.date",
            info={'colanderalchemy': {'exclude': True}},
        ),
    )
    # formatting precision
    precision = 2

    def get_amount(self):
        return self.amount

    @property
    def parent(self):
        return self.expense

    def __repr__(self):
        return u"<ExpensePayment id:{s.id} \
expense_sheet_id:{s.expense_sheet_id} \
amount:{s.amount} \
mode:{s.mode} \
date:{s.date}".format(s=self)
