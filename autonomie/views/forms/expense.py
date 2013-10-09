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
def deferred_type_id_validator(node, kw):
    """
        Return a validator for the expensetype
    """
    ids = [t.id for t in ExpenseType.query()]
    return colander.OneOf(ids)


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
    type_id = colander.SchemaNode(colander.Integer(),
            validator=deferred_type_id_validator)

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
