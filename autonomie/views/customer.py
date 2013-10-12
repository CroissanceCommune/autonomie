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
    Customer views
"""
import logging

from sqlalchemy import or_
from sqlalchemy.orm import undefer_group

from deform import Form

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from autonomie.models.customer import Customer
from autonomie.utils.widgets import ViewLink
from autonomie.utils.widgets import SearchForm
from autonomie.utils.widgets import PopUp
from autonomie.utils.views import submit_btn
from autonomie.views.forms.customer import (
        CUSTOMERSCHEMA,
        CustomerSearchSchema,
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


def get_customer_form(request):
    """
        Returns the customer add/edit form
    """
    schema = CUSTOMERSCHEMA.bind(request=request)
    form = Form(schema, buttons=(submit_btn,))
    return form


class CustomersList(BaseListView):
    title = u"Liste des clients"
    schema = CustomerSearchSchema()
    sort_columns = {'name':Customer.name,
                    "code":Customer.code,
                    "contactLastName":Customer.contactLastName}

    def query(self):
        company = self.request.context
        return Customer.query().filter(Customer.company_id == company.id)

    def filter_name_or_contact(self, records, appstruct):
        search = appstruct['search']
        if search:
            records = records.filter(
                or_(Customer.name.like("%" + search + "%"),
                    Customer.contactLastName.like("%" + search + "%")))
        return records

    def populate_actionmenu(self, appstruct):
        populate_actionmenu(self.request)
        if has_permission('add', self.request.context, self.request):
            form = get_customer_form(self.request)
            popup = PopUp("addform", u'Ajouter un client', form.render())
            self.request.popups = {popup.name: popup}
            self.request.actionmenu.add(popup.open_btn())
        searchform = SearchForm(u"Entreprise ou contact principal")
        searchform.set_defaults(appstruct)
        self.request.actionmenu.add(searchform)


class CustomersCsv(BaseCsvView):
    """
        Customer csv view
    """
    model = Customer

    @property
    def filename(self):
        return "clients.csv"

    def query(self):
        company = self.request.context
        return Customer.query().options(undefer_group('edit'))\
                .filter(Customer.company_id == company.id)


def customer_view(request):
    """
        Return the view of a customer
    """
    populate_actionmenu(request, request.context)
    return dict(title=u"Client : {0}".format(request.context.name),
                customer=request.context)


class CustomerAdd(BaseFormView):
    title = u"Ajouter un client"
    schema = CUSTOMERSCHEMA
    buttons = (submit_btn,)

    def before(self, form):
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        customer = Customer()
        customer.company = self.request.context
        customer = merge_session_with_post(customer, appstruct)
        self.dbsession.add(customer)
        self.dbsession.flush()
        message = u"Le client <b>{0}</b> a été ajouté avec succès".format(
                                                                customer.name)
        self.session.flash(message)
        return HTTPFound(self.request.route_path('customer', id=customer.id))


class CustomerEdit(BaseFormView):
    schema = CUSTOMERSCHEMA
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
        customer = merge_session_with_post(self.request.context, appstruct)
        customer = self.dbsession.merge(customer)
        self.dbsession.flush()
        message = u"Le client <b>{0}</b> a été édité avec succès".format(
                                                                customer.name)
        self.session.flash(message)
        return HTTPFound(self.request.route_path('customer', id=customer.id))

    def appstruct(self):
        """
            Populate the form with the current edited context (customer)
        """
        return self.request.context.appstruct()


def populate_actionmenu(request, customer=None):
    """
        populate the actionmenu
    """
    company_id = request.context.get_company_id()
    request.actionmenu.add(get_list_view_btn(company_id))
    if customer:
        request.actionmenu.add(get_view_btn(customer.id))
        if has_permission('edit', request.context, request):
            request.actionmenu.add(get_edit_btn(customer.id))

def get_list_view_btn(id_):
    return ViewLink(u"Liste des clients", "edit", path="company_customers",
                                                                    id=id_)

def get_view_btn(customer_id):
    return ViewLink(u"Voir", "view", path="customer", id=customer_id)

def get_edit_btn(customer_id):
    return ViewLink(u"Éditer", "edit", path="customer", id=customer_id,
                                        _query=dict(action="edit"))


def includeme(config):
    """
        Add module's views
    """
    config.add_route('customer',
                     '/customers/{id}',
                     traverse='/customers/{id}')

    config.add_route('company_customers',
                     '/company/{id:\d+}/customers',
                     traverse='/companies/{id}')
    config.add_route('company_customers_csv',
                     '/company/{id:\d+}/customers.csv',
                     traverse='/companies/{id}')

    config.add_view(CustomerAdd,
                    route_name='company_customers',
                    renderer='customer.mako',
                    request_method='POST',
                    permission='edit')
    config.add_view(CustomerAdd,
                    route_name='company_customers',
                    renderer='customer.mako',
                    request_param='action=add',
                    permission='edit')
    config.add_view(CustomerEdit,
                    route_name='customer',
                    renderer='customer.mako',
                    request_param='action=edit',
                    permission='edit')

    config.add_view(CustomersList,
                    route_name='company_customers',
                    renderer='company_customers.mako',
                    request_method='GET',
                    permission='edit')

    config.add_view(CustomersCsv,
                    route_name='company_customers_csv',
                    request_method='GET',
                    permission='edit')

    config.add_view(customer_view,
                    route_name='customer',
                    renderer='customer_view.mako',
                    request_method='GET',
                    permission='view')
