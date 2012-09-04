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
    Invoice model
"""
import datetime
import logging

from zope.interface import implementer

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import deferred
from sqlalchemy.orm import backref
from sqlalchemy.orm import validates
# Aye : ici on a du double dans la bdd, en attendant une éventuelle
# migration des données, on dépend entièrement de mysql
from sqlalchemy.dialects.mysql import DOUBLE

from autonomie.models.types import CustomDateType
from autonomie.models.utils import get_current_timestamp
from autonomie.exception import Forbidden
from autonomie.models import DBSESSION
from autonomie.models import DBBASE

from .compute import TaskCompute
from .interfaces import IMoneyTask
from .interfaces import IInvoice
from .interfaces import IPaidTask
from .task import Task
from .states import DEFAULT_STATE_MACHINES

log = logging.getLogger(__name__)

def get_next_officialNumber():
    """
        Return the next available official number
    """
    a = Invoice.get_officialNumber().first()[0]
    b = ManualInvoice.get_officialNumber().first()[0]
    c = CancelInvoice.get_officialNumber().first()[0]
    if not a:
        a = 0
    if not b:
        b = 0
    if not c:
        c = 0
    next_ = max(a,b,c) + 1
    return int(next_)

@implementer(IPaidTask, IInvoice, IMoneyTask)
class Invoice(Task, TaskCompute):
    """
        Invoice Model
    """
    __tablename__ = 'coop_invoice'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    __mapper_args__ = {
                       'polymorphic_identity':'invoice',
                       }
    IDTask = Column("IDTask", ForeignKey('coop_task.IDTask'), primary_key=True)
    IDEstimation = Column("IDEstimation", ForeignKey('coop_estimation.IDTask'))
    IDProject = Column("IDProject", ForeignKey('coop_project.IDProject'))
    sequenceNumber = Column("sequenceNumber", Integer, nullable=False)
    number = Column("number", String(100), nullable=False)
    tva = Column("tva", Integer, nullable=False, default=196)
    paymentConditions = deferred(Column("paymentConditions", Text),
                                 group='edit')
    deposit = deferred(Column('deposit', Integer, nullable=False, default=0),
                       group='edit')
    course = deferred(Column('course', Integer, nullable=False, default=0),
                      group='edit')
    officialNumber = Column("officialNumber", Integer)
    paymentMode = Column("paymentMode", String(10))
    displayedUnits = deferred(Column('displayedUnits', Integer,
                                    nullable=False, default=0),
                                    group='edit')
    discountHT = Column('discountHT', Integer, default=0)
    expenses = deferred(Column('expenses', Integer, default=0), group='edit')

    project = relationship("Project", backref=backref('invoices',
                                            order_by='Invoice.taskDate'))
    phase =  relationship("Phase", backref=backref("invoices",
                                                order_by='Invoice.taskDate'))
    estimation = relationship("Estimation",
                      backref="invoices",
                      primaryjoin="Invoice.IDEstimation==Estimation.IDTask")

    state_machine = DEFAULT_STATE_MACHINES['invoice']

    paid_states = ('resulted',)
    not_paid_states = ('valid', 'paid', 'gencinv')
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
        return self.CAEStatus in ('valid', 'paid', 'gencinv') and tolate

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

    @classmethod
    def get_number(cls, project, seq_number, taskDate, deposit=False):
        if deposit:
            tasknumber_tmpl = u"{0}_{1}_FA{2}_{3:%m%y}"
        else:
            tasknumber_tmpl = u"{0}_{1}_F{2}_{3:%m%y}"
        pcode = project.code
        ccode = project.client.code
        return tasknumber_tmpl.format( pcode, ccode, seq_number, taskDate)

    @validates("paymentMode")
    def validate_paymentMode(self, key, paymentMode):
        """
            Validate the paymentMode
        """
        if not paymentMode in ('CHEQUE', 'VIREMENT'):
            raise Forbidden(u'Mode de paiement inconnu')
        return paymentMode

    @classmethod
    def get_officialNumber(cls):
        """
            Return the next officialNumber available in the Invoice's table
            Take the max of official Number
            when taskDate startswith the current year
            taskdate is a string (YYYYMMDD)
        """
        current_year = datetime.date.today().year
        return DBSESSION.query(func.max(Invoice.officialNumber)).filter(
                Invoice.taskDate.between(current_year*10000,
                                         (current_year+1)*10000
                                    ))

    def gen_cancelinvoice(self, user_id):
        """
            Return a cancel invoice with self's informations
        """
        cancelinvoice = CancelInvoice()
        seq_number = self.project.get_next_cancelinvoice_number()
        cancelinvoice.name = u"Avoir {0}".format(seq_number)
        cancelinvoice.IDPhase = self.IDPhase
        cancelinvoice.CAEStatus = 'draft'
        cancelinvoice.taskDate = datetime.date.today()
        cancelinvoice.description = self.description

        cancelinvoice.IDInvoice = self.IDTask
        cancelinvoice.invoiceDate = self.taskDate
        cancelinvoice.invoiceNumber = self.officialNumber
        cancelinvoice.expenses = -1 * self.expenses
        cancelinvoice.displayedUnits = self.displayedUnits
        cancelinvoice.tva = self.tva
        cancelinvoice.sequenceNumber = seq_number
        cancelinvoice.number = CancelInvoice.get_number(self.project,
                            cancelinvoice.sequenceNumber,
                            cancelinvoice.taskDate)
        cancelinvoice.statusPerson = user_id
        cancelinvoice.IDProject = self.IDProject
        cancelinvoice.IDEmployee = user_id
        for line in self.lines:
            cancelinvoice.lines.append(line.gen_cancelinvoice_line())
        if self.discountHT:
            discount_line = CancelInvoiceLine(cost=self.discountHT,
                                          quantity=1,
                                          description=u"Remise HT",
                                          rowIndex=self.get_next_row_index(),
                                          unity='NONE')
            cancelinvoice.lines.append(discount_line)
        return cancelinvoice

    def get_next_row_index(self):
        return len(self.lines) + 1

    def valid_callback(self):
        """
            Validate an invoice
        """
        self.officialNumber = get_next_officialNumber()
        self.taskDate = datetime.date.today()

    def record_payment(self, mode, amount, resulted=False):
        """
            Validate a record payment
        """
        log.debug("Invoice payment recording")
        log.debug("  o There was to pay : %s" % self.topay())
        log.debug("    ->Is recorded : %s" % amount)
        payment = Payment(mode=mode, amount=amount)
        self.payments.append(payment)
        log.debug("     -> There still to pay : %s" % self.topay())
        if self.topay() == 0 or resulted:
            self.CAEStatus = 'resulted'
        return self

class InvoiceLine(DBBASE):
    """
        Invoice lines
        `IDInvoiceLine` int(11) NOT NULL auto_increment,
        `IDTask` int(11) NOT NULL,
        `rowIndex` int(11) NOT NULL,
        `description` text,
        `cost` int(11) default '0',
        `quantity` double default '1',
        `creationDate` int(11) default '0',
        `updateDate` int(11) default '0',
        `unity` varchar(10) default NULL,
        PRIMARY KEY  (`IDInvoiceLine`),
    """
    __tablename__ = 'coop_invoice_line'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column("IDInvoiceLine", Integer, primary_key=True)
    IDTask = Column(Integer, ForeignKey('coop_invoice.IDTask'))
    rowIndex = Column("rowIndex", Integer, default=1)
    description = Column("description", Text)
    cost = Column(Integer, default=0)
    quantity = Column(DOUBLE, default=1)
    creationDate = deferred(Column("creationDate", CustomDateType,
                                            default=get_current_timestamp))
    updateDate = deferred(Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp))
    unity = Column("unity", String(10))
    task = relationship("Invoice", backref=backref("lines",
                            order_by='InvoiceLine.rowIndex'))

    def duplicate(self):
        """
            duplicate a line
        """
        newone = InvoiceLine()
        newone.rowIndex = self.rowIndex
        newone.cost = self.cost
        newone.description = self.description
        newone.quantity = self.quantity
        newone.unity = self.unity
        return newone

    def gen_cancelinvoice_line(self):
        """
            Return a cancel invoice line duplicating this one
        """
        newone = CancelInvoiceLine()
        newone.rowIndex = self.rowIndex
        newone.cost = -1 * self.cost
        newone.description = self.description
        newone.quantity = self.quantity
        newone.unity = self.unity
        return newone

    def total(self):
        """
            Compute the line's total
        """
        return float(self.cost) * float(self.quantity)
@implementer(IPaidTask, IInvoice, IMoneyTask)
class CancelInvoice(Task, TaskCompute):
    """
        CancelInvoice model
        Could also be called negative invoice
    """
    __tablename__ = 'coop_cancel_invoice'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    __mapper_args__ = {'polymorphic_identity':'cancelinvoice'}
    IDTask = Column(Integer, ForeignKey('coop_task.IDTask'), primary_key=True)

    IDInvoice = Column(Integer, ForeignKey('coop_invoice.IDTask'),
                                                        default=None)
    IDProject = Column(Integer, ForeignKey('coop_project.IDProject'))
    sequenceNumber = deferred(Column(Integer), group='edit')
    number = Column(String(100))
    tva = Column(Integer, default=1960)
    reimbursementConditions = deferred(Column(String(255), default=None),
            group='edit')
    officialNumber = deferred(Column(Integer, default=None), group='edit')
    paymentMode = deferred(Column(String(80), default=None), group='edit')
    displayedUnits = Column(Integer, default=0)
    expenses = deferred(Column(Integer, default=0), group='edit')

    project = relationship("Project", backref=backref('cancelinvoices',
                                            order_by='CancelInvoice.taskDate')
                            )
    phase = relationship("Phase",
                          backref=backref("cancelinvoices",
                                          order_by='CancelInvoice.taskDate')
                          )
    invoice = relationship("Invoice",
                      backref=backref("cancelinvoice", uselist=False),
                      primaryjoin="CancelInvoice.IDInvoice==Invoice.IDTask")

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

    @classmethod
    def get_name(cls, seq_number):
        """
            return an cancelinvoice name
        """
        taskname_tmpl = u"Avoir {0}"
        return taskname_tmpl.format(seq_number)

    @classmethod
    def get_officialNumber(cls):
        """
            Return the greatest officialNumber actually used in the
            ManualInvoice table
        """
        current_year = datetime.date.today().year
        return DBSESSION.query(func.max(CancelInvoice.officialNumber)).filter(
                    func.year(CancelInvoice.taskDate) == current_year)

    def is_tolate(self):
        """
            Return False
        """
        return False

    @classmethod
    def get_number(cls, project, seq_number, taskDate):
        tasknumber_tmpl = u"{0}_{1}_A{2}_{3:%m%y}"
        pcode = project.code
        ccode = project.client.code
        return tasknumber_tmpl.format( pcode, ccode, seq_number, taskDate)

    def valid_callback(self):
        """
            Validate a cancelinvoice
            Generates an official number
        """
        self.officialNumber = get_next_officialNumber()
        self.taskDate = datetime.date.today()

@implementer(IInvoice)
class ManualInvoice(DBBASE):
    """
        Modèle pour les factures manuelles (ancienne version)
    """
    __tablename__ = 'symf_facture_manuelle'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id_ = Column('id', BigInteger, primary_key=True)
    officialNumber = Column('sequence_id', BigInteger)
    description = Column('libelle', String(255))
    montant_ht = Column("montant_ht", Integer)
    tva = Column("tva", Integer)
    payment_ok = Column("paiement_ok", Integer)
    statusDate = Column("paiement_date", Date())
    paymentMode = Column("paiement_comment", String(255))
    client_id = Column('client_id', String(5),
                            ForeignKey('coop_customer.id'))
    taskDate = Column("date_emission", Date(),
                                default=datetime.datetime.now)
    company_id = Column('compagnie_id', BigInteger,
                            ForeignKey('coop_company.IDCompany'))
    created_at = deferred(Column("created_at", DateTime,
                                      default=datetime.datetime.now))
    updated_at = deferred(Column("updated_at", DateTime,
                                      default=datetime.datetime.now,
                                      onupdate=datetime.datetime.now))
    client = relationship("Client",
                primaryjoin="Client.id==ManualInvoice.client_id",
                backref='manual_invoices')
    company = relationship("Company",
                primaryjoin="Company.id==ManualInvoice.company_id",
                  backref='manual_invoices')
    @property
    def statusComment(self):
        return None

    @property
    def payments(self):
        """
            Return a payment object for compatibility
            with other invoices
        """
        return [Payment(mode=self.paymentMode, amount=0, date=self.statusDate)]

    @property
    def id(self):
        return None

    @property
    def IDTask(self):
        return None

    @property
    def number(self):
        """
            return the invoice number
        """
        return u"FACT_MAN_{0}".format(self.officialNumber)

    def get_company(self):
        return self.company

    def get_client(self):
        return self.client

    def is_paid(self):
        return False

    def is_resulted(self):
        return self.payment_ok == 1

    def is_cancelled(self):
        return False

    def is_tolate(self):
        today = datetime.date.today()
        elapsed = today - self.taskDate
        return not self.is_resulted() and elapsed > datetime.timedelta(days=45)

    @validates("paymentMode")
    def validate_paymentMode(self, key, paymentMode):
        """
            Validate the paymentMode
        """
        if not paymentMode in (u'chèque', u'virement'):
            raise Forbidden(u'Mode de paiement inconnu')
        return paymentMode


    def is_cancelinvoice(self):
        """
            return false
        """
        return False

    def is_invoice(self):
        """
            return false
        """
        return False

    @classmethod
    def get_officialNumber(cls):
        """
            Return the greatest officialNumber actually used in the
            ManualInvoice table
        """
        current_year = datetime.date.today().year
        return DBSESSION.query(func.max(ManualInvoice.officialNumber)).filter(
                    func.year(ManualInvoice.taskDate) == current_year)

    def total_ht(self):
        return int(self.montant_ht * 100)

    def tva_amount(self):
        total_ht = self.total_ht()
        if self.tva:
            tva = int(self.tva)
        else:
            tva = 0
        tva = max(tva, 0)
        return int(float(total_ht) * (tva / 10000.0))

class CancelInvoiceLine(DBBASE):
    """
        CancelInvoice lines
        `id` int(11) NOT NULL auto_increment,
        `IDTask` int(11) NOT NULL,
        `rowIndex` int(11) NOT NULL,
        `description` text,
        `cost` int(11) default '0',
        `quantity` double default '1',
        `creationDate` int(11) default '0',
        `updateDate` int(11) default '0',
        `unity` varchar(10) default NULL,
        PRIMARY KEY  (`IDCancelInvoiceLine`),
    """
    __tablename__ = 'coop_cancel_invoice_line'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column(Integer, primary_key=True)
    IDTask = Column(Integer, ForeignKey('coop_cancel_invoice.IDTask'))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                                  onupdate=datetime.datetime.now)
    task = relationship("CancelInvoice", backref="lines",
                            order_by='CancelInvoiceLine.rowIndex'
                        )
    rowIndex = Column(Integer)
    description = Column(Text, default="")
    cost = Column(Integer, default=0)
    quantity = Column(DOUBLE, default=1)
    unity = Column(String(10), default=None)

    def duplicate(self):
        """
            duplicate a line
        """
        newone = CancelInvoiceLine()
        newone.rowIndex = self.rowIndex
        newone.cost = self.cost
        newone.description = self.description
        newone.quantity = self.quantity
        newone.unity = self.unity
        return newone

    def total(self):
        """
            Compute the line's total
        """
        return float(self.cost) * float(self.quantity)

class Payment(DBBASE):
    """
        Payment entry
    """
    __tablename__ = 'coop_payment'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column(Integer, primary_key=True)
    mode = Column(String(50))
    amount = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.now)
    IDTask = Column(Integer, ForeignKey('coop_task.IDTask'))
    document = relationship("Task",
                primaryjoin="Task.IDTask==Payment.IDTask",
                backref=backref('payments', order_by='Payment.date'))

    def get_amount(self):
        return self.amount

    def get_mode_str(self):
        """
            Return a user-friendly string describing the payment Mode
        """
        if self.mode == 'CHEQUE':
            return u"par chèque"
        elif self.mode == 'VIREMENT':
            return u"par virement"
        else:
            return u"mode paiement inconnu"

