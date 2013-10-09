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


def build_client_value(client=None):
    """
        return the tuple for building client select
    """
    if client:
        return (str(client.id), client.name)
    else:
        return ("0", u"Sélectionnez")


def build_client_values(clients):
    """
        Build human understandable client labels
        allowing efficient discrimination
    """
    options = [build_client_value()]
    options.extend([build_client_value(client)
                            for client in clients])
    return options

def get_clients_from_request(request):
    if request.context.__name__ == 'project':
        clients = request.context.company.clients
    elif request.context.__name__ == 'company':
        clients = request.context.clients
    else:
        clients = []
    return clients

@colander.deferred
def deferred_client_list(node, kw):
    request = kw['request']
    clients = get_clients_from_request(request)
    return deferred_autocomplete_widget(node,
                        {'choices':build_client_values(clients)})

@colander.deferred
def deferred_code_widget(node, kw):
    if kw['request'].context.__name__ == 'project':
        wid = DisabledInput()
    else:
        wid = widget.TextInputWidget(mask='****')
    return wid


@colander.deferred
def deferred_default_client(node, kw):
    """
        Return the client provided as request arg if there is one
    """
    request = kw['request']
    clients = get_clients_from_request(request)
    client = request.params.get('client')
    if client in [str(c.id) for c in clients]:
        return [int(client)]
    else:
        return colander.null


@colander.deferred
def deferred_client_validator(node, kw):
    request = kw['request']
    clients = get_clients_from_request(request)
    client_ids = [client.id for client in clients]
    def client_oneof(value):
        if value in ("0", 0):
            return u"Veuillez choisir un client"
        elif value not in client_ids:
            return u"Entrée invalide"
        return True
    return colander.Function(client_oneof)


class ClientSchema(colander.SequenceSchema):
    client_id = colander.SchemaNode(colander.Integer(),
            title=u"Client",
            widget=deferred_client_list,
            validator=deferred_client_validator)


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
    clients = ClientSchema(
            title=u"Clients",
            widget=widget.SequenceWidget(
                min_len=1,
                add_subitem_text_template=u"Ajouter un client"),
            default=deferred_default_client)


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
