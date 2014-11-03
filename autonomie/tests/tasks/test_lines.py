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

from autonomie.models.task import (InvoiceLine, CancelInvoiceLine,
                                        EstimationLine, PaymentLine)


LINE = {'description':u'text1', 'cost':10025, 'tva':1960,
          'unity':'DAY', 'quantity':1.25, 'rowIndex':1}

PAYMENT_LINE = {'description':u"Début",
                "paymentDate":datetime.date(2012, 12, 12),
                "amount":1000,
                "rowIndex":1}

class TestEstimationLine(unittest.TestCase):
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

class TestInvoiceLine(unittest.TestCase):
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

class TestCancelInvoiceLine(unittest.TestCase):
    def test_duplicate_line(self):
        line = CancelInvoiceLine(**LINE)
        dline = line.duplicate()
        for i in ('rowIndex', 'cost', 'tva', "description", "quantity", "unity"):
            self.assertEqual(getattr(dline, i), getattr(line, i))

    def test_total(self):
        i = CancelInvoiceLine(cost=1.25, quantity=1.25, tva=1960)
        self.assertEqual(i.total_ht(), 1.5625)
        self.assertEqual(i.total(), 1.86875)

class TestPaymentLine(unittest.TestCase):
    def test_duplicate(self):
        line = PaymentLine(**PAYMENT_LINE)
        dline = line.duplicate()
        for i in ('rowIndex', 'description', 'amount'):
            self.assertEqual(getattr(line, i), getattr(dline, i))
        today = datetime.date.today()
        self.assertEqual(dline.paymentDate, today)

