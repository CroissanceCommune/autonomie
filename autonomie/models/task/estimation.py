# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-09-2012
# * Last Modified :
#
# * Project :
#
"""
    The estimation model
"""
import datetime
import logging

from zope.interface import implementer

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import deferred
from sqlalchemy.orm import backref
# Aye : ici on a du double dans la bdd, en attendant une éventuelle
# migration des données, on dépend entièrement de mysql
from sqlalchemy.dialects.mysql import DOUBLE

from autonomie.models.types import CustomDateType
from autonomie.models.types import CustomDateType2
from autonomie.models.utils import get_current_timestamp
from autonomie.models import DBBASE

from .compute import TaskCompute
from .interfaces import IValidatedTask
from .interfaces import IMoneyTask
from .invoice import Invoice
from .invoice import InvoiceLine
from .task import Task
from .task import DiscountLine
from .states import DEFAULT_STATE_MACHINES

log = logging.getLogger(__name__)


@implementer(IValidatedTask, IMoneyTask)
class Estimation(Task, TaskCompute):
    """
        Estimation Model
    """
    __tablename__ = 'estimation'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset": 'utf8'}
    id = Column("id", ForeignKey('task.id'), primary_key=True, nullable=False)
    sequenceNumber = Column("sequenceNumber", Integer, nullable=False)
    number = Column("number", String(100), nullable=False)
    tva = Column("tva", Integer, nullable=False, default=196)
    deposit = Column("deposit", Integer, default=0)
    paymentConditions = deferred(
        Column("paymentConditions", Text),
        group='edit')
    exclusions = deferred(Column("exclusions", Text), group='edit')
    project_id = Column("project_id", ForeignKey('project.id'))
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
    paymentDisplay = deferred(
        Column('paymentDisplay', String(20), default="SUMMARY"),
        group='edit')
    project = relationship(
        "Project",
        backref=backref('estimations', order_by='Estimation.taskDate')
    )

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

    def duplicate(self, user, project, phase):
        """
            returns a duplicate estimation object
        """
        seq_number = project.get_next_estimation_number()
        taskDate = datetime.date.today()

        log.debug("# Estimation Duplication #")
        duple = Estimation()
        duple.CAEStatus = u'draft'
        duple.taskDate = taskDate
        duple.owner_id = self.owner_id
        duple.description = self.description
        duple.sequenceNumber = seq_number

        duple.name = self.get_name(seq_number)
        duple.number = self.get_number(project, seq_number, taskDate)

        duple.tva = self.tva
        duple.deposit = self.deposit
        duple.paymentConditions = self.paymentConditions
        duple.exclusions = self.exclusions
        duple.manualDeliverables = self.manualDeliverables
        duple.course = self.course
        duple.displayedUnits = self.displayedUnits
        duple.discountHT = self.discountHT
        duple.expenses = self.expenses
        duple.paymentDisplay = self.paymentDisplay
        # Setting relationships at the end of the duplication
        log.debug("    adding relationships")
        duple.phase = phase
        duple.statusPersonAccount = user
        duple.project = project
        for line in self.lines:
            duple.lines.append(line.duplicate())
        for line in self.payment_lines:
            duple.payment_lines.append(line.duplicate())
        for line in self.discounts:
            duple.discounts.append(line.duplicate())

        log.debug("-> Returning the duplicate")
        return duple

    def _common_args_for_generation(self, user_id):
        """
            Return the args common to all the generated invoices
        """
        return dict(project_id=self.project_id,
                    phase_id=self.phase_id,
                    CAEStatus = 'draft',
                    statusPerson = user_id,
                    owner_id=user_id,
                    estimation_id=self.id,
                    paymentConditions=self.paymentConditions,
                    description=self.description,
                    course=self.course)

    def _account_invoiceline(self, amount, description, tva=1960):
        """
            Return an account invoiceline
        """
        return InvoiceLine(cost=amount, description=description, tva=tva)

    def _account_invoice(self, args, count=0):
        """
            Return an account invoice
        """
        args['sequenceNumber'] = self.project.get_next_invoice_number() + count
        args['name'] = Invoice.get_name(count + 1, account=True)
        args['number'] = Invoice.get_number(self.project,
                                            args['sequenceNumber'],
                                            args['taskDate'],
                                            deposit=True)
        args['displayedUnits'] = 0
        return Invoice(**args)

    def _deposit_invoice(self, args, tva):
        """
            Return the deposit
        """
        args['taskDate'] = datetime.date.today()
        invoice = self._account_invoice(args)
        amount = self.deposit_amount()
        description = u"Facture d'accompte"
        line = self._account_invoiceline(amount, description, tva)
        invoice.lines.append(line)
        return invoice, line.duplicate()

    def _intermediate_invoices(self, args, paymentline, count, tva):
        """
            return an intermediary invoice described by "paymentline"
        """
        args['taskDate'] = paymentline.paymentDate
        invoice = self._account_invoice(args, count)
        if self.manualDeliverables:
            amount = paymentline.amount
        else:
            amount = self.paymentline_amount()
        description = paymentline.description
        line = self._account_invoiceline(amount, description, tva)
        invoice.lines.append(line)
        return invoice, line.duplicate()

    def _sold_invoice_name(self, seq_number, count):
        """
            Return the name of the last invoice
        """
        if count > 0:
            sold = True
        else:
            sold = False
        return Invoice.get_name(seq_number, sold=sold)

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

    def _sold_invoice(self, args, paymentline, count, account_lines):
        """
            Return the sold invoice
        """
        args['taskDate'] = paymentline.paymentDate
        args['sequenceNumber'] = self.project.get_next_invoice_number() + count
        args['name'] = self._sold_invoice_name(args['sequenceNumber'], count)
        args['number'] = Invoice.get_number(self.project,
                                            args['sequenceNumber'],
                                            args['taskDate'])
        args['displayedUnits'] = self.displayedUnits
        args['expenses'] = self.expenses
        args['discountHT'] = self.discountHT
        invoice = Invoice(**args)
        for line in self._sold_invoice_lines(account_lines):
            invoice.lines.append(line)
        for line in self.discounts:
            invoice.discounts.append(line.duplicate())
        return invoice

    def gen_invoices(self, user_id):
        """
            Return the invoices based on the current estimation
        """
        invoices = []
        lines = []
        common_args = self._common_args_for_generation(user_id)
        count = 0
        # Fix temporaire pour le montant de la tva pour les accomptes et autres
        tvas = self.get_tvas().keys()
        tva = tvas[0]
        if self.deposit > 0:
            deposit, line = self._deposit_invoice(common_args.copy(), tva)
            invoices.append(deposit)
            # We remember the lines to display them in the laste invoice
            lines.append(line)
            count += 1
        # all payment lines specified (less the last one)
        for paymentline in self.payment_lines[:-1]:
            invoice, line = self._intermediate_invoices(common_args.copy(),
                                                            paymentline,
                                                            count, tva)
            invoices.append(invoice)
            lines.append(line)
            count += 1

        invoice = self._sold_invoice(common_args.copy(),
                                     self.payment_lines[-1],
                                     count,
                                     lines)
        invoices.append(invoice)
        return invoices

    @classmethod
    def get_name(cls, seq_number):
        taskname_tmpl = u"Devis {0}"
        return taskname_tmpl.format(seq_number)

    @classmethod
    def get_number(cls, project, seq_number, taskDate):
        tasknumber_tmpl = u"{0}_{1}_D{2}_{3:%m%y}"
        pcode = project.code
        ccode = project.client.code
        return tasknumber_tmpl.format( pcode, ccode, seq_number, taskDate)

    def is_cancelled(self):
        """
            Return True if the invoice has been cancelled
        """
        return self.CAEStatus == 'aboest'

    # Computing
    def deposit_amount(self):
        """
            Compute the amount of the deposit
        """
        if self.deposit > 0:
            total = self.total()
            return int(total * int(self.deposit) / 100.0)
        return 0

    def get_nb_payment_lines(self):
        """
            Returns the number of payment lines configured
        """
        return len(self.payment_lines)

    def paymentline_amount(self):
        """
            Compute payment lines amounts in case of equal division
            (when manualDeliverables is 0)
            (when the user has checked 3 times)
        """
        total = self.total()
        deposit = self.deposit_amount()
        rest = total - deposit
        return int(rest / self.get_nb_payment_lines())

    def sold(self):
        """
            Compute the sold amount to finish on an exact value
            if we divide 10 in 3, we'd like to have something like :
                3.33 3.33 3.34
        """
        result = 0
        total = self.total()
        deposit = self.deposit_amount()
        rest = total - deposit
        payment_lines_num = self.get_nb_payment_lines()
        if payment_lines_num == 1 or not self.get_nb_payment_lines():
            result = rest
        else:
            if self.manualDeliverables == 0:
                line_amount = self.paymentline_amount()
                result = rest - ((payment_lines_num - 1) * line_amount)
            else:
                result = rest - sum(line.amount \
                        for line in self.payment_lines[:-1])
        return result

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


class EstimationLine(DBBASE):
    """
        Estimation lines
    """
    __tablename__ = 'estimation_line'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset": 'utf8'}
    id = Column("id", Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('estimation.id'))
    rowIndex = Column("rowIndex", Integer)
    description = Column("description", Text)
    cost = Column(Integer, default=0)
    quantity = Column(DOUBLE, default=1)
    tva = Column("tva", Integer, nullable=False, default=196)
    creationDate = deferred(Column("creationDate", CustomDateType,
                                            default=get_current_timestamp))
    updateDate = deferred(Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp))
    unity = Column("unity", String(10))
    task = relationship("Estimation", backref=backref("lines",
                            order_by='EstimationLine.rowIndex'))

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

    def total_ht(self):
        """
            Compute the line's total
        """
        return float(self.cost) * float(self.quantity)

    def tva_amount(self, totalht=None):
        """
            compute the tva amount of a line
        """
        totalht = self.total_ht()
        result = float(totalht) * (max(int(self.tva), 0) / 10000.0)
        return result

    def total(self):
        return self.tva_amount() + self.total_ht()

    def __repr__(self):
        return u"<EstimationLine id:{s.id} task_id:{s.task_id} cost:{s.cost}\
 quantity:{s.quantity} tva:{s.tva}".format(s=self)


class PaymentLine(DBBASE):
    """
        payments lines
    """
    __tablename__ = 'estimation_payment'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset": 'utf8'}
    id = Column("id", Integer, primary_key=True, nullable=False)
    task_id = Column(Integer, ForeignKey('estimation.id'))
    rowIndex = Column("rowIndex", Integer)
    description = Column("description", Text)
    amount = Column("amount", Integer)
    creationDate = deferred(Column("creationDate", CustomDateType,
                                            default=get_current_timestamp))
    updateDate = deferred(Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp))
    paymentDate = Column("paymentDate", CustomDateType2(11))
    estimation = relationship("Estimation", backref=backref('payment_lines',
                    order_by='PaymentLine.rowIndex'))

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
