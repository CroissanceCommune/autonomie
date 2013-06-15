# -*- coding: utf-8 -*-
# * File Name : subscribers.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 27-03-2012
# * Last Modified :
#
# * Project :
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
from autonomie.resources import main_js
from autonomie.views.render_api import api

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
    log.info(u"method:'%s' - uri:'%s', http_version:'%s' -  referer:'%s' - \
agent:'%s'" % (method, req_uri, http_version, referer, user_agent))


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
    main_js.need()


def includeme(config):
    """
        Bind the subscribers to the pyramid events
    """
    for before in (add_translation, add_api, add_main_js):
        config.add_subscriber(before, BeforeRender)

    for new_req in (log_request, add_request_attributes):
        config.add_subscriber(new_req, NewRequest)
