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
    form schemas for invoices related views
"""
from datetime import date
import colander

from deform import widget as deform_widget
from deform_bootstrap import widget as bootstrap_widget

from autonomie.views.forms.lists import BaseListsSchema
from autonomie.views.forms import main
from autonomie.views.forms.widgets import CustomChosenOptGroupWidget
from autonomie.models import company


STATUS_OPTIONS = (("both", u"Toutes les factures", ),
                  ("paid", u"Les factures payées", ),
                  ("notpaid", u"Seulement les impayés", ))


@colander.deferred
def deferred_fullcustomer_list_widget(node, kw):
    values = [('', '')]
    for comp in company.Company.query():
        values.append(
            deform_widget.OptGroup(
                comp.name,
                *[(cust.id, cust.name) for cust in comp.customers]
            )
        )
    return CustomChosenOptGroupWidget(
        values=values,
        placeholder=u"Sélectionner un client"
        )


@colander.deferred
def deferred_customer_list_widget(node, kw):
    values = [('', u'Sélectionner un client'), ]
    company = kw['request'].context
    values.extend(((cust.id, cust.name) for cust in company.customers))
    return bootstrap_widget.ChosenSingleWidget(
        values=values,
        placeholder=u'Sélectionner un client',
        )


@colander.deferred
def deferred_company_customer_validator(node, kw):
    """
    Ensure we don't query customers from other companies
    """
    company = kw['request'].context
    return colander.OneOf([customer.id for customer in company.customers])


def customer_node(is_admin=False):
    """
    return a customer selection node

        is_admin

            is the associated view restricted to company's invoices
    """
    if is_admin:
        deferred_customer_widget = deferred_fullcustomer_list_widget
        deferred_customer_validator = None
    else:
        deferred_customer_widget = deferred_customer_list_widget
        deferred_customer_validator = deferred_company_customer_validator

    return colander.SchemaNode(
            colander.Integer(),
            name='customer_id',
            widget=deferred_customer_widget,
            validator=deferred_customer_validator,
            missing=-1
        )


def get_list_schema(is_admin=False):
    """
    Return a schema for invoice listing

    is_admin

        If True, we don't provide the company selection node and we reduce the
        customers to the current company's
    """
    schema = BaseListsSchema().clone()

    schema.insert(0,
        colander.SchemaNode(
            colander.String(),
            name='status',
            widget=deform_widget.SelectWidget(values=STATUS_OPTIONS),
            validator=colander.OneOf([s[0] for s in STATUS_OPTIONS]),
            missing='both',
            ))

    schema.insert(0, customer_node(is_admin))

    if is_admin:
        schema.insert(0,
            main.company_node(
                name='company_id',
                missing=-1,
                widget_options={'default': ('', '')}
            ))

    schema.insert(0, main.year_select_node(name='year'))

    schema['search'].description = u"Identifiant du document"

    return schema


def range_validator(form, value):
    """
        Validate that end is higher or equal than start
    """
    if value['end'] > 0 and value['start'] > value['end']:
        exc = colander.Invalid(form,
             u"Le numéro de début doit être plus petit ou égal à celui de fin")
        exc['start'] = u"Doit être inférieur au numéro de fin"
        raise exc


class InvoicesPdfExport(colander.MappingSchema):
    """
        Schema for invoice bulk export
    """
    year = main.year_select_node(title=u"Année comptable")
    start = colander.SchemaNode(
            colander.Integer(),
            title=u"Numéro de début",
            description=u"Numéro à partir duquel exporter",
            )
    end = colander.SchemaNode(
            colander.Integer(),
            title=u"Numéro de fin",
            description=u"Numéro jusqu'auquel exporter \
(dernier document si vide)",
            missing=-1,
            )

pdfexportSchema = InvoicesPdfExport(
        title=u"Exporter un ensemble de factures dans un fichier pdf",
        validator=range_validator)
