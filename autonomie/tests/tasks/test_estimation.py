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

import unittest
import datetime
from mock import MagicMock
from autonomie.tests.base import BaseTestCase
from autonomie.models.task import (Estimation, DiscountLine, PaymentLine,
                    EstimationLine, Invoice)

from autonomie.models.client import Client
from autonomie.models.project import Project, Phase
from autonomie.models.user import User


ESTIMATION = dict(name=u"Devis 2",
                sequenceNumber=2,
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

class TestEstimation(BaseTestCase):
    def getOne(self):
        est = Estimation(**ESTIMATION)
        for line in LINES:
            est.lines.append(EstimationLine(**line))
        for line in DISCOUNTS:
            est.discounts.append(DiscountLine(**line))
        for line in PAYMENT_LINES:
            est.payment_lines.append(PaymentLine(**line))
        return est

    def test_set_number(self):
        est = Estimation()
        est.project = MagicMock(code="PRO1")
        est.client = MagicMock(code="CLI1")
        est.taskDate = datetime.date(1969, 07, 31)
        est.set_sequenceNumber(15)
        est.set_number()
        self.assertEqual(est.number, u"PRO1_CLI1_D15_0769")

    def test_set_name(self):
        est = Estimation()
        est.set_sequenceNumber(5)
        est.set_name()
        self.assertEqual(est.name, u"Devis 5")

    def test_duplicate_estimation(self):
        user = self.session.query(User).first()
        client = self.session.query(Client).first()
        project = self.session.query(Project).first()
        phase = self.session.query(Phase).first()
        est = self.getOne()
        est.phase = phase
        est.project = project
        est.owner = user
        est.client = client
        est.statusPersonAccount = user
        newest = est.duplicate(user, project, phase, client)
        for key in "client", "address", "expenses", "expenses_ht":
            self.assertEqual(getattr(newest, key), getattr(est, key))
        self.assertEqual(newest.CAEStatus, 'draft')
        self.assertEqual(newest.project, project)
        self.assertEqual(newest.statusPersonAccount, user)
        self.assertTrue(newest.number.startswith("VRND_IMDD_D2_"))
        self.assertTrue(newest.phase, phase)
        self.assertEqual(len(est.lines), len(newest.lines))
        self.assertEqual(len(est.payment_lines), len(newest.payment_lines))
        self.assertEqual(len(est.discounts), len(newest.discounts))

    def test_duplicate_estimation_integration(self):
        """
            Here we test the duplication on a real world case
            specifically, the client is not loaded in the session
            causing the insert statement to be fired during duplication
        """
        user = self.session.query(User).first()
        client = self.session.query(Client).first()
        project = self.session.query(Project).first()
        phase = self.session.query(Phase).first()
        est = self.getOne()
        est.phase = phase
        est.project = project
        est.owner = user
        est.client = client
        est.statusPersonAccount = user

        self.assertEqual(est.statusPersonAccount, user)
        self.assertEqual(est.project, project)
        est = self.session.merge(est)
        self.session.flush()

        newest = est.duplicate(user, project, phase, client)
        self.session.merge(newest)
        self.session.flush()
        self.assertEqual(newest.phase, phase)

    def assertPresqueEqual(self, val1, val2):
        self.assertTrue(val1-val2 <= 1)

    @unittest.skip(u"Le calcul de TVA inversé conduit irrémediablement à ce pb")
    def test_gen_invoice(self):
        user = self.session.query(User).first()
        client = self.session.query(Client).first()
        project = self.session.query(Project).first()
        phase = self.session.query(Phase).first()
        est = self.getOne()
        est.phase = phase
        est.project = project
        est.owner = user
        est.client = client
        est.statusPersonAccount = user
        invoices = est.gen_invoices(user)
        for inv in invoices:
            self.session.add(inv)
            self.session.flush()
        invoices = Invoice.query().filter(Invoice.estimation_id==est.id).all()
        #deposit :
        deposit = invoices[0]
        self.assertEqual(deposit.taskDate, datetime.date.today())
        self.assertEqual(deposit.financial_year, datetime.date.today().year)
        self.assertEqual(deposit.total(), est.deposit_amount_ttc())
        #intermediate invoices:
        intermediate_invoices = invoices[1:-1]
        for index, line in enumerate(PAYMENT_LINES[:-1]):
            inv = intermediate_invoices[index]
            # Here, the rounding strategy should be reviewed
            self.assertPresqueEqual(inv.total(), line['amount'])
            self.assertEqual(inv.taskDate, line['paymentDate'])
            self.assertEqual(inv.financial_year, line['paymentDate'].year)
        for inv in invoices:
            print inv.total()
        total = sum([inv.total() for inv in invoices])
        self.assertEqual(total, est.total())

