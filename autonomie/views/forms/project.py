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
    Form schemas for project edition
"""
import colander
import logging

from deform import widget

from autonomie.views.forms.widgets import deferred_autocomplete_widget
from autonomie.views.forms.widgets import get_date_input
from autonomie.views.forms.widgets import DisabledInput
from autonomie.views.forms.lists import BaseListsSchema

log = logging.getLogger(__name__)


def build_customer_value(customer=None):
    """
        return the tuple for building customer select
    """
    if customer:
        return (str(customer.id), customer.name)
    else:
        return ("0", u"Sélectionnez")


def build_customer_values(customers):
    """
        Build human understandable customer labels
        allowing efficient discrimination
    """
    options = [build_customer_value()]
    options.extend([build_customer_value(customer)
                            for customer in customers])
    return options

def get_customers_from_request(request):
    if request.context.__name__ == 'project':
        customers = request.context.company.customers
    elif request.context.__name__ == 'company':
        customers = request.context.customers
    else:
        customers = []
    return customers

@colander.deferred
def deferred_customer_list(node, kw):
    request = kw['request']
    customers = get_customers_from_request(request)
    return deferred_autocomplete_widget(node,
                        {'choices':build_customer_values(customers)})

@colander.deferred
def deferred_code_widget(node, kw):
    if kw['request'].context.__name__ == 'project':
        wid = DisabledInput()
    else:
        wid = widget.TextInputWidget(mask='****')
    return wid


@colander.deferred
def deferred_default_customer(node, kw):
    """
        Return the customer provided as request arg if there is one
    """
    request = kw['request']
    customers = get_customers_from_request(request)
    customer = request.params.get('customer')
    if customer in [str(c.id) for c in customers]:
        return [int(customer)]
    else:
        return colander.null


@colander.deferred
def deferred_customer_validator(node, kw):
    request = kw['request']
    customers = get_customers_from_request(request)
    customer_ids = [customer.id for customer in customers]
    def customer_oneof(value):
        if value in ("0", 0):
            return u"Veuillez choisir un client"
        elif value not in customer_ids:
            return u"Entrée invalide"
        return True
    return colander.Function(customer_oneof)


class CustomerSchema(colander.SequenceSchema):
    customer_id = colander.SchemaNode(colander.Integer(),
            title=u"Client",
            widget=deferred_customer_list,
            validator=deferred_customer_validator)


class ProjectSchema(colander.MappingSchema):
    """
        Schema for project
    """
    name = colander.SchemaNode(colander.String(),
            title=u"Nom du projet",
            validator=colander.Length(max=150), css_class='pull-left')
    code = colander.SchemaNode(colander.String(),
            title=u"Code du projet",
            widget=deferred_code_widget,
            validator=colander.Length(4))
    type = colander.SchemaNode(colander.String(),
            title="Type de projet",
            validator=colander.Length(max=150),
            missing=u'')
    definition = colander.SchemaNode(colander.String(),
            widget=widget.TextAreaWidget(cols=80, rows=4),
            title=u'Définition',
            missing=u'')
    startingDate = colander.SchemaNode(colander.Date(),
            title=u"Date de début",
            missing=u"",
            widget=get_date_input())
    endingDate = colander.SchemaNode(colander.Date(),
            title=u"Date de fin",
            missing=u"",
            widget=get_date_input())
    customers = CustomerSchema(
            title=u"Clients",
            widget=widget.SequenceWidget(
                min_len=1,
                add_subitem_text_template=u"Ajouter un client"),
            default=deferred_default_customer)


class PhaseSchema(colander.MappingSchema):
    """
        Schema for phase
    """
    name = colander.SchemaNode(colander.String(),
            validator=colander.Length(max=150))


phaseSchema = PhaseSchema()


class ProjectsListSchema(BaseListsSchema):
    archived = colander.SchemaNode(colander.String(),
                                    missing="0",
                                    validator=colander.OneOf(('0', '1')))
