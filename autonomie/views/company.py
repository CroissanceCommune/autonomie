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
    Views for the company handling
    Entry point for the main users
"""

import logging

from webhelpers.html.builder import HTML

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from autonomie.models.company import Company
from autonomie.models.user import User
from autonomie.utils.widgets import (
    ViewLink,
    StaticWidget,
)
from autonomie.views import (
    BaseFormView,
    submit_btn,
    merge_session_with_post,
    BaseListView,
)
from autonomie.forms.company import (
    COMPANYSCHEMA,
    CompanySchema,
    get_list_schema,
)


log = logging.getLogger(__name__)

def company_index(request):
    """
        index page for the company shows latest news :
            - last validated estimation/invoice
            - To be relaunched bill
    """
    company = request.context
    ret_val = dict(title=company.name.title(),
                company=company)
    all_invoices = []
    for project in company.projects:
        all_invoices.extend(project.invoices)


    # recovering elapsed invoices for warning
    elapsed_invoices = [invoice
                        for invoice in all_invoices if invoice.is_tolate()]
    elapsed_invoices = sorted(elapsed_invoices,
                              key=lambda a: a.taskDate,
                              reverse=True)
    ret_val['elapsed_invoices'] = elapsed_invoices
    return ret_val


def company_view(request):
    """
        Company main view
    """
    company = request.context
    populate_actionmenu(request, request.context)
    link_list = []
    link_list.append(
        ViewLink(
            u"Voir les clients",
            "manage",
            path="company_customers",
            id=company.id,
            icon='arrow-right'
        )
    )

    link_list.append(
        ViewLink(
            u"Voir les projets",
            "manage",
            path="company_projects",
            id=company.id,
            icon='arrow-right'
        )
    )

    link_list.append(
        ViewLink(
            u"Voir les factures",
            "manage",
            path="company_invoices",
            id=company.id,
            icon='arrow-right'
        )
    )

    link_list.append(
        ViewLink(
            u"Liste des rendez-vous",
            "manage",
            path="company_activities",
            id=company.id,
            icon='arrow-right'
        )
    )

    link_list.append(
        ViewLink(
            u"Liste des ateliers",
            "manage",
            path="company_workshops",
            id=company.id,
            icon='arrow-right'
        )
    )

    return dict(title=company.name.title(),
                company=company,
                link_list=link_list)


ENABLE_MSG = u"L'entreprise {0} a été (ré)activée."
DISABLE_MSG = u"L'entreprise {0} a été désactivée."

ENABLE_ERR_MSG = u"Erreur à l'activation de l'entreprise {0}."
DISABLE_ERR_MSG = u"Erreur à la désactivation de l'entreprise {0}."


def company_toggle_active(request, company, msg, err_msg, action):
    """
    Toggle compay enabled/disabled
    """
    if company is None:
        company = request.context

    try:
        getattr(company, action)()
        request.dbsession.merge(company)
        message = msg.format(company.name)
        log.info(message)
        request.session.flash(message)
        request.session.flash(message)
    except:
        err_message = err_msg.format(company.name)
        log.exception(err_message)
        request.session.flash(err_message, "error")

    if request.context.__name__ != 'company':
        # We don't want to raise a redirect if the view code is called from
        # another view
        return
    else:
        come_from = request.referer
        return HTTPFound(come_from)


def company_disable(request, company=None):
    """
    Disable a company
    """
    msg = DISABLE_MSG
    err_msg = DISABLE_ERR_MSG
    action = "disable"
    return company_toggle_active(request, company, msg, err_msg, action)


def company_enable(request, company=None):
    """
    Ensable a company
    """
    msg = ENABLE_MSG
    err_msg = ENABLE_ERR_MSG
    action = "enable"
    return company_toggle_active(request, company, msg, err_msg, action)


class CompanyList(BaseListView):
    title = u"Entreprises"
    schema = get_list_schema()
    sort_columns = dict(name=Company.name)
    default_sort = 'name'
    default_direction = 'asc'

    def query(self):
        return Company.query(active=False)

    def filter_active(self, query, appstruct):
        active = appstruct['active']
        return query.filter(Company.active == active)

    def filter_search(self, query, appstruct):
        search = appstruct.get('search')
        if search:
            query = query.filter(Company.name.like('%' + search + '%'))
        return query

    def populate_actionmenu(self, appstruct):
        self.request.actionmenu.add(self._get_active_btn(appstruct))

    def _get_active_btn(self, appstruct):
        """
            return the show active button
        """
        active = appstruct['active']
        if active == 'N':
            url = self.request.current_route_path(_query=dict(active="Y"))
            link = HTML.a(u"Afficher les entreprises actives",  href=url)
        else:
            url = self.request.current_route_path(_query=dict(active="N"))
            link = HTML.a(u"Afficher les entreprises désactivées", href=url)
        return StaticWidget(link)

class CompanyAdd(BaseFormView):
    """
        View class for company add
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
            form.set_appstruct(dict(user_id=self.request.params['user_id']))

    def submit_success(self, appstruct):
        """
        Edit the database entry and return redirect
        """
        user_id = appstruct.get('user_id')
        company = Company()
        company = merge_session_with_post(company, appstruct)
        if user_id is not None:
            user_account = User.get(user_id)
            if user_account is not None:
                company.employees.append(user_account)
        self.dbsession.add(company)
        self.dbsession.flush()
        message = u"L'entreprise '{0}' a bien été ajoutée".format(company.name)
        self.session.flash(message)
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
        if has_permission('edit', request.context, request):
            request.actionmenu.add(get_edit_btn(company.id))
            if not company.enabled():
                request.actionmenu.add(get_enable_btn(company.id))


def get_list_view_btn():
    """
        Return a link to the CAE's directory
    """
    return ViewLink(u"Annuaire", "view", path="users")


def get_view_btn(company_id):
    """
        Return a link to the view page
    """
    return ViewLink(u"Voir", "view", path="company", id=company_id)


def get_edit_btn(company_id):
    """
        Return a link to the edition form
    """
    return ViewLink(u"Modifier", "edit", path="company", id=company_id,
                                            _query=dict(action="edit"))


def get_enable_btn(company_id):
    """
        Return a link to the edition form
    """
    return ViewLink(u"Activer", "edit", path="company", id=company_id,
                                            _query=dict(action="enable"))


def make_panel_wrapper_view(panel_name):
    """
        Return a view wrapping the given panel
    """
    def myview(request):
        """
            Return a panel name for our panel wrapper
        """
        return {'panel_name': panel_name }
    return myview


def includeme(config):
    """
        Add all company related views
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
    config.add_view(
        CompanyList,
        route_name='companies',
        renderer='companies.mako',
        permission='manage',
    )
    config.add_view(
        CompanyAdd,
        route_name='companies',
        renderer="base/formpage.mako",
        request_param="action=add",
        permission="manage",
    )
    config.add_view(
        company_index,
        route_name='company',
        renderer='company_index.mako',
        request_param='action=index',
        permission='edit',
    )
    config.add_view(
        company_view,
        route_name='company',
        renderer='company.mako',
        permission="view",
    )
    config.add_view(
        CompanyEdit,
        route_name='company',
        renderer='base/formpage.mako',
        request_param='action=edit',
        permission="edit",
    )
    config.add_view(
        company_enable,
        route_name='company',
        request_param='action=enable',
        permission="edit",
    )
    config.add_view(
        company_disable,
        route_name='company',
        request_param='action=disable',
        permission="edit",
    )
    # same panel as html view
    for panel, request_param in (
            ('company_tasks', 'action=tasks_html',),
            ('company_events', 'action=events_html',),
            ):
        config.add_view(
            make_panel_wrapper_view(panel),
            route_name='company',
            renderer="panel_wrapper.mako",
            request_param=request_param,
            permission="edit",
        )
