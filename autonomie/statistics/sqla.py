# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Handle the SQLAlchemy stuff done in statistics
"""
import logging
import colander
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Numeric,
    Enum,
    Time,
    inspect,
)

from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
)

from colanderalchemy.schema import _creation_order

from autonomie.models import user
from .widgets import (
    NumericStatMapping,
    DateStatMapping,
    StringStatMapping,
    get_fixed_options_stat_mapping,
    get_relation_stat_mapping,
)


log = logging.getLogger(__name__)


def get_node_type_from_column(column_type):
    """
    Return the colander node type regarding the given SQLAlchemy column type
    """
    if isinstance(column_type, Boolean):
        type_ = colander.Boolean()

    elif isinstance(column_type, Date):
        type_ = colander.Date()

    elif isinstance(column_type, DateTime):
        type_ = colander.DateTime(default_tzinfo=None)

    elif isinstance(column_type, Enum):
        type_ = colander.String()

    elif isinstance(column_type, String):
        type_ = colander.String()

    elif isinstance(column_type, Time):
        type_ = colander.Time()

    else:
        raise NotImplementedError('Unknown type: %s' % column_type)
    return type_


def get_stat_mapping_from_column(column_type):
    """
    Return the stat mapping associated the given column_type
    """
    for type_ in Numeric, Integer, Float:
        if isinstance(column_type, type_):
            return NumericStatMapping()

    if isinstance(column_type, String):
        return StringStatMapping()

    if isinstance(column_type, Date) or isinstance(column_type, DateTime):
        return DateStatMapping()

    raise NotImplementedError('Unknown type : %s' % column_type)


class StatSchema(colander.Schema):
    """
    A schema handling statistic configuration

        model

            An SQLAlchemy model that should be used to get statistics
    """
    def __init__(self, model, *args, **kwargs):
        colander.Schema.__init__(self, *args, **kwargs)
        self.inspector = inspect(model)

        self.build_schema()

    def build_schema(self):
        """
        Build the form schema for statistics configuration
        """
        # On parcourt les attributs dans leur ordre de déclaration
        for prop in sorted(self.inspector.attrs, key=_creation_order):

            node = None

            if isinstance(prop, ColumnProperty):
                node = self.get_schema_from_column(prop)

            elif isinstance(prop, RelationshipProperty):
                node = self.get_schema_from_relationship(prop)

            else:
                log.debug(u"Unknown data type : %s" % prop.key)

            if node is not None:
                self.add(node)

    def get_schema_from_column(self, prop):
        """
        return the appropriate mapping in order to build stats for the given
        prop
        """
        name = prop.key
        datas = prop.info.get('stats', {})

        if datas.get('exclude', False):
            log.debug(u"Excluded column : %s" % name)
            return

        column = prop.columns[0]
        column_type = getattr(column.type, 'impl', column.type)

        title = datas.get('title', name)

        if datas.get('options') is not None:
            # It's a static options enumeration
            options = datas.get('options')
            node = get_fixed_options_stat_mapping(options)
        else:
            node = get_stat_mapping_from_column(column_type)

        node.name = name
        node.title = title
        return node

    def get_schema_from_relationship(self, prop):
        """
        Return the appropriate mapping for stats based on an option
        relationship
        """
        name = prop.key
        datas = prop.info.get('stats', {})

        if datas.get('exclude', False):
            log.debug(u"Excluded column : %s" % name)
            return

        title = datas.get('title', name)

        dest_model = prop.mapper

        # TODO : éviter d'implémenter le model
        if prop.uselist and isinstance(dest_model.class_(), user.ConfigurableOption):
            node = get_relation_stat_mapping(dest_model)
        else:
            log.warn(u"This type of relationships are not implemented yet in \
the stats module")
            return

        node.name = name
        node.title = title
        return node
