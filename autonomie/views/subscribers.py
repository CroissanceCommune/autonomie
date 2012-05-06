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
    # We test matchdict is present : it's not when inner render call is made
    if hasattr(request, "matchdict"):
        cid = request.matchdict.get('cid')
    else:
        cid = None
    menu = {}
    if cid:
        menu = [dict(label=u'Clients',
                     url=route_path('company_clients',
                                                request,
                                                cid=cid)),
                dict(label=u"Projets",
                     url=route_path('company_projects',
                                                request,
                                                cid=cid)),
                dict(label=u"Factures",
                     url=route_path('company_invoices',
                                    request,
                                    cid=cid)),
                dict(label=u"Trésorerie",
                    url=route_path('company_treasury',
                                    request,
                                    cid=cid)),
                dict(label=u"Paramètres",
                     url=route_path('company',
                                                request,
                                                cid=cid,
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
