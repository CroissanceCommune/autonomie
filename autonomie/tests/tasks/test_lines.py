# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 17-12-2012
# * Last Modified :
#
# * Project :
#
import datetime

from autonomie.tests.base import BaseTestCase
from autonomie.models.task import (InvoiceLine, CancelInvoiceLine,
                                        EstimationLine, PaymentLine)


LINE = {'description':u'text1', 'cost':10025, 'tva':1960,
          'unity':'DAY', 'quantity':1.25, 'rowIndex':1}

PAYMENT_LINE = {'description':u"Début",
                "paymentDate":datetime.date(2012, 12, 12),
                "amount":1000,
                "rowIndex":1}

class TestEstimationLine(BaseTestCase):
    def test_duplicate_line(self):
        line = EstimationLine(**LINE)
        dline = line.duplicate()
        for i in ('rowIndex', 'cost', 'tva', "description", "quantity", "unity"):
            self.assertEqual(getattr(dline, i), getattr(line, i))

    def test_gen_invoiceline(self):
        line = EstimationLine(**LINE)
        iline = line.gen_invoice_line()
        for i in ('rowIndex', 'cost', 'tva', "description", "quantity", "unity"):
            self.assertEqual(getattr(line, i), getattr(iline, i))

    def test_total(self):
        i = EstimationLine(cost=1.25, quantity=1.25, tva=1960)
        self.assertEqual(i.total_ht(), 1.5625)
        self.assertEqual(i.total(), 1.86875)

class TestInvoiceLine(BaseTestCase):
    def test_duplicate_line(self):
        line = InvoiceLine(**LINE)
        dline = line.duplicate()
        for i in ('rowIndex', 'cost', 'tva', "description", "quantity", "unity"):
            self.assertEqual(getattr(dline, i), getattr(line, i))


    def test_gen_cancelinvoice_line(self):
        line = InvoiceLine(**LINE)
        cline = line.gen_cancelinvoice_line()
        for i in ('rowIndex', "description", 'tva', "quantity", "unity"):
            self.assertEqual(getattr(cline, i), getattr(line, i))
        self.assertEqual(cline.cost, -1 * line.cost)

    def test_total(self):
        i = InvoiceLine(cost=1.25, quantity=1.25, tva=1960)
        self.assertEqual(i.total_ht(), 1.5625)
        self.assertEqual(i.total(), 1.86875)

class TestCancelInvoiceLine(BaseTestCase):
    def test_duplicate_line(self):
        line = CancelInvoiceLine(**LINE)
        dline = line.duplicate()
        for i in ('rowIndex', 'cost', 'tva', "description", "quantity", "unity"):
            self.assertEqual(getattr(dline, i), getattr(line, i))

    def test_total(self):
        i = CancelInvoiceLine(cost=1.25, quantity=1.25, tva=1960)
        self.assertEqual(i.total_ht(), 1.5625)
        self.assertEqual(i.total(), 1.86875)

class TestPaymentLine(BaseTestCase):
    def test_duplicate(self):
        line = PaymentLine(**PAYMENT_LINE)
        dline = line.duplicate()
        for i in ('rowIndex', 'description', 'amount'):
            self.assertEqual(getattr(line, i), getattr(dline, i))
        today = datetime.date.today()
        self.assertEqual(dline.paymentDate, today)

