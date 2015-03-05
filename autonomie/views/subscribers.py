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
    Subscribers
    Add menus to the returned datas before rendering
    Add a translation stuff to the templating context
"""
import logging

from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from pyramid.threadlocal import get_current_request

from autonomie.i18n import translate
from autonomie.utils.widgets import ActionMenu
from autonomie.resources import main_group
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


def get_req_uri(request):
    """
        Return the requested uri
    """
    return request.path_url + request.query_string


def log_request(event):
    """
        Log each request
    """
    request = event.request
    method = request.method
    req_uri = get_req_uri(request)
    http_version = request.http_version
    referer = request.referer
    user_agent = request.user_agent
    log.info(u"####################  NEW REQUEST COMING #################")
    log.info(event.request)
    log.info(u"The current session")
    log.info(event.request.session)


def add_request_attributes(event):
    """
        Add usefull tools to the request object
        that may be used inside the views
    """
    request = event.request
    request.translate = translate
    request.actionmenu = ActionMenu()
    request.popups = {}


def add_main_js(event):
    """
        Add the main required javascript dependency
    """
    main_group.need()


def includeme(config):
    """
        Bind the subscribers to the pyramid events
    """
    for before in (add_translation, add_api, add_main_js):
        config.add_subscriber(before, BeforeRender)

    for new_req in (log_request, add_request_attributes):
        config.add_subscriber(new_req, NewRequest)
