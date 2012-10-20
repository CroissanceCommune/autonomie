# -*- coding: utf-8 -*-
# * File Name : model.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : sam. 20 oct. 2012 07:07:18 CEST
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
from sqlalchemy.orm import deferred

from autonomie.models.types import CustomInteger

from autonomie.models import DBBASE

log = logging.getLogger(__name__)


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
    __tablename__ = 'operation_tresorerie'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset": 'utf8'}
    id = Column('id', BigInteger, primary_key=True)
    amount = Column("montant", Numeric)
    charge = Column("charge", Integer, default=0)
    company_id = Column('compagnie_id', CustomInteger,
                            ForeignKey('company.id'))
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

