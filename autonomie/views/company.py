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
    Views related to the Company model

    Permissions :
        admin_company : disable/enable add/remove employees
        view_company : view all informations concerning the company
        edit_company : edit company options

    A - Des permissions à définir sur l'ensemble de l'application
    B - Des groupes génériques qui rassemblent des permissions
    C - Des permissions spécifiques à certains users
    D - Des permissions par objets
"""

import logging
import colander

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound

from autonomie.models.company import (
    Company,
    CompanyActivity,
)
from autonomie.models.user.user import User
from autonomie.utils.widgets import (
    ViewLink,
    Link,
)
from autonomie.forms import (
    merge_session_with_post,
)
from autonomie.views import (
    BaseFormView,
    submit_btn,
    BaseListView,
    add_panel_view,
    DisableView,
)
from autonomie.views.render_api import format_account
from autonomie.forms.company import (
    COMPANYSCHEMA,
    CompanySchema,
    get_list_schema,
)


logger = logging.getLogger(__name__)


ENABLE_MSG = u"L'entreprise {0} a été (ré)activée."
DISABLE_MSG = u"L'entreprise {0} a été désactivée."

ENABLE_ERR_MSG = u"Erreur à l'activation de l'entreprise {0}."
DISABLE_ERR_MSG = u"Erreur à la désactivation de l'entreprise {0}."


def company_index(request):
    """
        index page for the company shows latest news :
            - last validated estimation/invoice
            - To be relaunched bill
    """
    company = request.context
    ret_val = dict(
        title=company.name.title(),
        company=company,
        elapsed_invoices=request.context.get_late_invoices()
    )
    return ret_val


def company_view(request):
    """
        Company main view
    """
    company = request.context
    populate_actionmenu(request)
    return dict(
        title=company.name.title(),
        company=company,
    )


class CompanyDisableView(DisableView):
    def on_disable(self):
        """
        Disable logins of users that are only attached to this company
        """
        for user in self.context.employees:
            other_enabled_companies = [
                company
                for company in user.companies
                if company.active and company.id != self.context.id
            ]
            if hasattr(user, 'login') and user.login.active and \
                    len(other_enabled_companies) == 0:
                user.login.active = False
                self.request.dbsession.merge(user.login)
                user_url = self.request.route_path(
                    '/users/{id}/login', id=user.id
                )
                self.request.session.flash(
                    u"Les identifiants de <a href='{0}'>{1}</a> ont été \
                    désactivés".format(user_url, user.label)
                )

    def redirect(self):
        return HTTPFound(self.request.referrer)


class CompanyList(BaseListView):
    title = u"Entreprises"
    schema = get_list_schema()
    sort_columns = dict(name=Company.name)
    default_sort = 'name'
    default_direction = 'asc'

    add_template_vars = (
        'title',
        'stream_actions',
    )

    def query(self):
        return Company.query(active=False)

    def filter_include_inactive(self, query, appstruct):
        include_inactive = appstruct.get('include_inactive', False)

        if include_inactive in ("false", False, colander.null):
            query = query.filter_by(active=True)

        return query

    def filter_search(self, query, appstruct):
        search = appstruct.get('search')
        if search:
            query = query.filter(Company.name.like('%' + search + '%'))
        return query

    def stream_actions(self, company):
        yield Link(
            self.request.route_path('company', id=company.id),
            u"Voir/Modifier",
            title=u"Voir/Modifier l'enseigne",
            icon='fa fa-pencil',
        )
        url = self.request.route_path(
            'company',
            id=company.id,
            _query=dict(action="disable")
        )
        if company.active:
            yield Link(
                url,
                u"Désactiver",
                title=u"Désactiver l'entreprise",
                icon='fa fa-book',
            )
        else:
            yield Link(
                url,
                u"Activer",
                title=u"Activer l'entreprise",
                icon='fa fa-book',
            )


def fetch_activities_objects(appstruct):
    """
    Fetch company activities in order to be able to associate them to the
    company
    """
    activities = appstruct.pop('activities', None)
    if activities:
        return [
            CompanyActivity.get(activity_id)
            for activity_id in activities
        ]
    return []


class CompanyAdd(BaseFormView):
    """
    View class for company add

    Have support for a user_id request param that allows to add the user
    directly on company creation

    """
    add_template_vars = ('title',)
    title = u"Ajouter une entreprise"
    schema = CompanySchema()
    buttons = (submit_btn,)

    def before(self, form):
        """
        prepopulate the form and the actionmenu
        """
        populate_actionmenu(self.request)
        if 'user_id' in self.request.params:
            appstruct = {"user_id": self.request.params['user_id']}

            come_from = self.request.referrer
            if come_from:
                appstruct['come_from'] = come_from

            form.set_appstruct(appstruct)

    def submit_success(self, appstruct):
        """
        Edit the database entry and return redirect
        """
        come_from = appstruct.pop('come_from', None)
        user_id = appstruct.get('user_id')
        company = Company()
        company.activities = fetch_activities_objects(appstruct)
        company = merge_session_with_post(company, appstruct)
        if user_id is not None:
            user_account = User.get(user_id)
            if user_account is not None:
                company.employees.append(user_account)

        self.dbsession.add(company)
        self.dbsession.flush()
        message = u"L'entreprise '{0}' a bien été ajoutée".format(company.name)
        self.session.flash(message)

        if come_from is not None:
            return HTTPFound(come_from)
        else:
            return HTTPFound(self.request.route_path("company", id=company.id))


class CompanyEdit(BaseFormView):
    """
        View class for company editing
    """
    add_template_vars = ('title',)
    schema = COMPANYSCHEMA
    buttons = (submit_btn,)

    @reify
    def title(self):
        """
            title property
        """
        return u"Modification de {0}".format(self.request.context.name.title())

    def before(self, form):
        """
            prepopulate the form and the actionmenu
        """
        appstruct = self.request.context.appstruct()
        appstruct['activities'] = [
            a.id for a in self.request.context.activities
        ]

        for filetype in ('logo', 'header'):
            # On récupère un éventuel id de fichier
            file_id = appstruct.pop('%s_id' % filetype, '')
            if file_id:
                # Si il y a déjà un fichier de ce type dans la base on construit
                # un appstruct avec un uid, un filename et une url de preview
                appstruct[filetype] = {
                    'uid': file_id,
                    'filename': '%s.png' % file_id,
                    'preview_url': self.request.route_path(
                        'filepng',
                        id=file_id,
                    )
                }

        form.set_appstruct(appstruct)
        populate_actionmenu(self.request, self.request.context)

    def submit_success(self, appstruct):
        """
        Edit the database entry and return redirect
        """
        self.request.context.activities = fetch_activities_objects(appstruct)
        company = merge_session_with_post(self.request.context, appstruct)
        company = self.dbsession.merge(company)
        self.dbsession.flush()
        message = u"Votre entreprise a bien été modifiée"
        self.session.flash(message)
        # Clear all informations stored in session by the tempstore used for the
        # file upload widget
        self.request.session.pop('substanced.tempstore')
        self.request.session.changed()
        return HTTPFound(self.request.route_path("company", id=company.id))


def populate_actionmenu(request, company=None):
    """
        add item in the action menu
    """
    request.actionmenu.add(get_list_view_btn())
    if company is not None:
        request.actionmenu.add(get_view_btn(company.id))


def get_list_view_btn():
    """
        Return a link to the CAE's directory
    """
    return ViewLink(u"Annuaire", "visit", path="/users")


def get_view_btn(company_id):
    """
        Return a link to the view page
    """
    return ViewLink(u"Voir", "visit", path="company", id=company_id)


def company_remove_employee_view(context, request):
    """
    Enlève un employé de l'entreprise courante
    """
    uid = request.params.get('uid')
    if not uid:
        request.session.flash('Missing uid parameter', 'error')
    user = User.get(uid)
    if not user:
        request.session.flash('User not found', 'error')

    if user in context.employees:
        context.employees = [
            employee for employee in context.employees if employee != user
        ]
        request.session.flash(
            u"L'utilisateur {0} ne fait plus partie de l'entreprise {1}".format(
                format_account(user), context.name)
        )
    url = request.referer
    if url is None:
        url = request.route_path('company', id=context.id)
    return HTTPFound(url)


def add_routes(config):
    """
    Configure routes for this module
    """
    config.add_route(
        'companies',
        "/companies",
    )
    config.add_route(
        'company',
        '/companies/{id:\d+}',
        traverse='/companies/{id}'
    )
    return config


def includeme(config):
    """
        Add all company related views
    """
    config = add_routes(config)
    config.add_view(
        CompanyList,
        route_name='companies',
        renderer='companies.mako',
        permission='admin_companies',
    )
    config.add_view(
        CompanyAdd,
        route_name='companies',
        renderer="base/formpage.mako",
        request_param="action=add",
        permission="admin_companies",
    )
    config.add_view(
        company_index,
        route_name='company',
        renderer='company_index.mako',
        request_param='action=index',
        permission='view_company',
    )
    config.add_view(
        company_view,
        route_name='company',
        renderer='company.mako',
        permission="visit",
    )
    config.add_view(
        CompanyEdit,
        route_name='company',
        renderer='base/formpage.mako',
        request_param='action=edit',
        permission="edit_company",
    )
    config.add_view(
        CompanyDisableView,
        route_name='company',
        request_param='action=disable',
        permission="admin_company",
    )
    config.add_view(
        company_remove_employee_view,
        route_name="company",
        request_param='action=remove',
        permission="admin_company",
    )
    # same panel as html view
    for panel, request_param in (
            ('company_tasks', 'action=tasks_html',),
            ('company_events', 'action=events_html',),
            ):
        add_panel_view(
            config,
            panel,
            route_name='company',
            request_param=request_param,
            permission="view_company",
        )
