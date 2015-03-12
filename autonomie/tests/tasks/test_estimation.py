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
from mock import MagicMock
from autonomie.models.task import (
    Estimation,
    DiscountLine,
    PaymentLine,
    EstimationLine,
)

from autonomie.models.customer import Customer
from autonomie.models.project import Project, Phase
from autonomie.models.user import User


ESTIMATION = dict(name=u"Devis 2",
                sequence_number=2,
                _number=u"estnumber",
                displayedUnits="1",
                expenses=1500,
                deposit=20,
                exclusions=u"Notes",
                paymentDisplay=u"ALL",
                paymentConditions=u"Conditions de paiement",
                taskDate=datetime.date(2012, 12, 10),
                description=u"Description du devis",
                manualDeliverables=1)

LINES = [{'description':u'text1',
          'cost':10025,
           'tva':1960,
          'unity':'DAY',
          'quantity':1.25,
          'rowIndex':1},
         {'description':u'text2',
          'cost':7500,
           'tva':1960,
          'unity':'month',
          'quantity':3,
          'rowIndex':2}]

DISCOUNTS = [{'description':u"Remise à 19.6", 'amount':2000, 'tva':1960}]
PAYMENT_LINES = [{'description':u"Début",
                  "paymentDate":datetime.date(2012, 12, 12),
                  "amount":1000,
                  "rowIndex":1},
                 {'description':u"Milieu",
                  "paymentDate":datetime.date(2012, 12, 13),
                  "amount":1000, "rowIndex":2},
                 {'description':u"Fin",
                  "paymentDate":datetime.date(2012, 12, 14),
                  "amount":150,
                  "rowIndex":3}]

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
def estimation():
    est = Estimation(**ESTIMATION)
    for line in LINES:
        est.lines.append(EstimationLine(**line))
    for line in DISCOUNTS:
        est.discounts.append(DiscountLine(**line))
    for line in PAYMENT_LINES:
        est.payment_lines.append(PaymentLine(**line))
    return est

def test_set_number():
    est = Estimation()
    est.project = MagicMock(code="PRO1")
    est.customer = MagicMock(code="CLI1")
    est.taskDate = datetime.date(1969, 07, 31)
    est.set_sequence_number(15)
    est.set_number()
    assert est.number == u"PRO1_CLI1_D15_0769"

def test_set_name():
    est = Estimation()
    est.set_sequence_number(5)
    est.set_name()
    assert est.name == u"Devis 5"

def test_duplicate_estimation(dbsession, estimation):
    user = dbsession.query(User).first()
    customer = dbsession.query(Customer).first()
    project = dbsession.query(Project).first()
    phase = dbsession.query(Phase).first()
    estimation.phase = phase
    estimation.project = project
    estimation.owner = user
    estimation.customer = customer
    estimation.statusPersonAccount = user
    newestimation = estimation.duplicate(user, project, phase, customer)
    for key in "customer", "address", "expenses", "expenses_ht":
        assert getattr(newestimation, key) == getattr(estimation, key)
    assert newestimation.CAEStatus == 'draft'
    assert newestimation.project == project
    assert newestimation.statusPersonAccount == user
    assert newestimation.number.startswith("P001_C001_D2_")
    assert newestimation.phase
    assert phase
    assert len(estimation.lines) == len(newestimation.lines)
    assert len(estimation.payment_lines) == len(newestimation.payment_lines)
    assert len(estimation.discounts) == len(newestimation.discounts)

##### WORK IN PROGRESS

def test_duplicate_estimation_integration(dbsession, estimation):
    """
        Here we test the duplication on a real world case
        specifically, the customer is not loaded in the session
        causing the insert statement to be fired during duplication
    """
    user = dbsession.query(User).first()
    customer = dbsession.query(Customer).first()
    project = dbsession.query(Project).first()
    phase = dbsession.query(Phase).first()
    estimation.phase = phase
    estimation.project = project
    estimation.owner = user
    estimation.customer = customer
    estimation.statusPersonAccount = user

    assert estimation.statusPersonAccount == user
    assert estimation.project == project
    estimation = dbsession.merge(estimation)
    dbsession.flush()

    newestimation = estimation.duplicate(user, project, phase, customer)
    dbsession.merge(newestimation)
    dbsession.flush()
    assert newestimation.phase == phase

def assertPresqueEqual(val1, val2):
    """
    A custom assert
    """
    assert val1-val2 <= 1

def test_light_gen_invoice(dbsession, estimation):
    from autonomie.models.task import Invoice
    user = dbsession.query(User).first()
    customer = dbsession.query(Customer).first()
    project = dbsession.query(Project).first()
    phase = dbsession.query(Phase).first()
    estimation.phase = phase
    estimation.project = project
    estimation.owner = user
    estimation.customer = customer
    estimation.statusPersonAccount = user
    invoices = estimation.gen_invoices(user)
    for inv in invoices:
        dbsession.add(inv)
        dbsession.flush()
    invoices = Invoice.query().filter(
        Invoice.estimation_id==estimation.id
    ).all()
    #deposit :
    deposit = invoices[0]
    assert deposit.taskDate == datetime.date.today()
    assert deposit.financial_year == datetime.date.today().year
    assert deposit.total() == estimation.deposit_amount_ttc()
    #intermediate invoices:
    intermediate_invoices = invoices[1:-1]

@pytest.mark.xfail(reason=u"Le calcul de TVA inversé conduit irrémediablement à ce pb")
def test_gen_invoice(dbsession, estimation):
    from autonomie.models.task import Invoice
    user = dbsession.query(User).first()
    customer = dbsession.query(Customer).first()
    project = dbsession.query(Project).first()
    phase = dbsession.query(Phase).first()
    estimation.phase = phase
    estimation.project = project
    estimation.owner = user
    estimation.customer = customer
    estimation.statusPersonAccount = user
    invoices = estimation.gen_invoices(user)
    for inv in invoices:
        dbsession.add(inv)
        dbsession.flush()
    invoices = Invoice.query().filter(
        Invoice.estimation_id==estimation.id
    ).all()
    #deposit :
    deposit = invoices[0]
    assert deposit.taskDate == datetime.date.today()
    assert deposit.financial_year == datetime.date.today().year
    assert deposit.total() == estimation.deposit_amount_ttc()
    #intermediate invoices:
    intermediate_invoices = invoices[1:-1]
    for index, line in enumerate(PAYMENT_LINES[:-1]):
        inv = intermediate_invoices[index]
        # Here, the rounding strategy should be reviewed
        assert inv.total() - line['amount'] <= 1
        assert inv.taskDate == line['paymentDate']
        assert inv.financial_year == line['paymentDate'].year

    total = sum([inv.total() for inv in invoices])
    assert total == estimation.total()
