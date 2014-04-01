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

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from autonomie import resources
from autonomie.models.company import Company
from autonomie.utils.views import submit_btn
from autonomie.utils.widgets import ViewLink
from autonomie.views.forms import BaseFormView
from autonomie.views.forms import merge_session_with_post
from autonomie.views.forms.company import COMPANYSCHEMA


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
    link_list.append(ViewLink(u"Voir les clients",
            "manage", path="company_customers", id=company.id,
            icon='icon-arrow-right'
            ))
    link_list.append(ViewLink(u"Voir les projets",
            "manage", path="company_projects", id=company.id,
            icon='icon-arrow-right'
            ))
    link_list.append(ViewLink(u"Voir les factures",
            "manage", path="company_invoices", id=company.id,
            icon='icon-arrow-right'
            ))
    return dict(title=company.name.title(),
                company=company,
                link_list=link_list)


def company_enable(request, company=None):
    """
        Enable a company
    """
    if company is None:
        company = request.context
    if not company.enabled():
        try:
            company.enable()
            request.dbsession.merge(company)
            log.info(u"The company {0} has been enabled".\
                    format(company.name))
            message = u"L'entreprise {0} a été (ré)activée".\
                    format(company.name)
            request.session.flash(message)
        except:
            err_msg = u"Erreur à l'activation de l'entreprise {0}"\
                    .format(company.name)
            log.exception(err_msg)
            request.session.flash(err_msg, "error")
    if request.context.__name__ == 'company':
        return HTTPFound(request.route_path("users"))


class CompanyAdd(BaseFormView):
    """
        View class for company add
    """
    add_template_vars = ('title',)
    title = u"Ajouter une entreprise"
    schema = COMPANYSCHEMA
    buttons = (submit_btn,)

    def before(self, form):
        """
            prepopulate the form and the actionmenu
        """
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        """
            Edit the database entry and return reidrect
        """
        company = Company()
        company = merge_session_with_post(company, appstruct)
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
        return u"Édition de {0}".format(self.request.context.name.title())

    def before(self, form):
        """
            prepopulate the form and the actionmenu
        """
        appstruct = self.request.context.appstruct()
        form.set_appstruct(appstruct)
        populate_actionmenu(self.request, self.request.context)

    def submit_success(self, appstruct):
        """
            Edit the database entry and return reidrect
        """
        company = merge_session_with_post(self.request.context, appstruct)
        company = self.dbsession.merge(company)
        self.dbsession.flush()
        message = u"Votre entreprise a bien été éditée"
        self.session.flash(message)
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
    return ViewLink(u"Éditer", "edit", path="company", id=company_id,
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
    config.add_route('company', '/company/{id:\d+}', traverse='/companies/{id}')
    config.add_view(company_index,
                    route_name='company',
                    renderer='company_index.mako',
                    request_param='action=index',
                    permission='edit')
    config.add_view(company_view,
                    route_name='company',
                    renderer='company.mako',
                    permission="view")
    config.add_view(CompanyEdit,
                    route_name='company',
                    renderer='company_edit.mako',
                    request_param='action=edit',
                    permission="edit")
    config.add_view(company_enable,
                    route_name='company',
                    renderer='company_edit.mako',
                    request_param='action=enable',
                    permission="edit")
    # same panel as html view
    for panel, request_param in (
            ('company_tasks', 'action=tasks_html',),
            ('company_activities', 'action=activities_html',),
            ):
        config.add_view(make_panel_wrapper_view(panel),
                route_name='company',
                renderer="panel_wrapper.mako",
                request_param=request_param,
                permission="edit")
