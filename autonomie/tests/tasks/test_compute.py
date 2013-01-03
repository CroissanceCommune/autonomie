# -*- coding: utf-8 -*-
# * File Name : test_compute.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-01-2013
# * Last Modified :
#
# * Project :
#
from autonomie.tests.base import BaseTestCase
from autonomie.models.task.compute import (LineCompute, TaskCompute,
        EstimationCompute, InvoiceCompute)

TASK = {"expenses":1500,}
LINES = [{'cost':10025, 'tva':1960, 'quantity':1.25},
         {'cost':7500,  'tva':1960, 'quantity':3},
         {'cost':-5200, 'tva':1960, 'quantity':1}]
DISCOUNTS = [{'amount':2000, 'tva':1960}]

# Values:
#         the money values are represented *100
#
# Rounding rules:
#         TVA, total_ttc and deposit are rounded (total_ht is not)

# Lines total should accept until 4 elements after the '.'(here they are *100)
# so it fits the limit case
#
# Line totals should be floats (here they are *100)
TASK_LINES_TOTAL_HT = (12531.25, 22500, -5200)
TASK_LINES_TVAS = (2456.125, 4410, -1019.2)

LINES_TOTAL_HT = sum(TASK_LINES_TOTAL_HT)
LINES_TOTAL_TVAS = sum(TASK_LINES_TVAS)

DISCOUNT_TOTAL_HT = sum([d['amount']for d in DISCOUNTS])
DISCOUNT_TVAS = (392,)
DISCOUNT_TOTAL_TVAS = sum(DISCOUNT_TVAS)

HT_TOTAL =  int(LINES_TOTAL_HT - DISCOUNT_TOTAL_HT)
TVA = int(LINES_TOTAL_TVAS - DISCOUNT_TOTAL_TVAS)

# TASK_TOTAL = lines + tva + expenses rounded
TASK_TOTAL = HT_TOTAL + TVA + TASK['expenses']

print "TASK_TOTAL : %s" % TASK_TOTAL


class Dummy(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DummyLine(Dummy, LineCompute):
    """
        Dummy line model
    """
    pass


class DummyTask(Dummy, TaskCompute):
    """
        Dummy task model
    """
    pass


class DummyInvoice(Dummy, InvoiceCompute):
    pass


class DummyEstimation(Dummy, EstimationCompute):
    pass


def get_lines(datas=LINES):
    lines = []
    for line in datas:
        lines.append(DummyLine(**line))
    return lines

def get_task(factory=DummyTask):
    t = factory(**TASK)
    t.lines = get_lines()
    t.discounts = get_lines(DISCOUNTS)
    return t

class TestTaskCompute(BaseTestCase):
    def test_lines_total_ht(self):
        task = get_task()
        self.assertEqual(task.lines_total_ht(), LINES_TOTAL_HT)

    def test_discounts_total_ht(self):
        task = get_task()
        self.assertEqual(task.discount_total_ht(), DISCOUNT_TOTAL_HT)

    def test_total_ht(self):
        est = get_task()
        self.assertEqual(est.total_ht(),
                    HT_TOTAL)

    def test_get_tvas(self):
        task = TaskCompute()
        task.lines = [DummyLine(cost=35000, quantity=1, tva=1960),
                      DummyLine(cost=40000, quantity=1, tva=550)]
        task.discounts = [DummyLine(amount=1200, tva=550),
                          DummyLine(amount=15000, tva=1960)]
        tvas = task.get_tvas()
        self.assertEqual(tvas.keys(), [1960, 550])
        self.assertEqual(tvas[1960], 3920)
        self.assertEqual(tvas[550], 2134)

    def test_tva_amount(self):
        # cf #501
        line = DummyLine(cost=5010, quantity=1, tva=1960)
        self.assertEqual(line.tva_amount(), 981.96)
        task = get_task()
        self.assertEqual(task.tva_amount(), TVA)

    def test_total_ttc(self):
        task = TaskCompute()
        task.lines = [DummyLine(cost=1030, quantity=1.25, tva=1960)]
        # cf ticket #501
        # line total : 12.875
        # tva : 2.5235 -> 2.52
        # A confirmer :l'arrondi ici bas
        # => total : 15.39 (au lieu de 15.395)
        self.assertEqual(task.total_ttc(), 1539)

    def test_total(self):
        est = get_task()
        self.assertEqual(est.total(), TASK_TOTAL)

    def test_no_tva(self):
        line = DummyLine(cost=3500, tva=-100)
        task = DummyTask(lines=[line])
        self.assertTrue(task.no_tva())

        line = DummyLine(cost=3500, tva=0)
        task = DummyTask(lines=[line])
        self.assertFalse(task.no_tva())

        line = DummyLine(cost=3500, tva=100)
        task.lines.append(line)
        self.assertFalse(task.no_tva())


class TestInvoiceCompute(BaseTestCase):
    def getOne(self):
        task = DummyInvoice()
        task.expenses = 0
        task.payments = [Dummy(amount=1500), Dummy(amount=1000)]
        task.lines =  [DummyLine(cost=6000, quantity=1, tva=0)]
        task.discounts = []
        return task

    def test_paid(self):
        task = self.getOne()
        self.assertEqual(task.paid(), 2500)

    def test_topay(self):
        task = self.getOne()
        self.assertEqual(task.topay(), 3500)


class TestEstimationCompute(BaseTestCase):
    def getOne(self):
        task = DummyEstimation()
        task.expenses = 0
        task.deposit = 20
        task.manualDeliverables = 0
        task.lines = [DummyLine(cost=10000, quantity=1, tva=1960)]
        task.discounts = []
        task.payment_lines = [Dummy(amount=1000),
                              Dummy(amount=1000),
                              Dummy(amount=150)]
        return task

    def test_deposit_amount(self):
        task = self.getOne()
        self.assertEqual(task.deposit_amount(), 2000)

    def test_get_nb_payment_lines(self):
        task = self.getOne()
        self.assertEqual(task.get_nb_payment_lines(), 3)

    def test_paymentline_amount(self):
        task = self.getOne()
        self.assertEqual(task.paymentline_amount(), 2666)

    def test_deposit_amount_ttc(self):
        task = self.getOne()
        # 2392 = 2000 * 119.6 / 100
        self.assertEqual(task.deposit_amount_ttc(), 2392)

    def test_sold(self):
        task = self.getOne()
        # 9568 = 11960 - 2392 - 2666 - 2666
        self.assertEqual(task.sold(), 4236)


class TestLineCompute(BaseTestCase):
    def test_line_compute(self):
        for index, line_obj in enumerate(get_lines()):
            self.assertEqual(line_obj.total_ht(), TASK_LINES_TOTAL_HT[index])
            self.assertEqual(line_obj.total(), TASK_LINES_TOTAL_HT[index] +\
                    TASK_LINES_TVAS[index])

    def test_discount_compute(self):
        for index, line_obj in enumerate(get_lines(DISCOUNTS)):
            self.assertEqual(line_obj.total_ht(), DISCOUNTS[index]['amount'])
            self.assertEqual(line_obj.total(), DISCOUNTS[index]['amount'] \
                    + DISCOUNT_TVAS[index])


