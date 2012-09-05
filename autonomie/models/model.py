# -*- coding: utf-8 -*-
# * File Name : model.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : mer. 05 sept. 2012 17:45:51 CEST
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
from sqlalchemy.orm import backref
from sqlalchemy.orm import deferred

from autonomie.models.types import CustomDateType
from autonomie.models.types import CustomInteger
from autonomie.models.utils import get_current_timestamp
from autonomie.models.client import Client
from autonomie.models.company import Company
from autonomie.models.project import Project
from autonomie.models.task import Task
from autonomie.models.task import Estimation
from autonomie.models.task import Invoice
from autonomie.models.task import CancelInvoice
from autonomie.models.task import ManualInvoice
from autonomie.models.task import CancelInvoiceLine
from autonomie.models.task import EstimationLine
from autonomie.models.task import InvoiceLine
from autonomie.models.task import PaymentLine
from autonomie.models.user import User


from autonomie.models import DBBASE
from autonomie.exception import Forbidden

log = logging.getLogger(__name__)

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

    @property
    def estimations(self):
        return self.get_documents_by_type('estimation')

    @property
    def invoices(self):
        return self.get_documents_by_type('invoice')

    @property
    def cancelinvoices(self):
        return self.get_documents_by_type('cancelinvoice')

    def get_documents_by_type(self, type_):
        """
            return the documents of the passed type
        """
        return [doc for doc in self.documents if doc.type_==type_]


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
    user_id = Column("user_id", Integer, ForeignKey('accounts.id'))
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
