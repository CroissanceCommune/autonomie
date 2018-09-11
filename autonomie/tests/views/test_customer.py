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

import colander

from autonomie.models.customer import Customer
from autonomie.views.customer import CustomerAdd, CustomerEdit
from autonomie.tests.base import Dummy


COMPANY_APPSTRUCT = {
    'name': 'Company',
    'lastname': u'Lastname',
    'address': 'Address',
    'zip_code': "21000",
    "city": "Dijon",
    'compte_cg': "Compte CG1515",
    'compte_tiers': "Compte Tiers",
    'code': 'CODE'
}


INDIVIDUAL_APPSTRUCT = {
    'lastname': u'Lastname 2',
    'firstname': u'FirstName',
    'address': 'Address',
    'zip_code': "21000",
    "city": "Dijon",
    'compte_cg': "Compte CG1515",
    'compte_tiers': "Compte Tiers",
    'code': 'CODE'
}


def get_company_customer():
    return Customer.query().filter(Customer.name == 'Company').one()


def get_individual_customer():
    return Customer.query().filter(Customer.lastname == 'Lastname 2').one()


class TestCustomerAdd():

    def test_is_company_form(self, get_csrf_request_with_db):
        pyramid_request = get_csrf_request_with_db(
            post={'__formid__': 'company'}
        )
        view = CustomerAdd(pyramid_request)
        assert view.is_company_form()
        pyramid_request.POST = {'__formid__': 'individual'}
        view = CustomerAdd(pyramid_request)
        assert not view.is_company_form()

    def test_schema(self, get_csrf_request_with_db):
        pyramid_request = get_csrf_request_with_db(
            post={'__formid__': 'company'}
        )
        view = CustomerAdd(pyramid_request)
        schema = view.schema
        assert schema['name'].missing == colander.required

        pyramid_request.POST = {'__formid__': 'individual'}
        view = CustomerAdd(pyramid_request)
        schema = view.schema
        assert schema['civilite'].missing == colander.required

    def test_submit_company_success(
        self, config, get_csrf_request_with_db, company
    ):
        config.add_route('customer', '/')
        pyramid_request = get_csrf_request_with_db(
            post={'__formid__': 'company'}
        )
        pyramid_request.context = company

        view = CustomerAdd(pyramid_request)
        view.submit_success(COMPANY_APPSTRUCT)
        customer = get_company_customer()
        for key, value in COMPANY_APPSTRUCT.items():
            assert getattr(customer, key) == value
        assert customer.type_ == 'company'
        assert customer.company == company

    def test_submit_individual_success(
        self, config, get_csrf_request_with_db, company
    ):
        config.add_route('customer', '/')
        pyramid_request = get_csrf_request_with_db(
            post={'__formid__': 'individual'}
        )
        pyramid_request.context = company

        view = CustomerAdd(pyramid_request)
        view.submit_success(INDIVIDUAL_APPSTRUCT)
        customer = get_individual_customer()
        for key, value in INDIVIDUAL_APPSTRUCT.items():
            assert getattr(customer, key) == value
        assert customer.type_ == 'individual'
        assert customer.company == company
        assert customer.label == customer._get_label()


class TestCustomerEdit():

    def test_customer_edit(self, config, customer, get_csrf_request_with_db):
        config.add_route('customer', '/')
        req = get_csrf_request_with_db()
        req.context = customer
        req.user = Dummy()

        appstruct = COMPANY_APPSTRUCT.copy()
        appstruct['lastname'] = u"Changed Lastname"
        appstruct['compte_cg'] = "1"
        appstruct['compte_tiers'] = "2"
        view = CustomerEdit(req)
        view.submit_success(appstruct)
        customer = get_company_customer()
        assert customer.lastname == u'Changed Lastname'
        assert customer.compte_cg == "1"
        assert customer.compte_tiers == "2"
        assert customer.label == customer._get_label()


def test_customer_delete(customer, get_csrf_request_with_db):
    req = get_csrf_request_with_db()
    cid = customer.id
    from autonomie.views.customer import customer_delete
    req.context = customer
    req.referer = '/'
    customer_delete(req)
    req.dbsession.flush()
    assert Customer.get(cid) is None


def test_customer_archive(customer, get_csrf_request_with_db):
    req = get_csrf_request_with_db()
    cid = customer.id
    from autonomie.views.customer import customer_archive
    req.context = customer
    req.referer = '/'
    customer_archive(req)
    req.dbsession.flush()
    assert Customer.get(cid).archived
    customer_archive(req)
    req.dbsession.flush()
    assert Customer.get(cid).archived is False
