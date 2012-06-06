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

from deform import ValidationFailure
from deform import Form
from deform import Button

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_path

from autonomie.models.model import Client
from autonomie.utils.forms import merge_session_with_post
from autonomie.views.forms import ClientSchema
from .base import ListView

log = logging.getLogger(__name__)
def get_client_form(edit=False, path=""):
    """
        Returns the client add/edit form
    """
    schema = ClientSchema().bind(edit=edit)
    form = Form(schema, actions=path, buttons=(Button(name='submit',
                                        title=u'Validez',
                                        type='submit'),))
    return form

class ClientView(ListView):
    """
        Client views
    """
    columns = ("code", "name", "contactLastName",)

    @view_config(route_name='company_clients', renderer='company_clients.mako',
                                               request_method='GET',
                                               permission='view')
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
        clients = self._get_clients(company, search, sort, direction)

        # Get pagination
        records = self._get_pagination(clients, current_page, items_per_page)
        # Get add form
        form = get_client_form(path=route_path('company_clients', self.request,
                                                id=company.id))

        return dict(title=u"Liste des clients",
                    clients=records,
                    company=company,
                    html_form=form.render())

    def _get_clients(self, company, search, sort, direction):
        """
            query clients against the database
        """
        toquery = (Client.id,
                   Client.contactLastName,
                   Client.contactFirstName,
                   Client.name)
        if company is not None:
            clients = self.dbsession.query(*toquery).filter(
                    Client.name.like(search+"%"),
                    Client.id_company == company.id).order_by(sort \
                                                    + " " \
                                                    + direction)
        else:
            clients = self.dbsession.query(*toquery).filter(
                Client.name.like(search+"%")).order_by(sort + " " + direction)
        return clients

    @view_config(route_name='company_clients', renderer='company_client.mako',\
                                                        request_method='POST')
    @view_config(route_name='company_client', renderer='company_client.mako',\
                                                request_param='action=edit')
    def company_client(self):
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
            edit = True
            title = u"Édition du client : {0}".format(client.name)

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
                return HTTPFound(route_path('company_client',
                                            self.request,
                                            id=client.id))
        else:
            html_form = form.render(client.appstruct())
        return dict(title=title,
                    client=client,
                    html_form=html_form,
                    company=client.company)

    @view_config(route_name='company_client', renderer='client_view.mako', \
                                                        request_method='GET')
    def company_client_view(self):
        """
            Return the view of a client
        """
        client = self.request.context
        return dict(title=u"Client : {0}".format(client.name),
                    client=client,
                    company=client.company)
