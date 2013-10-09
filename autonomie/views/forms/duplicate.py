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

def get_clients_from_request(request):
    project = request.context.project
    company = project.company
    return company.clients


def get_client_options(request):
    clients = get_clients_from_request(request)
    return [(cli.id, u"%s (%s)" % (cli.name, cli.code)) for cli in clients]


@colander.deferred
def deferred_client_choice(node, kw):
    request = kw['request']
    clients = get_client_options(request)
    return widget.SelectWidget(values=clients)


def get_current_client_from_request(request):
    return request.context.client


@colander.deferred
def deferred_default_client(node, kw):
    request = kw['request']
    return get_current_client_from_request(request).id


def get_project_options(request):
    client = get_current_client_from_request(request)
    return [(pro.id, u"%s (%s)" % (pro.name, pro.code)) \
                                for pro in client.projects]


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
def deferred_client_validator(node, kw):
    clients = get_client_options(kw['request'])
    return colander.OneOf([cli[0] for cli in clients])


def get_all_projects(request):
    clients = get_clients_from_request(request)
    all_projects = []
    for client in clients:
        for project in client.projects:
            all_projects.append(project)
    return all_projects


@colander.deferred
def deferred_project_validator(node, kw):
    projects = get_all_projects(kw['request'])
    return colander.OneOf([p.id for p in projects])


def get_all_phases(request):
    clients = get_clients_from_request(request)
    all_phases = []
    for client in clients:
        for project in client.projects:
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
    client = colander.SchemaNode(
        colander.Integer(),
        title=u"Client",
        widget=deferred_client_choice,
        default=deferred_default_client,
        validator=deferred_client_validator)
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


class PhaseChangeSchema(colander.MappingSchema):
    """
        Colander schema for moving a task from a phase to another
    """
    phase = colander.SchemaNode(
        colander.Integer(),
        title=u"Phase",
        widget=deferred_phase_choice,
        default=deferred_default_phase,
        validator=deferred_phase_validator)
