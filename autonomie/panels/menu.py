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
from __future__ import unicode_literals

"""
    Panels for the top main menus

    A common user has his company menu with customers, projects ...
    A manager or an admin has an admin menu and eventually a usermenu if he's
    consulting a companyr's account

    each user has his own menu with preferences, logout, holidays declaration
"""
import logging

from sqlalchemy import or_
from webhelpers.html import tags
from webhelpers.html import HTML

from autonomie.models.company import Company


logger = logging.getLogger(__name__)


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


def get_companies(request, cid):
    """
    Retrieve the companies the current user has access to

    :param obj request: The current pyramid request
    :param int cid: The current company id
    :returns: The list of companies
    :rtype: list
    """
    companies = []
    if request.has_permission('manage'):
        companies = Company.label_query().filter(
            or_(
                Company.active == True,
                Company.id == cid
            )
        ).all()
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


def _get_company_gestion_dropdown(request, cid):
    """
    Build and Return the 'Gestion' dropdown

    :param obj request: The request object
    :param int cid: The company id
    :returns: A DropDown
    :rtype: obj
    """
    gestion = DropDown(label="Gestion")

    href = request.route_path("company_estimations", id=cid)
    gestion.add_item("Devis", icon="fa fa-file-o", href=href)

    href = request.route_path("company_invoices", id=cid)
    gestion.add_item("Factures", icon="fa fa-file", href=href)

    href = request.route_path("company_expenses", id=cid)
    gestion.add_item("Notes de dépense", icon="fa fa-credit-card", href=href)

    href = request.route_path("commercial_handling", id=cid)
    gestion.add_item(
        "Gestion commerciale",
        icon="fa fa-line-chart",
        href=href
    )
    href = request.route_path(
        "/companies/{id}/accounting/treasury_measure_grids",
        id=cid
    )
    gestion.add_item(
        "État de trésorerie",
        icon="fa fa-money",
        href=href
    )

    href = request.route_path(
        "/companies/{id}/accounting/income_statement_measure_grids",
        id=cid
    )
    gestion.add_item(
        "Compte de résultat",
        icon="fa fa-table",
        href=href
    )

    if request.has_permission('add.training'):
        from autonomie.views.training.routes import TRAINING_DASHBOARD_URL
        href = request.route_path(TRAINING_DASHBOARD_URL, id=cid)
        gestion.add_item("Formation", icon="fa fa-graduation-cap", href=href)

    return gestion


def _get_company_accounting_documents_dropdown(request, cid):
    """
    Build the treasury related dropdown

    :param obj request: The request object
    :param int cid: The company id
    :returns: A DropDown
    :rtype: obj
    """
    docs = DropDown(label="Documents")

    href = request.route_path("treasury", id=cid)
    docs.add_item("Trésorerie", icon="fa fa-bank", href=href)

    href = request.route_path("incomestatement", id=cid)
    docs.add_item(
        "Compte de résultat",
        icon="fa fa-eur",
        href=href
    )

    href = request.route_path("salarysheet", id=cid)
    docs.add_item(
        "Bulletin de salaire",
        icon="fa fa-file-text-o",
        href=href
    )

    # C'est un entrepreneur
    if request.user.has_userdatas():
        href = request.route_path(
            '/users/{id}/userdatas/mydocuments',
            id=request.user.id
        )
        docs.add_item("Mes documents", icon='fa fa-folder-open', href=href)

    return docs


def _get_company_accompagnement_dropdown(request, cid):
    """
    Build the Accompagnement dropdown menu

    :param obj request: The request object
    :param int cid: The company id
    :returns: A DropDown
    :rtype: obj
    """
    accompagnement = DropDown(label="Accompagnement")

    href = request.route_path("company_activities", id=cid)
    accompagnement.add_item("Rendez-vous", icon="fa fa-calendar", href=href)

    href = request.route_path("company_workshops", id=cid)
    accompagnement.add_item("Ateliers", icon="fa fa-slideshare", href=href)

    href = request.route_path('user_competences', id=request.user.id)
    accompagnement.add_item("Compétences", href=href, icon="fa fa-star")
    return accompagnement


def _get_company_param_dropdown(request, cid):
    """
    Build the param dropdown

    :param obj request: The Pyramid request object
    :param int cid: The current company id
    :returns: A DropDown
    :rtype: obj
    """
    params = DropDown(label="Paramètres")

    href = request.route_path("company", id=cid)
    params.add_item("Paramètres", icon="fa fa-cogs", href=href)

    href = request.route_path("sale_categories", id=cid)
    params.add_item("Catalogue produits", icon="fa fa-book", href=href)
    return params


def get_company_menu(request, cid, css=None):
    """
    Build the Company related menu
    """
    menu = Menu(css=css)
    href = request.route_path("company_customers", id=cid)
    menu.add_item("Clients", icon="fa fa-users", href=href)

    from autonomie.views.project.routes import COMPANY_PROJECTS_ROUTE
    href = request.route_path(COMPANY_PROJECTS_ROUTE, id=cid)
    menu.add_item("Projets", icon="fa fa-folder-open-o", href=href)
    menu.add(_get_company_gestion_dropdown(request, cid))
    menu.add(_get_company_accounting_documents_dropdown(request, cid))
    menu.add(_get_company_accompagnement_dropdown(request, cid))
    menu.add(_get_company_param_dropdown(request, cid))
    return menu


def get_admin_menus(request):
    """
        Build the admin menu
    """
    menu = Menu()

    if request.has_permission("admin"):
        href = request.route_path("/admin")
        menu.add_item("Configuration", icon="fa fa-cogs", href=href)

    documents = DropDown(label="Documents")

    href = request.route_path("invoices")
    documents.add_item("Factures", icon="fa fa-list", href=href)

    href = request.route_path('expenses')
    documents.add_item('Notes de dépense', icon='fa fa-list', href=href)

    href = request.route_path("estimations")
    documents.add_item("Devis", icon="fa fa-list", href=href)

    menu.add(documents)

    if request.has_permission("admin_treasury"):
        treasury = DropDown(label="Comptabilité")

        href = request.route_path("/export/treasury/invoices")
        treasury.add_item(
            "Export des factures",
            icon="fa fa-edit",
            href=href
        )

        href = request.route_path("/export/treasury/expenses")
        treasury.add_item(
            "Export des notes de dépense",
            icon="fa fa-credit-card",
            href=href
        )

        href = request.route_path("/export/treasury/payments")
        treasury.add_item(
            "Export des encaissements",
            icon="fa fa-bank",
            href=href
        )

        href = request.route_path("/export/treasury/expense_payments")
        treasury.add_item(
            "Export des paiements de notes de dépense",
            icon="fa fa-bank",
            href=href
        )

        href = request.route_path("admin_treasury_all")
        treasury.add_item(
            "Bulletins de salaire",
            icon="fa fa-send-o",
            href=href
        )

        href = request.route_path("/accounting/operation_uploads")
        treasury.add_item(
            "Fichiers comptables déposés",
            icon="fa fa-money",
            href=href
        )

        menu.add(treasury)

    accompagnement = DropDown(label="Accompagnement")

    href = request.route_path('activities')
    accompagnement.add_item("Rendez-vous", href=href, icon="fa fa-calendar")

    href = request.route_path('workshops')
    accompagnement.add_item("Ateliers", href=href, icon="fa fa-slideshare")

    href = request.route_path('competences')
    accompagnement.add_item("Compétences", href=href, icon="fa fa-star")

    menu.add(accompagnement)

    gestion_sociale = DropDown(label="Gestion sociale")
    href = request.route_path('/userdatas')
    gestion_sociale.add_item("Consulter", href=href, icon="fa fa-users")

    href = request.route_path('statistics')
    gestion_sociale.add_item(
        "Statistiques",
        href=href,
        icon="fa fa-line-chart",
    )

    menu.add(gestion_sociale)

    if request.has_permission('admin_trainings'):
        formation = DropDown(label="Formations")
        href = request.route_path('/trainings')
        formation.add_item("Formations", href=href, icon="fa fa-list")
        href = request.route_path("/trainers")
        formation.add_item(
            "Annuaire des formateurs",
            icon="fa fa-graduation-cap",
            href=href
        )
        menu.add(formation)

    href = request.route_path("holidays")
    menu.add_item("Congés", icon="fa fa-space-shuttle", href=href)

    annuaire = DropDown(label="Annuaires")
    href = request.route_path("/users")
    annuaire.add_item("Utilisateurs", icon="fa fa-users", href=href)
    href = request.route_path("companies")
    annuaire.add_item("Entreprises", icon="fa fa-building", href=href)
    menu.add(annuaire)
    return menu


def company_choice(request, companies, cid):
    """
        Add the company choose menu
    """
    options = []
    for company in companies:
        if request.context.__name__ == 'company':
            url = request.current_route_path(id=company.id)
        else:
            url = request.route_path("company", id=company.id)

        name = company.name
        if not company.active:
            name += " (désactivée)"

        options.append((url, name))

    if request.context.__name__ == 'company':
        default = request.current_route_path(id=cid)
    else:
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
    menu.add_item("Mon compte", icon='fa fa-cog', href=href)

    href = request.route_path('user_holidays', id=request.user.id)
    menu.add_item("Mes congés", icon="fa fa-space-shuttle", href=href)

    href = request.route_path("logout")
    menu.add_item("Déconnexion", icon="fa fa-close", href=href)
    return menu


def menu_panel(context, request):
    """
        Top menu panel
    """
    logger.debug(" + Building the menu")
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
        companies = get_companies(request, cid)
        # If there is more than 1 company accessible for the current user, we
        # provide a usefull dropdown menu
        if len(companies) > 1:
            menu.insert(company_choice(request, companies, cid))

        href = request.route_path("/users")
        menu.add_item("Annuaire", icon="fa fa-book", href=href)
    logger.debug(" -> Menu built")
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
        companies = get_companies(request, cid)
        if len(companies) > 1:
            submenu.insert(company_choice(request, companies, cid))

    return {"submenu": submenu}


def admin_nav_panel(context, request):
    """
    A panel to render the navigation inside the administration interface
    """
    return dict(menus=context)


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
