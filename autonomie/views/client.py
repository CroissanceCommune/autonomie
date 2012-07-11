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

from autonomie.models.model import Client
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.widgets import ViewLink
from autonomie.utils.widgets import SearchForm
from autonomie.utils.views import submit_btn
from autonomie.views.forms import ClientSchema
from .base import ListView

log = logging.getLogger(__name__)
def get_client_form(edit=False, path=""):
    """
        Returns the client add/edit form
    """
    schema = ClientSchema().bind(edit=edit)
    form = Form(schema, actions=path, buttons=(submit_btn,))
    return form

class ClientView(ListView):
    """
        Client views
    """
    columns = ("code", "name", "contactLastName",)

    @view_config(route_name='company_clients', renderer='company_clients.mako',
                                               request_method='GET',
                                               permission='edit')
    def company_clients(self):
        """
            Return the list of all the clients
            The list is wrapped in a pagination tool
        """
        log.debug("Getting clients")
        search, sort, direction, current_page, items_per_page = \
                                                self._get_pagination_args()
        company = self.request.context
        # Request database
        clients = self._get_clients(company)
        clients = self._filter_clients(clients, search)
        clients = clients.order_by(sort + " " + direction).all()

        # Get pagination
        records = self._get_pagination(clients, current_page, items_per_page)
        # Get add form
        form = get_client_form(path=self.request.route_path('company_clients',
                                                id=company.id))

        self._set_actionmenu(company)

        return dict(title=u"Liste des clients",
                    clients=records,
                    company=company,
                    html_form=form.render(),
                    action_menu=self.actionmenu
                    )

    def _get_clients(self, company=None):
        """
            query clients against the database
        """
        toquery = (Client.id,
                   Client.contactLastName,
                   Client.contactFirstName,
                   Client.name)
        clients = self.dbsession.query(*toquery)
        if company is not None:
            clients = clients.filter(Client.id_company == company.id)
        return clients

    def _filter_clients(self, clients, search):
        """
            Return a filtered query
        """
        clients = clients.filter(or_(Client.name.like("%"+search+"%"),
                               Client.contactLastName.like("%"+search+"%")))
        return clients

    def _set_actionmenu(self, company, client=False, edit=False):
        """
            Set the current actionmenu
        """
        self.actionmenu.add(ViewLink(u"Liste des clients", "edit",
            path="company_clients", id=company.id))
        if edit:
            self.actionmenu.add(ViewLink(u"Voir", "view",
                path="client", id=client.id))
            self.actionmenu.add(ViewLink(u"Éditer", "edit",
             path="client", id=client.id, _query=dict(action="edit")))
        else:
            self.actionmenu.add(ViewLink(u"Ajouter un client", "add",
                js="$('#addform').dialog('open');"))
            self.actionmenu.add(SearchForm(u"Entreprise ou contact principal"))


    @view_config(route_name='company_clients', renderer='client.mako',\
                        request_method='POST', permission='edit')
    @view_config(route_name='client', renderer='client.mako',\
                                request_param='action=edit', permission='edit')
    def client(self):
        """
            Return :
            * the client editform
            or
            * the client addform when an error has occured
        """
        if self.request.context.__name__ == 'company':
            company = self.request.context
            client = Client()
            client.id_company = company.id
            edit = False
            title = u"Ajout d'un nouveau client"
        else:
            client = self.request.context
            company = client.company
            edit = True
            title = u"Édition du client : {0}".format(client.name)

        self._set_actionmenu(company, client, edit)

        form = get_client_form(edit=edit)
        if 'submit' in self.request.params:
            # form POSTed
            datas = self.request.params.items()
            try:
                app_datas = form.validate(datas)
            except ValidationFailure, errform:
                html_form = errform.render()
            else:
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

    @view_config(route_name='client', renderer='client_view.mako', \
                            request_method='GET', permission='view')
    def client_view(self):
        """
            Return the view of a client
        """
        client = self.request.context
        self._set_actionmenu(client.company, client, edit=True)
        return dict(title=u"Client : {0}".format(client.name),
                    client=client,
                    company=client.company,
                    action_menu=self.actionmenu
                    )
