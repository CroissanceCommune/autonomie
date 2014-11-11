# -*- coding: utf-8 -*-
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
"""
Sqlalchemy utilities to build exporters based on Sqlalchemy models
"""
from sqlalchemy import inspect
from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
)
from colanderalchemy.schema import _creation_order


class BaseSqlaExporter(object):
    """
    Base class for exporters
    """
    config_key = ''

    def __init__(self, model):
        self.inspector = inspect(model)

    def get_sorted_columns(self):
        """
        Return columns regarding their relevance in the model's declaration
        """
        return sorted(self.inspector.attrs, key=_creation_order)

    @staticmethod
    def get_info_field(prop):
        """
        Return the info attribute of the given property
        """
        if isinstance(prop, ColumnProperty):
            column = prop.columns[0]

        elif isinstance(prop, RelationshipProperty):
            column = prop

        return column.info

