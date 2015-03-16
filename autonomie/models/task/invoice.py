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
import colander
import deform

from zope.interface import implementer
from beaker.cache import cache_region

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    ForeignKey,
    DateTime,
    Text,
    func,
    distinct,
)
from sqlalchemy.orm import (
    relationship,
    deferred,
    backref,
    validates,
)
# Aye : ici on a du double dans la bdd, en attendant une éventuelle
# migration des données, on dépend entièrement de mysql
from sqlalchemy.dialects.mysql import DOUBLE

from autonomie import forms
from autonomie.models.types import (
    CustomDateType,
    PersistentACLMixin,
)
from autonomie.models.utils import get_current_timestamp
from autonomie.exception import Forbidden
from autonomie.models.base import (
    DBSESSION,
    DBBASE,
    default_table_args,
)

from autonomie.compute.task import (
    TaskCompute,
    LineCompute,
    InvoiceCompute,
)
from .interfaces import (
    IMoneyTask,
    IInvoice,
    IPaidTask,
)
from .task import Task
from .states import DEFAULT_STATE_MACHINES

log = logging.getLogger(__name__)


def get_next_official_number():
    """
        Return the next available official number
    """
    a = Invoice.get_official_number().first()[0]
    c = CancelInvoice.get_official_number().first()[0]
    if not a:
        a = 0
    if not c:
        c = 0
    next_ = max(a, c) + 1
    return int(next_)


@implementer(IPaidTask, IInvoice, IMoneyTask)
class Invoice(Task, InvoiceCompute):
    """
        Invoice Model
    """
    __tablename__ = 'invoice'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'invoice',}
    id = Column(
        ForeignKey('task.id'),
        primary_key=True,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}},
    )
    # Common with only estimations
    deposit = deferred(
        Column(Integer, nullable=False, default=0),
        group='edit',
    )
    course = deferred(
        Column(Integer, nullable=False, default=0),
        group='edit'
    )
    # Common with only cancelinvoices
    financial_year = deferred(Column(Integer, default=0), group='edit')
    exported = deferred(Column(Boolean(), default=False), group="edit")

    estimation_id = Column(
        ForeignKey('estimation.id'),
        info={'colanderalchemy': {'exclude': True}},
    )


    estimation = relationship(
        "Estimation",
        backref="invoices",
        primaryjoin="Invoice.estimation_id==Estimation.id",
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        },
    )
    lines = relationship(
        "InvoiceLine",
        order_by='InvoiceLine.rowIndex',
        cascade="all, delete-orphan",
        backref="task",
    )

    state_machine = DEFAULT_STATE_MACHINES['invoice']

    paid_states = ('resulted',)
    not_paid_states = ('valid', 'paid', )
    valid_states = paid_states + not_paid_states

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
        return self.CAEStatus == 'aboinv'

    def is_tolate(self):
        """
            Return True if a payment is expected since more than
            45 days
        """
        today = datetime.date.today()
        elapsed = today - self.taskDate
        if elapsed > datetime.timedelta(days=45):
            tolate = True
        else:
            tolate = False
        return self.CAEStatus in ('valid', 'paid', ) and tolate

    def is_viewable(self):
        return True

    @classmethod
    def get_name(cls, seq_number, account=False, sold=False):
        """
            return an invoice name
        """
        if account:
            taskname_tmpl = u"Facture d'acompte {0}"
        elif sold:
            taskname_tmpl = u"Facture de solde"
        else:
            taskname_tmpl = u"Facture {0}"
        return taskname_tmpl.format(seq_number)

    @property
    def number(self):
        tasknumber_tmpl = u"{s.project.code}_{s.customer.code}_{s._number}"
        return tasknumber_tmpl.format(s=self)

    def set_project(self, project):
        self.project = project

    def set_number(self, deposit=False):
        if deposit:
            tasknumber_tmpl = u"FA{s.sequence_number}_{s.taskDate:%m%y}"
        else:
            tasknumber_tmpl = u"F{s.sequence_number}_{s.taskDate:%m%y}"
        self._number = tasknumber_tmpl.format(s=self)

    def set_sequence_number(self, snumber):
        """
            Set the sequencenumber of an invoice
            :param snumber: sequence number get through
                project.get_next_invoice_number()
        """
        self.sequence_number = snumber

    def set_name(self, deposit=False, sold=False):
        if self.name in [None, ""]:
            if deposit:
                taskname_tmpl = u"Facture d'acompte {0}"
            elif sold:
                taskname_tmpl = u"Facture de solde"
            else:
                taskname_tmpl = u"Facture {0}"
            self.name = taskname_tmpl.format(self.sequence_number)

    @classmethod
    def get_official_number(cls):
        """
            Return the next official_number available in the Invoice's table
            Take the max of official Number
            when taskDate startswith the current year
            taskdate is a string (YYYYMMDD)
        """
        current_year = datetime.date.today().year
        return DBSESSION().query(func.max(Invoice.official_number)).filter(
                Invoice.taskDate.between(current_year * 10000,
                                         (current_year + 1) * 10000
                                    ))

    def gen_cancelinvoice(self, user):
        """
            Return a cancel invoice with self's informations
        """
        seq_number = self.project.get_next_cancelinvoice_number()
        cancelinvoice = CancelInvoice()
        cancelinvoice.taskDate = datetime.date.today()
        cancelinvoice.set_sequence_number(seq_number)
        cancelinvoice.set_name()
        cancelinvoice.set_number()
        cancelinvoice.address = self.address
        cancelinvoice.CAEStatus = 'draft'
        cancelinvoice.description = self.description

        cancelinvoice.invoice = self
        cancelinvoice.expenses = -1 * self.expenses
        cancelinvoice.expenses_ht = -1 * self.expenses_ht
        cancelinvoice.financial_year = self.financial_year
        cancelinvoice.display_units = self.display_units
        cancelinvoice.statusPersonAccount = user
        cancelinvoice.project = self.project
        cancelinvoice.owner = user
        cancelinvoice.phase = self.phase
        cancelinvoice.customer_id = self.customer_id

        for line in self.lines:
            cancelinvoice.lines.append(
                line.gen_cancelinvoice_line()
            )
        rowindex = self.get_next_row_index()

        for discount in self.discounts:
            discount_line = CancelInvoiceLine(
                cost=discount.amount,
                tva=discount.tva,
                quantity=1,
                description=discount.description,
                rowIndex=rowindex,
                unity='NONE',
            )
            rowindex += 1
            cancelinvoice.lines.append(discount_line)

        for index, payment in enumerate(self.payments):
            paid_line = CancelInvoiceLine(
                cost=payment.amount,
                tva=0,
                quantity=1,
                description=u"Paiement {0}".format(index + 1),
                rowIndex=rowindex,
                unity='NONE',
            )
            rowindex += 1
            cancelinvoice.lines.append(paid_line)
        return cancelinvoice

    def get_next_row_index(self):
        return len(self.lines) + 1

    def valid_callback(self):
        """
            Validate an invoice
        """
        self.official_number = get_next_official_number()
        self.taskDate = datetime.date.today()

    def record_payment(self, mode, amount, resulted=False):
        """
        Record a payment for the current invoice
        """
        log.info(u"Amount : {0}".format(amount))
        payment = Payment(mode=mode, amount=amount)
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
        seq_number = project.get_next_invoice_number()
        date = datetime.date.today()

        invoice = Invoice()
        invoice.statusPersonAccount = user
        invoice.phase = phase
        invoice.owner = user
        invoice.customer = customer
        invoice.project = project
        invoice.taskDate = date
        invoice.set_sequence_number(seq_number)
        invoice.set_number()
        invoice.set_name()
        if customer.id == self.customer_id:
            invoice.address = self.address
        else:
            invoice.address = customer.full_address

        invoice.CAEStatus = 'draft'
        invoice.description = self.description

        invoice.payment_conditions = self.payment_conditions
        invoice.deposit = self.deposit
        invoice.course = self.course
        invoice.display_units = self.display_units
        invoice.expenses = self.expenses
        invoice.expenses_ht = self.expenses_ht
        invoice.financial_year = date.year

        for line in self.lines:
            invoice.lines.append(line.duplicate())
        for line in self.discounts:
            invoice.discounts.append(line.duplicate())
        return invoice

    def __repr__(self):
        return u"<Invoice id:{s.id}>".format(s=self)


class InvoiceLine(DBBASE, LineCompute):
    """
        Invoice lines
    """
    __tablename__ = 'invoice_line'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}}
    )
    task_id = Column(
        Integer,
        ForeignKey('invoice.id', ondelete="cascade"),
        info={'colanderalchemy': forms.EXCLUDED}
    )
    rowIndex = Column(Integer, default=1,)
    description = Column(Text)
    cost = Column(Integer, default=0,)
    tva = Column(
        Integer,
        nullable=False,
        default=196,
    )
    quantity = Column(
        DOUBLE,
        default=1,
    )
    creationDate = deferred(
        Column(
            CustomDateType,
            default=get_current_timestamp,
            info={'colanderalchemy': forms.EXCLUDED},
        )
    )
    updateDate = deferred(
        Column(
            CustomDateType,
            default=get_current_timestamp,
            onupdate=get_current_timestamp,
            info={'colanderalchemy': forms.EXCLUDED}
        )
    )
    unity = Column(String(100),)
    product_id = Column(
        Integer,
        info={'colanderalchemy': forms.EXCLUDED}
    )
    product = relationship(
        "Product",
        primaryjoin="Product.id==InvoiceLine.product_id",
        uselist=False,
        foreign_keys=product_id,
        info={'colanderalchemy': forms.EXCLUDED}
    )

    def duplicate(self):
        """
            duplicate a line
        """
        newone = InvoiceLine()
        newone.rowIndex = self.rowIndex
        newone.cost = self.cost
        newone.tva = self.tva
        newone.description = self.description
        newone.quantity = self.quantity
        newone.unity = self.unity
        newone.product_id = self.product_id
        return newone

    def gen_cancelinvoice_line(self):
        """
            Return a cancel invoice line duplicating this one
        """
        newone = CancelInvoiceLine()
        newone.rowIndex = self.rowIndex
        newone.cost = -1 * self.cost
        newone.tva = self.tva
        newone.description = self.description
        newone.quantity = self.quantity
        newone.unity = self.unity
        newone.product_id = self.product_id
        return newone

    def __repr__(self):
        return u"<InvoiceLine id:{s.id} task_id:{s.task_id} cost:{s.cost} \
 quantity:{s.quantity} tva:{s.tva}>".format(s=self)


@implementer(IPaidTask, IInvoice, IMoneyTask)
class CancelInvoice(Task, TaskCompute):
    """
        CancelInvoice model
        Could also be called negative invoice
    """
    __tablename__ = 'cancelinvoice'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'cancelinvoice'}
    id = Column(Integer, ForeignKey('task.id'), primary_key=True)

    invoice_id = Column(
        Integer,
        ForeignKey('invoice.id'),
        default=None
    )

    financial_year = deferred(Column(Integer, default=0), group='edit')
    exported = deferred(Column(Boolean(), default=False), group="edit")

    invoice = relationship(
        "Invoice",
        backref=backref(
            "cancelinvoice",
            uselist=False,
            cascade='all, delete-orphan',
            info={'colanderalchemy': forms.EXCLUDED,}
        ),
        primaryjoin="CancelInvoice.invoice_id==Invoice.id")

    state_machine = DEFAULT_STATE_MACHINES['cancelinvoice']
    valid_states = ('valid', )

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

    def is_viewable(self):
        return True

    def set_name(self):
        if self.name in [None, ""]:
            taskname_tmpl = u"Avoir {0}"
            self.name = taskname_tmpl.format(self.sequence_number)

    @classmethod
    def get_official_number(cls):
        """
            Return the greatest official_number actually used in the
            ManualInvoice table
        """
        current_year = datetime.date.today().year
        return DBSESSION().query(func.max(CancelInvoice.official_number)).filter(
                    func.year(CancelInvoice.taskDate) == current_year)

    def is_tolate(self):
        """
            Return False
        """
        return False

    def set_sequence_number(self, snumber):
        """
            Set the sequencenumber of an invoice
            :param snumber: sequence number get through
                project.get_next_invoice_number()
        """
        self.sequence_number = snumber

    def set_number(self):
        tasknumber_tmpl = u"A{s.sequence_number}_{s.taskDate:%m%y}"
        self._number = tasknumber_tmpl.format(s=self)

    @property
    def number(self):
        tasknumber_tmpl = u"{s.project.code}_{s.customer.code}_{s._number}"
        return tasknumber_tmpl.format(s=self)

    def valid_callback(self):
        """
            Validate a cancelinvoice
            Generates an official number
        """
        self.official_number = get_next_official_number()
        self.taskDate = datetime.date.today()


class CancelInvoiceLine(DBBASE, LineCompute):
    """
        CancelInvoice lines
    """
    __tablename__ = 'cancelinvoice_line'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('cancelinvoice.id', ondelete="cascade"))
    created_at = Column(
        DateTime,
        default=datetime.datetime.now)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)
    rowIndex = Column(Integer)
    description = Column(Text, default="")
    cost = Column(Integer, default=0)
    tva = Column("tva", Integer, nullable=False, default=196)
    quantity = Column(DOUBLE, default=1)
    unity = Column(String(100), default=None)
    product_id = Column(Integer)
    product = relationship("Product",
            primaryjoin="Product.id==CancelInvoiceLine.product_id",
            uselist=False,
            foreign_keys=product_id)
    task = relationship(
        "CancelInvoice",
        backref=backref("lines",
            order_by='CancelInvoiceLine.rowIndex',
            cascade="all, delete-orphan"))

    def duplicate(self):
        """
            duplicate a line
        """
        newone = CancelInvoiceLine()
        newone.rowIndex = self.rowIndex
        newone.cost = self.cost
        newone.tva = self.tva
        newone.description = self.description
        newone.quantity = self.quantity
        newone.unity = self.unity
        newone.product_id = self.product_id
        return newone

    def __repr__(self):
        return u"<CancelInvoiceLine id:{s.id} task_id:{s.task_id} \
cost:{s.cost} quantity:{s.quantity} tva:{s.tva}".format(s=self)


class Payment(DBBASE, PersistentACLMixin):
    """
        Payment entry
    """
    __tablename__ = 'payment'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    mode = Column(String(50))
    amount = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.now)
    task_id = Column(Integer, ForeignKey('task.id', ondelete="cascade"))

    def get_amount(self):
        return self.amount

    def __repr__(self):
        return u"<Payment id:{s.id} task_id:{s.task_id} amount:{s.amount}\
 mode:{s.mode} date:{s.date}".format(s=self)


class PaymentMode(DBBASE):
    """
        Payment mode entry
    """
    __tablename__ = "paymentmode"
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    label = Column(String(120))


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
