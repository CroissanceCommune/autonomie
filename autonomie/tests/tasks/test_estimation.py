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
import datetime
from autonomie.models.task import (
    Estimation,
    DiscountLine,
    PaymentLine,
    TaskLine,
    TaskMention,
)

from autonomie.models.customer import Customer
from autonomie.models.project import Project, Phase
from autonomie.models.user import User
from autonomie.models.company import Company


ESTIMATION = dict(
    display_units="1",
    expenses=1500,
    deposit=20,
    address=u"Adresse",
    workplace=u"Lieu des travaux",
    exclusions=u"Notes",
    paymentDisplay=u"ALL",
    payment_conditions=u"Conditions de paiement",
    date=datetime.date(1969, 7, 31),
    description=u"Description du devis",
    manualDeliverables=1,
)

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
PAYMENT_LINES = [{'description':u"Début",
                  "paymentDate":datetime.date(2012, 12, 12),
                  "amount":1000,
                  "order":1},
                 {'description':u"Milieu",
                  "paymentDate":datetime.date(2012, 12, 13),
                  "amount":1000, "order":2},
                 {'description':u"Fin",
                  "paymentDate":datetime.date(2012, 12, 14),
                  "amount":150,
                  "order":3}]

# Values:
#         the money values are represented *100
#
# Rounding rules:
#         TVA, total_ttc and deposit are rounded (total_ht is not)

# Lines total should accept until 4 elements after the '.'(here they are *100)
# so it fits the limit case
#
# Line totals should be floats (here they are *100)
EST_LINES_TOTAL_HT = (12531.25, 22500)
EST_LINES_TVAS = (2456.125, 4410)

LINES_TOTAL_HT = sum(EST_LINES_TOTAL_HT)
LINES_TOTAL_TVAS = sum(EST_LINES_TVAS)

DISCOUNT_TOTAL_HT = sum([d['amount']for d in DISCOUNTS])
DISCOUNT_TVAS = (392,)
DISCOUNT_TOTAL_TVAS = sum(DISCOUNT_TVAS)

HT_TOTAL =  int(LINES_TOTAL_HT - DISCOUNT_TOTAL_HT)
TVA = int(LINES_TOTAL_TVAS - DISCOUNT_TOTAL_TVAS)

# EST_TOTAL = lines + tva + expenses rounded
EST_TOTAL = HT_TOTAL + TVA + ESTIMATION['expenses']
EST_DEPOSIT_HT = int(HT_TOTAL * ESTIMATION['deposit'] / 100.0)
EST_DEPOSIT = int(EST_TOTAL * ESTIMATION['deposit'] / 100.0)
PAYMENTSSUM = sum([p['amount'] for p in PAYMENT_LINES[:-1]])

EST_SOLD = EST_TOTAL - EST_DEPOSIT - PAYMENTSSUM


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
def estimation(project, user, customer, company, phase):
    est = Estimation(
        company,
        customer,
        project,
        phase,
        user,
    )
    for key, value in ESTIMATION.items():
        setattr(est, key, value)
    for line in LINES:
        est.add_line(TaskLine(**line))
    for line in DISCOUNTS:
        est.discounts.append(DiscountLine(**line))
    for line in PAYMENT_LINES:
        est.payment_lines.append(PaymentLine(**line))
    est.mentions = [
        TaskMention(label='mention1', title='title1', full_text='text1')
    ]
    return est


def test_set_numbers(estimation):
    estimation.set_numbers(5, 18)
    assert estimation.internal_number == u"company1 1969-07 D5"
    assert estimation.name == u"Devis 18"
    assert estimation.project_index == 18


def test_duplicate_estimation(dbsession, estimation):
    newestimation = estimation.duplicate(
        estimation.owner,
        estimation.project,
        estimation.phase,
        estimation.customer,
    )
    for key in "customer", "address", "expenses_ht", "workplace":
        assert getattr(newestimation, key) == getattr(estimation, key)
    assert newestimation.status == 'draft'
    assert newestimation.project == estimation.project
    assert newestimation.statusPersonAccount == estimation.owner
    assert newestimation.internal_number.startswith("company1 {0:%Y-%m}".format(
        datetime.date.today()
    ))
    assert newestimation.phase
    assert newestimation.mentions == estimation.mentions
    assert phase
    assert len(estimation.default_line_group.lines) == len(newestimation.default_line_group.lines)
    assert len(estimation.payment_lines) == len(newestimation.payment_lines)
    assert len(estimation.discounts) == len(newestimation.discounts)


def test_duplicate_estimation_integration(dbsession, estimation):
    """
        Here we test the duplication on a real world case
        specifically, the customer is not loaded in the session
        causing the insert statement to be fired during duplication
    """
    estimation = dbsession.merge(estimation)
    dbsession.flush()

    newestimation = estimation.duplicate(
        estimation.owner,
        estimation.project,
        estimation.phase,
        estimation.customer,

    )

    dbsession.merge(newestimation)
    dbsession.flush()
    assert newestimation.phase == estimation.phase
    assert newestimation.project == estimation.project


def test_light_gen_invoice(dbsession, estimation):
    from autonomie.models.task import Invoice
    invoices = estimation.gen_invoices(estimation.owner)
    for inv in invoices:
        dbsession.add(inv)
        dbsession.flush()

    invoices = Invoice.query().filter(
        Invoice.estimation_id==estimation.id
    ).all()

    #deposit :
    deposit = invoices[0]
    assert deposit.date == datetime.date.today()
    assert deposit.address == estimation.address
    assert deposit.workplace == estimation.workplace
    assert deposit.financial_year == datetime.date.today().year
    assert deposit.total() == estimation.deposit_amount_ttc()
    assert deposit.mentions == estimation.mentions


@pytest.mark.xfail(reason=u"Le calcul de TVA inversé conduit irrémediablement à ce pb")
def test_gen_invoice(dbsession, estimation):
    from autonomie.models.task import Invoice
    invoices = estimation.gen_invoices(user)
    for inv in invoices:
        dbsession.add(inv)
        dbsession.flush()
    invoices = Invoice.query().filter(
        Invoice.estimation_id==estimation.id
    ).all()
    #deposit :
    deposit = invoices[0]
    assert deposit.date == datetime.date.today()
    assert deposit.financial_year == datetime.date.today().year
    assert deposit.total() == estimation.deposit_amount_ttc()
    assert deposit.mentions == estimation.mentions
    #intermediate invoices:
    intermediate_invoices = invoices[1:-1]
    for index, line in enumerate(PAYMENT_LINES[:-1]):
        inv = intermediate_invoices[index]
        # Here, the rounding strategy should be reviewed
        assert inv.total() - line['amount'] <= 1
        assert inv.date == line['paymentDate']
        assert inv.financial_year == line['paymentDate'].year
        assert inv.mentions == estimation.mentions

    total = sum([i.total() for i in invoices])
    assert total == estimation.total()
