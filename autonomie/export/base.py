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
    Boolean,
    Date,
    DateTime,
    inspect,
)
from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
)
from autonomie.views.render_api import (
    format_date,
    format_datetime,
)
from .sqla import BaseSqlaExporter
BLACKLISTED_KEYS = ()


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
    formatter = None
    if hasattr(column, 'columns'):
        column = column.columns[0]
        column_type = getattr(column.type, 'impl', column.type)

        if isinstance(column_type, Boolean):
            formatter = format_boolean

        elif isinstance(column_type, Date):
            formatter = format_date

        elif isinstance(column_type, DateTime):
            formatter = format_datetime

    return formatter


class SqlaExporter(BaseExporter, BaseSqlaExporter):
    """
    Provide tools to inspect a model and provide the datas needed for the export

    If relation:
        if related_key :
            {'title': id_field_title, 'related_key': related_key}
    """
    config_key = ''

    def __init__(self, model):
        BaseExporter.__init__(self)
        BaseSqlaExporter.__init__(self, model)
        self.headers = self._collect_headers()

    def _collect_headers(self):
        """
        Collect headers from the models attribute info col
        """
        res = []

        for prop in self.get_sorted_columns():

            if prop.key in BLACKLISTED_KEYS:
                continue

            info_dict = self.get_info_field(prop)
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

            if isinstance(prop, RelationshipProperty):
                main_infos = self._collect_relationship(main_infos, prop, res)
                if not main_infos or not main_infos.has_key('related_key'):
                    # If still no success, we forgot this one
                    print("Maybe there's missing some informations \
about a relationship")
                    continue
            else:
                main_infos = self._merge_many_to_one_field_from_fkey(
                    main_infos, prop, res
                )
                if main_infos is None:
                    continue

            res.append(main_infos)
        return res

    def _collect_relationship(self, main_infos, prop, result):
        """
        collect a relationship header:
            * remove onetomany relationship
            * merge foreignkeys with associated manytoone rel if we were able to
                find an attribute that will represent the destination model
                (generally a label of a configurable option)

        :param dict main_infos: The already collected datas about this column
        :param obj prop: The property mapper of the relationship
        :param list result: The actual collected headers
        :returns: a dict with the datas matching this header
        """
        # No handling of the uselist relationships for the moment
        if prop.uselist:
            main_infos = None
        else:
            related_field_inspector = inspect(prop.mapper)

            self._merge_many_to_one_field(main_infos, prop, result)

            if not main_infos.has_key('related_key'):
                # If one of those keys exists in the corresponding
                # option, we use it as reference key
                for rel_key in ('label', 'name', 'title'):
                    if related_field_inspector.attrs.has_key(rel_key):
                        main_infos['related_key'] = rel_key
                        break
        return main_infos

    def _merge_many_to_one_field(self, main_infos, prop, result):
        """
        Find the associated id foreignkey and get the title from it
        Remove this fkey field from the export

        :param dict main_infos: The already collected datas about this column
        :param obj prop: The property mapper of the relationship
        :param list result: The actual collected headers
        :returns: a title
        """
        title = None
        # We first find the related foreignkey to get the good title
        rel_base = list(prop.local_columns)[0]
        related_fkey_name = rel_base.name
        for val in result:
            if val['name'] == related_fkey_name:
                title = val['label']
                main_infos['label'] = title
                result.remove(val)
                break

        return main_infos

    def _merge_many_to_one_field_from_fkey(self, main_infos, prop, result):
        """
        Find the relationship associated with this fkey and set the title

        :param dict main_infos: The already collected datas about this column
        :param obj prop: The property mapper of the relationship
        :param list result: The actual collected headers
        :returns: a main_infos dict or None
        """
        if prop.columns[0].foreign_keys and prop.key.endswith('_id'):
            # We have a foreign key, we'll try to merge it with the
            # associated foreign key
            rel_name = prop.key[0:-3]
            for val in result:
                if val["name"] == rel_name:
                    val["label"] = main_infos['label']
                    main_infos = None # We can forget this field in export
                    break
        return main_infos

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
        val = getattr(obj, name, None)

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
