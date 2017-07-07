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
from autonomie.compute.task import (
    LineCompute,
    DiscountLineCompute,
    GroupCompute,
    TaskCompute,
    EstimationCompute,
    InvoiceCompute,
)
from autonomie.compute import math_utils

TASK = {"expenses":1500000, "expenses_ht":1000000}
LINES = [
    [
        {'cost':10025000, 'tva': 1960, 'quantity': 1.25},
        {'cost':7500000,  'tva': 1960, 'quantity': 3},
        {'cost':-5200000, 'tva': 1960, 'quantity': 1},
#        {'cost':2, 'tva':1960, 'quantity': 1},
#        {'cost':100000, 'tva':1960, 'quantity': 0.00003},
    ],
    [
        {'cost':10025000, 'tva':1960, 'quantity':1.25},
        {'cost':7500000,  'tva':1960, 'quantity':3},
        {'cost':-5200000, 'tva':1960, 'quantity':1},
#        {'cost':2, 'tva':1960, 'quantity': 1},
#        {'cost':100000, 'tva':1960, 'quantity': 0.00003},
    ],
]
DISCOUNTS = [{'amount': 2000000, 'tva':1960}]

# Values:
#         the money values are represented *100000
#
# Rounding rules:
#         TVA, total_ttc and deposit are rounded (total_ht is not)

# Lines total should be integers (here they are
# *100000) so it fits the limit case
#
# Line totals should be integers (here they are *100000)
from autonomie.tests.base import Dummy
TASK_LINES_TOTAL_HT = (12531250.0, 22500000, -5200000, ) # 2, 3 )
TASK_LINES_TVAS = (2456125, 4410000, -1019200, )  # 0.392, 0.588)

LINES_TOTAL_HT = sum(TASK_LINES_TOTAL_HT) * 2
LINES_TOTAL_TVAS = sum(TASK_LINES_TVAS) * 2
EXPENSE_TVA = 196000

DISCOUNT_TOTAL_HT = sum([d['amount']for d in DISCOUNTS])
DISCOUNT_TVAS = (392000,)
DISCOUNT_TOTAL_TVAS = sum(DISCOUNT_TVAS)

# Totals should be multiple of 1000 (ending to be floats with 2 numbers after
# the comma
HT_TOTAL =  math_utils.floor_to_precision(
    LINES_TOTAL_HT - DISCOUNT_TOTAL_HT + TASK['expenses_ht']
)
TVA = math_utils.floor_to_precision(
    LINES_TOTAL_TVAS - DISCOUNT_TOTAL_TVAS + EXPENSE_TVA
)

# TASK_TOTAL = lines + tva + expenses rounded
TASK_TOTAL = HT_TOTAL + TVA + TASK['expenses']


class DummyLine(Dummy, LineCompute):
    """
        Dummy line model
    """
    pass


class DummyGroup(Dummy, GroupCompute):
    """
    dummy line group model
    """
    pass


class DummyTask(Dummy, TaskCompute):
    """
        Dummy task model
    """
    pass


class DummyDiscountLine(Dummy, DiscountLineCompute):
    pass


class DummyInvoice(Dummy, InvoiceCompute):
    cancelinvoices = []
    pass


class DummyCancelInvoice(Dummy, TaskCompute):
    status = 'valid'


class DummyEstimation(Dummy, EstimationCompute):
    pass


@pytest.fixture
def group():
    group = DummyGroup()
    group.lines = [DummyLine(cost=0.001, quantity=0.1)]
    return group


def get_lines(datas, factory=DummyLine):
    lines = []
    for line in datas:
        lines.append(DummyLine(**line))
    return lines


def get_groups():
    groups = []
    for group in LINES:
        g = DummyGroup(lines=[])
        g.lines = get_lines(group)
        groups.append(g)
    return groups


def get_task(factory=DummyTask):
    t = factory(**TASK)
    t.line_groups = get_groups()
    t.discounts = get_lines(DISCOUNTS, factory=DummyDiscountLine)
    return t


@pytest.fixture
def def_tva():
    return MagicMock(
        name="tva1",
        value=1960,
        default=0,
        compte_cg="TVA0001",
        compte_a_payer="TVAAPAYER0001",
        code='CTVA0001'
    )


@pytest.fixture
def tva10():
    return MagicMock(
        name="tva 10%",
        value=1000,
        default=0,
        compte_cg="TVA10",
        code='CTVA10'
    )


@pytest.fixture
def invoice_bug363(def_tva, tva10):
    prod = MagicMock(name="product 2", compte_cg="P0002", tva=tva10)
    lines = []

    for cost, qtity in (
        (15000000, 1),
        (2000000, 86),
        (-173010000, 1),
        (10000000, 1),
        (-201845000, 1),
        (4500000, 33),
        (1800000, 74),
        (3500000, 28),
    ):
        lines.append(
            DummyLine(
                cost=cost,
                quantity=qtity,
                tva=tva10.value,
                product=prod,
                tva_object=tva10
            )
        )

    group = DummyGroup(lines=lines)
    company = Dummy(name="company", code_compta='COMP_CG', contribution=None)
    customer = Dummy(name="customer", compte_tiers="CUSTOMER",
                     compte_cg='CG_CUSTOMER')
    invoice = TaskCompute()
    invoice.default_tva = def_tva.value
    invoice.expenses_tva = def_tva.value
    invoice.date = datetime.date(2016, 05, 04)
    invoice.customer = customer
    invoice.company = company
    invoice.official_number = "INV_002"
    invoice.line_groups = [group]
    invoice.all_lines = group.lines
    invoice.expenses_ht = 0
    invoice.expenses = 0
    return invoice


class TestTaskCompute():
    def test_lines_total_ht(self):
        task = get_task()
        assert task.groups_total_ht() == LINES_TOTAL_HT

    def test_discounts_total_ht(self):
        task = get_task()
        assert task.discount_total_ht() == DISCOUNT_TOTAL_HT

    def test_total_ht(self):
        est = get_task()
        assert est.total_ht() == HT_TOTAL

    def test_get_tvas(self):
        task = get_task()
        tvas = task.get_tvas()
        assert tvas[1960] == TVA

    def test_get_tvas_multiple(self):
        task = TaskCompute()
        task.line_groups = [DummyGroup(
            lines=[
                DummyLine(cost=35000000, quantity=1, tva=1960),
                DummyLine(cost=40000000, quantity=1, tva=550)
            ]
        )]
        task.discounts = [DummyDiscountLine(amount=1200000, tva=550),
                          DummyDiscountLine(amount=15000000, tva=1960)]
        tvas = task.get_tvas()
        assert tvas.keys() == [1960, 550]
        assert tvas[1960] == 3920000
        assert tvas[550] == 2134000

    def test_get_tvas_multiple_rounding(self):
        task = TaskCompute()
        task.line_groups = [DummyGroup(
            lines=[
                DummyLine(cost=10004000, quantity=1, tva=1000),
                DummyLine(cost=5002000, quantity=1, tva=2000),
            ]
        )]
        # Ref https://github.com/CroissanceCommune/autonomie/issues/305
        tvas = task.get_tvas()
        assert tvas[1000] == 1000000
        assert task.tva_amount() == 2000000

    def test_tva_amount(self):
        # cf #501
        line = DummyLine(cost=5010000, quantity=1, tva=1960)
        assert line.tva_amount() == 981960
        task = get_task()
        assert task.tva_amount() == TVA

    def test_total_ttc(self):
        task = TaskCompute()
        task.line_groups = [DummyGroup(
            lines=[DummyLine(cost=1030000, quantity=1.25, tva=1960)]
        )]
        # cf ticket #501
        # line total : 12.875
        # tva : 2.5235 -> 2.52
        # => total : 15.40 (au lieu de 15.395)
        assert task.total_ttc() == 1540000

    def test_total(self):
        est = get_task()
        assert est.total() == TASK_TOTAL

    def test_no_tva(self):
        line = DummyLine(cost=3500000, tva=-100)
        group = DummyGroup(lines=[line])
        task = DummyTask(line_groups=[group])
        assert task.no_tva()

        line = DummyLine(cost=3500000, tva=0)
        group = DummyGroup(lines=[line])
        task = DummyTask(line_groups=[group])
        assert not task.no_tva()

        line = DummyLine(cost=3500000, tva=100)
        group = DummyGroup(lines=[line])
        task = DummyTask(line_groups=[group])
        assert not task.no_tva()

    def test_get_tvas_by_product(self, invoice_bug363):
        assert invoice_bug363.get_tvas_by_product()['P0002'] == 20185000

    def test_get_tva_ht_parts(self):
        task = TaskCompute()
        task.expenses_tva = 2000
        task.line_groups = [DummyGroup(
            lines=[
                DummyLine(cost=-120000000, quantity=1, tva=2000),
                DummyLine(cost=-120000000, quantity=0.5, tva=2000),
            ]
        )]
        task.expenses_ht = -36000000
        assert task.tva_ht_parts()[2000] == -216000000.0


class TestInvoiceCompute():
    def getOne(self):
        task = DummyInvoice()
        task.expenses = 0
        task.payments = [Dummy(amount=1500000), Dummy(amount=1000000)]
        task.line_groups =  [DummyGroup(
            lines=[DummyLine(cost=6000000, quantity=1, tva=0)]
        )]
        task.discounts = []
        return task

    def test_paid(self):
        task = self.getOne()
        assert task.paid() == 2500000

    def test_topay(self):
        task = self.getOne()
        assert task.topay() == 3500000

    def test_topay_with_cancelinvoice(self):
        task = self.getOne()
        cinv1 = DummyCancelInvoice()
        cinv1.line_groups = [DummyGroup(
            lines=[DummyLine(cost=-500000, quantity=1, tva=0)]
        )]
        cinv2 = DummyCancelInvoice()
        cinv2.line_groups = [DummyGroup(
            lines=[DummyLine(cost=-600000, quantity=1, tva=0)]
        )]
        task.cancelinvoices = [cinv1, cinv2]
        assert task.cancelinvoice_amount() == 1100000
        assert task.topay() == 2400000


class TestEstimationCompute():
    def getOne(self):
        task = DummyEstimation()
        task.expenses_ht = 20000
        task.deposit = 20
        task.manualDeliverables = 0
        task.line_groups = [
            DummyGroup(
                lines=[
                    DummyLine(cost=5000000, quantity=1, tva=1960),
                    DummyLine(cost=5000000, quantity=1, tva=1960),
                    DummyLine(cost=1000000, quantity=1, tva=500),
                ]
            )
        ]
        task.discounts = []
        task.payment_lines = [Dummy(amount=4000000),
                              Dummy(amount=6000000),
        # le dernier montant ne compte pas (le solde est calculé)
                              Dummy(amount=50000)]
        return task

    def test_add_ht_by_tva(self):
        lines = [DummyLine(cost=5000000, quantity=1, tva=1960),
                DummyLine(cost=1000000, quantity=1, tva=500)]
        task = self.getOne()
        dico = {}
        task.add_ht_by_tva(dico, lines)
        assert dico.keys() == [1960, 500]

    #Deposit
    def test_deposit_amounts(self):
        task = self.getOne()
        amounts = task.deposit_amounts()
        assert amounts.keys() == [1960, 500]
        assert amounts[1960] == 2004000
        assert amounts[500] == 200000

    def test_deposit_amount_ttc(self):
        task = self.getOne()
        # 2606780 = 2004000 * 119.6 / 100 + 200000 * 105/100
        assert task.deposit_amount_ttc() == 2607000

    # Payment lines (with equal repartition)
    def test_get_nb_payment_lines(self):
        task = self.getOne()
        assert task.get_nb_payment_lines() == 3

    def test_paymentline_amounts(self):
        task = self.getOne()
        amounts = task.paymentline_amounts()
        assert amounts.keys() == [1960, 500]
        assert int(amounts[1960]) == 2672000
        assert int(amounts[500]) == 266666

    def test_paymentline_amount_ttc(self):
        task = self.getOne()
        # 3475.712 = 2672 * 119.6/100 + 266 * 105/100.0
        assert task.paymentline_amount_ttc() == 3476000

    def test_sold(self):
        task = self.getOne()
        sold = task.sold()
        deposit = task.deposit_amount_ttc()
        paymentline = task.paymentline_amount_ttc()
        nblines = task.get_nb_payment_lines() -1
        assert sold + deposit + paymentline * nblines ==  task.total()

    # Payment lines (with non manual repartition)
    def test_manual_payment_line_amounts(self):
        def compute_payment_ttc(payment):
            total = 0
            for tva, ht in payment.items():
                line = DummyLine(tva=tva, cost=ht)
                total += line.total()
            return total

        task = self.getOne()
        task.manualDeliverables = 1
        payments = task.manual_payment_line_amounts()
        assert payments[0].keys() == [1960]
        assert payments[1].keys() == [1960, 500]
        assert payments[2].keys() == [500]
        deposit = task.deposit_amount_ttc()
        amount1 = compute_payment_ttc(payments[0])
        amount2 = compute_payment_ttc(payments[1])
        assert math_utils.floor(amount1) == 4000000
        assert math_utils.floor(amount2) == 6000000
        total = task.sold() + deposit + amount1 + amount2
        assert math_utils.floor_to_precision(total) == task.total()


class TestLineCompute():
    def test_line_compute(self):
        for index, line_obj in enumerate(get_lines(LINES[0])):
            assert line_obj.total_ht() == TASK_LINES_TOTAL_HT[index]
            assert line_obj.total() == TASK_LINES_TOTAL_HT[index] +\
                    TASK_LINES_TVAS[index]

    def test_discount_compute(self):
        for index, line_obj in enumerate(get_lines(DISCOUNTS)):
            assert line_obj.total_ht() == DISCOUNTS[index]['amount']
            assert line_obj.total() == DISCOUNTS[index]['amount'] \
                    + DISCOUNT_TVAS[index]


class TestGroupCompute():
    def test_cents(self, group):
        assert group.total_ht() == 0.0001
