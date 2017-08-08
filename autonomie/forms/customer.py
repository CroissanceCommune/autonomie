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
    Customer handling forms schemas
"""
import colander
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.forms.lists import BaseListsSchema


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


def customer_after_bind(node, kw):
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


def get_company_customer_schema():
    """
    return the schema for user add/edit regarding the current user's role
    """
    from autonomie.models.customer import Customer
    schema = SQLAlchemySchemaNode(Customer)
    schema['name'].missing = colander.required
    return schema


def get_individual_customer_schema():
    """
    return the schema for user add/edit regarding the current user's role
    """
    from autonomie.models.customer import Customer
    excludes = ('name', 'tva_intracomm', 'function',)
    schema = SQLAlchemySchemaNode(Customer, excludes=excludes)

    schema['firstname'].title = u"Prénom"
    schema['firstname'].missing = colander.required
    schema['lastname'].title = u'Nom'
    schema['civilite'].missing = colander.required
    return schema
