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
from pyramid import testing
from mock import MagicMock
from autonomie.models.task import (
    CancelInvoice,
    Invoice,
    TaskLine,
    DiscountLine,
)
from autonomie.models.user import User
from autonomie.models.customer import Customer
from autonomie.models.project import Phase, Project

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
    sequence_number=2,
    taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
    description=u"Description de la facture",
    _number=u"invoicenumber",
    expenses=0,
    expenses_ht=0,
    prefix="prefix",
    financial_year=2015,
)


@pytest.fixture
def invoice():
    inv = Invoice(**INVOICE)
    for line in LINES:
        inv.default_line_group.lines.append(TaskLine(**line))
    for discount in DISCOUNTS:
        inv.discounts.append(DiscountLine(**discount))
    return inv


def test_set_name():
    cinv = CancelInvoice()
    cinv.set_sequence_number(5)
    cinv.set_name()
    assert cinv.name == u"Avoir 5"

def test_get_number():
    cinv = CancelInvoice()
    cinv.project = MagicMock(code="PRO1")
    cinv.customer = MagicMock(code="CLI1")
    cinv.taskDate = datetime.date(1969, 07, 31)
    cinv.set_sequence_number(15)
    cinv.set_number()
    assert cinv.number == u"PRO1_CLI1_A15_0769"

def test_set_name():
    invoice = Invoice()
    invoice.set_sequence_number(5)
    invoice.set_name()
    assert invoice.name == u"Facture 5"
    invoice.name = ""
    invoice.set_name(sold=True)
    assert invoice.name == u"Facture de solde"
    invoice.name = ""
    invoice.set_name(deposit=True)
    assert invoice.name == u"Facture d'acompte 5"


def test_set_number():
    invoice = Invoice()
    invoice.customer = MagicMock(code="CLI1")
    invoice.project = MagicMock(code="PRO1")
    seq_number = 15
    invoice.set_sequence_number(15)
    invoice.set_name()
    date = datetime.date(1969, 07, 31)
    invoice.taskDate = date
    invoice.set_number()
    assert invoice.number == u"PRO1_CLI1_F15_0769"
    invoice.set_number(deposit=True)
    assert invoice.number == u"PRO1_CLI1_FA15_0769"


def test_gen_cancelinvoice(dbsession, invoice):
    user = User.query().first()
    project = Project.query().first()
    invoice.project = project
    invoice.owner = user
    invoice.statusPersonAccount = user
    dbsession.add(invoice)
    dbsession.flush()
    cinv = invoice.gen_cancelinvoice(user)
    dbsession.add(cinv)
    dbsession.flush()

    assert cinv.name == "Avoir 1"
    assert cinv.total_ht() == -1 * invoice.total_ht()
    today = datetime.date.today()
    assert cinv.taskDate == today
    assert cinv.prefix == invoice.prefix
    assert cinv.financial_year == invoice.financial_year

def test_gen_cancelinvoice_payment(dbsession, invoice):
    user = User.query().first()
    project = Project.query().first()
    invoice.project = project
    invoice.owner = user
    invoice.statusPersonAccount = user
    invoice.record_payment(mode="c", amount=1500)
    cinv = invoice.gen_cancelinvoice(user)
    assert len(cinv.default_line_group.lines) ==  len(invoice.default_line_group.lines) + len(invoice.discounts) + 1
    assert cinv.default_line_group.lines[-1].cost == 1500

def test_duplicate_invoice(dbsession, invoice):
    user = dbsession.query(User).first()
    customer = dbsession.query(Customer).first()
    project = dbsession.query(Project).first()
    phase = dbsession.query(Phase).first()
    invoice.owner = user
    invoice.statusPersonAccount = user
    invoice.project = project
    invoice.phase = phase
    invoice.customer = customer
    invoice.address = customer.address

    newinvoice = invoice.duplicate(user, project, phase, customer)
    assert len(invoice.default_line_group.lines) == len(newinvoice.default_line_group.lines)
    assert len(invoice.discounts) == len(newinvoice.discounts)
    assert invoice.project == newinvoice.project
    assert newinvoice.statusPersonAccount == user
    assert newinvoice.phase == phase
    for key in "customer", "address", "expenses", "expenses_ht":
        assert getattr(newinvoice, key) == getattr(invoice, key)

def test_duplicate_invoice_financial_year(dbsession, invoice):
    user = dbsession.query(User).first()
    customer = dbsession.query(Customer).first()
    project = dbsession.query(Project).first()
    phase = dbsession.query(Phase).first()
    invoice.owner = user
    invoice.statusPersonAccount = user
    invoice.project = project
    invoice.phase = phase
    invoice.customer = customer
    invoice.financial_year = 1900

    newinvoice = invoice.duplicate(user, project, phase, customer)
    assert newinvoice.financial_year == datetime.date.today().year

def test_duplicate_invoice_integration(dbsession, invoice):
    user = dbsession.query(User).first()
    project = dbsession.query(Project).first()
    phase = dbsession.query(Phase).first()
    customer = dbsession.query(Customer).first()

    invoice.phase = phase
    invoice.customer = customer
    invoice.owner = user
    invoice.statusPersonAccount = user
    invoice.project = project
    dbsession.add(invoice)
    dbsession.flush()
    newest = invoice.duplicate(user, project, phase, customer)
    dbsession.add(newest)
    dbsession.flush()
    assert newest.phase_id == phase.id
    assert newest.owner_id == user.id
    assert newest.statusPerson == user.id
    assert newest.project_id == project.id


def test_valid_invoice(config, dbsession, invoice):
    dbsession.add(invoice)
    dbsession.flush()
    config.testing_securitypolicy(userid='test', permissive=True)

    request = testing.DummyRequest()
    invoice.set_status('wait', request, 1)
    dbsession.merge(invoice)
    dbsession.flush()
    invoice.set_status('valid', request, 1)
    today = datetime.date.today()
    assert invoice.taskDate == today
    assert invoice.official_number == 1

def test_valid_payment(config, dbsession, invoice):
    dbsession.add(invoice)
    dbsession.flush()
    config.testing_securitypolicy(userid='test', permissive=True)

    request = testing.DummyRequest()
    invoice.set_status('wait', request, 1)
    dbsession.merge(invoice)
    dbsession.flush()
    invoice.set_status('valid', request, 1)
    dbsession.merge(invoice)
    dbsession.flush()
    invoice.set_status("paid", request, 1, amount=150, mode="CHEQUE")
    invoice = dbsession.merge(invoice)
    dbsession.flush()
    invoice = dbsession.query(Invoice)\
            .filter(Invoice.id==invoice.id).first()

    assert invoice.CAEStatus == 'paid'
    assert len(invoice.payments) == 1
    assert invoice.payments[0].amount == 150
