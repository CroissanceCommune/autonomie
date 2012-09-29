#-*-coding:utf-8*-*
# * File Name : model.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : sam. 29 sept. 2012 18:06:53 CEST
#
# * Project : autonomie
#
"""
    Database session objects
    Needs to be initialized at module top level
    to avoid problems with the model autoload methods
"""

from sqlalchemy.ext import declarative
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from zope.sqlalchemy import ZopeTransactionExtension

DBSESSION = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
DBMETADATA = MetaData()


class ORMClass(object):
    """
        Base class for our models providing usefull query and get methods
    """
    @classmethod
    def query(cls):
        """
            return a query
        """
        return DBSESSION.query(cls)

    @classmethod
    def get(cls, id_):
        """
            Return a query
        """
        return DBSESSION.query(cls).get(id_)


DBBASE = declarative.declarative_base(cls=ORMClass)
DBBASE.metadata = DBMETADATA


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
