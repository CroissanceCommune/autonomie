# -*- coding: utf-8 -*-
# * File Name : test_estimation.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 26-12-2012
# * Last Modified :
#
# * Project :
#
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
        self.assertEqual(newest.CAEStatus, 'draft')
        self.assertEqual(newest.project, project)
        self.assertEqual(newest.statusPersonAccount, user)
        self.assertTrue(newest.number.startswith("VRND_IMDD_D2_"))
        self.assertTrue(newest.phase, phase)
        self.assertEqual(len(est.lines), len(newest.lines))
        self.assertEqual(len(est.payment_lines), len(newest.payment_lines))
        self.assertEqual(len(est.discounts), len(newest.discounts))
        self.assertEqual(newest.client, est.client)
        self.assertEqual(newest.address, est.address)

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

    def test_estimation_deposit(self):
        est = self.getOne()
        self.assertEqual(est.deposit_amount(), EST_DEPOSIT_HT)

    def test_sold(self):
        est = self.getOne()
        self.assertEqual(est.sold(), EST_SOLD)

    def test_payments_sum(self):
        est = self.getOne()
        self.assertEqual(est.sold() + est.deposit_amount_ttc()
                + sum([p.amount for p in est.payment_lines[:-1]]),
                est.total())

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
        self.assertEqual(deposit.total_ht(), est.deposit_amount())
        self.assertEqual(deposit.lines[0].tva, 1960)
        #intermediate invoices:
        intermediate_invoices = invoices[1:-1]
        for index, line in enumerate(PAYMENT_LINES[:-1]):
            inv = intermediate_invoices[index]
            # ce test échouera jusqu'à ce qu'on ait trouvé une solution
            # alternative à la configuration des acomptes
            self.assertEqual(inv.total_ht(), line['amount'])
            self.assertEqual(inv.taskDate, line['paymentDate'])
            self.assertEqual(inv.lines[0].tva, 1960)
        total = sum([inv.total() for inv in invoices])
        self.assertEqual(total, est.total())

