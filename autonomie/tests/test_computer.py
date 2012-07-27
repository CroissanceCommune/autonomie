# -*- coding: utf-8 -*-
# * File Name : test_computer.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-07-2012
# * Last Modified :
#
# * Project :
#
import datetime
from copy import deepcopy
from mock import MagicMock
from .base import BaseTestCase

from autonomie.utils.task import TaskComputing, ManualInvoiceComputing
from autonomie.models.model import (Task, Estimation,
        Invoice, ManualInvoice, EstimationLine, InvoiceLine,
        CancelInvoiceLine, PaymentLine)

est= {"sequenceNumber":1,
        "number":u"TEST_EST_01",
        "tva":196,
        "deposit":30,
        "paymentConditions":u"Conditions de paiement",
        "exclusions":u"Notes sur le projet",
        "IDProject":1,
        "manualDeliverables":0,
        "course":0,
        "displayedUnits":0,
        "discountHT":150,
        "expenses":150,
        "paymentDisplay":1,
        "IDPhase":1,
        "name":u"Devis de test1",
        "CAEStatus":"draft",
        "taskDate":datetime.date.today(),
        "IDEmployee":1,
        "description":u"Devis de test",}

est_lines = [
        {
    "cost":10025,
    "quantity":1.25,
    "unity":"DAY",
    "description":u"Prestation 1",
    "rowIndex":1,
    },
        {
    "cost":7500,
    "quantity":3,
    "unity":"DAY",
    "description":u"Prestation 2",
    "rowIndex":2,
    },
        {
    "cost":-5200,
    "quantity":1,
    "unity":"DAY",
    "description":u"Remise exceptionnelle",
    "rowIndex":3,
    },

    ]
# Lines total should accept until 4 elements after the . (here they are *100)
# so it fits the limit case
est_lines_total = (12531.25,22500, -5200)
# Round function is launched after the tva count
est_tva = int((sum(est_lines_total) - est['discountHT'])*196/10000.0)
est_total = sum(est_lines_total) - est['discountHT'] + est['expenses'] + est_tva
est_deposit = int(est_total * float(est['deposit']) / 100.0)
est_sold = est_total - est_deposit

payment_lines = [
        {'rowIndex':1,
            'description':u"Solde",
            'amount':est_deposit,
            'paymentDate':datetime.date.today()}
        ]

class TestCompute(BaseTestCase):
    """
        Test the task computer object
    """
    def setUp(self):
        BaseTestCase.setUp(self)
        self.estimation = Estimation(**est)
        for l in est_lines:
            line = EstimationLine(**l)
            self.estimation.lines.append(line)
        for l in payment_lines:
            line = PaymentLine(**l)
            self.estimation.payment_lines.append(line)
        self.computer = TaskComputing(self.estimation)

    def test_compute_line_total(self):
        for i, line in enumerate(est_lines):
            self.assertEqual(self.computer.compute_line_total(
                EstimationLine(**line)), est_lines_total[i])

    def test_compute_lines_total(self):
        self.assertEqual(sum(est_lines_total),
                self.computer.compute_lines_total())

    def test_compute_totalht(self):
        self.assertEqual(self.computer.compute_totalht(),
                sum(est_lines_total) - self.estimation.discountHT)

    def test_compute_tva(self):
        self.assertEqual(self.computer.compute_tva(), est_tva)

    def test_compute_ttc(self):
        self.assertEqual(self.computer.compute_total(), est_total)

    def test_compute_deposit(self):
        self.assertEqual(self.computer.compute_deposit(), est_deposit)

    def test_compute_sold(self):
        self.assertEqual(self.computer.compute_sold(), est_sold)
        # Verify missing payment lines gives a correct sold
        estimation = Estimation(**est)
        for l in est_lines:
            estimation.lines.append(EstimationLine(**l))
        comp = TaskComputing(estimation)
        self.assertEqual(comp.compute_sold(), est_sold)

    def test_payments_sum(self):
        self.assertEqual(self.computer.compute_sold() + \
                         self.computer.compute_deposit(),
                            self.computer.compute_total())

