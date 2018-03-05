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
    Panels for the top main menus

    A common user has his company menu with customers, projects ...
    A manager or an admin has an admin menu and eventually a usermenu if he's
    consulting a companyr's account

    each user has his own menu with preferences, logout, holidays declaration
"""
import logging

from webhelpers.html import tags
from webhelpers.html import HTML
from pyramid.security import has_permission

from autonomie.models.company import Company


log = logging.getLogger(__name__)


class Item(dict):
    """
        A single menu item

        {'label': the label to display,
         'icon': the icon,
         'href': the link}
    """
    __type__ = "item"

    def selected(self, request):
        href = self.get('href')

        if href in request.current_route_path():
            return True
        else:
            return False


class HtmlItem(dict):
    """
        A static html item that's used to carry html generated code
        {'html': the html code}
    """
    __type__ = 'static'


class Menu(dict):
    """
        A menu object
    """
    def __init__(self, css=None, **elements):
        dict.__init__(self, **elements)
        self.css = css
        self.items = []

    def add_item(self, label, icon="", href=""):
        """
            Usefull shortcut to add an item to the menu
        """
        self.add(Item(label=label, icon=icon, href=href))

    def add(self, element):
        """
            Add an element to the menu
        """
        self.items.append(element)

    def insert(self, element):
        """
            Insert an element at the begining of the menu
        """
        self.items.insert(0, element)

    def __nonzero__(self):
        return self.items != []


class DropDown(Menu):
    """
        A dropdown menu
    """
    __type__ = "dropdown"


def get_cid(request, submenu=False):
    """
        Extract the current company id from the request, if there is one

    :param obj request: the pyramid request
    :param bool submenu: Do we ask this for the submenu ?
    """
    cid = None
    if len(request.user.active_companies) == 1 and not submenu:
        cid = request.user.active_companies[0].id

    # The current context provide a get_company_id utility that allows to
    # retrieve the concerned company
    elif hasattr(request, "context"):
        if hasattr(request.context, "get_company_id"):
            cid = request.context.get_company_id()

    else:
        return request.user.active_companies[0].id

    return cid


def get_companies(request):
    """
        Retrieve the companies the current user has access to
    """
    companies = []
    if request.has_permission('manage'):
        companies = Company.query().all()
    else:
        companies = request.user.active_companies
    return companies


def get_company(request, cid):
    """
        Retrieve the current company object
    """
    if not hasattr(request, "_company"):
        company = Company.get(cid)
        request._company = company
    return request._company


def get_company_menu(request, cid, css=None):
    """
        Build the usermenu
    """
    menu = Menu(css=css)
    href = request.route_path("company_customers", id=cid)
    menu.add_item(u"Clients", icon="fa fa-users", href=href)

    href = request.route_path("company_projects", id=cid)
    menu.add_item(u"Projets", icon="fa fa-folder-open-o", href=href)

    # Gestion
    gestion = DropDown(label=u"Gestion")

    href = request.route_path("company_estimations", id=cid)
    gestion.add_item(u"Devis", icon="fa fa-file-o", href=href)

    href = request.route_path("company_invoices", id=cid)
    gestion.add_item(u"Factures", icon="fa fa-file", href=href)

    href = request.route_path("company_expenses", id=cid)
    gestion.add_item(u"Notes de dépense", icon="fa fa-credit-card", href=href)

    href = request.route_path("commercial_handling", id=cid)
    gestion.add_item(
        u"Gestion commerciale",
        icon="fa fa-line-chart",
        href=href
    )

    href = request.route_path(
        "/companies/{id}/accounting/treasury_measure_grids",
        id=cid
    )
    gestion.add_item(
        u"État de trésorerie",
        icon="fa fa-money",
        href=href
    )
    href = request.route_path(
        "/companies/{id}/accounting/income_statement_measure_grids",
        id=cid
    )
    gestion.add_item(
        u"Compte de résultat",
        icon="fa fa-table",
        href=href
    )

    menu.add(gestion)

    # Docs
    docs = DropDown(label=u"Documents")

    href = request.route_path("treasury", id=cid)
    docs.add_item(u"Trésorerie", icon="fa fa-bank", href=href)

    href = request.route_path("incomestatement", id=cid)
    docs.add_item(
        u"Compte de résultat",
        icon="fa fa-eur",
        href=href
    )

    href = request.route_path("salarysheet", id=cid)
    docs.add_item(
        u"Bulletin de salaire",
        icon="fa fa-file-text-o",
        href=href
    )

    # C'est un entrepreneur
    if request.user.has_userdatas():
        href = request.route_path(
            '/users/{id}/userdatas/mydocuments',
            id=request.user.id
        )
        docs.add_item(u"Mes documents", icon='fa fa-folder-open', href=href)

    menu.add(docs)

    # Accompagnement
    accompagnement = DropDown(label=u"Accompagnement")

    href = request.route_path("company_activities", id=cid)
    accompagnement.add_item(u"Rendez-vous", icon="fa fa-calendar", href=href)

    href = request.route_path("company_workshops", id=cid)
    accompagnement.add_item(u"Ateliers", icon="fa fa-slideshare", href=href)

    href = request.route_path('user_competences', id=request.user.id)
    accompagnement.add_item(u"Compétences", href=href, icon="fa fa-star")

    menu.add(accompagnement)

    # Params
    params = DropDown(label=u"Paramètres")

    href = request.route_path("company", id=cid)
    params.add_item(u"Paramètres", icon="fa fa-cogs", href=href)

    href = request.route_path("sale_categories", id=cid)
    params.add_item(u"Catalogue produits", icon="fa fa-book", href=href)

    menu.add(params)

    return menu


def get_admin_menus(request):
    """
        Build the admin menu
    """
    menu = Menu()

    if has_permission("admin", request.context, request):
        href = request.route_path("admin_index")
        menu.add_item(u"Configuration", icon="fa fa-cogs", href=href)

    documents = DropDown(label=u"Documents")

    href = request.route_path("invoices")
    documents.add_item(u"Factures", icon="fa fa-file", href=href)

    href = request.route_path('expenses')
    documents.add_item(u'Notes de dépense', icon='fa fa-file-o', href=href)

    href = request.route_path("estimations")
    documents.add_item(u"Devis", icon="fa fa-file-o", href=href)

    menu.add(documents)

    if has_permission("admin_treasury", request.context, request):
        treasury = DropDown(label=u"Comptabilité")

        href = request.route_path("/export/treasury/invoices")
        treasury.add_item(
            u"Export des factures",
            icon="fa fa-edit",
            href=href
        )

        href = request.route_path("/export/treasury/expenses")
        treasury.add_item(
            u"Export des notes de dépense",
            icon="fa fa-credit-card",
            href=href
        )

        href = request.route_path("/export/treasury/payments")
        treasury.add_item(
            u"Export des encaissements",
            icon="fa fa-bank",
            href=href
        )

        href = request.route_path("/export/treasury/expense_payments")
        treasury.add_item(
            u"Export des paiements de notes de dépense",
            icon="fa fa-bank",
            href=href
        )

        href = request.route_path("admin_treasury_all")
        treasury.add_item(
            u"Bulletins de salaire",
            icon="fa fa-send-o",
            href=href
        )

        href = request.route_path("/accounting/operation_uploads")
        treasury.add_item(
            u"Fichiers comptables déposés",
            icon="fa fa-money",
            href=href
        )

        menu.add(treasury)

    accompagnement = DropDown(label=u"Accompagnement")

    href = request.route_path('activities')
    accompagnement.add_item(u"Rendez-vous", href=href, icon="fa fa-calendar")

    href = request.route_path('workshops')
    accompagnement.add_item(u"Ateliers", href=href, icon="fa fa-slideshare")

    href = request.route_path('competences')
    accompagnement.add_item(u"Compétences", href=href, icon="fa fa-star")

    menu.add(accompagnement)

    gestion_sociale = DropDown(label=u"Gestion sociale")
    href = request.route_path('/userdatas')
    gestion_sociale.add_item(u"Consulter", href=href, icon="fa fa-users")

    href = request.route_path('statistics')
    gestion_sociale.add_item(
        u"Statistiques",
        href=href,
        icon="fa fa-line-chart",
    )

    menu.add(gestion_sociale)

    href = request.route_path("holidays")
    menu.add_item(u"Congés", icon="fa fa-space-shuttle", href=href)
    return menu


def company_choice(request, companies, cid):
    """
        Add the company choose menu
    """
    if request.context.__name__ == 'company':
        options = (
            (request.current_route_path(id=company.id),
             company.name) for company in companies
        )
        default = request.current_route_path(id=cid)
    else:
        options = (
            (request.route_path("company", id=company.id),
             company.name) for company in companies
        )
        default = request.route_path("company", id=cid)
    html_attrs = {
        'class': 'company-search',
        'id': "company-select-menu",
    }
    html_code = HTML.li(
        tags.select("companies", default, options, **html_attrs)
    )
    return HtmlItem(html=html_code)


def get_usermenu(request):
    """
        Return the user menu (My account, holidays ...)
    """
    menu = Menu()
    href = request.route_path(
        '/users/{id}',
        id=request.user.id,
    )
    menu.add_item(u"Mon compte", icon='fa fa-cog', href=href)

    href = request.route_path('user_holidays', id=request.user.id)
    menu.add_item(u"Mes congés", icon="fa fa-space-shuttle", href=href)

    href = request.route_path("logout")
    menu.add_item(u"Déconnexion", icon="fa fa-close", href=href)
    return menu


def menu_panel(context, request):
    """
        Top menu panel
    """
    log.debug(u"Entering the menu panel")
    # If we've no user in the current request, we don't return anything
    if not getattr(request, 'user'):
        return {}

    usermenu = get_usermenu(request)

    menu = None
    cid = get_cid(request)

    if request.has_permission('manage'):
        menu = get_admin_menus(request)

    elif cid:
        menu = get_company_menu(request, cid)
        companies = get_companies(request)
        # If there is more than 1 company accessible for the current user, we
        # provide a usefull dropdown menu
        if len(companies) > 1:
            menu.insert(company_choice(request, companies, cid))

    if menu is not None:
        href = request.route_path("/users")
        menu.add_item(u"Annuaire", icon="fa fa-book", href=href)

    return {
        'menu': menu,
        'usermenu': usermenu,
    }


def submenu_panel(context, request):
    """
        Submenu panel
    """
    # If we've no user in the current request, we don't return anything
    if not getattr(request, 'user'):
        return {}

    # There are no submenus for non admins
    if not request.has_permission('manage'):
        return {}

    cid = get_cid(request, submenu=True)
    if not cid:
        return {}

    submenu = get_company_menu(request, cid, "nav-pills")
    if submenu:
        companies = get_companies(request)
        if len(companies) > 1:
            submenu.insert(company_choice(request, companies, cid))

    return {"submenu": submenu}


def admin_nav_panel(context, request, menus):
    """
    A panel to render the navigation inside the administration interface
    """
    return dict(menus=menus)


def includeme(config):
    """
        Pyramid's inclusion mechanism
    """
    config.add_panel(
        menu_panel,
        'menu',
        renderer='/panels/menu.mako',
    )
    config.add_panel(
        submenu_panel,
        'submenu',
        renderer='/panels/menu.mako',
    )
    config.add_panel(
        admin_nav_panel,
        'admin_nav',
        renderer='/panels/admin_nav.mako',
    )
