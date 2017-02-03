# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
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
#

"""
    Invoice model
"""
import datetime
import logging
import deform

from zope.interface import implementer
from beaker.cache import cache_region

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    Boolean,
    String,
    ForeignKey,
    DateTime,
    func,
    distinct,
    extract,
)
from sqlalchemy.orm import (
    relationship,
    deferred,
    backref,
)

from autonomie import forms
from autonomie.models.types import (
    PersistentACLMixin,
)
from autonomie.models.base import (
    DBSESSION,
    DBBASE,
    default_table_args,
)
from autonomie.compute import math_utils
from autonomie.compute.task import (
    TaskCompute,
    InvoiceCompute,
)
from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)
from .interfaces import (
    IMoneyTask,
    IInvoice,
    IPaidTask,
)
from .task import (
    Task,
    TaskLine,
)
from .states import DEFAULT_STATE_MACHINES

log = logging.getLogger(__name__)


class InvoiceService(object):
    """
    Service for invoice and cancelinvoice management
    """
    def _get_next_official_number(year=None):
        """
        Return the next available official number

        :param int year: The year we'd like to query a number for
        """
        next_ = 1
        if year is None:
            year = datetime.date.today().year

        query = DBSESSION().query(func.max(Task.official_number))
        query = query.filter(extract('year', Task.date) == year)
        last = query.first()[0]
        if last:
            next_ = last + 1

        return next_

    def valid_callback(self, task):
        """
        Validation callback (launched after task validation)

        Set the date to current
        Set the official number

        :param obj task: The task object
        """
        if task.official_number is None:
            task.official_number = self._get_next_official_number()

        task.date = datetime.date.today()


def invoice_tolate(invoicedate, status):
    """
        Return True if a payment is expected since more than
        45 days
    """
    res = False
    if status in ('valid', 'paid'):
        today = datetime.date.today()
        elapsed = today - invoicedate
        if elapsed > datetime.timedelta(days=45):
            res = True
        else:
            res = False
    return res


def translate_invoices(invoicequery, from_point):
    """
    Translate invoice numbers to 'from_point'

    :param iter invoicequery: An iterable
    :param int from_point: from_point

    The first invoice will get from_point as official_number
    """
    for invoice in invoicequery:
        invoice.official_number = from_point
        from_point += 1
        DBSESSION().merge(invoice)

    return from_point


@implementer(IPaidTask, IInvoice, IMoneyTask)
class Invoice(Task, InvoiceCompute):
    """
        Invoice Model
    """
    __tablename__ = 'invoice'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'invoice', }
    id = Column(
        ForeignKey('task.id'),
        primary_key=True,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}},
    )
    # seems it's not used anymore
    deposit = deferred(
        Column(
            Integer,
            nullable=False,
            info={'colanderalchemy': {'exclude': True}},
            default=0
        ),
        group='edit',
    )
    # Common with only estimations
    course = deferred(
        Column(
            Integer,
            info={'colanderalchemy': {'title': u"Concerne une formation"}},
            nullable=False,
            default=0
        ),
        group='edit'
    )
    # Common with only cancelinvoices
    financial_year = deferred(
        Column(
            Integer,
            info={'colanderalchemy': {'title': u"Année fiscale de référence"}},
            default=0
        ),
        group='edit'
    )
    exported = deferred(
        Column(
            Boolean(),
            info={'colanderalchemy': {'title': u"A déjà été exportée ?"}},
            default=False), group="edit")

    estimation_id = Column(
        ForeignKey('estimation.id'),
        info={'colanderalchemy': {'exclude': True}},
    )

    estimation = relationship(
        "Estimation",
        primaryjoin="Invoice.estimation_id==Estimation.id",
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        },
    )
    state_machine = DEFAULT_STATE_MACHINES['invoice']

    paid_states = ('resulted',)
    not_paid_states = ('valid', 'paid', )
    valid_states = paid_states + not_paid_states

    _number_tmpl = u"{s.company.name} {s.date:%Y-%m} F{s.company_index}"

    _name_tmpl = u"Facture {0}"

    _deposit_name_tmpl = u"Facture d'acompte {0}"

    _sold_name_tmpl = u"Facture de solde {0}"

    def _get_project_index(self, project):
        """
        Return the index of the current object in the associated project
        :param obj project: A Project instance in which we will look to get the
        current doc index
        :returns: The next number
        :rtype: int
        """
        return project.get_next_invoice_index()

    def _get_company_index(self, company):
        """
        Return the index of the current object in the associated company
        :param obj company: A Company instance in which we will look to get the
        current doc index
        :returns: The next number
        :rtype: int
        """
        return company.get_next_invoice_index()

    def set_deposit_label(self):
        self.name = self._deposit_name_tmpl.format(self.project_index)

    def set_sold_label(self):
        self.name = self._sold_name_tmpl.format(self.project_index)

    def is_draft(self):
        return self.CAEStatus in ('draft', 'invalid',)

    def is_editable(self, manage=False):
        if manage:
            return self.CAEStatus in ('draft', 'invalid', 'wait', None,)
        else:
            return self.CAEStatus in ('draft', 'invalid', None,)

    def is_valid(self):
        return self.CAEStatus == 'valid'

    def has_been_validated(self):
        return self.CAEStatus in self.valid_states

    def is_waiting(self):
        return self.CAEStatus == "wait"

    def is_invoice(self):
        return True

    def is_paid(self):
        return self.CAEStatus == 'paid'

    def is_resulted(self):
        return self.CAEStatus == 'resulted'

    def is_cancelled(self):
        """
            Return True is the invoice has been cancelled
        """
        return False

    def set_project(self, project):
        self.project = project

    def gen_cancelinvoice(self, user):
        """
            Return a cancel invoice with self's informations
        """
        cancelinvoice = CancelInvoice(
            company=self.company,
            project=self.project,
            customer=self.customer,
            phase=self.phase,
            user=user,
        )
        cancelinvoice.address = self.address
        cancelinvoice.workplace = self.workplace
        cancelinvoice.CAEStatus = 'draft'
        cancelinvoice.description = self.description

        cancelinvoice.invoice = self
        cancelinvoice.expenses_ht = -1 * self.expenses_ht
        cancelinvoice.financial_year = self.financial_year
        cancelinvoice.prefix = self.prefix
        cancelinvoice.display_units = self.display_units

        cancelinvoice.line_groups = []
        for group in self.line_groups:
            cancelinvoice.line_groups.append(
                group.gen_cancelinvoice_group()
            )
        order = self.get_next_row_index()

        for discount in self.discounts:
            discount_line = TaskLine(
                cost=discount.amount,
                tva=discount.tva,
                quantity=1,
                description=discount.description,
                order=order,
                unity='NONE',
            )
            order += 1
            cancelinvoice.default_line_group.lines.append(discount_line)

        for index, payment in enumerate(self.payments):
            paid_line = TaskLine(
                cost=math_utils.reverse_tva(
                    payment.amount,
                    payment.tva.value,
                    False,
                ),
                tva=payment.tva.value,
                quantity=1,
                description=u"Paiement {0}".format(index + 1),
                order=order,
                unity='NONE',
            )
            order += 1
            cancelinvoice.default_line_group.lines.append(paid_line)
        cancelinvoice.mentions = self.mentions
        return cancelinvoice

    def get_next_row_index(self):
        return len(self.default_line_group.lines) + 1

    def record_payment(self, **kw):
        """
        Record a payment for the current invoice
        """
        resulted = kw.pop('resulted', False)
        if kw['amount'] > 0:
            payment = Payment()
            for key, value in kw.iteritems():
                setattr(payment, key, value)
            log.info(u"Amount : {0}".format(payment.amount))
            self.payments.append(payment)
        return self.check_resulted(force_resulted=resulted)

    def check_resulted(self, force_resulted=False, user_id=None):
        """
        Check if the invoice is resulted or not and set the appropriate status
        """
        old_status = self.CAEStatus
        log.debug(u"-> There still to pay : %s" % self.topay())
        if self.topay() == 0 or force_resulted:
            self.CAEStatus = 'resulted'
        elif len(self.payments) > 0:
            self.CAEStatus = 'paid'
        else:
            self.CAEStatus = 'valid'
        # If the status has changed, we update the statusPerson
        if user_id is not None and old_status != self.CAEStatus:
            self.statusPerson = user_id
        return self

    def duplicate(self, user, project, phase, customer):
        """
            Duplicate the current invoice
        """
        invoice = Invoice(
            self.company,
            customer,
            project,
            phase,
            user,
        )

        if customer.id == self.customer_id:
            invoice.address = self.address
        else:
            invoice.address = customer.full_address

        invoice.workplace = self.workplace

        invoice.CAEStatus = 'draft'
        invoice.description = self.description

        invoice.payment_conditions = self.payment_conditions
        invoice.deposit = self.deposit
        invoice.course = self.course
        invoice.display_units = self.display_units
        invoice.expenses_ht = self.expenses_ht
        invoice.financial_year = datetime.date.today().year

        invoice.line_groups = []
        for group in self.line_groups:
            invoice.line_groups.append(group.duplicate())

        for line in self.discounts:
            invoice.discounts.append(line.duplicate())

        invoice.mentions = self.mentions
        return invoice

    def __repr__(self):
        return u"<Invoice id:{s.id}>".format(s=self)

    def __json__(self, request):
        datas = Task.__json__(self, request)

        datas.update(
            dict(
                deposit=self.deposit,
                course=self.course,
                financial_year=self.financial_year,
                exported=self.exported,
                estimation_id=self.estimation_id,
            )
        )
        return datas


@implementer(IPaidTask, IInvoice, IMoneyTask)
class CancelInvoice(Task, TaskCompute):
    """
        CancelInvoice model
        Could also be called negative invoice
    """
    __tablename__ = 'cancelinvoice'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'cancelinvoice'}
    id = Column(
        Integer,
        ForeignKey('task.id'),
        info={'colanderalchemy': forms.get_hidden_field_conf()},
        primary_key=True)

    invoice_id = Column(
        Integer,
        ForeignKey('invoice.id'),
        info={
            'colanderalchemy': {
                'title': u"Identifiant de la facture associée"
            }
        },
        default=None
    )

    financial_year = deferred(
        Column(
            Integer,
            info={
                'colanderalchemy': {
                    'title': u"Année fiscale de référence",
                }
            },
            default=0
        ),
        group='edit'
    )
    exported = deferred(
        Column(
            Boolean(),
            info={
                'colanderalchemy': {
                    "title": "A déjà été exportée ?",
                }
            },
            default=False
        ),
        group="edit"
    )

    invoice = relationship(
        "Invoice",
        backref=backref(
            "cancelinvoices",
            info={'colanderalchemy': forms.EXCLUDED, }
        ),
        primaryjoin="CancelInvoice.invoice_id==Invoice.id",
        info={'colanderalchemy': forms.EXCLUDED, }
    )

    state_machine = DEFAULT_STATE_MACHINES['cancelinvoice']
    valid_states = ('valid', )

    _number_tmpl = u"{s.company.name} {s.date:%Y-%m} A{s.company_index}"

    _name_tmpl = u"Avoir {0}"

    def _get_project_index(self, project):
        """
        Return the index of the current object in the associated project
        :param obj project: A Project instance in which we will look to get the
        current doc index
        :returns: The next number
        :rtype: int
        """
        return project.get_next_invoice_index()

    def _get_company_index(self, company):
        """
        Return the index of the current object in the associated company
        :param obj company: A Company instance in which we will look to get the
        current doc index
        :returns: The next number
        :rtype: int
        """
        return company.get_next_invoice_index()

    def is_editable(self, manage=False):
        if manage:
            return self.CAEStatus in ('draft', 'invalid', 'wait', None,)
        else:
            return self.CAEStatus in ('draft', 'invalid', None,)

    def is_draft(self):
        return self.CAEStatus in ('draft', 'invalid')

    def is_valid(self):
        return self.CAEStatus == 'valid'

    def has_been_validated(self):
        return self.CAEStatus in self.valid_states

    def is_paid(self):
        return False

    def is_resulted(self):
        return self.has_been_validated()

    def is_cancelled(self):
        return False

    def is_waiting(self):
        return self.CAEStatus == 'wait'

    def is_cancelinvoice(self):
        return True

    def is_tolate(self):
        """
            Return False
        """
        return False

    def __repr__(self):
        return u"<CancelInvoice id:{s.id}>".format(s=self)

    def __json__(self, request):
        datas = Task.__json__(self, request)

        datas.update(
            dict(
                invoice_id=self.invoice_id,
                financial_year=self.financial_year,
                exported=self.exported,
            )
        )
        return datas


class Payment(DBBASE, PersistentACLMixin):
    """
        Payment entry
    """
    __tablename__ = 'payment'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True
    )
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
    amount = Column(BigInteger())
    remittance_amount = Column(String(255))
    date = Column(DateTime(), default=datetime.datetime.now)
    exported = Column(Boolean(), default=False)
    task_id = Column(Integer, ForeignKey('task.id', ondelete="cascade"))
    bank_id = Column(ForeignKey('bank_account.id'))
    tva_id = Column(ForeignKey('tva.id'), nullable=True)
    bank = relationship(
        "BankAccount",
        backref=backref(
            'payments',
            order_by="Payment.date",
            info={'colanderalchemy': {'exclude': True}},
        ),
    )
    tva = relationship(
        "Tva",
        backref=backref(
            'payments',
            order_by="Payment.date",
            info={'colanderalchemy': {'exclude': True}},
        ),
    )
    # Formatting precision
    precision = 5

    # Usefull aliases
    @property
    def invoice(self):
        return self.task

    @property
    def parent(self):
        return self.task

    # Simple function
    def get_amount(self):
        return self.amount

    def __unicode__(self):
        return u"<Payment id:{s.id} task_id:{s.task_id} amount:{s.amount}\
 mode:{s.mode} date:{s.date}".format(s=self)


class PaymentMode(DBBASE):
    """
        Payment mode entry
    """
    __colanderalchemy_config__ = {
        "title": u"un mode de paiement",
        "help_msg": u"Configurer les modes de paiement pour la saisie des \
encaissements des factures",
        "validation_msg": u"Les modes de paiement ont bien été configurés"
    }
    __tablename__ = "paymentmode"
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': forms.get_hidden_field_conf()},
    )
    label = Column(
        String(120),
        info={'colanderalchemy': {'title': u"Libellé"}}
    )


class BankAccount(ConfigurableOption):
    """
    Bank accounts used for payment registry
    """
    __colanderalchemy_config__ = {
        "title": u"un compte banque",
        'validation_msg': u"Les comptes banques ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')
    code_journal = Column(
        String(120),
        info={
            "colanderalchemy": {
                'title': u"Code journal Banque",
                'description': u"""Code journal utilisé pour les exports
                des encaissements et des règlements des notes de dépense""",
            }
        },
        nullable=False,
    )

    compte_cg = Column(
        String(120),
        info={
            "colanderalchemy": {'title': u"Compte CG Banque"}
        },
        nullable=False,
    )
    default = Column(
        Boolean(),
        default=False,
        info={
            "colanderalchemy": {'title': u"Utiliser ce compte par défaut"}
        }
    )


# Usefull queries
def get_invoice_years():
    """
        Return a cached query for the years we have invoices configured
    """
    @cache_region("long_term", "taskyears")
    def taskyears():
        """
            return the distinct financial years available in the database
        """
        query = DBSESSION().query(distinct(Invoice.financial_year))
        query = query.order_by(Invoice.financial_year)
        years = [year[0] for year in query]
        current = datetime.date.today().year
        if current not in years:
            years.append(current)
        return years
    return taskyears()
