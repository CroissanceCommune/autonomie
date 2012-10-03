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

from deform import ValidationFailure
from deform import Form

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from autonomie.models.client import Client
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.widgets import ViewLink
from autonomie.utils.widgets import SearchForm
from autonomie.utils.widgets import PopUp
from autonomie.utils.views import submit_btn
from autonomie.views.forms import ClientSchema
from .base import ListView

log = logging.getLogger(__name__)


def get_client_form(company, client=None):
    """
        Returns the client add/edit form
    """
    schema = ClientSchema().bind(company=company, client=client)
    form = Form(schema, buttons=(submit_btn,))
    return form


class ClientView(ListView):
    """
        Client views
    """
    columns = ("code", "name", "contactLastName",)

    def __init__(self, request):
        super(ClientView, self).__init__(request)
        self._set_actionmenu()

    def _set_actionmenu(self):
        """
            set the action menu
        """
        self.actionmenu.add(ViewLink(u"Liste des clients", "edit",
                                      path="company_clients",
                                      id=self.context.get_company_id()))

        if self.context.__name__ == 'client':
            self.actionmenu.add(self._get_view_button())
            if has_permission('edit', self.context, self.request):
                self.actionmenu.add(self._get_edit_button())

    @view_config(route_name='company_clients', renderer='company_clients.mako',
                                               request_method='GET',
                                               permission='edit')
    def company_clients(self):
        """
            Return the list of all the clients
            The list is wrapped in a pagination tool
        """
        search, sort, direction, current_page, items_per_page = \
                                                self._get_pagination_args()
        company = self.request.context
        # Request database
        clients = self._get_clients(company)
        clients = self._filter_clients(clients, search)
        clients = clients.order_by(sort + " " + direction).all()

        # Get pagination
        records = self._get_pagination(clients, current_page, items_per_page)

        # Add form
        if has_permission('add', self.context, self.request):
            form = get_client_form(company)
            popup = PopUp("addform", u'Ajouter un client', form.render())
            popups = {popup.name: popup}
            self.actionmenu.add(popup.open_btn())

        # Search form
        self.actionmenu.add(SearchForm(u"Entreprise ou contact principal"))

        return dict(title=u"Liste des clients",
                    clients=records,
                    company=company,
                    popups=popups,
                    action_menu=self.actionmenu
                    )

    def _get_clients(self, company=None):
        """
            query clients against the database
        """
        toquery = (Client.id,
                   Client.code,
                   Client.contactLastName,
                   Client.contactFirstName,
                   Client.name)
        clients = self.dbsession.query(*toquery)
        if company is not None:
            clients = clients.filter(Client.company_id == company.id)
        return clients

    def _filter_clients(self, clients, search):
        """
            Return a filtered query
        """
        clients = clients.filter(
            or_(Client.name.like("%" + search + "%"),
                Client.contactLastName.like("%" + search + "%")
            )
        )
        return clients

    @view_config(route_name='company_clients', renderer='client.mako',
                 request_method='POST', permission='edit')
    @view_config(route_name='client', renderer='client.mako',
                request_param='action=edit', permission='edit')
    def client(self):
        """
            Return :
            * the client editform
            or
            * the client addform when an error has occured
        """
        if self.request.context.__name__ == 'company':
            company = self.context
            client = Client()
            client.company_id = company.id
            edit = False
            title = u"Ajout d'un nouveau client"
            form = get_client_form(company)
        else:
            client = self.context
            company = client.company
            edit = True
            title = u"Édition du client : {0}".format(client.name)
            form = get_client_form(company, client)

        if 'submit' in self.request.params:
            # form POSTed
            datas = self.request.params.items()
            log.debug(u"Client form submission : {0}".format(datas))
            try:
                app_datas = form.validate(datas)
            except ValidationFailure, errform:
                html_form = errform.render()
            else:
                log.debug(u"Values are valid : {0}".format(app_datas))
                client = merge_session_with_post(client, app_datas)
                client = self.dbsession.merge(client)
                self.dbsession.flush()
                if edit:
                    message = u"Le client <b>{0}</b> a été édité avec \
succès".format(client.name)
                else:
                    #TODO : auto add a new project
                    message = u"Le client <b>{0}</b> a été ajouté avec \
succès".format(client.name)
                self.request.session.flash(message, queue='main')
                return HTTPFound(self.request.route_path('client',
                                            id=client.id))
        else:
            html_form = form.render(client.appstruct())
        return dict(title=title,
                    client=client,
                    html_form=html_form,
                    company=company,
                    action_menu=self.actionmenu)

    @view_config(route_name='client', renderer='client_view.mako',
                 request_method='GET', permission='view')
    def client_view(self):
        """
            Return the view of a client
        """
        return dict(title=u"Client : {0}".format(self.context.name),
                    client=self.context,
                    company=self.context.company,
                    action_menu=self.actionmenu
                    )

    def _get_view_button(self):
        """
            return a view button
        """
        return ViewLink(u"Voir", "view", path="client", id=self.context.id)

    def _get_edit_button(self):
        """
            Return an edit button
        """
        return ViewLink(u"Éditer", "edit", path="client", id=self.context.id,
                                            _query=dict(action="edit"))
