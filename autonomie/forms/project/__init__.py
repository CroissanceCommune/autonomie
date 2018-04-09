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
import deform
import functools

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.customer import Customer
from autonomie.models.project import (
    Project,
)
from autonomie import forms
from autonomie.forms.lists import BaseListsSchema
from autonomie.forms.customer import get_customer_select_node

log = logging.getLogger(__name__)


def customer_objectify(id_):
    """
    Objectify the associated form node schema (an id schemanode)

    Return the customer object with the given id_

    Note :
        colanderalchemy schemanode is to a model and provides a objectify method
        used to convert an appstruct to the appropriate model.  For the
        project->customer relationship, we need to be able to configure only
        existing elements. Since we didn't found a clear way to do it with
        colanderalchemy, we add the node manually and fit the colanderalchemy
        way of working by implementing usefull methods (namely objectify and
        dictify)
    """
    obj = Customer.get(id_)
    return obj


def customer_dictify(obj):
    """
    Return a representation of the current model, used to fill the associated
    form node
    """
    return obj.id


def check_begin_end_date(form, value):
    """
    Check the project beginning date preceeds the end date
    """
    ending = value.get('ending_date')
    starting = value.get('starting_date')

    if ending is not None and starting is not None:
        if not ending >= starting:
            exc = colander.Invalid(
                form,
                u"La date de début doit précéder la date de fin du projet"
            )
            exc['starting_date'] = u"Doit précéder la date de fin"
            raise exc


def _customize_project_schema(schema):
    """
    Customize the project schema to add widgets/validators ...

    :param obj schema: a colander.SchemaNode instance
    """
    schema.validator = check_begin_end_date
    customize = functools.partial(forms.customize_field, schema)
    customize('name', missing=colander.required)
    customize(
        'definition',
        widget=deform.widget.TextAreaWidget(css_class='col-md-10')
    )

    # Add a custom node to be able to associate existing customers
    customer_id_node = get_customer_select_node(name="un client")
    customer_id_node.objectify = customer_objectify
    customer_id_node.dictify = customer_dictify

    schema.insert(
        3,
        colander.SchemaNode(
            colander.Sequence(),
            customer_id_node,
            widget=deform.widget.SequenceWidget(min_len=1),
            title=u"Clients",
            name='customers'
        )
    )
    return schema


def get_add_edit_project_schema():
    """
    Return the project Edition/add form schema
    """
    excludes = ("_acl", "id", "company_id", "archived", "customers",
                "invoices", "tasks", "estimations", "cancelinvoices",)
    schema = SQLAlchemySchemaNode(Project, excludes=excludes)
    schema = _customize_project_schema(schema)
    return schema


class PhaseSchema(colander.MappingSchema):
    """
        Schema for phase
    """
    name = colander.SchemaNode(
        colander.String(),
        title=u"Nom du dossier",
        validator=colander.Length(max=150),
    )


def get_list_schema():
    """
    Return the schema for the project search form
    :rtype: colander.Schema
    """
    schema = BaseListsSchema().clone()

    schema['search'].description = u"Projet ou nom du client"

    schema.add(
        colander.SchemaNode(
            colander.Boolean(),
            name='archived',
            label=u"Inclure les projets archivés",
            missing=False,
        )
    )

    return schema