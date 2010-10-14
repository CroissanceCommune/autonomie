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
    The estimation model
"""
import datetime
import logging

from zope.interface import implementer

from sqlalchemy import (
        Column,
        Integer,
        String,
        ForeignKey,
        Text,
        )
from sqlalchemy.orm import (
        relationship,
        deferred,
        backref,
)
# Aye : ici on a du double dans la bdd, en attendant une éventuelle
# migration des données, on dépend entièrement de mysql
from sqlalchemy.dialects.mysql import DOUBLE

from autonomie.models.types import (
        CustomDateType,
        CustomDateType2)
from autonomie.models.utils import get_current_timestamp
from autonomie.models.base import (
        DBBASE,
        default_table_args,
        )

from autonomie.compute.task import (
        EstimationCompute,
        LineCompute,
        )
from .interfaces import (
        IValidatedTask,
        IMoneyTask,
        )
from .invoice import (
        Invoice,
        InvoiceLine,
        )
from .task import (
        Task,
        DiscountLine,
        )
from .states import DEFAULT_STATE_MACHINES

log = logging.getLogger(__name__)


@implementer(IValidatedTask, IMoneyTask)
class Estimation(Task, EstimationCompute):
    """
        Estimation Model
    """
    __tablename__ = 'estimation'
    __table_args__ = default_table_args
    id = Column("id", ForeignKey('task.id'), primary_key=True, nullable=False)
    sequenceNumber = Column("sequenceNumber", Integer, nullable=False)
    _number = Column("number", String(100), nullable=False)
    tva = Column("tva", Integer, nullable=False, default=196)
    deposit = Column("deposit", Integer, default=0)
    paymentConditions = deferred(
        Column("paymentConditions", Text),
        group='edit')
    exclusions = deferred(Column("exclusions", Text), group='edit')
    project_id = Column("project_id", ForeignKey('project.id'))
    customer_id = Column('customer_id', Integer, ForeignKey('customer.id'))
    manualDeliverables = deferred(
        Column("manualDeliverables", Integer),
        group='edit')
    course = deferred(
        Column('course', Integer, nullable=False, default=0),
        group='edit')
    displayedUnits = deferred(
        Column('displayedUnits', Integer, nullable=False, default=0),
        group='edit')
    discountHT = Column('discountHT', Integer, default=0)
    expenses = deferred(
        Column('expenses', Integer, default=0),
        group='edit')
    expenses_ht = deferred(
        Column(Integer, default=0, nullable=False),
        group='edit')
    paymentDisplay = deferred(
        Column('paymentDisplay', String(20), default="SUMMARY"),
        group='edit')
    address = Column("address", Text, default="")
    project = relationship(
        "Project",
        backref=backref('estimations', order_by='Estimation.taskDate')
    )
    client = relationship(
            "Customer",
            primaryjoin="Customer.id==Estimation.customer_id",
            backref=backref('estimations', order_by='Estimation.taskDate'))

    __mapper_args__ = {'polymorphic_identity': 'estimation', }

    state_machine = DEFAULT_STATE_MACHINES['estimation']

    def is_draft(self):
        return self.CAEStatus in ('draft', 'invalid',)

    def is_editable(self, manage=False):
        if manage:
            return self.CAEStatus in ('draft', 'invalid', 'wait', None)
        else:
            return self.CAEStatus in ('draft', 'invalid', None)

    def is_valid(self):
        return self.CAEStatus == 'valid'

    def has_been_validated(self):
        return self.CAEStatus in ('valid', 'geninv',)

    def is_waiting(self):
        return self.CAEStatus == 'wait'

    def is_estimation(self):
        return True

    def duplicate(self, user, project, phase, client):
        """
            returns a duplicate estimation object
        """
        seq_number = project.get_next_estimation_number()
        date = datetime.date.today()

        estimation = Estimation()
        estimation.statusPersonAccount = user
        estimation.phase = phase
        estimation.owner = user
        estimation.client = client
        estimation.project = project
        estimation.taskDate = date
        estimation.set_sequenceNumber(seq_number)
        estimation.set_number()
        estimation.set_name()
        if client.id == self.customer_id:
            estimation.address = self.address
        else:
            estimation.address = client.full_address

        estimation.description = self.description
        estimation.CAEStatus = "draft"

        estimation.deposit = self.deposit
        estimation.paymentConditions = self.paymentConditions
        estimation.exclusions = self.exclusions
        estimation.manualDeliverables = self.manualDeliverables
        estimation.course = self.course
        estimation.displayedUnits = self.displayedUnits
        estimation.discountHT = self.discountHT
        estimation.expenses = self.expenses
        estimation.expenses_ht = self.expenses_ht
        estimation.paymentDisplay = self.paymentDisplay
        for line in self.lines:
            estimation.lines.append(line.duplicate())
        for line in self.payment_lines:
            estimation.payment_lines.append(line.duplicate())
        for line in self.discounts:
            estimation.discounts.append(line.duplicate())
        return estimation

    def _account_invoiceline(self, amount, description, tva=1960):
        """
            Return an account invoiceline
        """
        return InvoiceLine(cost=amount, description=description, tva=tva)

    def _make_deposit(self, invoice):
        """
            Return a deposit invoice
        """
        invoice.taskDate = datetime.date.today()
        invoice.financial_year = invoice.taskDate.year
        invoice.displayedUnits = 0
        invoice.set_name(deposit=True)
        invoice.set_number(deposit=True)

        for tva, amount in self.deposit_amounts().items():
            description = u"Facture d'acompte"
            line = self._account_invoiceline(amount, description, tva)
            invoice.lines.append(line)
        return invoice, [line.duplicate() for line in invoice.lines]

    def _make_intermediary(self, invoice, paymentline, amounts):
        """
            return an intermediary invoice described by "paymentline"
        """
        invoice.taskDate = paymentline.paymentDate
        invoice.financial_year = paymentline.paymentDate.year
        invoice.displayedUnits = 0
        invoice.set_name()
        invoice.set_number()
        for tva, amount in amounts.items():
            description = paymentline.description
            line = self._account_invoiceline(amount, description, tva)
            invoice.lines.append(line)
        return invoice, [line.duplicate() for line in invoice.lines]

    def _sold_invoice_lines(self, account_lines):
        """
            return the lines that will appear in the sold invoice
        """
        sold_lines = []
        for line in self.lines:
            sold_lines.append(line.gen_invoice_line())
        rowIndex = len(self.lines)
        for line in account_lines:
            rowIndex = rowIndex + 1
            line.cost = -1 * line.cost
            line.rowIndex = rowIndex
            sold_lines.append(line)
        return sold_lines

    def _make_sold(self, invoice, paymentline, paid_lines, is_sold):
        """
            Return the sold invoice
        """
        invoice.taskDate = paymentline.paymentDate
        invoice.financial_year = paymentline.paymentDate.year
        invoice.set_name(sold=is_sold)
        invoice.set_number()

        invoice.displayedUnits = self.displayedUnits
        invoice.expenses = self.expenses
        invoice.expenses_ht = self.expenses_ht
        for line in self._sold_invoice_lines(paid_lines):
            invoice.lines.append(line)
        for line in self.discounts:
            invoice.discounts.append(line.duplicate())
        return invoice

    def _get_common_invoice(self, seq_number, user):
        """
            Return an invoice object with common args for
            all the generated invoices
        """
        inv = Invoice()
        # Relationship
        inv.client = self.client
        inv.project = self.project
        inv.phase = self.phase
        inv.owner = user
        inv.statusPersonAccount = user
        inv.estimation = self

        # Common args
        inv.paymentConditions=self.paymentConditions
        inv.description=self.description
        inv.course=self.course
        inv.address = self.address
        inv.CAEStatus = "draft"
        inv.set_sequenceNumber(seq_number)
        return inv

    def gen_invoices(self, user):
        """
            Return the invoices based on the current estimation
        """
        invoices = []
        # Used to mark the existence of intermediary invoices
        is_sold = len(self.payment_lines) > 1
        # Used to store the amount of the intermediary invoices
        paid_lines = []
        # Sequence number that will be incremented by hand
        seq_number = self.project.get_next_invoice_number()
        if self.deposit > 0:
            invoice = self._get_common_invoice(seq_number, user)
            deposit, lines = self._make_deposit(invoice)
            invoices.append(deposit)
            # We remember the lines to display them in the last invoice
            paid_lines.extend(lines)
            seq_number += 1

        if self.manualDeliverables == 1:
            payments = self.manual_payment_line_amounts()
            # all payment lines specified (less the last one)
            for index, amounts in enumerate(payments[:-1]):
                line = self.payment_lines[index]
                invoice = self._get_common_invoice(seq_number, user)
                invoice, lines = self._make_intermediary(invoice, line, amounts)
                paid_lines.extend(lines)
                seq_number += 1
        else:
            amounts = self.paymentline_amounts()
            for line in self.payment_lines[:-1]:
                invoice = self._get_common_invoice(seq_number, user)
                invoice, lines = self._make_intermediary(invoice, line, amounts)
                paid_lines.extend(lines)
                seq_number += 1

        invoice = self._get_common_invoice(seq_number, user)
        pline = self.payment_lines[-1]
        invoice = self._make_sold(invoice, pline, paid_lines, is_sold)
        invoices.append(invoice)
        return invoices

    def set_name(self):
        taskname_tmpl = u"Devis {0}"
        self.name = taskname_tmpl.format(self.sequenceNumber)

    def set_number(self):
        tasknumber_tmpl = u"D{s.sequenceNumber}_{s.taskDate:%m%y}"
        self._number = tasknumber_tmpl.format(s=self)

    def set_sequenceNumber(self, snumber):
        self.sequenceNumber = snumber

    @property
    def number(self):
        tasknumber_tmpl = u"{s.project.code}_{s.client.code}_{s._number}"
        return tasknumber_tmpl.format(s=self)

    def is_cancelled(self):
        """
            Return True if the invoice has been cancelled
        """
        return self.CAEStatus == 'aboest'

    def add_line(self, line=None, **kwargs):
        """
            Add a line to the current task
        """
        if line is None:
            line = EstimationLine(**kwargs)
        self.lines.append(line)

    def add_discount(self, line=None, **kwargs):
        """
            Add a discount line to the current task
        """
        if line is None:
            line = DiscountLine(**kwargs)
        self.discounts.append(line)

    def add_payment(self, line=None, **kwargs):
        """
            Add a payment line to the current task
        """
        if line is None:
            line = PaymentLine(**kwargs)
        self.payments.append(line)

    def set_lines(self, lines):
        """
            Set the lines
        """
        self.lines = lines

    def set_discounts(self, lines):
        """
            Set the discounts
        """
        self.discounts = lines

    def set_payments(self, lines):
        """
            set the payment lines
        """
        self.payments = lines

    def __repr__(self):
        return u"<Estimation id:{s.id}>".format(s=self)


class EstimationLine(DBBASE, LineCompute):
    """
        Estimation lines
    """
    __tablename__ = 'estimation_line'
    __table_args__ = default_table_args
    id = Column("id", Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('estimation.id', ondelete="cascade"))
    rowIndex = Column("rowIndex", Integer)
    description = Column("description", Text)
    cost = Column(Integer, default=0)
    quantity = Column(DOUBLE, default=1)
    tva = Column("tva", Integer, nullable=False, default=196)
    creationDate = deferred(
        Column("creationDate",
            CustomDateType,
            default=get_current_timestamp))
    updateDate = deferred(
        Column("updateDate",
            CustomDateType,
            default=get_current_timestamp,
            onupdate=get_current_timestamp))
    unity = Column("unity", String(100))
    task = relationship(
        "Estimation",
        backref=backref("lines", order_by='EstimationLine.rowIndex',
                        cascade="all, delete-orphan"))

    def duplicate(self):
        """
            duplicate a line
        """
        newone = EstimationLine()
        newone.rowIndex = self.rowIndex
        newone.cost = self.cost
        newone.description = self.description
        newone.quantity = self.quantity
        newone.tva = self.tva
        newone.unity = self.unity
        return newone

    def gen_invoice_line(self):
        """
            return the equivalent InvoiceLine
        """
        line = InvoiceLine()
        line.rowIndex = self.rowIndex
        line.cost = self.cost
        line.description = self.description
        line.quantity = self.quantity
        line.tva = self.tva
        line.unity = self.unity
        return line

    def __repr__(self):
        return u"<EstimationLine id:{s.id} task_id:{s.task_id} cost:{s.cost}\
 quantity:{s.quantity} tva:{s.tva}".format(s=self)


class PaymentLine(DBBASE):
    """
        payments lines
    """
    __tablename__ = 'estimation_payment'
    __table_args__ = default_table_args
    id = Column("id", Integer, primary_key=True, nullable=False)
    task_id = Column(Integer, ForeignKey('estimation.id', ondelete="cascade"))
    rowIndex = Column("rowIndex", Integer)
    description = Column("description", Text)
    amount = Column("amount", Integer)
    creationDate = deferred(
        Column("creationDate",
            CustomDateType,
            default=get_current_timestamp))
    updateDate = deferred(
        Column("updateDate",
            CustomDateType,
            default=get_current_timestamp,
            onupdate=get_current_timestamp))
    paymentDate = Column("paymentDate", CustomDateType2(11))
    task = relationship(
        "Estimation",
        backref=backref('payment_lines', order_by='PaymentLine.rowIndex',
            cascade="all, delete-orphan"))

    def duplicate(self):
        """
            duplicate a paymentline
        """
        return PaymentLine(rowIndex=self.rowIndex,
                             amount=self.amount,
                             description=self.description,
                             paymentDate=datetime.date.today())

    def __repr__(self):
        return u"<PaymentLine id:{s.id} task_id:{s.task_id} amount:{s.amount}\
 date:{s.paymentDate}".format(s=self)
