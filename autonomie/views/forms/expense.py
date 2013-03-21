# -*- coding: utf-8 -*-
# * File Name : treasury.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 06-03-2013
# * Last Modified :
#
# * Project :
#
"""
    Form models related to the expenses configuration
    * expense status configuration
    * period selection
    * expenseline configuration
"""
import colander
from datetime import date
from deform import widget

from autonomie.models.treasury import ExpenseType
from autonomie.views.render_api import month_name
from autonomie.views.forms.widgets import deferred_year_select_widget
from autonomie.views.forms.widgets import deferred_today
from .custom_types import AmountType


@colander.deferred
def default_year(node, kw):
    return date.today().year


@colander.deferred
def default_month(node, kw):
    return date.today().month


@colander.deferred
def deferred_code_validator(node, kw):
    """
        Return a validator for the analytic code
    """
    codes = [t.code for t in ExpenseType.query()]
    return colander.OneOf(codes)


class PeriodSelectSchema(colander.MappingSchema):
    year = colander.SchemaNode(colander.Integer(),
            widget=deferred_year_select_widget,
            default=default_year,
            missing=default_year,
            title=u"")
    month = colander.SchemaNode(colander.Integer(),
            widget=widget.SelectWidget(values=[(month, month_name(month))
                                                for month in range(1,13)],
                                                css_class='input-small'),
            default=default_month,
            missing=default_month,
            title=u"")



class ExpenseStatusSchema(colander.MappingSchema):
    comment = colander.SchemaNode(colander.String(),
            widget=widget.TextAreaWidget(cols=80, rows=2),
                                    title=u"Communication avec la CAE",
            description=u"Message à destination des membres de la CAE qui \
valideront votre feuille de notes de frais",
            missing=u"",
            default=u"")


class BaseLineSchema(colander.MappingSchema):
    """
        Base Expenseline schema
    """
    date = colander.SchemaNode(colander.Date(), missing=deferred_today,
            default=deferred_today)
    category = colander.SchemaNode(colander.String(),
            validator=colander.OneOf(('1', '2')))
    description = colander.SchemaNode(colander.String(), missing=u'')
    valid = colander.SchemaNode(colander.Boolean(), missing=False)
    code = colander.SchemaNode(colander.String(),
            validator=deferred_code_validator)

class ExpenseKmLineSchema(BaseLineSchema):
    """
        Expense line schema for kilometric fees
    """
    start = colander.SchemaNode(colander.String(), missing=u"")
    end = colander.SchemaNode(colander.String(), missing=u"")
    km = colander.SchemaNode(AmountType())


class ExpenseLineSchema(BaseLineSchema):
    """
        Expense line schema, validates the different expense line schemes
    """
    ht = colander.SchemaNode(AmountType())
    tva = colander.SchemaNode(AmountType())


class ExpenseLineSchemaAddon(ExpenseLineSchema):
    id = colander.SchemaNode(colander.Integer())

class ExpenseLinesSchema(colander.SequenceSchema):
    line = ExpenseLineSchemaAddon()

class ExpenseKmLineSchemaAddon(ExpenseKmLineSchema):
    id = colander.SchemaNode(colander.Integer())

class ExpenseKmLinesSchema(colander.SequenceSchema):
    line = ExpenseKmLineSchemaAddon()

class ExpenseSheetSchema(ExpenseStatusSchema):
    lines = ExpenseLinesSchema()
    kmlines = ExpenseKmLinesSchema()
