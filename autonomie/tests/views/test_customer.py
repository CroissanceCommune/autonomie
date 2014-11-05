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

import pytest

from autonomie.models.customer import Customer
from autonomie.models.company import Company
from autonomie.views.customer import CustomerAdd, CustomerEdit
from autonomie.tests.base import Dummy

APPSTRUCT = {'name':'Company', 'contactLastName':u'Lastname',
             'contactFirstName':u'FirstName',
             'address':'Address should be multiline',
             'zipCode': "21000",
             "city": "Dijon",
             'compte_cg':"Compte CG1515",
             'compte_tiers':"Compte Tiers", 'code': 'CODE'}


def get_user(contractor=True):
    return Dummy(is_contractor=lambda :contractor)

@pytest.fixture
def customer(config, content, get_csrf_request_with_db):
    config.add_route('customer', '/')
    request = get_csrf_request_with_db()
    comp = Company.query().first()
    comp.__name__ = 'company'
    request.context = comp
    request.user = get_user()
    view = CustomerAdd(request)
    view.submit_success(APPSTRUCT)
    return getOne()

def getOne():
    return Customer.query().filter(Customer.name=='Company').one()

def test_add(customer):
    for attr, value in APPSTRUCT.items():
        assert getattr(customer, attr) == value

def test_customer_edit(customer, get_csrf_request_with_db):
    customer.__name__ = 'customer'
    req = get_csrf_request_with_db()
    req.context = customer
    req.user = get_user(contractor=False)
    appstruct = APPSTRUCT.copy()
    appstruct['contactLastName'] = u"Changed Lastname"
    appstruct['compte_cg'] = "1"
    appstruct['compte_tiers'] = "2"
    view = CustomerEdit(req)
    view.submit_success(appstruct)
    customer = getOne()
    assert customer.contactLastName == u'Changed Lastname'
    assert customer.compte_cg == "1"
    assert customer.compte_tiers == "2"
