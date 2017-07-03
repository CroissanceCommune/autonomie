# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
    Before Render Subscribers

        + Add tools used in templating

        + Require the main_js js ressource

"""
import logging

from pyramid.events import BeforeRender
from pyramid.threadlocal import get_current_request

from autonomie.views.render_api import Api

log = logging.getLogger(__name__)


def add_translation(event):
    """
        Add a translation func to the templating context
    """
    request = event.get('req')
    if not request:
        request = get_current_request()
    event['_'] = request.translate


def add_api(event):
    """
        Add an api to the templating context
    """
    if event.get('renderer_name', '') != 'json':
        request = event['request']
        api = getattr(request, 'template_api', None)
        if api is None and request is not None:
            api = Api(event['context'], event['request'])
        event['api'] = api


def includeme(config):
    """
        Bind the subscribers to the pyramid events
    """
    for before in (add_translation, add_api):
        config.add_subscriber(before, BeforeRender)
