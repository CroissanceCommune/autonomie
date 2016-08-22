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

import datetime
import pytest

from autonomie.models.task.states import record_payment
from autonomie.models.task import Payment
from autonomie.models.task import Invoice, TaskLineGroup, TaskLine
from autonomie.models.user import User
from autonomie.models.customer import Customer
from autonomie.models.project import Phase, Project
from autonomie.models.company import Company

INVOICE = dict( name=u"Facture 2",
                sequence_number=2,
                date=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de la facture",
                expenses=0,
                expenses_ht=0)

LINE = {'description':u'text1', 'cost':10000000, 'tva':1960,
              'unity':'DAY', 'quantity':1, 'order':1}

PAYMENTS = [
            {'amount':1500000, 'mode':'CHEQUE'},
            {'amount':1895000, 'mode':'CHEQUE'},
            ]


@pytest.fixture
def phase(content):
    return Phase.query().first()


@pytest.fixture
def project(content):
    proj = Project.query().first()
    proj.code = "PRO1"
    return proj


@pytest.fixture
def user(content):
    return User.query().first()


@pytest.fixture
def company(content):
    return Company.query().first()


@pytest.fixture
def customer(content):
    res = Customer.query().first()
    res.code = "CLI1"
    return res


@pytest.fixture
def invoice(project, user, customer, company, phase):
    invoice = Invoice(
        company,
        customer,
        project,
        phase,
        user,
    )
    invoice.line_groups = [TaskLineGroup(lines=[TaskLine(**LINE)])]
    for i in PAYMENTS:
        invoice.payments.append(Payment(**i))
    return invoice


def test_record_payment(invoice):
    request_params = {'amount':1500000, 'mode':'cheque'}
    record_payment(invoice, **request_params)
    assert len(invoice.payments) == 3
    assert invoice.payments[2].amount == 1500000


def test_payment_get_amount():
    payment = Payment(**PAYMENTS[1])
    assert payment.get_amount() == 1895000


def test_invoice_topay(invoice):
    assert invoice.paid() == 3395000
    assert invoice.topay() == 11960000 - 3395000


def test_resulted_manual(invoice):
    invoice.CAEStatus = 'wait'
    invoice.CAEStatus = 'valid'
    invoice.CAEStatus = 'paid'
    request_params = {'amount':0, 'mode':'cheque', 'resulted':True}
    record_payment(invoice, **request_params)
    assert invoice.CAEStatus == 'resulted'


def test_resulted_auto(invoice):
    invoice.CAEStatus = 'wait'
    invoice.CAEStatus = 'valid'
    invoice.CAEStatus = 'paid'
    request_params = {'amount':int(invoice.topay()), 'mode':'cheque'}
    record_payment(invoice, **request_params)
    assert invoice.CAEStatus == 'resulted'
