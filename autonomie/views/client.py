# -*- coding: utf-8 -*-
# * File Name : customer.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 28-03-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Client views
"""
import logging

from sqlalchemy import or_
from sqlalchemy.orm import undefer_group

from deform import Form

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from autonomie.models.client import Client
from autonomie.utils.widgets import ViewLink
from autonomie.utils.widgets import SearchForm
from autonomie.utils.widgets import PopUp
from autonomie.utils.views import submit_btn
from autonomie.views.forms.client import (
        CLIENTSCHEMA,
        ClientSearchSchema,
        )
from autonomie.views.forms import (
        BaseFormView,
        merge_session_with_post,
        )
from .base import (
        BaseListView,
        BaseCsvView,
        )

log = logging.getLogger(__name__)


def get_client_form(request):
    """
        Returns the client add/edit form
    """
    schema = CLIENTSCHEMA.bind(request=request)
    form = Form(schema, buttons=(submit_btn,))
    return form


class ClientsList(BaseListView):
    title = u"Liste des clients"
    schema = ClientSearchSchema()
    sort_columns = {'name':Client.name,
                    "code":Client.code,
                    "contactLastName":Client.contactLastName}

    def query(self):
        company = self.request.context
        return Client.query().filter(Client.company_id == company.id)

    def filter_name_or_contact(self, records, appstruct):
        search = appstruct['search']
        if search:
            records = records.filter(
                or_(Client.name.like("%" + search + "%"),
                    Client.contactLastName.like("%" + search + "%")))
        return records

    def populate_actionmenu(self, appstruct):
        populate_actionmenu(self.request)
        if has_permission('add', self.request.context, self.request):
            form = get_client_form(self.request)
            popup = PopUp("addform", u'Ajouter un client', form.render())
            self.request.popups = {popup.name: popup}
            self.request.actionmenu.add(popup.open_btn())
        searchform = SearchForm(u"Entreprise ou contact principal")
        searchform.set_defaults(appstruct)
        self.request.actionmenu.add(searchform)


class ClientsCsv(BaseCsvView):
    """
        Client csv view
    """
    model = Client

    @property
    def filename(self):
        return "clients.csv"

    def query(self):
        company = self.request.context
        return Client.query().options(undefer_group('edit'))\
                .filter(Client.company_id == company.id)


def client_view(request):
    """
        Return the view of a client
    """
    populate_actionmenu(request, request.context)
    return dict(title=u"Client : {0}".format(request.context.name),
                client=request.context)


class ClientAdd(BaseFormView):
    title = u"Ajouter un client"
    schema = CLIENTSCHEMA
    buttons = (submit_btn,)

    def before(self, form):
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        client = Client()
        client.company = self.request.context
        client = merge_session_with_post(client, appstruct)
        self.dbsession.add(client)
        self.dbsession.flush()
        message = u"Le client <b>{0}</b> a été ajouté avec succès".format(
                                                                client.name)
        self.session.flash(message)
        return HTTPFound(self.request.route_path('client', id=client.id))


class ClientEdit(BaseFormView):
    schema = CLIENTSCHEMA
    buttons = (submit_btn,)

    @reify
    def title(self):
        return u"Éditer le client '{0}'".format(self.request.context.name)

    def before(self, form):
        """
            prepopulate the form and the actionmenu
        """
        populate_actionmenu(self.request, self.request.context)

    def submit_success(self, appstruct):
        """
            Edit the database entry
        """
        client = merge_session_with_post(self.request.context, appstruct)
        client = self.dbsession.merge(client)
        self.dbsession.flush()
        message = u"Le client <b>{0}</b> a été édité avec succès".format(
                                                                client.name)
        self.session.flash(message)
        return HTTPFound(self.request.route_path('client', id=client.id))

    def appstruct(self):
        """
            Populate the form with the current edited context (client)
        """
        return self.request.context.appstruct()


def populate_actionmenu(request, client=None):
    """
        populate the actionmenu
    """
    company_id = request.context.get_company_id()
    request.actionmenu.add(get_list_view_btn(company_id))
    if client:
        request.actionmenu.add(get_view_btn(client.id))
        if has_permission('edit', request.context, request):
            request.actionmenu.add(get_edit_btn(client.id))

def get_list_view_btn(id_):
    return ViewLink(u"Liste des clients", "edit", path="company_clients",
                                                                    id=id_)

def get_view_btn(client_id):
    return ViewLink(u"Voir", "view", path="client", id=client_id)

def get_edit_btn(client_id):
    return ViewLink(u"Éditer", "edit", path="client", id=client_id,
                                        _query=dict(action="edit"))


def includeme(config):
    """
        Add module's views
    """
    config.add_route('client',
                     '/clients/{id}',
                     traverse='/clients/{id}')

    config.add_route('company_clients',
                     '/company/{id:\d+}/clients',
                     traverse='/companies/{id}')
    config.add_route('company_clients_csv',
                     '/company/{id:\d+}/clients.csv',
                     traverse='/companies/{id}')

    config.add_view(ClientAdd,
                    route_name='company_clients',
                    renderer='client.mako',
                    request_method='POST',
                    permission='edit')
    config.add_view(ClientAdd,
                    route_name='company_clients',
                    renderer='client.mako',
                    request_param='action=add',
                    permission='edit')
    config.add_view(ClientEdit,
                    route_name='client',
                    renderer='client.mako',
                    request_param='action=edit',
                    permission='edit')

    config.add_view(ClientsList,
                    route_name='company_clients',
                    renderer='company_clients.mako',
                    request_method='GET',
                    permission='edit')

    config.add_view(ClientsCsv,
                    route_name='company_clients_csv',
                    request_method='GET',
                    permission='edit')

    config.add_view(client_view,
                    route_name='client',
                    renderer='client_view.mako',
                    request_method='GET',
                    permission='view')
