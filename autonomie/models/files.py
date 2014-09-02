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
from cStringIO import StringIO
from sqlalchemy import (
    Integer,
    Column,
    ForeignKey,
    String,
    Boolean,
)

from sqlalchemy.orm import (
    deferred,
)

from sqlalchemy.dialects.mysql.base import LONGBLOB

from autonomie.models.base import default_table_args
from autonomie.models.node import Node


class File(Node):
    """
        A file model
    """
    __tablename__ = 'file'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'file'}
    id = Column(Integer, ForeignKey('node.id'), primary_key=True)
    description = Column(String(100), default="")
    data = deferred(Column(LONGBLOB()))
    mimetype = Column(String(100))
    size = Column(Integer)

    def getvalue(self):
        """
        Method making our file object compatible with the common file rendering
        utility
        """
        return self.data

    @property
    def label(self):
        """
        Simple shortcut for getting a label for this file
        """
        return self.description or self.name

    @property
    def data_obj(self):
        res = StringIO()
        res.write(self.data)
        return res


class Template(File):
    """
    A template model for odt templates
    """
    __tablename__ = 'templates'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'template'}
    id = Column(ForeignKey('file.id'), primary_key=True)
    active = Column(Boolean(), default=True)
