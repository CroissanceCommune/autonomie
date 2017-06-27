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
from autonomie.models.task import (
    CancelInvoice,
    Invoice,
    TaskLine,
    DiscountLine,
    TaskMention,
    Payment,
)

from autonomie.models.tva import (
    Tva,
)
from autonomie.models.user import User
from autonomie.models.customer import Customer
from autonomie.models.project import Phase, Project
from autonomie.models.company import Company

LINES = [{'description':u'text1',
          'cost':10025,
           'tva':1960,
          'unity':'DAY',
          'quantity':1.25,
          'order':1},
         {'description':u'text2',
          'cost':7500,
           'tva':1960,
          'unity':'month',
          'quantity':3,
          'order':2}]

DISCOUNTS = [{'description':u"Remise à 19.6", 'amount':2000, 'tva':1960}]

INVOICE = dict(
    name=u"Facture 2",
    project_index=2,
    date=datetime.date(2012, 12, 10), #u"10-12-2012",
    description=u"Description de la facture",
    _number=u"invoicenumber",
    expenses=0,
    expenses_ht=0,
    prefix="prefix",
    financial_year=2015,
    address=u"Adresse",
    workplace=u"Lieu d'éxécution des travaux",
    payment_conditions="OOO"
)


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
    for key, value in INVOICE.items():
        setattr(invoice, key, value)

    for line in LINES:
        invoice.default_line_group.lines.append(TaskLine(**line))
    for discount in DISCOUNTS:
        invoice.discounts.append(DiscountLine(**discount))
    invoice.mentions = [TaskMention(label='1', title='t1', full_text='text')]

    invoice.address = customer.address

    return invoice


@pytest.fixture
def cancelinvoice(project, user, customer, company, phase):
    cancelinvoice = CancelInvoice(
        company,
        customer,
        project,
        phase,
        user,
    )
    cancelinvoice.address = customer.address
    cancelinvoice.date = datetime.date(2012, 12, 10)

    return cancelinvoice


@pytest.fixture
def tva(dbsession):
    tva = Tva(name='TVA 20%', value=2000, default=True)
    dbsession.add(tva)
    dbsession.flush()
    return tva


@pytest.fixture
def service_request(pyramid_request, config):
    return pyramid_request


def test_set_numbers(invoice, cancelinvoice):
    invoice.set_numbers(15, 1)
    assert invoice.internal_number == u"company1 2012-12 F15"
    assert invoice.name == u"Facture 1"

    cancelinvoice.set_numbers(15, 5)
    assert cancelinvoice.name == u"Avoir 5"
    assert cancelinvoice.internal_number == u"company1 2012-12 A15"


def test_set_deposit_label(invoice):
    invoice.set_numbers(5, 8)
    invoice.set_deposit_label()
    assert invoice.name == u"Facture d'acompte 8"


def test_set_sold_label(invoice):
    invoice.set_numbers(5, 8)
    invoice.set_sold_label()
    assert invoice.name == u"Facture de solde 8"

def test_duplicate_invoice(dbsession, invoice):
    newinvoice = invoice.duplicate(
        invoice.owner,
        invoice.project,
        invoice.phase,
        invoice.customer,
    )
    assert len(invoice.default_line_group.lines) == len(newinvoice.default_line_group.lines)
    assert len(invoice.discounts) == len(newinvoice.discounts)
    assert newinvoice.project == invoice.project
    assert newinvoice.company == invoice.company
    assert newinvoice.statusPersonAccount == invoice.statusPersonAccount
    assert newinvoice.phase == invoice.phase
    assert newinvoice.mentions == invoice.mentions
    for key in "customer", "address", "expenses_ht", "workplace":
        assert getattr(newinvoice, key) == getattr(invoice, key)

def test_duplicate_invoice_financial_year(dbsession, invoice):
    invoice.financial_year = 1900
    newinvoice = invoice.duplicate(
        invoice.owner,
        invoice.project,
        invoice.phase,
        invoice.customer,
    )
    assert newinvoice.financial_year == datetime.date.today().year

def test_duplicate_invoice_integration(dbsession, invoice):
    dbsession.add(invoice)
    dbsession.flush()
    newest = invoice.duplicate(
        invoice.owner,
        invoice.project,
        invoice.phase,
        invoice.customer,
    )
    dbsession.add(newest)
    dbsession.flush()
    assert newest.phase_id == invoice.phase_id
    assert newest.owner_id == invoice.owner_id
    assert newest.statusPerson == invoice.statusPerson
    assert newest.project_id == invoice.project_id
    assert newest.company_id == invoice.company_id


def test_valid_invoice(config, dbsession, invoice, service_request):
    dbsession.add(invoice)
    dbsession.flush()
    config.testing_securitypolicy(userid='test', permissive=True)

    invoice.set_status('wait', service_request, 1)
    dbsession.merge(invoice)
    dbsession.flush()
    invoice.set_status('valid', service_request, 1)
    today = datetime.date.today()
    assert invoice.date == today
    assert invoice.official_number == 1


def test_gen_cancelinvoice(dbsession, invoice):
    dbsession.add(invoice)
    dbsession.flush()
    cinv = invoice.gen_cancelinvoice(invoice.owner)
    dbsession.add(cinv)
    dbsession.flush()

    assert cinv.total_ht() == -1 * invoice.total_ht()
    today = datetime.date.today()
    assert cinv.date == today
    assert cinv.prefix == invoice.prefix
    assert cinv.financial_year == invoice.financial_year
    assert cinv.mentions == invoice.mentions
    assert cinv.address == invoice.address
    assert cinv.workplace == invoice.workplace
    assert cinv.project == invoice.project
    assert cinv.company == invoice.company
    assert cinv.phase == invoice.phase

def test_gen_cancelinvoice_payment(dbsession, invoice, tva):
    invoice.payments = [
        Payment(mode="c", amount=120000000, tva=tva)
    ]
    cinv = invoice.gen_cancelinvoice(invoice.owner)
    assert len(cinv.default_line_group.lines) ==  len(invoice.default_line_group.lines) + len(invoice.discounts) + 1
    assert cinv.default_line_group.lines[-1].cost == 100000000
    assert cinv.default_line_group.lines[-1].tva == 2000

def test_valid_payment(config, dbsession, invoice, service_request):
    dbsession.add(invoice)
    dbsession.flush()
    config.testing_securitypolicy(userid='test', permissive=True)

    invoice.set_status('wait', service_request, 1)
    dbsession.merge(invoice)
    dbsession.flush()
    invoice.set_status('valid', service_request, 1)
    dbsession.merge(invoice)
    dbsession.flush()
    invoice.set_status("paid", service_request, 1, amount=150, mode="CHEQUE")
    invoice = dbsession.merge(invoice)
    dbsession.flush()
    invoice = dbsession.query(Invoice)\
            .filter(Invoice.id==invoice.id).first()

    assert invoice.paid_status == 'paid'
    assert len(invoice.payments) == 1
    assert invoice.payments[0].amount == 150
