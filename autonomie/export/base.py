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
Base export class
"""

from sqlalchemy import (
    inspect,
    Boolean,
    Date,
    DateTime,
)
from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
)
from colanderalchemy.schema import _creation_order
from autonomie.views.render_api import (
    format_date,
    format_datetime,
)

class BaseExporter(object):
    """
    Define base classes to export datas

        writer = Exporter(headers)
        for row in rows:
            writer.add_row(row)

        file_buffer = writer.render()

        headers

            list of dict in the form {'name': <name>, 'label': <label>}
            name is the name of the rows' attribute we will retrieve the value
            from
            label is the label we will put at the top of the column

        datas

    """
    headers = []
    def __init__(self):
        self._datas = []

    @staticmethod
    def format_row(row):
        """
        Row formatter, should be implemented in subclasses
        """
        return row

    def add_row(self, row):
        """
            Add a row to our buffer
        """
        self._datas.append(self.format_row(row))

    def set_datas(self, datas):
        """
        bulk add rows
        """
        for data in datas:
            self.add_row(data)

    def render(self):
        """
        Render the datas as a file buffer
        """
        raise NotImplementedError()


def format_boolean(value):
    """
    Format a boolean value
    """
    return "Y" and value or "N"


def get_formatter_from_column(column):
    """
    Return a formatter regarding the given SQLAlchemy column type
    """
    print("Getting a formatter")
    column = column.columns[0]
    column_type = getattr(column.type, 'impl', column.type)
    print column_type

    formatter = None

    if isinstance(column_type, Boolean):
        formatter = format_boolean

    elif isinstance(column_type, Date):
        formatter = format_date

    elif isinstance(column_type, DateTime):
        print("Its a datetime")
        formatter = format_datetime

    return formatter


def get_info_field(prop):
    """
    Return the info attribute of the given property
    """
    if isinstance(prop, ColumnProperty):
        column = prop.columns[0]

    elif isinstance(prop, RelationshipProperty):
        column = prop

    return column.info


class SqlaExporter(BaseExporter):
    """
    Provide tools to inspect a model and provide the datas needed for the export

    """
    config_key = ''

    def __init__(self, model):
        self.inspector = inspect(model)
        self.headers = self._collect_headers()
        super(SqlaExporter, self).__init__()

    def _collect_headers(self):
        """
        Collect headers from the models attribute info col
        """
        res = []

        columns = sorted(self.inspector.attrs, key=_creation_order)

        for prop in columns:

            info_dict = get_info_field(prop)
            main_infos = info_dict.get('export', {}).copy()

            infos = main_infos.get(self.config_key, {})

            if infos.get('exclude', False) or main_infos.get('exclude', False):
                continue

            title = info_dict.get('colanderalchemy', {}).get('title')

            if title is not None and not main_infos.has_key('label'):
                main_infos['label'] = title
            main_infos.setdefault('label', prop.key)

            main_infos['name'] = prop.key

            main_infos.update(infos)

            # We keep the original prop in case it's usefull
            main_infos['__col__'] = prop

            if isinstance(prop, RelationshipProperty) \
               and not main_infos.has_key('related_key'):
                print("Maybe there's missing some informations about a \
relationship")
                continue

            res.append(main_infos)
        return res

    def add_row(self, obj):
        """
        fill a new row with the given obj

            obj

               instance of the exporter's model
        """
        row = {}
        for column in self.headers:

            if isinstance(column['__col__'], ColumnProperty):
                value = self._get_column_cell_val(obj, column)

            elif isinstance(column['__col__'], RelationshipProperty):
                value = self._get_relationship_cell_val(obj, column)

            row[column['name']] = value

        self._datas.append(self.format_row(row))

    def _get_formatted_val(self, obj, name, column):
        """
        Format the value of the attribute 'name' from the given object
        """
        val = getattr(obj, name)

        formatter = column.get('formatter')
        if formatter is None:
            formatter = get_formatter_from_column(column['__col__'])

        if formatter is not None:
            val = formatter(val)
        return val

    def _get_relationship_cell_val(self, obj, column):
        """
        Return the value to insert in a relationship cell
        """
        name = column['name']
        related_key = column.get('related_key', 'label')

        related_obj = getattr(obj, name, None)

        if related_obj is None:
            return ""
        if column['__col__'].uselist: # OneToMany
            _vals = []
            for rel_obj in related_obj:
                _vals.append(
                    self._get_formatted_val(rel_obj, related_key, column)
                )
            val = '\n'.join(_vals)
        else:
            val = self._get_formatted_val(related_obj, related_key, column)

        return val

    def _get_column_cell_val(self, obj, column):
        """
        Return a value of a "column" cell
        """
        name = column['name']
        return self._get_formatted_val(obj, name, column)
