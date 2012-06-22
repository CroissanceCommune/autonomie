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

from webhelpers.html import tags

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from pyramid.threadlocal import get_current_request

from autonomie.i18n import translate
from autonomie.models.model import Company
from autonomie.models.main import get_companies as get_all_companies
from autonomie.utils.widgets import Menu
from autonomie.utils.widgets import MainMenuItem
from autonomie.utils.widgets import MenuDropDown
from autonomie.utils.widgets import StaticWidget

def get_cid(request):
    """
        Return the current cid from the request
    """
    cid = None
    if hasattr(request, "user") and request.user and \
                            request.user.companies == 1:
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
        dbsession = request.dbsession()
        companies = get_all_companies(dbsession)
    else:
        companies = request.user.companies
    return companies

def get_company(request, cid):
    """
        Return the current company object
    """
    dbsession = request.dbsession()
    company = dbsession.query(Company).filter(Company.id==cid).first()
    return company

def get_user_menu(cid, css=None):
    """
        Return the menu for a common user
    """
    menu = None
    if cid:
        menu = Menu("base/mainmenu.mako", css=css)
        menu.add(MainMenuItem(u"Clients", "edit",
                                path="company_clients", id=cid))
        menu.add(MainMenuItem(u"Projets", "edit",
                                path="company_projects", id=cid))
        gestion = MenuDropDown(u"Gestion", "edit")
        gestion.add(MainMenuItem(u"Factures", "edit",
                                path="company_invoices", id=cid))
        gestion.add(MainMenuItem(u"Trésorerie", "edit",
                                path="company_treasury", id=cid))
        menu.add(gestion)
        menu.add(MainMenuItem(u"Paramètres", "edit",
                                path="company", id=cid))
    return menu

def get_admin_menus(cid):
    """
        Return the menu for admin or managers
    """
    menu = Menu("base/mainmenu.mako")
    menu.add(MainMenuItem(u"Factures", "manage", path="invoices"))
    menu.add(MainMenuItem(u"Configuration", "admin", path="admin_index"))
    submenu = get_user_menu(cid, "nav-pills")
    return menu, submenu

def company_menu(request, companies, cid):
    """
        Add the company choose menu
    """
    menu = get_company( request, cid ).name
    if len(companies) > 1:
        options = ((request.route_path("company", id=company.id),
                    company.name) for company in companies)
        default = request.route_path("company", id=cid)
        html_attrs = {'class':'floatted company-search',
                      'id':"company-select-menu"}
        menu = tags.select("companies", default, options, **html_attrs)
    menu = StaticWidget(menu, "view")
    return menu

@subscriber(BeforeRender)
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
        else:
            menu = get_user_menu(cid)
            companies = get_companies(request)
            menu.add(company_menu(request, companies, cid))

        menu.add(MainMenuItem(u"Annuaire", "view", path="users"))

        event.update({'menu':menu})
        if submenu:
            companies = get_companies(request)
            submenu.insert(company_menu(request, companies, cid))
            event.update({'submenu':submenu})

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
