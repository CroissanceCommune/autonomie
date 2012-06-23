# -*- coding: utf-8 -*-
# * File Name : model.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : sam. 23 juin 2012 15:26:10 CEST
#
# * Project : autonomie
#
"""
    Autonomie's SQLA models
"""
import os
import datetime
import time

from hashlib import md5

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import Numeric
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.orm import backref
from sqlalchemy.types import TypeDecorator
from sqlalchemy.types import Integer as Integer_type
from sqlalchemy.types import String as String_type

from autonomie.models import DBBASE
from autonomie.utils.exception import Forbidden

class CustomDateType(TypeDecorator):
    """
        Custom date type used because our database is using
        integers to store date's timestamp
    """
    impl = Integer_type
    def process_bind_param(self, value, dialect):
        if value is None or not value:
            return int(time.time())
        elif isinstance(value, datetime.datetime):
            return int(time.mktime(value.timetuple()))
        elif isinstance(value, int):
            return value
        return time.mktime(value.timetuple())

    def process_result_value(self, value, dialect):
        if value:
            return datetime.datetime.fromtimestamp(float(value))
        else:
            return datetime.datetime.now()

def format_to_taskdate(value):
    """
        format a datetime.date object to a 'taskdate' format:
        an integer composed from a string YYYYmmdd
        Sorry .... it's not my responsability
    """
    if value is None:
        return None
    elif isinstance(value, datetime.date):
        if value.year < 1900:
            value.year = 1901
        return int(value.strftime("%Y%m%d"))
    else:
        return int(value)

DEFAULT_DATETIME = datetime.date(2000, 1, 1)

def format_from_taskdate(value):
    """
        return a datetime.date object from an integer in 'taskdate' format
    """
    if value:
        value = str(value)
        try:
            year = int(value[0:4])
            assert year > 1910
        except:
            year = 2000
        try:
            month = int(value[4:6])
            assert month in range(1,12)
        except:
            month = 1
        try:
            day = int(value[6:8])
            assert day in range(1,31)
        except:
            day = 1
        try:
            return datetime.date(year, month, day)
        except:
            return datetime.date(year, 1, 1)
    else:
        return DEFAULT_DATETIME

class CustomDateType2(TypeDecorator):
    """
        Custom date type used because our database is using
        custom integers to store dates
        YYYYMMDD
    """
    impl = Integer_type
    def process_bind_param(self, value, dialect):
        return format_to_taskdate(value)

    def process_result_value(self, value, dialect):
        return format_from_taskdate(value)

class CustomFileType(TypeDecorator):
    """
        Custom Filetype used to glue deform fileupload tools with
        the database element
    """
    impl = String_type
    def __init__(self, prefix, *args, **kw):
        TypeDecorator.__init__(self, *args, **kw)
        self.prefix = prefix

    def process_bind_param(self, value, dialect):
        """
            process the insertion of the value
            write the file to persistent storage
        """
        ret_val = None
        if isinstance(value, dict):
            ret_val = value.get('filename', '')
        return ret_val

    def process_result_value(self, value, dialect):
        """
            Get the datas from database
        """
        if value:
            return dict(filename = value,
                        uid=self.prefix + value)
        else:
            return dict(filename="",
                        uid=self.prefix)

class CustomInteger(TypeDecorator):
    """
        Custom integer, allow long to int automatic conversion
    """
    impl = Integer_type
    def process_bind_param(self, value, dialect):
        """
            On insertion
        """
        if isinstance(value, long):
            value = int(value)
        return value

    def process_result_value(self, value, dialect):
        """
            On query
        """
        if isinstance(value, long):
            value = int(value)
        return value

def _get_current_timestamp():
    """
        returns current time
    """
    return int(time.time())

company_employee = Table('coop_company_employee', DBBASE.metadata,
    Column("IDCompany", Integer, ForeignKey('coop_company.IDCompany')),
    # IDEmployee est identique dans la table coop_employee
    Column("IDEmployee", Integer, ForeignKey('egw_accounts.account_id')),
    autoload=True)

class Company(DBBASE):
    """
        `IDCompany` int(11) NOT NULL auto_increment,
        `name` varchar(150) NOT NULL,
        `object` varchar(255) NOT NULL,
        `email` varchar(255) default NULL,
        `phone` varchar(20) NOT NULL,
        `mobile` varchar(20) default NULL,
        `comments` text,
        `creationDate` int(11) NOT NULL,
        `updateDate` int(11) NOT NULL,
        `active` varchar(1) NOT NULL default 'Y',
        `IDGroup` int(11) NOT NULL,
        `logo` varchar(255) default NULL,
        `header` varchar(255) default NULL,
        `logoType` varchar(255) default NULL,
        `headerType` varchar(255) default NULL,
        `IDEGWUser` int(11) NOT NULL, # Company EGW account
        `RIB` varchar(255) default NULL,
        `IBAN` varchar(255) default NULL,
        PRIMARY KEY  (`IDCompany`)
    """
    __tablename__ = 'coop_company'
    __table_args__ = {'autoload':True}
    id = Column("IDCompany", Integer, primary_key=True)
    name = Column("name", String(150))
    clients = relationship("Client",
                            order_by="Client.id",
                            backref='company')
    projects = relationship("Project",
                            order_by="Project.id",
                            backref="company")
    creationDate = Column("creationDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType(11),
                                        default=_get_current_timestamp,
                                        onupdate=_get_current_timestamp)
    goal = Column("object", String(255))
    logo = Column("logo", CustomFileType("logo_", 255))
    header = Column("header", CustomFileType("header_", 255))
    IDGroup = Column("IDGroup", Integer, default=0)
    phone = Column("phone", String(20), default="")
    IDEGWUser = Column("IDEGWUser", Integer, default=0)

    def get_path(self):
        """
            get the relative filepath specific to the given company
        """
        return os.path.join("company", str(self.id))

    def get_header_filepath(self):
        """
            Returns the header's relative filepath
        """
        if self.header:
            return os.path.join(self.get_path(),
                            'header',
                            self.header['filename'])
        else:
            return None

    def get_logo_filepath(self):
        """
            Return the logo's relative filepath
        """
        if self.logo:
            return os.path.join(self.get_path(),
                            'logo',
                             self.logo['filename'])
        else:
            return None

    def get_company_id(self):
        """
            Return the current company id
            Allows company id access through request's context
        """
        return self.id

    @classmethod
    def query(cls, dbsession, keys=None):
        if keys:
            return dbsession.query(*keys)
        else:
            return dbsession.query(Company).order_by(Company.name)


class User(DBBASE):
    """
        `account_id` int(11) NOT NULL auto_increment,
        `account_lid` varchar(64) NOT NULL,
        `account_pwd` varchar(100) NOT NULL,
        `account_firstname` varchar(50) default NULL,
        `account_lastname` varchar(50) default NULL,
        `account_lastlogin` int(11) default NULL,
        `account_lastloginfrom` varchar(255) default NULL,
        `account_lastpwd_change` int(11) default NULL,
        `account_status` varchar(1) NOT NULL default 'A',
        `account_expires` int(11) default NULL,
        `account_type` varchar(1) default NULL,
        `person_id` int(11) default NULL,
        `account_primary_group` int(11) NOT NULL default '0',
        `account_email` varchar(100) default NULL,
        `account_challenge` varchar(100) default NULL,
        `account_response` varchar(100) default NULL,
        PRIMARY KEY  (`account_id`),
        UNIQUE KEY `egw_accounts_account_lid` (`account_lid`)

    """
    __tablename__ = 'egw_accounts'
    __table_args__ = {'autoload':True}
    id = Column('account_id', Integer, primary_key=True)
    login = Column('account_lid', String(64))
    pwd = Column("account_pwd", String(100))
    lastname = Column("account_lastname", String(50))
    firstname = Column("account_firstname", String(50))
    email = Column("account_email", String(100))
    companies = relationship("Company",
                             secondary=company_employee,
                             backref="employees")
    primary_group = Column("account_primary_group",
                            Integer)

    @staticmethod
    def _encode_pass(password):
        return md5(password).hexdigest()

    def set_password(self, password):
        """
            Set the user's password
        """
        self.pwd = self._encode_pass(password)

    def auth(self, password):
        """
            Authentify the current record with password
        """
        if password:
            return self.pwd == self._encode_pass(password)
        else:
            return False

    def get_company(self, cid):
        """
            Return the company
        """
        if not isinstance(cid, int):
            cid = int(cid)
        for company in self.companies:
            if company.id == cid:
                return company
        raise KeyError

    def is_admin(self):
        """
            return true if the user is and administrator
        """
        return self.primary_group == 1

    def is_manager(self):
        """
            return True if the user is a manager
        """
        return self.primary_group == 2

    def is_contractor(self):
        """
            return True if the user is a contractor
        """
        return self.primary_group == 3

    @classmethod
    def query(cls, dbsession):
        """
            Query users
            Note : join on companies allows us to avoid egw accounts
                    which are not used inside egw's coopagest plugin
        """
        return dbsession.query(User).join(User.companies)

class Employee(DBBASE):
    """
        `IDEmployee` int(11) NOT NULL,
        `comments` text,
        `creationDate` int(11) NOT NULL,
        `updateDate` int(11) NOT NULL,
        `IDContact` int(11) default NULL,
        PRIMARY KEY  (`IDEmployee`)
    """
    __tablename__ = 'coop_employee'
    __table_args__ = {'autoload':True}
    id = Column("IDEmployee", Integer, primary_key=True)
    creationDate = Column("creationDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType(11),
                                        default=_get_current_timestamp,
                                        onupdate=_get_current_timestamp)

class Task(DBBASE):
    """
        Metadata pour une tâche (estimation, invoice)
      `IDTask` int(11) NOT NULL auto_increment, #identifiant de la tâche
      `IDPhase` int(11) NOT NULL,           # identifiant de la phase associée
      `name` varchar(150) NOT NULL,         # Nom de la tâche

      `CAEStatus` varchar(10) default NULL, # Statut de la tâche
             valid/abort/paid/draft/geninv/aboinv/aboest/sent/wait/none
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
    __tablename__ = 'coop_task'
    __table_args__ = {'autoload':True}
    IDTask = Column(Integer, primary_key=True)
    taskDate = Column("taskDate", CustomDateType2(11))
    creationDate = Column("creationDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType(11),
                                        default=_get_current_timestamp,
                                        onupdate=_get_current_timestamp)
    statusDate = Column("statusDate", CustomDateType(11),
                                        default=_get_current_timestamp,
                                        onupdate=_get_current_timestamp)
    IDPhase = Column("IDPhase", ForeignKey('coop_phase.IDPhase'))

    CAEStatus = Column('CAEStatus', String(10))
    statusPerson = Column("statusPerson",
                          ForeignKey('egw_accounts.account_id'))
    statusPersonAccount = relationship("User",
                        primaryjoin="Task.statusPerson==User.id",
                        backref="taskStatuses")
    IDEmployee = Column("IDEmployee",
                            ForeignKey('egw_accounts.account_id'))
    owner = relationship("User",
                        primaryjoin="Task.IDEmployee==User.id",
                            backref="ownedTasks")


    def get_status_str(self, _type="estimation"):
        """
            Return human readable string for task status
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
        suffix = u" par {firstname} {lastname} le {date}".format(
                firstname=firstname, lastname=lastname, date=date)
        if _type == "estimation":
            genre = ""
        else:
            genre = "e"
        statuses = dict((
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
            ))
        status_str = statuses.get(self.CAEStatus, u"Statut inconnu").format(
                                                                genre=genre)
        return status_str + suffix

    def is_draft(self):
        """
            Return True if this task is in a draft status (or equivalent)
        """
        return self.CAEStatus in ('draft', 'invalid',)

    def is_editable(self, manage=False):
        """
            return True if this task is editable for the user
        """
        if manage:
            return self.CAEStatus in ('draft', 'invalid', 'wait',)
        else:
            return self.CAEStatus in ('draft', 'invalid',)

    def is_valid(self):
        """
            Return True if the task is valid
        """
        return self.CAEStatus == 'valid'

    def has_been_validated(self):
        """
            Return True if the task has been validated
        """
        return self.CAEStatus in ('valid', 'geninv', 'sent', "recinv",)

    def is_waiting(self):
        """
            Return True if the task is in a wait status
        """
        return self.CAEStatus == "wait"

    @validates('CAEStatus')
    def validate_status(self, key, status):
        """
            validate the caestatus change
        """
        message = u"Vous n'êtes pas autorisé à assigner ce statut {0}à ce \
document."
        actual_status = self.CAEStatus
        message = message.format(status)
        if status in ('draft', 'wait',):
            if not actual_status in (None, 'draft', 'invalid'):
                raise Forbidden(message)
        elif status in ('valid',):
            if not actual_status in ('wait',):
                raise Forbidden(message)
        elif status in ('invalid',):
            if not actual_status in ('wait', ):
                raise Forbidden(message)
        elif status in ('aboest',):
            if not actual_status in ('valid', 'sent', 'invalid', 'wait'):
                raise Forbidden(message)
        elif status in ('geninv',):
            if not actual_status in ('valid', 'sent',):
                raise Forbidden(message)
        elif status in ('sent',):
            if not actual_status in ('valid', "recinv"):
                raise Forbidden(message)
        elif status in ('paid',):
            if not actual_status in ('valid', 'sent', "recinv"):
                raise Forbidden(message)
        elif status in ('aboinv', 'abort',):
            if not actual_status in ('valid', 'sent', "recinv", "invalid", \
                                                                    "wait"):
                raise Forbidden(message)
        elif status in ('recinv',):
            if not actual_status in ('valid', 'sent', "recinv",):
                raise Forbidden(message)
        else:
            assert False
        return status

    def get_company(self):
        """
            Return the company owning this task
        """
        if self.project:
            return self.project.company
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

class Estimation(Task):
    """
       `IDTask` int(11) NOT NULL,
      `sequenceNumber` int(11) NOT NULL,        # Indice du devis dans la phase
      `number` varchar(100) NOT NULL,           # identifiant du devis
      `tva` int(11) NOT NULL default '196',     # tva à utiliser dans
                                                  ce devis (*100)
      `discount` int(11) NOT NULL default '0',  # Non utilisé
      `deposit` int(11) NOT NULL default '0',   # accompte (pourcentage)
      `paymentConditions` text,                 # condition de paiement
      `exclusions` text,                        # Notes
      `IDProject` int(11) NOT NULL,             # id du projet auquel
                                                  appartient ce devis
      `manualDeliverables` tinyint(4) default NULL, # les dates des conditions
                                        de paiement ont été fixées manuellement
      `course` tinyint(4) NOT NULL default '0',   # est-ce un cours (0/1)
      `displayedUnits` tinyint(4) NOT NULL default '0', # afficher les unités
                                                                        (0/1)
      `discountHT` int(11) NOT NULL default '0',    #remise HT
      `expenses` int(11) NOT NULL default '0',      # frais
      `paymentDisplay` varchar(20) default 'SUMMARY', #afficher les conditions
                            de paiement ALL/NONE/SUMMARY
      PRIMARY KEY  (`IDTask`),
      KEY `coop_estimation_sequenceNumber` (`sequenceNumber`),
      KEY `coop_estimation_IDProject` (`IDProject`),
      KEY `IDProject` (`IDProject`)
    """
    __tablename__ = 'coop_estimation'
    __table_args__ = {'autoload':True}

    IDTask = Column("IDTask", ForeignKey('coop_task.IDTask'), primary_key=True)

    IDProject = Column("IDProject", ForeignKey('coop_project.IDProject'))
    project = relationship("Project",
                            backref=backref('estimations',
                                            order_by='Estimation.taskDate')
                            )
    phase =  relationship("Phase",
                          backref=backref("estimations",
                          order_by='Estimation.taskDate'))

    def duplicate(self):
        """
            returns a duplicate estimation object
        """
        duple = Estimation()
        duple.IDPhase = self.IDPhase
        duple.taskDate = datetime.date.today()
        duple.IDEmployee = self.IDEmployee
        duple.description = self.description

        duple.tva = self.tva
        duple.discount = self.discount
        duple.deposit = self.deposit
        duple.paymentConditions = self.paymentConditions
        duple.exclusions = self.exclusions
        duple.IDProject = self.IDProject
        duple.manualDeliverables = self.manualDeliverables
        duple.course = self.course
        duple.displayedUnits = self.displayedUnits
        duple.discountHT = self.discountHT
        duple.expenses = self.expenses
        duple.paymentDisplay = self.paymentDisplay
        return duple

    def is_deletable(self):
        """
            Returns True if the estimation could be deleted
        """
        return self.CAEStatus not in ('geninv',)

    def is_cancelled(self):
        """
            Return True is the invoice has been cancelled
        """
        return self.CAEStatus == 'aboest'

class Invoice(Task):
    """
       `IDTask` int(11) NOT NULL,
       `IDEstimation` int(11) DEFAULT '0',
       `IDProject` int(11) NOT NULL,
       `sequenceNumber` int(11) NOT NULL,
       `number` varchar(100) NOT NULL,
       `tva` int(11) NOT NULL DEFAULT '196',
       `discount` int(11) NOT NULL DEFAULT '0',
       `paymentConditions` text,
       `estimationDate` int(11) DEFAULT '0',
       `estimationNumber` varchar(100) DEFAULT NULL,
       `deposit` tinyint(4) NOT NULL DEFAULT '0',
       `course` tinyint(4) NOT NULL DEFAULT '0',
       `officialNumber` int(11) DEFAULT NULL,
       `paymentMode` varchar(10) DEFAULT NULL,
       `displayedUnits` tinyint(4) NOT NULL DEFAULT '0',
       `discountHT` int(11) NOT NULL DEFAULT '0',
       `expenses` int(11) NOT NULL DEFAULT '0',
       PRIMARY KEY (`IDTask`),
       KEY `IDProject` (`IDProject`),
       KEY `IDEstimation` (`IDEstimation`)
    """
    __tablename__ = 'coop_invoice'
    __table_args__ = {'autoload':True}
    IDTask = Column("IDTask", ForeignKey('coop_task.IDTask'), primary_key=True)

    IDEstimation = Column("IDEstimation", ForeignKey('coop_estimation.IDTask'))
    IDProject = Column("IDProject", ForeignKey('coop_project.IDProject'))
    project = relationship("Project", backref=backref('invoices',
                                            order_by='Invoice.taskDate')
                            )
    phase =  relationship("Phase",
                          backref=backref("invoices",
                                          order_by='Invoice.taskDate')
                          )
    estimation = relationship("Estimation",
                      backref="invoice",
                      primaryjoin="Invoice.IDEstimation==Estimation.IDTask",
                                )
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
        return self.CAEStatus in ('valid', 'sent',) and tolate

    def is_paid(self):
        """
            Return True if the invoice is paid
        """
        return self.CAEStatus == 'paid'

    def is_cancelled(self):
        """
            Return True is the invoice has been cancelled
        """
        return self.CAEStatus == 'aboinv'

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

    @validates("paymentMode")
    def validate_paymentMode(self, key, paymentMode):
        """
            Validate the paymentMode
        """
        if not paymentMode in ('CHEQUE', 'VIREMENT'):
            raise Forbidden(u'Mode de paiement inconnu')
        return paymentMode

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
    __table_args__ = {'autoload':True}
    id = Column("IDWorkLine", Integer, primary_key=True)
    IDTask = Column(Integer, ForeignKey('coop_estimation.IDTask'))
    creationDate = Column("creationDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType(11),
                                        default=_get_current_timestamp,
                                        onupdate=_get_current_timestamp)
    task = relationship("Estimation", backref="lines",
                            order_by='EstimationLine.rowIndex'
                        )
    def get_unity_label(self):
        """
            return unitie's label
        """
        labels = dict(
                NONE=u'-',
                HOUR=u"heure(s)",
                DAY=u"jour(s)",
                WEEK=u"semaine(s)",
                MONTH=u"mois",
                FEUIL=u"feuillet(s)",
                PACK=u"forfait",
                )
        return labels.get(self.unity, '-')

    def duplicate(self):
        """
            duplicate an estimationline
        """
        newone = EstimationLine()
        newone.rowIndex = self.rowIndex
        newone.cost = self.cost
        newone.description = self.description
        newone.quantity = self.quantity
        newone.unity = self.unity
        return newone

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
    __table_args__ = {'autoload':True}
    id = Column("IDInvoiceLine", Integer, primary_key=True)
    IDTask = Column(Integer, ForeignKey('coop_invoice.IDTask'))
    creationDate = Column("creationDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType(11),
                                        default=_get_current_timestamp,
                                        onupdate=_get_current_timestamp)
    task = relationship("Invoice", backref="lines",
                            order_by='InvoiceLine.rowIndex'
                        )
                        #enable_typechecks=False )

    def get_unity_label(self):
        """
            return unitie's label
        """
        labels = dict(
                NONE=u'-',
                HOUR=u"heure(s)",
                DAY=u"jour(s)",
                WEEK=u"semaine(s)",
                MONTH=u"mois",
                FEUIL=u"feuillet(s)",
                PACK=u"forfait",
                )
        return labels.get(self.unity, '-')

    def duplicate(self):
        """
            duplicate an estimationline
        """
        newone = InvoiceLine()
        newone.rowIndex = self.rowIndex
        newone.cost = self.cost
        newone.description = self.description
        newone.quantity = self.quantity
        newone.unity = self.unity
        return newone

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
    __table_args__ = {'autoload':True}
    creationDate = Column("creationDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType(11),
                                        default=_get_current_timestamp,
                                        onupdate=_get_current_timestamp)
    IDTask = Column(Integer, ForeignKey('coop_estimation.IDTask'))
    estimation = relationship("Estimation", backref=backref('payment_lines',
                    order_by='PaymentLine.rowIndex'))
    paymentDate = Column("paymentDate", CustomDateType2(11))

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

class Client(DBBASE):
    """
       `code` varchar(4) NOT NULL,
        `IDContact` int(11) default '0',
        `comments` text,
        `creationDate` int(11) NOT NULL,
        `updateDate` int(11) NOT NULL,
        `IDCompany` int(11) NOT NULL,
        `intraTVA` varchar(50) default NULL,
        `address` varchar(255) default NULL,
        `zipCode` varchar(20) default NULL,
        `city` varchar(255) default NULL,
        `country` varchar(150) default NULL,
        `phone` varchar(50) default NULL,
        `email` varchar(255) default NULL,
        `contactLastName` varchar(255) default NULL,
        `name` varchar(255) default NULL,
        `contactFirstName` varchar(255) default NULL,
        PRIMARY KEY  (`code`),
        KEY `IDCompany` (`IDCompany`)
    """
    __tablename__ = 'coop_customer'
    __table_args__ = {'autoload':True}
    id = Column('code', String(4), primary_key=True)
    id_company = Column("IDCompany", Integer,
                                    ForeignKey('coop_company.IDCompany'))
    creationDate = Column("creationDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType(11),
                                        default=_get_current_timestamp,
                                        onupdate=_get_current_timestamp)
    projects = relationship("Project", backref="client")
    name = Column("name", String(255), default=None)
    contactFirstName = Column("contactFirstName", String(255), default=None)
    contactLastName = Column("contactLastName", String(255), default=None)

    def get_company_id(self):
        return self.company.id

class Project(DBBASE):
    """
        `IDProject` int(11) NOT NULL auto_increment,
        `name` varchar(150) NOT NULL,
        `customerCode` varchar(4) NOT NULL,
        `type` varchar(150) default NULL,
        `code` varchar(4) NOT NULL,
        `definition` text,
        `creationDate` int(11) NOT NULL,
        `updateDate` int(11) NOT NULL,
        `startingDate` int(11) default NULL,
        `endingDate` int(11) default NULL,
        `status` varchar(20) NOT NULL,
        `IDCompany` int(11) NOT NULL,
        `dispatchType` varchar(10) NOT NULL default 'PERCENT',
        `archived` tinyint(4) NOT NULL default '0',
        PRIMARY KEY  (`IDProject`),
        KEY `IDCompany` (`IDCompany`)
    """
    __tablename__ = 'coop_project'
    __table_args__ = {'autoload':True}
    id = Column('IDProject', Integer, primary_key=True)
    id_company = Column("IDCompany", Integer,
                                    ForeignKey('coop_company.IDCompany'))
    code_client = Column("customerCode", String(4),
                                    ForeignKey('coop_customer.code'))
    creationDate = Column("creationDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType(11),
                                        default=_get_current_timestamp,
                                        onupdate=_get_current_timestamp)
    startingDate = Column("startingDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    endingDate = Column("endingDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    name = Column("name", String(255))
    archived = Column("archived", String(255), default=0)

    def get_estimation(self, taskid):
        """
            Returns the estimation with id taskid
        """
        for estimation in self.estimations:
            if estimation.IDTask == int(taskid):
                return estimation
        raise KeyError("No such task in this project")

    def get_invoice(self, taskid):
        """
            Returns the estimation with id taskid
        """
        for invoice in self.invoices:
            if invoice.IDTask == int(taskid):
                return invoice
        raise KeyError("No such task in this project")

    def is_archived(self):
        """
            Return True if the project is archived
        """
        return self.archived == 1

    def is_deletable(self):
        """
            Return True if this project could be deleted
        """
        return self.archived == 1 and not self.invoices

    def get_company_id(self):
        return self.company.id


class Phase(DBBASE):
    """
        Phase d'un projet
        `IDPhase` int(11) NOT NULL auto_increment,
        `IDProject` int(11) NOT NULL,
        `name` varchar(150) NOT NULL,
        `IDPreviousPhase` int(11) NOT NULL default '0',
        `creationDate` int(11) NOT NULL,
        `updateDate` int(11) NOT NULL,
    """
    __tablename__ = 'coop_phase'
    __table_args__ = {'autoload':True}
    id = Column('IDPhase', Integer, primary_key=True)
    name = Column("name", String(150), default=u'Phase par défaut')
    id_project = Column('IDProject', Integer,
                        ForeignKey('coop_project.IDProject'))
    project = relationship("Project", backref="phases")
    creationDate = Column("creationDate", CustomDateType(11),
                                            default=_get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType(11),
                                        default=_get_current_timestamp,
                                        onupdate=_get_current_timestamp)
    def is_default(self):
        """
            return True is this phase is a default one
        """
        return self.name in (u'Phase par défaut', u"default", u"défaut",)

class Tva(DBBASE):
    """
        coop_tva
        `id` int(2) NOT NULL auto_increment,
        `name` varchar(8) NOT NULL,
        `value` int(5)
        `default` int(2) default 0 #rajouté par mise à jour 1.2
    """
    __tablename__ = 'coop_tva'
    __table_args__ = {'autoload':True}

    @classmethod
    def query(cls, dbsession):
        return dbsession.query(Tva).order_by('value')

class TaskStatus(DBBASE):
    """
        `IDTask` int(11) NOT NULL,
        `statusCode` varchar(10) NOT NULL,
        `statusComment` text,
        `statusPerson` int(11) default NULL,
        `statusDate` int(11) default NULL,
        KEY `IDTask` (`IDTask`),
        KEY `statusCode` (`statusCode`)
    """
    __tablename__ = 'coop_task_status'
    __table_args__ = {'autoload':True}
    id = Column("id", Integer, primary_key=True)
    id_task = Column('IDTask', Integer,
                        ForeignKey('coop_task.IDTask'))
    task = relationship("Task", backref="taskstatus")

class Config(DBBASE):
    """
        Table containing the main configuration
          `config_app` varchar(50) NOT NULL,
          `config_name` varchar(255) NOT NULL,
          `config_value` text,
          PRIMARY KEY  (`config_app`,`config_name`)
    """
    __tablename__ = 'egw_config'
    __table_args__ = {'autoload':True}
    app = Column("config_app", String(255), primary_key=True)
    name = Column("config_name", String(255), primary_key=True)
    value = Column("config_value", Text())

class ManualInvoice(DBBASE):
    """
        symf_facture_manuelle
        `id` bigint(20) NOT NULL auto_increment,
        `sequence_id` bigint(20) NOT NULL,
        `libelle` varchar(255) character set utf8 default NULL,
        `montant_ht` decimal(18,2) default NULL,
        `tva` decimal(18,2) default NULL,
        `paiement_ok` tinyint(1) default NULL,
        `paiement_date` date default NULL,
        `paiement_comment` varchar(255) character set utf8 default NULL,
        `client_id` varchar(5) character set utf8 NOT NULL,
        `date_emission` date default NULL,
        `compagnie_id` bigint(20) NOT NULL,
        `created_at` datetime NOT NULL,
        `updated_at` datetime NOT NULL,
        PRIMARY KEY  (`id`),
        UNIQUE KEY `id` (`id`)
    """
    __tablename__ = 'symf_facture_manuelle'
    __table_args__ = {'autoload':True}
    created_at = Column("created_at", DateTime,
                                      default=datetime.datetime.now)
    updated_at = Column("updated_at", DateTime,
                                      default=datetime.datetime.now,
                                      onupdate=datetime.datetime.now)
    id = Column('id', BigInteger, primary_key=True)
    client_id = Column('client_id', String(5),
                            ForeignKey('coop_customer.code'))
    company_id = Column('compagnie_id', BigInteger,
                            ForeignKey('coop_company.IDCompany'))
    client = relationship("Client",
                primaryjoin="Client.id==ManualInvoice.client_id",
                  backref='manual_invoices')
    company = relationship("Company",
                primaryjoin="Company.id==ManualInvoice.company_id",
                  backref='manual_invoices')
    taskDate = Column('date_emission', Date())
    description = Column('libelle', String(255))
    officialNumber = Column('sequence_id', BigInteger)
    paymentMode = Column("paiement_comment", String(255))
    statusDate = Column("paiement_date", Date())
    payment_ok = Column("paiement_ok", Integer)
    taskDate = Column("date_emission", Date(),
                                default=datetime.datetime.now)

    def is_paid(self):
        """
            return True if it's paid
        """
        return self.payment_ok == 1

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

    def is_tolate(self):
        today = datetime.date.today()
        elapsed = today - self.taskDate
        return not self.is_paid() and elapsed > datetime.timedelta(days=45)

    @property
    def number(self):
        """
            return the invoice number
        """
        return u"FACT_MAN_{0}".format(self.officialNumber)

    @property
    def project(self):
        """
            return None
        """
        return None

    def get_company(self):
        """
            return the company
        """
        return self.company

class OperationComptable(DBBASE):
    """
        Recense les opérations comptables
        `id` bigint(20) NOT NULL auto_increment,
        `montant` decimal(18,2) default NULL,
        `charge` tinyint(1) default NULL,
        `compagnie_id` bigint(20) NOT NULL,
        `date` date default NULL,
        `libelle` varchar(255) collate utf8_unicode_ci default NULL,
        `created_at` datetime NOT NULL,
        `updated_at` datetime NOT NULL,
        `annee` bigint(20) default NULL,
        `type` text collate utf8_unicode_ci,
        PRIMARY KEY  (`id`),
        UNIQUE KEY `id` (`id`)
    """
    __tablename__ = 'symf_operation_treso'
    __table_args__ = {'autoload':True}
    id = Column('id', BigInteger, primary_key=True)
    company_id = Column('compagnie_id', CustomInteger,
                            ForeignKey('coop_company.IDCompany'))
    company = relationship("Company",
                       primaryjoin="Company.id==OperationComptable.company_id",
                       backref='operation_comptable')
    created_at = Column("created_at", DateTime,
                                        default=datetime.datetime.now)
    updated_at = Column("updated_at", DateTime,
                                        default=datetime.datetime.now,
                                        onupdate=datetime.datetime.now)
    charge = Column("charge", Integer, default=0)
    date = Column("date", Date(), default=datetime.date.today)
    label = Column("libelle", String, default="")
    year = Column("annee", BigInteger)
    amount = Column("montant", Numeric)

class CancelInvoice(Task):
    """
       `IDTask` int(11) NOT NULL,
       `sequenceNumber` int(11) NOT NULL,
       `number` varchar(100) NOT NULL,
       `tva` int(11) NOT NULL DEFAULT '196',
       `reimbursementConditions` text,
       `officialNumber` int(11) DEFAULT NULL,
       `paymentMode` varchar(10) DEFAULT NULL,
       `displayedUnits` tinyint(4) NOT NULL DEFAULT '0',
       `expenses` int(11) NOT NULL DEFAULT '0',
       `IDProject` int(11) NOT NULL,
       `IDInvoice` int(11) DEFAULT '0',
       `invoiceDate` int(11) DEFAULT '0',
       `invoiceNumber` varchar(100) DEFAULT NULL,
       PRIMARY KEY (`IDTask`),
       KEY `IDProject` (`IDProject`),
       KEY `IDEstimation` (`IDEstimation`)
    """
    __tablename__ = 'coop_cancel_invoice'
    __table_args__ = {'mysql_engine': 'MyISAM'}
    IDTask = Column(Integer, ForeignKey('coop_task.IDTask'), primary_key=True)

    IDInvoice = Column(Integer, ForeignKey('coop_invoice.IDTask'))
    IDProject = Column(Integer, ForeignKey('coop_project.IDProject'))
    sequenceNumber = Column(Integer)
    number = Column(String(100))
    tva = Column(Integer, default=1960)
    reimbursementConditions = Column(String(255), default=None)
    officialNumber = Column(Integer, default=None)
    paymentMode = Column(String(80), default=None)
    displayedUnits = Column(Integer, default=0)
    expenses = Column(Integer, default=0)

    project = relationship("Project", backref=backref('cancelinvoices',
                                            order_by='CancelInvoice.taskDate')
                            )
    phase = relationship("Phase",
                          backref=backref("cancelinvoices",
                                          order_by='CancelInvoice.taskDate')
                          )
    invoice = relationship("Invoice",
                      backref="cancelinvoice",
                      primaryjoin="CancelInvoice.IDInvoice==Invoice.IDTask",
                                )
    def is_paid(self):
        """
            Return True if the invoice is paid
        """
        return self.CAEStatus == 'paid'

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

class Holliday(DBBASE):
    """
        Hollidays table
        Stores the start and end date for holliday declaration
        user_id
        start_date
        end_date
    """
    __tablename__ = "coop_holliday"
    __table_args__ = {'mysql_engine': 'MyISAM'}
    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey('egw_accounts.account_id'))
    start_date = Column(Date)
    end_date = Column(Date)
    user = relationship("User",
                        backref=backref("hollidays",
                                        order_by="Holliday.start_date"),
                        primaryjoin="Holliday.user_id==User.id"
                        )

    @classmethod
    def query(cls, dbsession, user_id=None):
        """
            query the database for the current class instances
            @dbsession : instanciated dbsession
            @user_id: id of the user we want the holliday from
        """
        q = dbsession.query(Holliday)
        if user_id:
            q = q.filter(Holliday.user_id==user_id)
        return q.order_by("start_date")

