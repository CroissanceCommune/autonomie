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


import colander
from deform import widget
from autonomie import forms


def get_customers_from_request(request):
    project = request.context.project
    company = project.company
    return company.customers


def get_customer_options(request):
    customers = get_customers_from_request(request)
    return [(cli.id, u"%s (%s)" % (cli.name, cli.code)) for cli in customers]


@colander.deferred
def deferred_customer_choice(node, kw):
    request = kw['request']
    customers = get_customer_options(request)
    return widget.SelectWidget(values=customers)


def get_current_customer_from_request(request):
    return request.context.customer


@colander.deferred
def deferred_default_customer(node, kw):
    request = kw['request']
    return get_current_customer_from_request(request).id


def get_project_options(request):
    customer = get_current_customer_from_request(request)
    return [(pro.id, u"%s (%s)" % (pro.name, pro.code))
            for pro in customer.projects]


@colander.deferred
def deferred_project_choice(node, kw):
    projects = get_project_options(kw['request'])
    return widget.SelectWidget(values=projects)


def get_current_project_from_request(request):
    return request.context.project


@colander.deferred
def deferred_default_project(node, kw):
    request = kw['request']
    return get_current_project_from_request(request).id


def get_phases_options(request):
    project = get_current_project_from_request(request)
    return [(phase.id, phase.name) for phase in project.phases]


@colander.deferred
def deferred_phase_choice(node, kw):
    phases = get_phases_options(kw['request'])
    return widget.SelectWidget(values=phases)


@colander.deferred
def deferred_default_phase(node, kw):
    request = kw['request']
    return request.context.phase.id


@colander.deferred
def deferred_customer_validator(node, kw):
    customers = get_customer_options(kw['request'])
    return colander.OneOf([cli[0] for cli in customers])


def get_all_projects(request):
    customers = get_customers_from_request(request)
    all_projects = []
    for customer in customers:
        for project in customer.projects:
            all_projects.append(project)
    return all_projects


@colander.deferred
def deferred_project_validator(node, kw):
    projects = get_all_projects(kw['request'])
    return colander.OneOf([p.id for p in projects])


def get_all_phases(request):
    customers = get_customers_from_request(request)
    all_phases = []
    for customer in customers:
        for project in customer.projects:
            all_phases.extend(project.phases)
    return all_phases


@colander.deferred
def deferred_phase_validator(node, kw):
    phases = get_all_phases(kw['request'])
    return colander.OneOf([p.id for p in phases])


class DuplicateSchema(colander.MappingSchema):
    """
        colander schema for duplication recording
    """
    customer = colander.SchemaNode(
        colander.Integer(),
        title=u"Client",
        widget=deferred_customer_choice,
        default=deferred_default_customer,
        validator=deferred_customer_validator)
    project = colander.SchemaNode(
        colander.Integer(),
        title=u"Projet",
        widget=deferred_project_choice,
        default=deferred_default_project,
        validator=deferred_project_validator)
    phase = colander.SchemaNode(
        colander.Integer(),
        title=u"Phase",
        widget=deferred_phase_choice,
        default=deferred_default_phase,
        validator=deferred_phase_validator)


class EditMetadataSchema(colander.MappingSchema):
    """
        Colander schema for moving a task from a phase to another
    """
    name = colander.SchemaNode(
        colander.String(),
        title=u"Libellé du document",
        validator=colander.Length(max=255),
        missing="",
        )
    date = forms.today_node(title=u"Date")
    phase_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Phase",
        widget=deferred_phase_choice,
        validator=deferred_phase_validator)


def remove_some_fields(schema, kw):
    request = kw['request']

    if len(request.context.project.phases) == 1:
        del(schema['phase_id'])

    if not request.has_permission('admin_task'):
        del(schema['date'])

    return schema


EDIT_METADATASCHEMA = EditMetadataSchema(after_bind=remove_some_fields)
