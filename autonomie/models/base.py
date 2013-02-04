# -*- coding: utf-8 -*-
# * File Name : base.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 04-02-2013
# * Last Modified :
#
# * Project :
#
"""
    Database access base objects
    DBSESSION : database session factory
    DBBASE : base object for models
"""

from sqlalchemy.ext import declarative
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from zope.sqlalchemy import ZopeTransactionExtension

DBSESSION = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class ORMClass(object):
    """
        Base class for our models providing usefull query and get methods
    """
    @classmethod
    def query(cls):
        """
            return a query
        """
        return DBSESSION().query(cls)

    @classmethod
    def get(cls, id_):
        """
            Return a query
        """
        return DBSESSION().query(cls).get(id_)


DBBASE = declarative.declarative_base(cls=ORMClass)


def record_to_appstruct(self):
    """
        Transform a SQLAlchemy object into a deform compatible dict
        usefull to autofill an editform directly from db recovered datas
    """
    return dict([(k, self.__dict__[k])
                for k in sorted(self.__dict__) if '_sa_' != k[:4]])

# Add a bounded method to the DBBASE object
#DBBASE.appstruct = types.MethodType( record_to_appstruct, DBBASE )
DBBASE.appstruct = record_to_appstruct


#default_table_args = {'mysql_engine': 'MyISAM', "mysql_charset": 'utf8'}
default_table_args = {'mysql_engine': 'InnoDB', "mysql_charset": 'utf8'}
