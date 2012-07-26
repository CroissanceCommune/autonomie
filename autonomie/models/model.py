# -*- coding: utf-8 -*-
# * File Name : model.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : jeu. 26 juil. 2012 13:24:54 CEST
#
# * Project : autonomie
#
"""
    Autonomie's SQLA models
"""
import datetime
import logging


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
from sqlalchemy.orm import deferred
from sqlalchemy import func

from autonomie.models.types import CustomDateType
from autonomie.models.types import CustomDateType2
from autonomie.models.types import CustomInteger
from autonomie.models.utils import get_current_timestamp
from autonomie.models.user import User
from autonomie.models.company import Company
from autonomie.models.task import Task
from autonomie.models.task import Estimation
from autonomie.models.task import Invoice
from autonomie.models.task import CancelInvoice
from autonomie.models.task import ManualInvoice


from autonomie.models import DBBASE
from autonomie.utils.exception import Forbidden

log = logging.getLogger(__name__)


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
    cost = Column("cost", Integer)
    quantity = Column("quantity", Integer)
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
    rowIndex = Column("rowIndex", Integer)
    description = Column("description", Text)
    cost = Column("cost", Integer)
    quantity = Column("quantity", Integer)
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

    def gen_cancel_invoice_line(self):
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
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column('code', String(4), primary_key=True)
    comments = deferred(Column("comments", Text), group='edit')
    creationDate = Column("creationDate", CustomDateType,
                                            default=get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp)
    id_company = Column("IDCompany", Integer,
                                    ForeignKey('coop_company.IDCompany'))
    intraTVA = deferred(Column("intraTVA", String(50)), group='edit')
    address = deferred(Column("address", String(255)), group='edit')
    zipCode = deferred(Column("zipCode", String(20)), group='edit')
    city = deferred(Column("city", String(255)), group='edit')
    country = deferred(Column("country", String(150)), group='edit')
    phone = deferred(Column("phone", String(50)), group='edit')
    email = deferred(Column("email", String(255)), group='edit')
    contactLastName = deferred(Column("contactLastName",
                    String(255), default=None), group='edit')
    name = Column("name", String(255), default=None)
    contactFirstName = deferred(Column("contactFirstName",
                    String(255), default=None), group='edit')
    projects = relationship("Project", backref="client")

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
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column('IDProject', Integer, primary_key=True)
    name = Column("name", String(255))
    code_client = Column("customerCode", String(4),
                                    ForeignKey('coop_customer.code'))
    code = Column("code", String(4), nullable=False)
    definition = deferred(Column("definition", Text), group='edit')

    id_company = Column("IDCompany", Integer,
                                    ForeignKey('coop_company.IDCompany'))
    creationDate = deferred(Column("creationDate", CustomDateType,
                                            default=get_current_timestamp))
    updateDate = deferred(Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp))
    startingDate = deferred(Column("startingDate", CustomDateType,
                                default=get_current_timestamp), group='edit')
    endingDate = deferred(Column("endingDate", CustomDateType,
                                default=get_current_timestamp), group='edit')

    type = deferred(Column('type', String(150)), group='edit')
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
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column('IDPhase', Integer, primary_key=True)
    id_project = Column('IDProject', Integer,
                        ForeignKey('coop_project.IDProject'))
    name = Column("name", String(150), default=u'Phase par défaut')
    project = relationship("Project", backref="phases")
    creationDate = deferred(Column("creationDate", CustomDateType,
                                            default=get_current_timestamp))
    updateDate = deferred(Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp))
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
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(8), nullable=False)
    value = Column("value", Integer)
    default = Column("default", Integer)

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
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column("id", Integer, primary_key=True)
    id_task = Column('IDTask', Integer,
                        ForeignKey('coop_task.IDTask'))
    statusCode = Column("statusCode", String(10))
    statusComment = Column("statusComment", Text)
    statusDate = Column("statusDate", Integer)
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
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    app = Column("config_app", String(50), primary_key=True)
    name = Column("config_name", String(255), primary_key=True)
    value = Column("config_value", Text())

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
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column('id', BigInteger, primary_key=True)
    amount = Column("montant", Numeric)
    charge = Column("charge", Integer, default=0)
    company_id = Column('compagnie_id', CustomInteger,
                            ForeignKey('coop_company.IDCompany'))
    date = Column("date", Date(), default=datetime.date.today)
    label = Column("libelle", String(255), default="")
    company = relationship("Company",
                       primaryjoin="Company.id==OperationComptable.company_id",
                       backref='operation_comptable')
    created_at = deferred(Column("created_at", DateTime,
                                        default=datetime.datetime.now))
    updated_at = deferred(Column("updated_at", DateTime,
                                        default=datetime.datetime.now,
                                        onupdate=datetime.datetime.now))
    year = Column("annee", BigInteger)
    type = Column("type", Text)


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
    quantity = Column(Integer, default=1)
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

class Holliday(DBBASE):
    """
        Hollidays table
        Stores the start and end date for holliday declaration
        user_id
        start_date
        end_date
    """
    __tablename__ = "coop_holliday"
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
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
