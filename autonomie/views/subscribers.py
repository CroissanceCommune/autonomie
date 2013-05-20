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
from webhelpers.html import tags
from webhelpers.html import HTML

from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from pyramid.threadlocal import get_current_request

from autonomie.i18n import translate
from autonomie.models.company import Company
from autonomie.utils.widgets import Menu
from autonomie.utils.widgets import MainMenuItem
from autonomie.utils.widgets import MenuDropDown
from autonomie.utils.widgets import StaticWidget
from autonomie.utils.widgets import ActionMenu
from autonomie.resources import main_js
from autonomie.views.render_api import api

log = logging.getLogger(__name__)


def get_cid(request):
    """
        Return the current cid from the request
    """
    cid = None
    if len(request.user.companies) == 1 and request.user.is_contractor():
        cid = request.user.companies[0].id
    elif hasattr(request, "context") and hasattr(request.context,
                                                "get_company_id"):
        cid = request.context.get_company_id()
    return cid


def get_companies(request):
    """
        Return available companies from the request object
    """
    companies = []
    if request.user.is_admin() or request.user.is_manager():
        companies = Company.query().all()
    else:
        companies = request.user.companies
    return companies


def get_company(request, cid):
    """
        Return the current company object
    """
    if not hasattr(request, "_company"):
        company = Company.get(cid)
        request._company = company
    return request._company


def get_user_menu(cid, css=None):
    """
        Return the menu for a common user
    """
    menu = None
    if cid:
        menu = Menu("base/mainmenu.mako", css=css)
        menu.add(MainMenuItem(u"Clients", "view",
            icon="icon-white icon-user",
            path="company_clients",
            id=cid))
        menu.add(MainMenuItem(u"Projets", "view",
            icon="icon-white icon-folder-open",
            path="company_projects",
            id=cid))
        gestion = MenuDropDown(u"Gestion", "view")
        gestion.add(MainMenuItem(u"Factures", "view",
            icon="icon-list-alt",
            path="company_invoices",
            id=cid))
#        gestion.add(MainMenuItem(u"Trésorerie", "view",
#            icon="icon-info-sign",
#            path="treasury",
#            id=cid))
#        gestion.add(MainMenuItem(u"Compte de résultat", "view",
#            icon="icon-info-sign",
#            path="incomestatement",
#            id=cid))
#        gestion.add(MainMenuItem(u"Bulletin de salaire",
#            icon="icon-info-sign",
#            path="salarysheet",
#            id=cid))
        gestion.add(MainMenuItem(u"Gestion commerciale",
            icon="icon-list-alt",
            path="commercial_handling",
            id=cid))
        menu.add(gestion)
        params = MenuDropDown(u"Paramètres", "view")
        params.add(MainMenuItem(u"Paramètres", "view",
            icon="icon-cog",
                                path="company", id=cid))
        params.add(MainMenuItem(u"Notes de frais", "view",
            icon="icon-cog",
            path="company_expenses", id=cid))
        menu.add(params)
    return menu


def get_admin_menus(cid):
    """
        Return the menu for admin or managers
    """
    menu = Menu("base/mainmenu.mako")
    menu.add(MainMenuItem(u"Factures", "manage", path="invoices",
        icon="icon-white icon-list-alt"))
    menu.add(MainMenuItem(u"Congés", "manage", path="holidays",
        icon="icon-white icon-plane"
        ))
    menu.add(MainMenuItem(u"Configuration", "admin", path="admin_index",
        icon="icon-white icon-cog"))
    submenu = get_user_menu(cid, "nav-pills")
    return menu, submenu


def company_menu(request, companies, cid):
    """
        Add the company choose menu
    """
    menu = HTML.li(HTML.h2(get_company(request, cid).name))
    menu = MainMenuItem(
        get_company(request, cid).name, "view",
        path="company", id=cid, _query=dict(action="index")
    )
    if len(companies) > 1:
        if request.context.__name__ == 'company':
            options = ((request.current_route_path(id=company.id),
                    company.name) for company in companies)
            default = request.current_route_path(id=cid)
        else:
            options = ((request.route_path("company", id=company.id),
                    company.name) for company in companies)
            default = request.route_path("company", id=cid)
        html_attrs = {'class': 'floatted company-search',
                      'id': "company-select-menu"}
        menu = HTML.li(
                tags.select("companies", default, options, **html_attrs))
        menu = StaticWidget(menu, "view")
    return menu


def add_menu(event):
    """
        Add the menu to the returned datas (before rendering)
        if cid is not None
    """
    request = event['req']
    menu = None
    submenu = None
    if request and hasattr(request, 'user') and request.user:
        cid = get_cid(request)
        if request.user.is_admin() or request.user.is_manager():
            menu, submenu = get_admin_menus(cid)
        elif cid:
            menu = get_user_menu(cid)
            companies = get_companies(request)
            if len(companies) > 1:
                menu.insert(company_menu(request, companies, cid))

        if menu:
            menu.add(MainMenuItem(u"Annuaire", "view",
                        icon="icon-white icon-book", path="users"))
            event.update({'menu': menu})
        if submenu:
            companies = get_companies(request)
            submenu.insert(company_menu(request, companies, cid))
            event.update({'submenu': submenu})


def add_translation(event):
    """
        Add a translation func to the templating context
    """
    request = event['req']
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
    for before in (add_menu, add_translation, add_api, add_main_js):
        config.add_subscriber(before, BeforeRender)

    for new_req in (log_request, add_request_attributes):
        config.add_subscriber(new_req, NewRequest)
