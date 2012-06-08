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
    add_menu : add a menu to the returned datas at BeforeRender
               if the company id is set
"""

from pyramid.url import route_path
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from pyramid.threadlocal import get_current_request

from autonomie.i18n import translate

@subscriber(BeforeRender)
def add_menu(event):
    """
        Add the menu to the returned datas (before rendering)
        if cid is not None
    """
    request = event['req']
    cid = None
    # We test matchdict is present : it's not when inner render call is made
    if hasattr(request, "context") and hasattr(request.context, "get_company_id"):
        cid = request.context.get_company_id()
    elif hasattr(request, "user") and request.user:
        if len(request.user.companies):
            cid = request.user.companies[0].id
    menu = {}
    if cid:
        menu = [dict(label=u'Clients',
                     url=route_path('company_clients',
                                                request,
                                                id=cid)),
                dict(label=u"Projets",
                     url=route_path('company_projects',
                                                request,
                                                id=cid)),
                dict(label=u"Factures",
                     url=route_path('company_invoices',
                                    request,
                                    id=cid)),
                dict(label=u"Trésorerie",
                    url=route_path('company_treasury',
                                    request,
                                    id=cid)),
                dict(label=u"Paramètres",
                     url=route_path('company',
                                                request,
                                                id=cid,
                                                _query={'edit':True})),
               ]
        event.update({'menu':menu})

@subscriber(BeforeRender)
def add_renderer_globals(event):
    """
        Add some global functions to allow translation in mako templates
    """
    request = event['req']
    if not request:
        request = get_current_request()
    event['_'] = request.translate

@subscriber(NewRequest)
def add_localizer(event):
    """
        Add some translation tool to the request object
    """
    request = event.request
    request.translate = translate
