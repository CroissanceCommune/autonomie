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
import datetime
import colander
import deform
import functools

from sqlalchemy import distinct
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.utils import strings
from autonomie.models.expense.sheet import (
    ExpenseSheet,
    get_expense_years,
    ExpenseLine,
    ExpenseKmLine,
)

from autonomie.models.expense.types import (
    ExpenseType,
    ExpenseKmType
)
from autonomie.forms.user import user_node
from .custom_types import AmountType
from autonomie import forms
from autonomie.forms.payments import (
    get_amount_topay,
    deferred_amount_default,
    deferred_payment_mode_widget,
    deferred_payment_mode_validator,
    deferred_bank_widget,
    deferred_bank_validator,
)
from autonomie.models.payments import BankAccount


STATUS_OPTIONS = (
    ("all", u"Toutes les notes de dépense", ),
    ("wait", u'En attente de validation', ),
    ("valid", u'Validées', ),
    ('justified', u"Justficatifs reçus"),
    ("paid", u"Partiellement payées", ),
    ("resulted", u'Payées', ),
)


@colander.deferred
def deferred_type_id_validator(node, kw):
    """
    deferred Expensetype id validator
    """
    from autonomie.models.expense.types import ExpenseType
    ids = [t.id for t in ExpenseType.query()]
    return colander.OneOf(ids)


@colander.deferred
def deferred_unique_expense(node, kw):
    """
    Return a validator to check if the expense is unique
    """
    from autonomie.models.expense.sheet import ExpenseSheet
    request = kw['request']
    if isinstance(request.context, ExpenseSheet):
        company_id = request.context.company_id
        user_id = request.context.user_id
    else:
        if 'uid' in request.matchdict:
            user_id = request.matchdict['uid']
        else:
            user_id = request.user.id

        company_id = request.context.id

    def validator(node, value):
        """
        The validator
        """
        month = value['month']
        year = value['year']

        query = ExpenseSheet.query().filter_by(month=month)
        query = query.filter_by(year=year)
        query = query.filter_by(user_id=user_id)
        query = query.filter_by(company_id=company_id)
        if query.count() > 0:
            exc = colander.Invalid(
                node,
                u"Une note de dépense pour la période {0} {1} existe "
                u"déjà".format(
                    strings.month_name(month),
                    year,
                )
            )
            exc['month'] = u"Une note de dépense existe"
            exc['year'] = u"Une note de dépense existe"
            raise exc
    return validator


@colander.deferred
def deferred_expense_total_validator(node, kw):
    """
        validate the amount to keep the sum under the total
    """
    topay = get_amount_topay(kw)
    max_msg = u"Le montant ne doit pas dépasser %s (total ttc - somme \
des paiements)" % (topay / 100.0)
    min_msg = u"Le montant doit être positif"
    return colander.Range(
        min=0, max=topay, min_err=min_msg, max_err=max_msg,
    )


class ExpensePaymentSchema(colander.MappingSchema):
    """
    Schéma de saisi des paiements des notes de dépense
    """
    come_from = forms.come_from_node()
    amount = colander.SchemaNode(
        AmountType(),
        title=u"Montant du paiement",
        validator=deferred_expense_total_validator,
        default=deferred_amount_default,
    )
    date = forms.today_node()
    mode = colander.SchemaNode(
        colander.String(),
        title=u"Mode de paiement",
        widget=deferred_payment_mode_widget,
        validator=deferred_payment_mode_validator,
    )
    bank_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Banque",
        missing=colander.drop,
        widget=deferred_bank_widget,
        validator=deferred_bank_validator,
        default=forms.get_deferred_default(BankAccount),
    )
    waiver = colander.SchemaNode(
        colander.Boolean(),
        title=u"Abandon de créance",
        description="""Indique que ce paiement correspond à un abandon de
créance à la hauteur du montant indiqué (le Mode de paiement et la Banque sont
alors ignorés)""",
        default=False,
    )
    resulted = colander.SchemaNode(
        colander.Boolean(),
        title=u"Soldé",
        description="""Indique que le document est soldé (
ne recevra plus de paiement), si le montant indiqué correspond au
montant de feuille de notes de dépense celle-ci est soldée automatiquement""",
        default=False,
    )


def customize_schema(schema):
    """
    Add custom field configuration to the schema

    :param obj schema: colander Schema
    """
    schema.validator = deferred_unique_expense
    customize = functools.partial(forms.customize_field, schema)
    customize(
        'month',
        widget=forms.get_month_select_widget({}),
        validator=colander.OneOf(range(1, 13)),
        default=forms.default_month,
        missing=colander.required,
    )
    customize(
        'year',
        widget=forms.get_year_select_deferred(
            query_func=get_expense_years
        ),
        validator=colander.Range(
            min=0, min_err=u"Veuillez saisir une année valide"
        ),
        default=forms.default_year,
        missing=colander.required,
    )


def get_add_edit_sheet_schema():
    """
    Return a schema for expense add/edit

    Only month and year are available for edition

    :rtype: colanderalchemy.SQLAlchemySchemaNode
    """
    from autonomie.models.expense.sheet import ExpenseSheet
    schema = SQLAlchemySchemaNode(
        ExpenseSheet,
        includes=('month', 'year'),
    )
    customize_schema(schema)
    return schema


def get_add_edit_line_schema(factory):
    """
    Build a schema for expense line

    :param class model: The model for which we want to generate the schema
    :rerturns: A SQLAlchemySchemaNode schema
    """
    excludes = ('sheet_id',)
    schema = SQLAlchemySchemaNode(factory, excludes=excludes)

    if factory == ExpenseLine:
        forms.customize_field(
            schema,
            'type_id',
            validator=forms.get_deferred_select_validator(
                ExpenseType,
                filters=[('type', 'expense')]
            ),
            missing=colander.required,
        )
    elif factory == ExpenseKmLine:
        forms.customize_field(
            schema,
            'type_id',
            validator=forms.get_deferred_select_validator(
                ExpenseKmType,
                filters=[('year', datetime.date.today().year)]
            ),
            missing=colander.required,
        )

    forms.customize_field(
        schema,
        'ht',
        missing=colander.required,
    )
    forms.customize_field(
        schema,
        'tva',
        missing=colander.required,
    )
    forms.customize_field(
        schema,
        'km',
        missing=colander.required,
    )
    return schema


class BookMarkSchema(colander.MappingSchema):
    """
        Schema for bookmarks
    """
    type_id = colander.SchemaNode(
        colander.Integer(),
        validator=deferred_type_id_validator
    )
    description = colander.SchemaNode(
        colander.String(),
        missing=u"",
    )
    ht = colander.SchemaNode(colander.Float())
    tva = colander.SchemaNode(colander.Float())


def get_list_schema():
    """
    Build a form schema for expensesheet listing
    """
    schema = forms.lists.BaseListsSchema().clone()

    schema['search'].description = u"Identifiant du document"

    schema.insert(0, colander.SchemaNode(
        colander.String(),
        name=u'status',
        widget=deform.widget.SelectWidget(values=STATUS_OPTIONS),
        validator=colander.OneOf([s[0] for s in STATUS_OPTIONS]),
        missing='all',
        default='all',
    ))

    schema.insert(0, forms.year_select_node(
        name='year',
        title=u"Année",
        query_func=get_expense_years,
    ))

    schema.insert(0, forms.month_select_node(
        title=u"Mois",
        missing=-1,
        default=-1,
        name='month',
        widget_options={'default_val': (-1, '')},
    ))

    schema.insert(
        0,
        user_node(
            title=u"Utilisateur",
            missing=colander.drop,
            name=u'owner_id',
            widget_options={
                'default_option': ('', u'Tous les entrepreneurs'),
                'placeholder': u"Sélectionner un entrepreneur"},
        )
    )

    return schema
