# -*- coding: utf-8 -*-
# * File Name : task.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 25-07-2012
# * Last Modified :
#
# * Project :
#
"""
    Model for base tasks

    Sqldump for a task :
      `IDTask` int(11) NOT NULL auto_increment, #identifiant de la tâche
      `IDPhase` int(11) NOT NULL,           # identifiant de la phase associée
      `name` varchar(150) NOT NULL,         # Nom de la tâche

      `CAEStatus` varchar(10) default NULL, # Statut de la tâche
             valid/abort/paid/draft/geninv/aboinv/aboest/sent/wait/none/recinv
      `statusComment` text,                 # Commentaire sur le statut
                                 communication entrepr/CAE
                                 information de paiement ([par chèque ...])
      `statusPerson` int(11) default NULL,  #Id de la personne associée
                                                aux informations de status
      `statusDate` int(11) default NULL,

      `customerStatus` varchar(10) default NULL, # Reste vide
      `taskDate` int(11) default '0',       # Date
      `IDEmployee` int(11) NOT NULL,        #Id de la personne propriétaire
      `document` varchar(255) default NULL,
      `creationDate` int(11) NOT NULL,
      `updateDate` int(11) NOT NULL,
      `description` text,                   #description
      `documentType` varchar(255) default NULL, # header à envoyer pour
                                l'ouverture du document
                                (doit être réservé aux tâches personnalisées)
      `rank` int(11) default NULL,  # Ordre des tâches
      PRIMARY KEY  (`IDTask`),
      KEY `IDPhase` (`IDPhase`),
      KEY `IDEmployee` (`IDEmployee`)
"""
import datetime
import logging

from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implementer

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.orm import deferred
from sqlalchemy.orm import backref
from sqlalchemy import func

# Aye : ici on a du double dans la bdd, en attendant une éventuelle
# migration des données, on dépend entièrement de mysql
from sqlalchemy.dialects.mysql import DOUBLE

from autonomie.models.types import CustomDateType
from autonomie.models.types import CustomDateType2
from autonomie.models.utils import get_current_timestamp
from autonomie.models import DBBASE
from autonomie.utils.exception import Forbidden

log = logging.getLogger(__name__)

class ITask(Interface):
    """
        Task interface, need to be implemented by all documents
    """
    def get_status_str():
        """
            Provide a human readble string for the current task status
        """

    def is_invoice():
        """
            is the current task an invoice ?
        """

    def is_estimation():
        """
            Is the current task an estimation ?
        """

    def is_cancelinvoice():
        """
            Is the current task a cancelled invoice ?
        """

class IValidatedTask(ITask):
    """
        Interface for task needing to be validated by the office
    """
    def is_draft():
        """
            Return the draft status of a document
        """

    def is_editable(manage):
        """
            Is the current task editable ?
        """

    def is_valid():
        """
            Is the current task valid
        """

    def has_been_validated():
        """
            Has the current task been validated ?
        """

    def is_waiting():
        """
            Is the current task waiting for approval
        """

    def is_sent():
        """
            Has the current document been sent to a client
        """

    def is_cancelled():
        """
            Has the current document been cancelled
        """

class IMoneyTask(Interface):
    """
        Interface for task handling money
    """
    def lines_total():
        """
            Return the sum of the document lines
        """

    def total_ht():
        """
            return the HT total of the document
        """

    def discount_amount():
        """
            Return the discount
        """

    def tva_amount(totalht):
        """
            compute the tva
        """

    def total_ttc():
        """
            compute the ttc value before expenses
        """

    def total():
        """
            compute the total to be paid
        """

    def expenses_amount():
        """
            return the TTC expenses
        """


class IPaidTask(Interface):
    """
        Task interface for task needing to be paid
    """
    def is_tolate():
        """
            Is the payment of the current task to late ?
        """

    def is_paid():
        """
            Has the current task been paid
        """


class IInvoice(Interface):
    """
        Invoice interface (used to get an uniform invoice list display
        See templates/invoices.mako (under invoice.model) to see the expected
        common informations
    """
    statusComment = Attribute("""statusComment to allow discussion""")
    statusDate = Attribute("""The date the status has last been changed""")
    officialNumber = Attribute("""official number used in sage""")
    taskDate = Attribute("""Date of the task""")
    id = Attribute("""the document sql id""")
    IDTask = Attribute("""Another name for the id""")
    number = Attribute("""the document's non official number""")
    description = Attribute("""the document description string""")

    def get_company():
        """
            Return the company this task is related to
        """

    def get_client():
        """
            Return the client this document is related to
        """

    def is_paid():
        """
            Has the current task been paid
        """

    def is_cancelled():
        """
            Has the current document been cancelled
        """

    def is_tolate():
        """
            Is it too late
        """

    def is_invoice():
        """
            is the current task an invoice ?
        """

    def is_cancelinvoice():
        """
            Is the current task a cancelled invoice ?
        """

    def get_paymentmode_str():
        """
            Return the string for the payment mode display
        """


class TaskCompute(object):

    # Computing functions
    def lines_total(self):
        return sum(line.total() for line in self.lines)

    def total_ht(self):
        return self.lines_total() - self.discount_amount()

    def discount_amount(self):
        if hasattr(self, "discountHT"):
            return int(self.discountHT)
        else:
            return 0

    def tva_amount(self, totalht=None):
        if not totalht:
            totalht = self.total_ht()
        result = int(float(totalht) * (max(int(self.tva), 0) / 10000.0))
        return result

    def total_ttc(self):
        totalht = self.total_ht()
        tva_amount = self.tva_amount(totalht)
        return int(totalht + tva_amount)

    def total(self):
        return self.total_ttc() + self.expenses_amount()

    def expenses_amount(self):
        result = int(self.expenses)
        return result

DEF_STATUS = u"Statut inconnu"
STATUS = dict((
            ("draft", u"Brouillon modifié",),
            ("wait", u"Validation demandée",),
            ("valid", u"Validé{genre}"),
            ('invalid', u"Invalidé{genre}",),
            ("abort", u"Annulé{genre}",),
            ("geninv", u"Facture générée",),
            ("aboinv", u"Facture annulée",),
            ("aboest", u"Devis annulé",),
            ("sent", u"Document envoyé",),
            ("paid", u"Paiement reçu",),
            ("recinv", u"Client relancé",),
            ('gencinv', u"Avoir généré",),
            ))

EST_STATUS_DICT = {None:('draft',),
                   'draft':('wait', 'duplicate',),
                   'wait':('valid', 'invalid', 'duplicate',),
                   'invalid':('wait', 'duplicate',),
                   'valid':('sent', 'aboest', 'geninv', 'duplicate',),
                   'sent':('aboest', 'geninv', 'duplicate', ),
                   'aboest':('delete',),
                   'geninv':('duplicate',)}
INV_STATUS_DICT = {None:('draft',),
    'draft':('wait', 'duplicate',),
    'wait':('valid', 'invalid', 'duplicate',),
    'invalid':('wait', 'duplicate',),
    'valid':('sent', 'aboinv', 'paid', 'duplicate', 'recinv', "gencinv",),
    'sent':('aboinv', 'paid', 'duplicate', 'recinv', "gencinv" ,),
    'aboinv':('delete',),
    'paid':('duplicate',),
    'recinv':('aboinv', 'paid', 'duplicate',"gencinv",)}

CINV_STATUS_DICT = {'draft':('wait',),
                    'wait':('valid', 'invalid',),
                    'invalid':('wait',),
                    'valid':('sent', 'paid', 'recinv',),
                    'sent':('paid', 'recinv',),
                    'recinv':('paid',),
                    None:('draft',)}

@implementer(ITask)
class Task(DBBASE):
    """
        Metadata pour une tâche (estimation, invoice)
    """
    __tablename__ = 'coop_task'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    __mapper_args__ = {'polymorphic_identity':'task'}

    IDTask = Column(Integer, primary_key=True)
    IDPhase = Column("IDPhase", ForeignKey('coop_phase.IDPhase'))
    name = Column("name", String(255))
    CAEStatus = Column('CAEStatus', String(10))
    statusComment = Column("statusComment", Text)
    statusPerson = Column("statusPerson",
                          ForeignKey('egw_accounts.account_id'))
    statusDate = Column("statusDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp)
    taskDate = Column("taskDate", CustomDateType2)
    IDEmployee = Column("IDEmployee",
                            ForeignKey('egw_accounts.account_id'))
    creationDate = deferred(Column("creationDate", CustomDateType,
                                            default=get_current_timestamp))
    updateDate = Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp)
    description = Column("description", Text)
    statusPersonAccount = relationship("User",
                        primaryjoin="Task.statusPerson==User.id",
                        backref="taskStatuses")
    owner = relationship("User",
                        primaryjoin="Task.IDEmployee==User.id",
                            backref="ownedTasks")

    status_dict = {None:('draft',)}

    def get_status_suffix(self):
        """
            return the status suffix for rendering a pretty status string
        """
        if self.statusPersonAccount:
            firstname = self.statusPersonAccount.firstname
            lastname = self.statusPersonAccount.lastname
        else:
            firstname = "Inconnu"
            lastname = ""
        if self.statusDate:
            if isinstance(self.statusDate, datetime.date) or \
                    isinstance(self.statusDate, datetime.datetime):
                date = self.statusDate.strftime("%d/%m/%Y")
            else:
                date = ""
        else:
            date = ""
        return u" par {firstname} {lastname} le {date}".format(
                firstname=firstname, lastname=lastname, date=date)

    def get_status_str(self):
        """
            Return human readable string for task status
            Task are actually simple documents
        """
        status_str = u"Déposé"
        return status_str + self.get_status_suffix()

    def is_invoice(self):
        return False

    def is_estimation(self):
        return False

    def is_cancelinvoice(self):
        return False

    @validates('CAEStatus')
    def validate_status(self, key, status):
        """
            validate the caestatus change
        """
        log.debug(u"# CAEStatus change #")

        actual_status = self.CAEStatus
        log.debug(u" + was {0}, becomes {1}".format(actual_status, status))
        allowed_status = self.status_dict.get(actual_status, [])


        if status != actual_status and status not in allowed_status:
            message = u"Vous n'êtes pas autorisé à assigner ce statut {0} à \
ce document.".format(status)
            raise Forbidden(message)
        return status

    def get_company(self):
        """
            Return the company owning this task
        """
        if self.project:
            return self.project.company
        else:
            return None

    def get_client(self):
        """
            Return the client of the current task
        """
        if self.project:
            return self.project.client
        else:
            return None

    def get_company_id(self):
        """
            Return the id of the company owning this task
        """
        return self.project.company.id

    @property
    def id(self):
        return self.IDTask

@implementer(IValidatedTask, IMoneyTask)
class Estimation(Task, TaskCompute):
    """
        Estimation Model
    """
    __tablename__ = 'coop_estimation'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    IDTask = Column("IDTask", ForeignKey('coop_task.IDTask'),
                primary_key=True, nullable=False)
    sequenceNumber = Column("sequenceNumber", Integer,
                nullable=False)
    number = Column("number", String(100), nullable=False)
    tva = Column("tva", Integer, nullable=False, default=196)
    deposit = Column("deposit", Integer, default=0)
    paymentConditions = deferred(Column("paymentConditions", Text),
                        group='edit')
    exclusions = deferred(Column("exclusions", Text),
                        group='edit')
    IDProject = Column("IDProject", ForeignKey('coop_project.IDProject'))
    manualDeliverables = deferred(Column("manualDeliverables", Integer),
                        group='edit')
    course = deferred(Column('course', Integer,
                                    nullable=False, default=0),
                                    group='edit')
    displayedUnits = deferred(Column('displayedUnits', Integer,
                                    nullable=False, default=0),
                                    group='edit')
    discountHT = Column('discountHT', Integer, default=0)
    expenses = deferred(Column('expenses', Integer, default=0),
                                group='edit')
    paymentDisplay = deferred(Column('paymentDisplay', String(20),
                                                default="SUMMARY"),
                                                group='edit')
    project = relationship("Project",
                            backref=backref('estimations',
                                            order_by='Estimation.taskDate')
                            )
    phase =  relationship("Phase",
                          backref=backref("estimations",
                          order_by='Estimation.taskDate'))
    __mapper_args__ = {
                        'polymorphic_identity':'estimation',
                       }

    status_dict = EST_STATUS_DICT

    #ITask interface
    def get_status_str(self):
        status_str = STATUS.get(self.CAEStatus, DEF_STATUS).format(genre=u"")
        return status_str + self.get_status_suffix()

    def is_draft(self):
        return self.CAEStatus in ('draft', 'invalid',)

    def is_editable(self, manage=False):
        if manage:
            return self.CAEStatus in ('draft', 'invalid', 'wait',)
        else:
            return self.CAEStatus in ('draft', 'invalid')

    def is_valid(self):
        return self.CAEStatus == 'valid'

    def has_been_validated(self):
        return self.CAEStatus in ('valid', 'geninv', 'sent',)

    def is_waiting(self):
        return self.CAEStatus == 'wait'

    def is_sent(self):
        return self.CAEStatus == "sent"


    def is_estimation(self):
        return True

    def get_next_actions(self):
        """
            Return the next available actions regarding the current status
        """
        return matchdict[self.CAEStatus]

    def duplicate(self, user, project):
        """
            returns a duplicate estimation object
        """
        seq_number = project.get_next_estimation_number()
        taskDate = datetime.date.today()

        log.debug("# Estimation Duplication #")
        duple = Estimation()
        duple.CAEStatus = u'draft'
        duple.IDPhase = self.IDPhase
        duple.taskDate = taskDate
        duple.IDEmployee = self.IDEmployee
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
        duple.lines = self.get_duplicated_lines()
        duple.payment_lines = self.get_duplicated_payment_lines()

        # Setting relationships at the end of the duplication
        log.debug("    adding relationships")
        duple.statusPersonAccount = user
        duple.project = project
        log.debug("-> Returning the duplicate")
        return duple

    def _common_args_for_generation(self, user_id):
        """
            Return the args common to all the generated invoices
        """
        return dict(IDProject = self.IDProject,
                    IDPhase = self.IDPhase,
                    CAEStatus = 'draft',
                    statusPerson = user_id,
                    IDEmployee = user_id,
                    tva = self.tva,
                    IDEstimation=self.IDTask,
                    paymentConditions=self.paymentConditions,
                    description=self.description,
                    course=self.course)

    def _account_invoiceline(self, amount, description):
        """
            Return an account invoiceline
        """
        return InvoiceLine(cost=amount, description=description)

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

    def _deposit_invoice(self, args):
        """
            Return the deposit
        """
        args['taskDate'] = datetime.date.today()
        invoice = self._account_invoice(args)
        amount = self.deposit_amount()
        description=u"Facture d'accompte"
        line = self._account_invoiceline(amount, description)
        invoice.lines.append(line)
        return invoice, line.duplicate()

    def _intermediate_invoices(self, args, paymentline, count):
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
        line = self._account_invoiceline(amount, description)
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
        return invoice

    def gen_invoices(self, user_id):
        """
            Return the invoices based on the current estimation
        """
        invoices = []
        lines = []
        common_args = self._common_args_for_generation(user_id)
        count = 0
        if self.deposit > 0:
            deposit, line = self._deposit_invoice(common_args.copy())
            invoices.append(deposit)
            # We remember the lines to display them in the laste invoice
            lines.append(line)
            count += 1
        # all payment lines specified (less the last one)
        for paymentline in self.payment_lines[:-1]:
            invoice, line = self._intermediate_invoices(common_args.copy(),
                                                            paymentline,
                                                            count)
            invoices.append(invoice)
            lines.append(line)
            count += 1

        invoice = self._sold_invoice(common_args.copy(),
                                     self.payment_lines[-1],
                                     count,
                                     lines)
        invoices.append(invoice)
        return invoices


    def get_duplicated_lines(self):
        """
            return duplicated lines
        """
        newlines = []
        for line in self.lines:
            newlines.append(line.duplicate())
        return newlines

    def get_duplicated_payment_lines(self):
        """
            return duplicated payment lines
        """
        newlines = []
        for line in self.payment_lines:
            newlines.append(line.duplicate())
        return newlines

    @classmethod
    def get_name(cls, seq_number):
        taskname_tmpl = u"Devis {0}"
        return taskname_tmpl.format(seq_number)

    @classmethod
    def get_number(cls, project, seq_number, taskDate):
        tasknumber_tmpl = u"{0}_{1}_D{2}_{3:%m%y}"
        pcode = project.code
        ccode = project.client.id
        return tasknumber_tmpl.format( pcode, ccode, seq_number, taskDate)

    def is_deletable(self):
        """
            Returns True if the estimation could be deleted
        """
        return self.CAEStatus not in ('geninv',)

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
                result = rest - ((payment_lines_num-1) * line_amount)
            else:
                result = rest - sum(line.amount \
                        for line in self.payment_lines[:-1])
        return result

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
                      backref="invoice",
                      primaryjoin="Invoice.IDEstimation==Estimation.IDTask")

    status_dict = INV_STATUS_DICT

    def get_status_str(self):
        status_str = STATUS.get(self.CAEStatus, DEF_STATUS).format(genre=u'e')
        return status_str + self.get_status_suffix()

    def is_draft(self):
        return self.CAEStatus in ('draft', 'invalid',)

    def is_editable(self, manage=False):
        if manage:
            return self.CAEStatus in ('draft', 'invalid', 'wait',)
        else:
            return self.CAEStatus in ('draft', 'invalid',)

    def is_valid(self):
        return self.CAEStatus == 'valid'

    def has_been_validated(self):
        return self.CAEStatus in ('valid', 'geninv', 'sent', "recinv",)

    def is_waiting(self):
        return self.CAEStatus == "wait"

    def is_sent(self):
        return self.CAEStatus == "sent"

    def is_invoice(self):
        return True

    def is_paid(self):
        return self.CAEStatus == 'paid'

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
        return self.CAEStatus in ('valid', 'sent','recinv') and tolate

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

    def get_next_actions(self):
        """
            Return the next available actions regarding the current status
        """
        return matchdict[self.CAEStatus]

    def get_paymentmode_str(self):
        """
            Return a user-friendly string describing the payment Mode
        """
        if self.paymentMode == 'CHEQUE':
            return u"par chèque"
        elif self.paymentMode == 'VIREMENT':
            return u"par virement"
        else:
            return u"mode paiement inconnu"

    @classmethod
    def get_number(cls, project, seq_number, taskDate, deposit=False):
        if deposit:
            tasknumber_tmpl = u"{0}_{1}_FA{2}_{3:%m%y}"
        else:
            tasknumber_tmpl = u"{0}_{1}_F{2}_{3:%m%y}"
        pcode = project.code
        ccode = project.client.id
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
    def get_officialNumber(cls, dbsession):
        """
            Return the next officialNumber available in the Invoice's table
            Take the max of official Number
            when taskDate startswith the current year
            taskdate is a string (YYYYMMDD)
        """
        current_year = datetime.date.today().year
        return dbsession.query(func.max(Invoice.officialNumber)).filter(
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
                      backref="cancelinvoice",
                      primaryjoin="CancelInvoice.IDInvoice==Invoice.IDTask")

    status_dict = CINV_STATUS_DICT

    def get_status_str(self):
        status_str = STATUS.get(self.CAEStatus, DEF_STATUS).format(genre=u'')
        if self.CAEStatus == 'paid':
            status_str = u"Réglé"
        return status_str + self.get_status_suffix()


    def is_draft(self):
        return self.CAEStatus in ('draft', 'invalid')

    def is_editable(self, manage=False):
        if manage:
            return self.CAEStatus in ('draft', 'invalid', 'wait',)
        else:
            return self.CAEStatus in ('draft', 'invalid',)

    def is_valid(self):
        return self.CAEStatus == 'valid'

    def has_been_validated(self):
        return self.CAEStatus in ('valid', 'sent', "recinv",)

    def is_waiting(self):
        return self.CAEStatus == 'wait'

    def is_sent(self):
        return self.CAEStatus == "sent"

    def is_cancelinvoice(self):
        return True

    def is_paid(self):
        return self.CAEStatus == 'paid'

    def is_cancelled(self):
        return False

    @classmethod
    def get_name(cls, seq_number):
        """
            return an cancelinvoice name
        """
        taskname_tmpl = u"Avoir {0}"
        return taskname_tmpl.format(seq_number)

    def get_paymentmode_str(self):
        """
            Return a user-friendly string describing the payment Mode
        """
        if self.paymentMode == 'CHEQUE':
            return u"par chèque"
        elif self.paymentMode == 'VIREMENT':
            return u"par virement"
        else:
            return u"mode paiement inconnu"

    @classmethod
    def get_officialNumber(cls, dbsession):
        """
            Return the greatest officialNumber actually used in the
            ManualInvoice table
        """
        current_year = datetime.date.today().year
        return dbsession.query(func.max(CancelInvoice.officialNumber)).filter(
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
        ccode = project.client.id
        return tasknumber_tmpl.format( pcode, ccode, seq_number, taskDate)

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
                            ForeignKey('coop_customer.code'))
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
    def statusDate(self):
        return None

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
        return self.payment_ok == 1

    def is_cancelled(self):
        return False

    def is_tolate(self):
        today = datetime.date.today()
        elapsed = today - self.taskDate
        return not self.is_paid() and elapsed > datetime.timedelta(days=45)

    def get_paymentmode_str(self):
        """
            Return the payment mode string
        """
        if self.paymentMode == u'chèque':
            return u"par chèque"
        elif self.paymentMode == u'virement':
            return u"par virement"
        else:
            return u""

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
    def get_officialNumber(cls, dbsession):
        """
            Return the greatest officialNumber actually used in the
            ManualInvoice table
        """
        current_year = datetime.date.today().year
        return dbsession.query(func.max(ManualInvoice.officialNumber)).filter(
                    func.year(ManualInvoice.taskDate) == current_year)

    def total_ht(self):
        return int(self.montant_ht * 100)

    def tva_amount(self):
        total_ht = self.total_ht()
        tva = max(int(self.tva), 0)
        return int(float(total_ht) * (tva / 10000.0))

class EstimationLine(DBBASE):
    """
      `IDWorkLine` int(11) NOT NULL auto_increment,
      `IDTask` int(11) NOT NULL,
      `rowIndex` int(11) NOT NULL,          # index de la ligne
      `description` text,                   # "Prestation"
      `cost` int(11) default NULL,          # montant
      `quantity` double default NULL,       #quantité
      `creationDate` int(11) default NULL,
      `updateDate` int(11) default NULL,
      `unity` varchar(10) default NULL,     # unité
      PRIMARY KEY  (`IDWorkLine`),
      KEY `coop_estimation_line_IDTask` (`IDTask`),
      KEY `coop_estimation_line_rowIndex` (`rowIndex`),
      KEY `IDTask` (`IDTask`)
    """
    __tablename__ = 'coop_estimation_line'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column("IDWorkLine", Integer, primary_key=True)
    IDTask = Column(Integer, ForeignKey('coop_estimation.IDTask'))
    rowIndex = Column("rowIndex", Integer)
    description = Column("description", Text)
    cost = Column(Integer, default=0)
    quantity = Column(DOUBLE, default=1)
    creationDate = deferred(Column("creationDate", CustomDateType,
                                            default=get_current_timestamp))
    updateDate = deferred(Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp))
    unity = Column("unity", String(10))
    task = relationship("Estimation", backref=backref("lines",
                            order_by='EstimationLine.rowIndex'))

    def get_unity_label(self, pretty=False):
        """
            return unitie's label
        """
        if pretty:
            default = u""
        else:
            default = u"-"
        labels = dict(
                NONE=default,
                HOUR=u"heure(s)",
                DAY=u"jour(s)",
                WEEK=u"semaine(s)",
                MONTH=u"mois",
                FEUIL=u"feuillet(s)",
                PACK=u"forfait",
                )
        return labels.get(self.unity, default)

    def duplicate(self):
        """
            duplicate a line
        """
        newone = EstimationLine()
        newone.rowIndex = self.rowIndex
        newone.cost = self.cost
        newone.description = self.description
        newone.quantity = self.quantity
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
        line.unity = self.unity
        return line

    def total(self):
        """
            Compute the line's total
        """
        return float(self.cost) * float(self.quantity)


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

    def get_unity_label(self, pretty=False):
        """
            return unitie's label
        """
        if pretty:
            default = u""
        else:
            default = u"-"
        labels = dict(
                NONE=default,
                HOUR=u"heure(s)",
                DAY=u"jour(s)",
                WEEK=u"semaine(s)",
                MONTH=u"mois",
                FEUIL=u"feuillet(s)",
                PACK=u"forfait",
                )
        return labels.get(self.unity, default)

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

    def get_unity_label(self, pretty=False):
        """
            return unitie's label
        """
        if pretty:
            default = u""
        else:
            default = u"-"
        labels = dict(
                NONE=default,
                HOUR=u"heure(s)",
                DAY=u"jour(s)",
                WEEK=u"semaine(s)",
                MONTH=u"mois",
                FEUIL=u"feuillet(s)",
                PACK=u"forfait",
                )
        return labels.get(self.unity, default)

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

class PaymentLine(DBBASE):
    """
        coop_estimation_payment
        `IDPaymentLine` int(11) NOT NULL auto_increment,
        `IDTask` int(11) NOT NULL,
        `rowIndex` int(11) NOT NULL,
        `description` text,
        `amount` int(11) default NULL,
        `creationDate` int(11) default NULL,
        `updateDate` int(11) default NULL,
        `paymentDate` int(11) default NULL,
    """
    __tablename__ = 'coop_estimation_payment'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column("IDPaymentLine", Integer, primary_key=True, nullable=False)
    IDTask = Column(Integer, ForeignKey('coop_estimation.IDTask'))
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
        newone = PaymentLine()
        newone.rowIndex = self.rowIndex
        newone.amount = self.amount
        newone.description = self.description
        newone.paymentDate = datetime.date.today()
        return newone
