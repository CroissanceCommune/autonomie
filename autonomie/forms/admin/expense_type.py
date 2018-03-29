# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import functools
import colander

from colanderalchemy import SQLAlchemySchemaNode

from autonomie import forms
from autonomie.models.expense.types import (
    ExpenseType,
    ExpenseKmType,
    ExpenseTelType,
)


def _customize_expense_type_fields(schema):
    """
    Customize schema to add ui related stuff

    :param obj schema: a colander.Schema
    """
    customize = functools.partial(forms.customize_field, schema)
    customize('label', missing=colander.required)
    return schema


def get_expense_type_schema(factory=ExpenseType, excludes=None, includes=None):
    """
    Build a form schema for ExpenseType administration
    """
    if includes is not None:
        excludes = None
    else:
        excludes = ('type', 'active', 'id')

    schema = SQLAlchemySchemaNode(factory, includes=includes, excludes=excludes)
    schema = _customize_expense_type_fields(schema)
    return schema


def get_expense_kmtype_schema(excludes=None, includes=None):
    """
    Build a form schema for ExpenseKmType administration
    """
    return get_expense_type_schema(factory=ExpenseKmType)


def get_expense_teltype_schema(excludes=None, includes=None):
    """
    Build a form schema for ExpenseTelType administration
    """
    schema = get_expense_type_schema(factory=ExpenseTelType)
    customize = functools.partial(forms.customize_field, schema)
    customize('percentage', missing=colander.required)
    return schema
