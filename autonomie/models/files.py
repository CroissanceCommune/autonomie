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
    File model
"""
import hashlib
import os

import cStringIO
from datetime import datetime
from sqlalchemy import (
    Integer,
    Column,
    ForeignKey,
    DateTime,
    String,
    Boolean,
    event,
)

from sqlalchemy.orm import (
    relationship,
    backref,
)

from depot.fields.sqlalchemy import (
    UploadedFileField,
    _SQLAMutationTracker,
)

from autonomie_base.models.base import (
    default_table_args,
    DBBASE,
    DBSESSION,
)
from autonomie_base.models.types import PersistentACLMixin
from autonomie.models.node import Node
from autonomie.utils.filedepot import _to_fieldstorage
from autonomie.export.utils import detect_file_headers
from autonomie.forms import EXCLUDED


class File(Node):
    """
        A file model
    """
    __tablename__ = 'file'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'file'}
    id = Column(Integer, ForeignKey('node.id'), primary_key=True)
    description = Column(String(100), default="")
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
        return self.description or self.name

    @property
    def data_obj(self):
        return cStringIO.StringIO(self.data.file.read())

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
        # Ref #384 : enforce this method
        if isinstance(value, (cStringIO.InputType, file)):
            value.seek(0)
            value = value.read()

        if isinstance(value, bytes):
            value = _to_fieldstorage(
                fp=cStringIO.StringIO(value),
                filename=target.name,
                size=len(value)
            )
        newvalue = _SQLAMutationTracker._field_set(
            target,
            value,
            oldvalue,
            initiator
        )

        if newvalue is None:
            return
        target.filename = newvalue.filename
        target.mimetype = detect_file_headers(newvalue.filename)
        target.size = newvalue.file.content_length

        return newvalue


class Template(File):
    """
    A template model for odt templates
    """
    __tablename__ = 'templates'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'template'}
    id = Column(ForeignKey('file.id'), primary_key=True)
    active = Column(Boolean(), default=True)

    @property
    def label(self):
        return self.name

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
    def query(cls,):
        return DBSESSION().query(cls).order_by(cls.created_at)


class TemplatingHistory(DBBASE, PersistentACLMixin):
    """
    Record all the templating fired for a given userdata account
    """
    __tablename__ = "template_history"
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime(),
        default=datetime.now,
        info={'colanderalchemy': {'title': u"Date de génération"}},
    )
    user_id = Column(
        ForeignKey('accounts.id'),
        info={
            'colanderalchemy': EXCLUDED,
            "export": EXCLUDED,
        },
    )
    userdatas_id = Column(
        ForeignKey('user_datas.id'),
        info={
            'colanderalchemy': EXCLUDED,
            "export": EXCLUDED,
        },
    )
    template_id = Column(
        ForeignKey('templates.id'),
        info={
            'colanderalchemy': {'title': u"Type de document"}
        }
    )

    user = relationship(
        "User",
        info={
            'colanderalchemy': EXCLUDED,
            "export": EXCLUDED,
        },
    )
    userdatas = relationship(
        "UserDatas",
        backref=backref(
            "template_history",
            cascade='all, delete-orphan',
            info={
                'colanderalchemy': EXCLUDED,
                'export': {
                    'exclude': True,
                    'stats': {
                        'label': u"Génération de documents - ",
                        'exclude': False
                    },
                },
            }
        ),
        info={
            'colanderalchemy': EXCLUDED,
            "export": EXCLUDED,
        },
    )
    template = relationship(
        "Template",
        backref=backref(
            "templated",
            cascade='all, delete-orphan',
            info={'export': {'exclude': True}, },
        )
    )
