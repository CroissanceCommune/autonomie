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
from colanderalchemy import SQLAlchemySchemaNode
from autonomie.views.forms.lists import BaseListsSchema

def get_list_schema():
    schema = BaseListsSchema().clone()
    schema['search'].description = u"Entreprise ou contact principal"

    return schema


def get_contractor_customer_schema():
    """
    Rerturn the contractor customer form
    """
    return SQLAlchemySchemaNode(
        Customer,
        excludes=('compte_tiers', 'compte_cg'),
    )


def get_manager_customer_schema():
    """
    Return the manager customer form
    """
    return SQLAlchemySchemaNode(Customer)


def get_customer_schema(request):
    """
    return the schema for user add/edit regarding the current user's role
    """
    if request.user.is_contractor():
        schema = get_contractor_customer_schema()
    else:
        schema = get_manager_customer_schema()
    return schema
