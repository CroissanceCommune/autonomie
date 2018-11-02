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
Customer handling forms schemas and related widgets
"""
import colander
import deform
from colanderalchemy import SQLAlchemySchemaNode

from autonomie_base.consts import CIVILITE_OPTIONS as ORIG_CIVILITE_OPTIONS
from autonomie.models.customer import Customer
from autonomie.models.company import Company
from autonomie.models.project import Project
from autonomie.compute.math_utils import convert_to_int
from autonomie import forms
from autonomie.forms.lists import BaseListsSchema

# For customers we also want 'Mr et Mme'
# For customers we also want 'Mr et Mme'
CIVILITE_OPTIONS = ORIG_CIVILITE_OPTIONS + (
    ('M. et Mme', u"Monsieur et Madame"),
    ('M. ou Mme', u"Monsieur ou Madame"),
    ('M. et M.', u"Monsieur et Monsieur"),
    ('Mr ou Mr', u"Monsieur ou Monsieur"),
    ('Mme et Mme', u"Madame et Madame"),
    ('Mme ou Mme', u"Madame ou Madame"),
)


def _build_customer_select_value(customer):
    """
        return the tuple for building customer select
    """
    label = customer.label
    if customer.code:
        label += u" ({0})".format(customer.code)
    return (customer.id, label)


def build_customer_values(customers):
    """
        Build human understandable customer labels
        allowing efficient discrimination
    """
    return [_build_customer_select_value(customer) for customer in customers]


def get_customers_from_request(request):
    """
    Extract a customers list from the request object

    :param obj request: The pyramid request object
    :returns: A list of customers
    :rtype: list
    """
    if isinstance(request.context, Project):
        company_id = request.context.company.id
    elif isinstance(request.context, Company):
        company_id = request.context.id
    else:
        return []

    customers = Customer.label_query()
    customers = customers.filter_by(company_id=company_id)
    customers = customers.filter_by(archived=False)

    return customers.order_by(Customer.label).all()


def get_current_customer_id_from_request(request):
    """
    Return the current customer from the request object

    :param obj request: The current pyramid request object
    """
    result = None
    if 'customer' in request.params:
        result = convert_to_int(request.params.get('customer'))
    return result


def get_deferred_customer_select(
    query_func=get_customers_from_request,
    default_option=None,
    **widget_options
):
    """
    Dynamically build a deferred customer select with (or without) a void
    default value

    """
    @colander.deferred
    def deferred_customer_select(node, kw):
        """
        Collecting customer select datas from the given request's context

        :param dict kw: Binding dict containing a request key
        :returns: A deform.widget.Select2Widget
        """
        request = kw['request']
        customers = query_func(request)
        values = list(build_customer_values(customers))
        if default_option is not None:
            values.insert(0, default_option)

        return deform.widget.Select2Widget(
            values=values,
            **widget_options
        )
    return deferred_customer_select


@colander.deferred
def deferred_default_customer(node, kw):
    """
    Collect the default customer value from a request's context

    :param dict kw: Binding dict containing a request key
    :returns: The current customer or colander.null
    """
    request = kw['request']
    customer_id = get_current_customer_id_from_request(request)
    result = colander.null
    if customer_id is not None:
        # On checke pour éviter de se faire avoir si le customer est passé en
        # paramètre
        customers = get_customers_from_request(request)
        if customer_id in [c.id for c in customers]:
            result = customer_id
    return result


def get_deferred_customer_select_validator(
    query_func=get_customers_from_request
):
    @colander.deferred
    def deferred_customer_validator(node, kw):
        """
        Build a customer option validator based on the request's context

        :param dict kw: Binding dict containing a request key
        :returns: A colander validator
        """
        request = kw['request']
        customers = query_func(request)
        customer_ids = [customer.id for customer in customers]

        def customer_oneof(value):
            if value in ("0", 0):
                return u"Veuillez choisir un client"
            elif value not in customer_ids:
                return u"Entrée invalide"
            return True

        return colander.Function(customer_oneof)


def customer_node_factory(**kw):
    """
    Shortcut used to build a colander schema node

    all arguments are optionnal

    Allow following options :

        any key under kw

            colander.SchemaNode options :

                * title,
                * description,
                * default,
                * missing
                * ...

        widget_options

            deform.widget.Select2Widget options as a dict

        query_func

            A callable expecting the request parameter and returning the current
            customer that should be selected

    e.g:

        >>> get_customers_from_request(
            title=u"Client",
            query_func=get_customers_list,
            default=get_current_customer,
            widget_options={}
        )


    """
    title = kw.pop('title', u'')
    default = kw.pop('default', deferred_default_customer)
    query_func = kw.pop('query_func', get_customers_from_request)
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
        colander.Integer(),
        title=title,
        default=default,
        widget=get_deferred_customer_select(
            query_func=query_func,
            **widget_options
        ),
        validator=get_deferred_customer_select_validator(query_func),
        **kw
    )


customer_choice_node_factory = forms.mk_choice_node_factory(
    customer_node_factory,
    title=u"Choix du client",
    resource_name="un client",
)


def get_list_schema():
    """
    Return the schema for the customer search list
    """
    schema = BaseListsSchema().clone()
    schema['search'].description = u"Entreprise ou contact principal"
    schema.add(
        colander.SchemaNode(
            colander.Boolean(),
            name='archived',
            label=u"Inclure les clients archivés",
        )
    )
    schema.add(
        colander.SchemaNode(
            colander.Boolean(),
            name='individual',
            label=u"Inclure les particuliers",
            default=True,
        )
    )
    schema.add(
        colander.SchemaNode(
            colander.Boolean(),
            name='company',
            label=u"Inclure les personnes morales \
(entreprises, association ...)",
            default=True,
        )
    )
    return schema


def _customer_after_bind(node, kw):
    """
    After bind method for the customer model schema

    removes nodes if the user have no rights to edit them

    :param obj node: SchemaNode corresponding to the Customer
    :param dict kw: The bind parameters
    """
    request = kw['request']
    if not request.has_permission('admin_treasury', request.context):
        del node['compte_tiers']
        del node['compte_cg']


def _customize_schema(schema):
    """
    Add common widgets configuration for the customer forms schema

    :param obj schema: The Customer form schema
    """
    schema['civilite'].widget = forms.get_select(
        CIVILITE_OPTIONS[1:],
    )
    schema['civilite'].validator = colander.OneOf(
        [a[0] for a in CIVILITE_OPTIONS]
    )
    schema['address'].widget = deform.widget.TextAreaWidget(
        cols=25,
        row=1,
    )
    schema['email'].validator = forms.mail_validator()
    schema['comments'].widget = deform.widget.TextAreaWidget(
        css_class="col-md-10"
    )
    return schema


def get_company_customer_schema():
    """
    return the schema for user add/edit regarding the current user's role
    """
    schema = SQLAlchemySchemaNode(Customer)
    schema = _customize_schema(schema)
    schema['name'].missing = colander.required
    schema.after_bind = _customer_after_bind
    return schema


def get_individual_customer_schema():
    """
    return the schema for user add/edit regarding the current user's role
    """
    excludes = ('name', 'tva_intracomm', 'function',)
    schema = SQLAlchemySchemaNode(Customer, excludes=excludes)
    schema = _customize_schema(schema)
    schema['firstname'].title = u"Prénom"
    schema['lastname'].title = u'Nom'
    schema['civilite'].missing = colander.required
    schema.after_bind = _customer_after_bind
    return schema


def get_add_edit_customer_schema(excludes=None, includes=None):
    """
    Build a generic add edit customer schema
    """
    if includes is not None:
        excludes = None
    elif excludes is None:
        excludes = ('company_id',)

    schema = SQLAlchemySchemaNode(
        Customer,
        excludes=excludes,
        includes=includes
    )
