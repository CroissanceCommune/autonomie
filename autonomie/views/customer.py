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

from autonomie.models.customer import (
    Customer,
    FORM_GRID,
)
from autonomie.utils.widgets import (
    ViewLink,
    PopUp,
)
from autonomie.forms.customer import (
    get_list_schema,
    get_customer_schema,
)
from deform_extensions import GridFormWidget
from autonomie.views import (
    BaseListView,
    BaseCsvView,
    BaseFormView,
    submit_btn,
)
from autonomie.views.csv_import import (
    CsvFileUploadView,
    ConfigFieldAssociationView,
)

log = logging.getLogger(__name__)

def get_customer_form(request):
    """
        Returns the customer add/edit form
    """
    schema = get_customer_schema(request)
    schema = schema.bind(request=request)
    form = Form(schema, buttons=(submit_btn,))
    form.widget = GridFormWidget(grid=FORM_GRID)
    return form


class CustomersListTools(object):
    """
    Customer list tools
    """
    title = u"Liste des clients"
    schema = get_list_schema()
    sort_columns = {
        'name':Customer.name,
        "code":Customer.code,
        "contactLastName":Customer.contactLastName,
    }

    def query(self):
        company = self.request.context
        return Customer.query().filter(Customer.company_id == company.id)

    def filter_name_or_contact(self, records, appstruct):
        """
        Filter the records by customer name or contact lastname
        """
        search = appstruct['search']
        if search:
            records = records.filter(
                or_(Customer.name.like("%" + search + "%"),
                    Customer.contactLastName.like("%" + search + "%")))
        return records


class CustomersListView(CustomersListTools, BaseListView):
    """
    Customer listing view
    """
    def populate_actionmenu(self, appstruct):
        """
        Populate the actionmenu regarding the user's rights
        """
        populate_actionmenu(self.request, self.context)
        if has_permission('add', self.request.context, self.request):
            form = get_customer_form(self.request)
            popup = PopUp("addform", u'Ajouter un client', form.render())
            self.request.popups = {popup.name: popup}
            self.request.actionmenu.add(popup.open_btn())


class CustomersCsv(CustomersListTools, BaseCsvView):
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
    """
    Customer add form
    """
    add_template_vars = ('title', 'codes', )
    title = u"Ajouter un client"
    _schema = None
    buttons = (submit_btn,)
    validation_msg = u"Le client a bien été ajouté"

    @property
    def codes(self):
        codes = [model.code for model in self.context.customers]
        codes.sort()
        return codes

    # Schema is here a property since we need to build it dynamically regarding
    # the current request (the same should have been built using the after_bind
    # method ?)
    @property
    def schema(self):
        """
        The getter for our schema property
        """
        if self._schema == None:
            self._schema = get_customer_schema(self.request)
        return self._schema

    @schema.setter
    def schema(self, value):
        """
        A setter for the schema property
        The BaseClass in pyramid_deform gets and sets the schema attribute that
        is here transformed as a property
        """
        self._schema = value

    def before(self, form):
        populate_actionmenu(self.request, self.context)
        form.widget = GridFormWidget(grid=FORM_GRID)

    def submit_success(self, appstruct):

        if self.context.__name__ == 'company':
            # It's an add form
            model = self.schema.objectify(appstruct)
            model.company = self.context
            self.dbsession.add(model)
        else:
            # It's an edition one
            model = self.schema.objectify(appstruct, self.context)
            model = self.dbsession.merge(model)

        self.dbsession.flush()

        self.session.flash(self.validation_msg)
        return HTTPFound(
            self.request.route_path(
                'customer',
                id=model.id
            )
        )


class CustomerEdit(CustomerAdd):
    """
    Customer edition form
    """
    add_template_vars = ('title', 'codes',)
    validation_msg = u"Le client a été modifié avec succès"

    def appstruct(self):
        """
        Populate the form with the current edited context (customer)
        """
        return self.schema.dictify(self.request.context)

    @reify
    def title(self):
        return u"Modifier le client '{0}'".format(
            self.request.context.name
        )

    @property
    def codes(self):
        codes = [model.code for model in self.context.company.customers \
                if model is not self.context]
        codes.sort()
        return codes


def populate_actionmenu(request, context):
    """
        populate the actionmenu for the different views (list/add/edit ...)
    """
    company_id = request.context.get_company_id()
    request.actionmenu.add(get_list_view_btn(company_id))
    if context.__name__ == 'customer':
        request.actionmenu.add(get_view_btn(context.id))
        if has_permission('edit', request.context, request):
            request.actionmenu.add(get_edit_btn(context.id))


def get_list_view_btn(id_):
    return ViewLink(u"Liste des clients", "edit", path="company_customers",
                                                                    id=id_)


def get_view_btn(customer_id):
    return ViewLink(u"Voir", "view", path="customer", id=customer_id)


def get_edit_btn(customer_id):
    return ViewLink(u"Modifier", "edit", path="customer", id=customer_id,
                                        _query=dict(action="edit"))


class CustomerImportStep1(CsvFileUploadView):
    title = u"Import des clients, étape 1 : chargement d'un fichier au \
format csv"
    model_types = ("customers",)
    default_model_type = 'customers'

    def get_next_step_route(self, args):
        return self.request.route_path(
            "company_customers_import_step2",
            id=self.context.id,
            _query=args
        )


class CustomerImportStep2(ConfigFieldAssociationView):
     title = u"Import de clients, étape 2 : associer les champs"
     model_types = CustomerImportStep1.model_types

     def get_previous_step_route(self):
         return self.request.route_path(
             "company_customers_import_step1",
             id=self.context.id,
         )

     def get_default_values(self):
         log.info("Asking for default values : %s" % self.context.id)
         return dict(company_id=self.context.id)


def includeme(config):
    """
        Add module's views
    """
    config.add_route(
        'customer',
        '/customers/{id}',
        traverse='/customers/{id}',
    )

    config.add_route(
        'company_customers',
        '/company/{id:\d+}/customers',
        traverse='/companies/{id}',
    )

    config.add_route(
        'customers.csv',
        '/company/{id:\d+}/customers.csv',
        traverse='/companies/{id}'
    )


    for i in range(2):
        index = i + 1
        route_name = 'company_customers_import_step%d' % index
        path = '/company/{id:\d+}/customers/import/%d' %index
        config.add_route(route_name, path, traverse='/companies/{id}')

    config.add_view(
        CustomerAdd,
        route_name='company_customers',
        renderer='customer.mako',
        request_method='POST',
        permission='edit',
    )

    config.add_view(
        CustomerAdd,
        route_name='company_customers',
        renderer='customer.mako',
        request_param='action=add',
        permission='edit',
    )

    config.add_view(
        CustomerEdit,
        route_name='customer',
        renderer='customer.mako',
        request_param='action=edit',
        permission='edit',
    )

    config.add_view(
        CustomersListView,
        route_name='company_customers',
        renderer='company_customers.mako',
        request_method='GET',
        permission='edit',
    )

    config.add_view(
        CustomersCsv,
        route_name='customers.csv',
        request_method='GET',
        permission='edit',
    )

    config.add_view(
        customer_view,
        route_name='customer',
        renderer='customer_view.mako',
        request_method='GET',
        permission='view',
    )

    config.add_view(
        CustomerImportStep1,
        route_name="company_customers_import_step1",
        permission="edit",
        renderer="base/formpage.mako",
    )

    config.add_view(
        CustomerImportStep2,
        route_name="company_customers_import_step2",
        permission="edit",
        renderer="base/formpage.mako",
    )
