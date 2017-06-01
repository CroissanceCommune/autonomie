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
    Config model stores :
    Autonomie's welcome message
    Documents footers, headers ...
"""
from cStringIO import StringIO
from sqlalchemy import (
    Column,
    Text,
    Integer,
    String,
    event,
)

from depot.fields.sqlalchemy import (
    UploadedFileField,
    _SQLAMutationTracker,
)

from autonomie_base.models.base import DBBASE, DBSESSION
from autonomie_base.models.base import default_table_args
from autonomie.export.utils import detect_file_headers
from autonomie.utils.filedepot import _to_fieldstorage


class ConfigFiles(DBBASE):
    """
        A file model
    """
    __tablename__ = 'config_files'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True)
    name = Column(String(100))
    data = Column(UploadedFileField)
    mimetype = Column(String(100))
    size = Column(Integer)

    def getvalue(self):
        """
        Method making our file object compatible with the common file rendering
        utility
        """
        return self.data.file.read()

    @property
    def label(self):
        """
        Simple shortcut for getting a label for this file
        """
        return self.name

    @classmethod
    def get(cls, key):
        """
        Override the default get method to get by key and not by id
        """
        return cls.query().filter(cls.key == key).first()

    @classmethod
    def set(cls, key, appstruct):
        """
        Set a file for the given key, if the key isn't field yet, add a new
        instance
        """
        instance = cls.get(key)
        if instance is None:
            instance = cls(key=key)
        for attr_name, attr_value in appstruct.items():
            setattr(instance, attr_name, attr_value)
        if instance.id is not None:
            DBSESSION().merge(instance)
        else:
            DBSESSION().add(instance)

    @classmethod
    def __declare_last__(cls):
        # Unconfigure the event set in _SQLAMutationTracker, we have _save_data
        mapper = cls._sa_class_manager.mapper
        args = (mapper.attrs['data'], 'set', _SQLAMutationTracker._field_set)
        if event.contains(*args):
            event.remove(*args)

        # Declaring the event on the class attribute instead of mapper property
        # enables proper registration on its subclasses
        event.listen(cls.data, 'set', cls._set_data, retval=True)

    @classmethod
    def _set_data(cls, target, value, oldvalue, initiator):
        if isinstance(value, bytes):
            value = _to_fieldstorage(fp=StringIO(value),
                                     filename=target.filename,
                                     size=len(value))

        newvalue = _SQLAMutationTracker._field_set(
            target, value, oldvalue, initiator)

        if newvalue is None:
            return
        target.filename = newvalue.filename
        target.mimetype = detect_file_headers(newvalue.filename)
        target.size = newvalue.file.content_length

        return newvalue


class Config(DBBASE):
    """
        Table containing the main configuration
          `config_app` varchar(50) NOT NULL,
          `config_name` varchar(255) NOT NULL,
          `config_value` text,
          PRIMARY KEY  (`config_app`,`config_name`)
    """
    __tablename__ = 'config'
    __table_args__ = default_table_args
    app = Column(
        "config_app",
        String(50),
        primary_key=True,
        default='autonomie',
    )
    name = Column("config_name", String(255), primary_key=True)
    value = Column("config_value", Text())

    def __init__(self, **kwargs):
        kwargs['app'] = 'autonomie'
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

    @classmethod
    def get(cls, keyname, default=None):
        query = super(Config, cls).query()
        query = query.filter(Config.app == 'autonomie')
        query = query.filter(Config.name == keyname)
        result = query.first()
        if default and result is None:
            result = default
        return result

    @classmethod
    def query(cls):
        query = super(Config, cls).query()
        return query.filter(Config.app == 'autonomie')

    @classmethod
    def set(cls, key, value):
        instance = cls.get(key)
        if instance is None:
            instance = cls(name=key)

        instance.value = value
        DBSESSION().merge(instance)


def get_config():
    """
        Return a dictionnary with the config objects
    """
    return dict((entry.name, entry.value)
                for entry in Config.query().all())
