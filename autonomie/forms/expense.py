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
import deform

from autonomie.models.treasury import (
    ExpenseType,
    get_expense_years,
)
from autonomie.models import user
from autonomie.models.task.invoice import get_invoice_years
from .custom_types import AmountType
from autonomie import forms


STATUS_OPTIONS = (
    ("all", u"Toutes les notes de dépense", ),
    ("valid", u'Validées', ),
    ("resulted", u'Payées', ),
    ("wait", u'En attente de validation', ),
)


@colander.deferred
def deferred_type_id_validator(node, kw):
    """
        Return a validator for the expensetype
    """
    ids = [t.id for t in ExpenseType.query()]
    return colander.OneOf(ids)


class PeriodSelectSchema(colander.MappingSchema):
    year = forms.year_select_node(query_func=get_invoice_years)
    month = forms.month_select_node(title=u'')


class ExpenseStatusSchema(colander.MappingSchema):
    comment = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(cols=80, rows=2),
        title=u"Communication avec la CAE",
        description=u"Message à destination des membres de la CAE qui \
        valideront votre feuille de notes de dépense",
        missing=colander.drop,
        default=u"",
    )


class BaseLineSchema(colander.MappingSchema):
    """
        Base Expenseline schema
    """
    date = forms.today_node(missing=forms.deferred_today)
    category = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(('1', '2'))
        )
    description = colander.SchemaNode(colander.String(), missing=u'')
    valid = colander.SchemaNode(colander.Boolean(), missing=False)
    type_id = colander.SchemaNode(
        colander.Integer(),
        validator=deferred_type_id_validator,
        )


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


class BookMarkSchema(colander.MappingSchema):
    """
        Schema for bookmarks
    """
    type_id = colander.SchemaNode(
        colander.Integer(),
        validator=deferred_type_id_validator
    )
    description = colander.SchemaNode(colander.String())
    ht = colander.SchemaNode(colander.Float())
    tva = colander.SchemaNode(colander.Float())


def get_list_schema():
    schema = forms.lists.BaseListsSchema().clone()

    schema['search'].description = u"Identifiant du document"

    schema.insert(0, colander.SchemaNode(
        colander.String(),
        name=u'status',
        widget=deform.widget.SelectWidget(values=STATUS_OPTIONS),
        validator=colander.OneOf([s[0] for s in STATUS_OPTIONS]),
        missing='all',
    ))

    schema.insert(0, forms.year_select_node(
        name='year',
        title=u"Année",
        query_func=get_expense_years,
    ))

    schema.insert(0, forms.month_select_node(
        title=u"Mois",
        missing=-1,
        name='month',
        widget_options={'default_val': (-1, '')},
    ))

    schema.insert(0, user.user_node(
        title=u"Utilisateur",
        missing=-1,
        name=u'owner_id',
        widget_options={
            'default_option': (-1, ''),
            'placeholder': u"Sélectionner un entrepreneur"},
    ))

    return schema
