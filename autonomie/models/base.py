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
    Database access base objects
    DBSESSION : database session factory
    DBBASE : base object for models
"""
from sqlalchemy.ext import declarative
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import MetaData
from zope.sqlalchemy import ZopeTransactionExtension

DBSESSION = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class ORMClass(object):
    """
        Base class for our models providing usefull query and get methods
    """
    @classmethod
    def query(cls, *args):
        """
            return a query
        """
        if not args:
            return DBSESSION().query(cls)
        else:
            query_args = []
            for arg in args:
                cls_attr = getattr(cls, arg, None)
                if cls_attr is not None:
                    query_args.append(cls_attr)
            return DBSESSION().query(*query_args)

    @classmethod
    def get(cls, id_):
        """
            Return a query
        """
        return DBSESSION().query(cls).get(id_)

    @declared_attr
    def __tablename__(cls):
        from autonomie.utils.ascii import camel_case_to_name
        return camel_case_to_name(cls.__name__)


NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

METADATA = MetaData(naming_convention=NAMING_CONVENTION)


DBBASE = declarative.declarative_base(
    cls=ORMClass,
    metadata=METADATA,
)


def record_to_appstruct(self):
    """
        Transform a SQLAlchemy object into a deform compatible dict
        usefull to autofill an editform directly from db recovered datas
    """
    return dict([(k, self.__dict__[k])
                for k in sorted(self.__dict__) if '_sa_' != k[:4]
                and self.__dict__[k] is not None])


DBBASE.appstruct = record_to_appstruct


default_table_args = {'mysql_engine': 'InnoDB', "mysql_charset": 'utf8'}
