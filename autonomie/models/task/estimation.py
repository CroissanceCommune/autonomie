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
import deform

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
from autonomie.models.types import (
    CustomDateType,
    CustomDateType2,
)
from autonomie.models.utils import get_current_timestamp
from autonomie.models.base import (
    DBBASE,
    default_table_args,
)

from autonomie.compute.task import (
    EstimationCompute,
)
from .interfaces import (
    IValidatedTask,
    IMoneyTask,
)
from .invoice import (
    Invoice,
)
from .task import (
    Task,
    DiscountLine,
    TaskLine,
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
    __mapper_args__ = {'polymorphic_identity': 'estimation', }
    id = Column(
        ForeignKey('task.id'),
        primary_key=True,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}},
    )
    # common with only invoices
    deposit = Column(Integer, default=0)
    course = deferred(Column(Integer, nullable=False, default=0), group='edit')

    # Specific to estimations
    exclusions = deferred(Column(Text), group='edit')
    manualDeliverables = deferred(Column(Integer), group='edit')
    paymentDisplay = deferred(
        Column(String(20), default="SUMMARY"),
        group='edit')

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

    def duplicate(self, user, project, phase, customer):
        """
            returns a duplicate estimation object
        """
        seq_number = project.get_next_estimation_number()
        date = datetime.date.today()

        estimation = Estimation()
        estimation.statusPersonAccount = user
        estimation.phase = phase
        estimation.owner = user
        estimation.customer = customer
        estimation.project = project
        estimation.date = date
        estimation.set_sequence_number(seq_number)
        estimation.set_number()
        estimation.set_name()
        if customer.id == self.customer_id:
            estimation.address = self.address
        else:
            estimation.address = customer.full_address

        estimation.description = self.description
        estimation.CAEStatus = "draft"

        estimation.deposit = self.deposit
        estimation.payment_conditions = self.payment_conditions
        estimation.exclusions = self.exclusions
        estimation.manualDeliverables = self.manualDeliverables
        estimation.course = self.course
        estimation.display_units = self.display_units
        estimation.expenses = self.expenses
        estimation.expenses_ht = self.expenses_ht
        estimation.paymentDisplay = self.paymentDisplay
        estimation.line_groups = []
        for group in self.line_groups:
            estimation.line_groups.append(group.duplicate())
        for line in self.payment_lines:
            estimation.payment_lines.append(line.duplicate())
        for line in self.discounts:
            estimation.discounts.append(line.duplicate())
        estimation.mentions = self.mentions
        return estimation

    def _account_invoiceline(self, amount, description, tva=1960):
        """
            Return an account invoiceline
        """
        return TaskLine(cost=amount, description=description, tva=tva)

    def _make_deposit(self, invoice):
        """
            Return a deposit invoice
        """
        invoice.date = datetime.date.today()
        invoice.financial_year = invoice.date.year
        invoice.display_units = 0
        invoice.set_name(deposit=True)
        invoice.set_number(deposit=True)

        for tva, amount in self.deposit_amounts().items():
            description = u"Facture d'acompte"
            line = self._account_invoiceline(amount, description, tva)
            invoice.default_line_group.lines.append(line)
        return invoice, [l.duplicate()
                         for l in invoice.default_line_group.lines]

    def _make_intermediary(self, invoice, paymentline, amounts):
        """
            return an intermediary invoice described by "paymentline"
        """
        invoice.date = paymentline.paymentDate
        invoice.financial_year = paymentline.paymentDate.year
        invoice.display_units = 0
        invoice.set_name()
        invoice.set_number()
        for tva, amount in amounts.items():
            description = paymentline.description
            line = self._account_invoiceline(amount, description, tva)
            invoice.default_line_group.lines.append(line)
        return invoice, [l.duplicate()
                         for l in invoice.default_line_group.lines]

    def _sold_invoice_lines(self, account_lines):
        """
            return the lines that will appear in the sold invoice
        """
        sold_groups = []
        for group in self.line_groups:
            sold_groups.append(group.duplicate())
        order = len(self.line_groups)
        for line in account_lines:
            order = order + 1
            line.cost = -1 * line.cost
            line.order = order
            # On ajoute les lignes au groupe créé par défaut
            sold_groups[0].lines.append(line)
        return sold_groups

    def _make_sold(self, invoice, paymentline, paid_lines, is_sold):
        """
            Return the sold invoice
        """
        invoice.date = paymentline.paymentDate
        invoice.financial_year = paymentline.paymentDate.year
        invoice.set_name(sold=is_sold)
        invoice.set_number()

        invoice.display_units = self.display_units
        invoice.expenses = self.expenses
        invoice.expenses_ht = self.expenses_ht
        # On supprimer le default_task_line group car insère ceux du devis
        invoice.line_groups = []
        for group in self._sold_invoice_lines(paid_lines):
            invoice.line_groups.append(group)
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
        inv.customer = self.customer
        inv.project = self.project
        inv.phase = self.phase
        inv.owner = user
        inv.statusPersonAccount = user
        inv.estimation = self

        # Common args
        inv.payment_conditions = self.payment_conditions
        inv.description = self.description
        inv.course = self.course
        inv.address = self.address
        inv.CAEStatus = "draft"
        inv.set_sequence_number(seq_number)
        inv.mentions = self.mentions
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
        if self.name in [None, ""]:
            taskname_tmpl = u"Devis {0}"
            self.name = taskname_tmpl.format(self.sequence_number)

    def set_number(self):
        tasknumber_tmpl = u"D{s.sequence_number}_{s.date:%m%y}"
        self._number = tasknumber_tmpl.format(s=self)

    def set_sequence_number(self, snumber):
        self.sequence_number = snumber

    @property
    def number(self):
        tasknumber_tmpl = u"{s.project.code}_{s.customer.code}_{s._number}"
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
            line = TaskLine(**kwargs)
        self.default_line_group.lines.append(line)

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
        self.default_line_group.lines = lines

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
        return u"<Estimation id:{s.id} ({s.CAEStatus}>".format(s=self)

    def __json__(self, request):
        result = Task.__json__(self, request)
        result.update(
            dict(
                deposit=self.deposit,
                exclusions=self.exclusions,
                manual_deliverables=self.manualDeliverables,
                manualDeliverables=self.manualDeliverables,
                course=self.course,
                paymentDisplay=self.paymentDisplay,
                payment_lines=[
                    line.__json__(request)
                    for line in self.payment_lines
                ]
            )
        )
        return result


class PaymentLine(DBBASE):
    """
        payments lines
    """
    __tablename__ = 'estimation_payment'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True, nullable=False)
    task_id = Column(Integer, ForeignKey('estimation.id', ondelete="cascade"))
    order = Column(Integer)
    description = Column(Text)
    amount = Column(Integer)
    creationDate = deferred(
        Column(
            CustomDateType,
            default=get_current_timestamp))
    updateDate = deferred(
        Column(
            CustomDateType,
            default=get_current_timestamp,
            onupdate=get_current_timestamp))
    paymentDate = Column(CustomDateType2)
    task = relationship(
        "Estimation",
        backref=backref(
            'payment_lines',
            order_by='PaymentLine.order',
            cascade="all, delete-orphan"
        )
    )

    def duplicate(self):
        """
            duplicate a paymentline
        """
        return PaymentLine(
            order=self.order,
            amount=self.amount,
            description=self.description,
            paymentDate=datetime.date.today()
        )

    def __repr__(self):
        return u"<PaymentLine id:{s.id} task_id:{s.task_id} amount:{s.amount}\
 date:{s.paymentDate}".format(s=self)

    def __json__(self, request):
        return dict(
            order=self.order,
            index=self.order,
            description=self.description,
            cost=self.amount,
            amount=self.amount,
            paymentDate=self.paymentDate,
        )
