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

from autonomie_base.models.base import DBSESSION
from autonomie.models.customer import Customer
from autonomie.models.project import (
    Project,
)
from autonomie.models.project.types import (
    ProjectType,
    SubProjectType,
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


@colander.deferred
def deferred_default_project_type(node, kw):
    """
    Load the default ProjectType on bind
    """
    res = DBSESSION().query(ProjectType.id).filter_by(default=True).first()
    if res is not None:
        res = res[0]
    else:
        res = colander.null
    return res


@colander.deferred
def deferred_project_type_widget(node, kw):
    """
    Build a ProjectType radio checkbox widget on bind
    Filter project types by active and folowing the associated rights
    """
    request = kw['request']
    project_types = ProjectType.query_for_select()

    values = []
    for project_type in project_types:
        if not project_type.private or \
                request.has_permission('add.%s' % project_type.name):
            values.append((project_type.id, project_type.label))
    return deform.widget.RadioChoiceWidget(values=values)


@colander.deferred
def deferred_subproject_type_widget(node, kw):
    """
    Build a SubProjectType checkbox list widget on bind

    Only show active subprojecttypes than can be associated to the current's
    project type
    """
    request = kw['request']
    ptype_id = request.context.project_type_id

    subproject_types_query = SubProjectType.query_for_select()
    subproject_types_query.filter(
        SubProjectType.other_project_types.any(
            ProjectType.id == ptype_id
        )
    )

    values = []
    for subproject_type in subproject_types_query:
        if not subproject_type.private or \
                request.has_permission('add.%s' % subproject_type.name):
            values.append((subproject_type.id, subproject_type.label))

    return deform.widget.CheckboxChoiceWidget(values=values)


def _customize_project_schema(schema):
    """
    Customize the project schema to add widgets/validators ...

    :param obj schema: a colander.SchemaNode instance
    """
    if 'starting_date' in schema:
        schema.validator = check_begin_end_date

    customize = functools.partial(forms.customize_field, schema)
    if 'name 'in schema:
        customize('name', missing=colander.required, title=u"Nom du projet")

    if 'project_type_id' in schema:
        customize(
            'project_type_id',
            title=u"Type de projet",
            widget=deferred_project_type_widget,
            default=deferred_default_project_type,
            missing=colander.required,
        )

    if 'subtypes' in schema:
        customize(
            "subtypes",
            title=u"Types d'affaires",
            description=u"Le type d'affaire qui peut être mené dans ce projet",
            missing=colander.drop,
            children=[forms.get_sequence_child_item_id_node(SubProjectType)],
            widget=deferred_subproject_type_widget
        )

    return schema


def _add_customer_node_to_schema(schema):
    """
    Build a custom customer selection node and add it to the schema

    :param obj schema: a colander.SchemaNode instance
    """
    # Add a custom node to be able to associate existing customers
    customer_id_node = get_customer_select_node(name="un client")
    customer_id_node.objectify = customer_objectify
    customer_id_node.dictify = customer_dictify

    schema.add(
        colander.SchemaNode(
            colander.Sequence(),
            customer_id_node,
            widget=deform.widget.SequenceWidget(min_len=1),
            title=u"Clients",
            name='customers'
        )
    )
    return schema


def get_add_project_schema():
    """
    Build a schema for project add
    """
    schema = SQLAlchemySchemaNode(Project, includes=("name", 'project_type_id'))
    _customize_project_schema(schema)
    _add_customer_node_to_schema(schema)
    return schema


def get_add_step2_project_schema():
    """
    Build a schema for the second step of project add
    """
    schema = SQLAlchemySchemaNode(
        Project,
        includes=(
            'code',
            'description',
            'definition',
            'starting_date',
            'ending_date',
            'subtypes',
        ),
    )
    _customize_project_schema(schema)
    return schema


def get_edit_project_schema():
    """
    Return the project Edition/add form schema
    """
    excludes = (
        "_acl", "id", "company_id", "archived", "customers",
        "invoices", "tasks", "estimations", "cancelinvoices",
        "project_type_id", "project_type", "subtypes",
    )
    schema = SQLAlchemySchemaNode(Project, excludes=excludes)
    _customize_project_schema(schema)
    _add_customer_node_to_schema(schema)
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
