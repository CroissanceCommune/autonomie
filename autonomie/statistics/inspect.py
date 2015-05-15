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

import logging
from collections import OrderedDict
from sqlalchemy import (
    Date,
    DateTime,
    Float,
    Integer,
    Numeric,
    Boolean,
)
from sqlalchemy.orm import (
    RelationshipProperty,
)
from sqla_inspect.base import BaseSqlaInspector


logger = logging.getLogger(__name__)


class Column(dict):
    """
    The column object wrapping the model's attribute
    """
    def __json__(self, request):
        return dict(
            label=self.get('label'),
            name=self.get('name'),
            key=self.get('key'),
            type=self.get('type', 'string'),
        )


def get_data_type(prop):
    """
    Returns the type of datas

    :param obj prop: The column object returned by the sqlalchemy model
    inspection
    :returns: A string representing the type of the column
    """
    type_ = 'string'
    sqla_column = prop.columns[0]

    column_type = getattr(sqla_column.type, 'impl', sqla_column.type)

    if isinstance(column_type, (Date, DateTime,)):
        type_ = 'date'
    elif isinstance(column_type, (Integer, Numeric, Float,)):
        type_ = 'number'
    elif isinstance(column_type, Boolean):
        type_ = 'bool'
    return type_


class StatisticInspector(BaseSqlaInspector):
    """
    A sqla inspector made for statistics

    model

        The model we want to inspect

    excludes

        The name of the attributes we want to exclude from inspection

    exclude_relationships

        Should we exclude relationships (usefull for limiting recursive
        inspection)
    """
    config_key = 'stats'

    def __init__(self, model, excludes=(), exclude_relationships=False):
        BaseSqlaInspector.__init__(self, model)
        self.model = model
        self.excludes = excludes
        self.exclude_relationships = exclude_relationships
        self.columns = self._collect_columns()

    def _collect_columns(self):
        """
        Collect the columns names, titles, ...

        Single attribute :
            name: for column identification
            label : for UI
            prop : The property (sqla object from which handle all datas
            column : The associated sqlalchemy.Column object

        OneToMany relationship :
            related_class: The related class
            related_key: The related key we may act on

        ManyToOne relationship :
            for each field of the destination class:
                related_class: The related_class
                name: for column identification
                label : for UI
                prop : The property (sqla object from which handle all datas
                column : The associated sqlalchemy.Column object


        """
        result = OrderedDict()
        todrop = []
        for prop in self.get_sorted_columns():
            if prop.key in self.excludes:
                continue
            info_dict = self.get_info_field(prop)
            colanderalchemy_infos = info_dict.get('colanderalchemy', {})

            export_infos = info_dict.get('export', {}).copy()
            stats_infos = export_infos.get(self.config_key, {}).copy()

            if export_infos.get('exclude', False):
                if stats_infos.get('exclude', True):
                    continue

            infos = export_infos
            infos.update(stats_infos)

            ui_label = colanderalchemy_infos.get('title', prop.key)
            datas = Column({
                'name': prop.key,
                'label': ui_label,
                'prop': prop,
                'column': prop.class_attribute,
            })
            datas.update(infos)

            if isinstance(prop, RelationshipProperty):

                if prop.uselist:
                    # A one to many relationship

                    # 1 get the result of the mapper's inspection
                    # 2 append a prefix to the names and labels
                    # 3 merge the resulting dict with the current one
                    if self.exclude_relationships:
                        # On zappe les relations o2M pour éviter les boucles
                        continue
                    res = StatisticInspector(
                        prop.mapper,
                        self.excludes,
                        True
                    ).columns

                    keys = res.keys()
                    for key in keys:
                        # We modifiy the keys and the labels (we append the
                        # related before to identify the relationship)
                        # <rel_name>-<remote attribute>
                        new_key = "%s-%s" % (prop.key, key)
                        res[new_key] = res.pop(key)
                        res[new_key]['label'] = "%s %s" % (
                            datas['label'],
                            res[new_key]['label'],
                        )
                        res[new_key]['rel_type'] = 'onetomany'
                        # On a besoin de la classe pour les outerjoin et
                        res[new_key]['join_class'] = prop.class_attribute
                        res[new_key]['key'] = new_key
                    result.update(res)

                else:
                    # On doit avoir directement les ids des options (objets
                    # distants) disponibles
                    # (sera fait lors de la génération du schéma)

                    # On utilisera la colonne avec l'id
                    todrop.append("%s_id" % prop.key)
                    datas['rel_type'] = 'manytoone'
                    datas['type'] = 'optrel'
                    # On a besoin de la classe liée pour la génération du form
                    # (récupérer les options disponibles)
                    datas['related_class'] = prop.mapper.class_
                    datas['key'] = datas['name']
                    result[datas['name']] = datas
            else:
                datas['type'] = get_data_type(prop)
                datas['key'] = datas['name']
                result[datas['name']] = datas

        for id_key in todrop:
            if id_key in result:
                ui_label = result[id_key].get('label')
                rel_key = id_key[:-3]
                if rel_key in result:
                    result[rel_key]['label'] = ui_label
                    result[rel_key]['column'] = result[id_key]['column']
                result.pop(id_key)
        return result

    def get_datas(self, key):
        """
        Return the inspected datas for the key

        :param str key: A column name
        """
        return self.columns.get(key)

    def get_json_columns(self):
        """
        Return the json representation of the dict of columns
        """
        result = OrderedDict()
        for key, value in self.columns.items():
            result[key] = value.__json__(None)
        return result
