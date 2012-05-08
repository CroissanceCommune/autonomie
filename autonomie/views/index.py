# -*- coding: utf-8 -*-
# * File Name : views.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : mar. 08 mai 2012 16:52:26 CEST
#
# * Project : autonomie
#
"""
    Index view
"""
import logging
from pyramid.view import view_config
from pyramid.url import route_path
from pyramid.httpexceptions import HTTPFound

#from autonomie.utils.main import JsVar

log = logging.getLogger(__name__)

#def menuitem(request, label, url, icon='', children=None):
#    """
#        returns a menu entry
#    """
#    if not icon:
#        icon = "icon.png"
#    icon = request.static_url("autonomie:static/{0}".format(icon))
#    return dict(label=label, icon=icon, url=url, children=children)
#
#def build_menu(request, companies):
#    """
#        Return the company choice menu
#    """
#    menudatas = list()
#    for indice, company in enumerate(companies):
#        url = "#submenu/{0}".format(indice)
#        children = build_submenu(request, company.IDCompany)
#        menudatas.append(menuitem(request, company.name, url,
#                                            children=children))
#    return menudatas
#
#def build_submenu(request, company_id):
#    """
#        Return the submenu for a given company
#    """
#    args = _query = {"company_id":company_id}
#    client_url = "#company/{0}/clients".format(company_id)
#    return [menuitem(request, 'Clients', client_url,
#                                          icon='client.png'
#                                          ),
#            menuitem(request, 'Devis/Facture', route_url('estimationlist',
#                                                request, _query=args),
#                                                icon='devis.png')
#               ]

@view_config(route_name='index', renderer='index.mako')
def index(request):
    """
        Index page
    """
    avatar = request.session['user']
    companies = avatar.companies
    if len(companies) == 1:
        company = companies[0]
        return HTTPFound(route_path('company', request, cid=company.id))
    else:
        for company in companies:
            company.url = route_path("company", request, cid=company.id)
            company.icon = request.static_url("autonomie:static/company.png")
        return dict(title=u"Bienvenue dans Autonomie",
                    companies=avatar.companies)


#@view_config(route_name='index', renderer='index.mako')
#def default_index(request):
#    """
#        Return only a title for the page
#    """
#    log.debug(authenticated_userid(request))
#    avatar = request.session['user']
#    companies = avatar.companies
#    menu = build_menu(request, companies)
#    return dict(title="Bienvenu dans Coopagest v2",
#                menus=JsVar(menu))
#
