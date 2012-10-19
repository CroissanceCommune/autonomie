# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 10-04-2012
# * Last Modified :
#
# * Project : autonomie
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


class ProjectSchema(colander.MappingSchema):
    """
        Schema for project
    """
    name = colander.SchemaNode(colander.String(),
            title=u"Nom du projet",
            validator=colander.Length(max=150), css_class='floatted')
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
    client_id = colander.SchemaNode(colander.Integer(),
                                    title=u"Client",
                                    widget=deferred_client_list)


class PhaseSchema(colander.MappingSchema):
    """
        Schema for phase
    """
    name = colander.SchemaNode(colander.String(),
                               validator=colander.Length(max=150))
phaseSchema = PhaseSchema()
