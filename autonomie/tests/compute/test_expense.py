# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
import pytest

from mock import MagicMock
from autonomie.compute.expense import (
    ExpenseCompute,
    ExpenseLineCompute,
    ExpenseKmLineCompute,
)


@pytest.fixture
def simple_type():
    return MagicMock(type='expense')


@pytest.fixture
def teltype():
    return MagicMock(percentage=50.415, type='expensetel')


@pytest.fixture
def kmtype():
    return MagicMock(amount=0.38888, label="", code="")


class DummyAmount(object):
    def __init__(self, amount):
        self.amount = amount

    def get_amount(self):
        return self.amount


def test_expense_compute():
    sheet = ExpenseCompute()
    sheet.lines = (MagicMock(total=10), MagicMock(total=20))
    sheet.kmlines = (MagicMock(total=10), MagicMock(total=60))
    assert sheet.total == 100
    sheet.payments = (DummyAmount(amount=15), DummyAmount(amount=15),)
    assert sheet.topay() == 70
    assert sheet.paid() == 30


def test_expense_line_compute(teltype):
    compute = ExpenseLineCompute()
    compute.type_object = teltype
    assert compute._compute_value(99.53) == 50


def test_expense_kmline_compute(kmtype):
    compute = ExpenseKmLineCompute()
    compute.type_object = kmtype
    compute.km = 100
    assert compute.total == 39


def test_expense_line(simple_type):
    compute = ExpenseLineCompute()
    compute.type_object = simple_type
    assert compute._compute_value(99.53) == 100


def test_real_world_error(mk_expense_type):
    from autonomie.models.expense.sheet import (
        ExpenseKmLine,
        ExpenseLine,
    )
    # test based on a real world problem that raised the error
    kmtype = mk_expense_type(amount=0.38)
    kmlines = []
    for km in [3000, 2800, 280, 200, 540, 2800, 3600, 3000, 3000, 4400, 2000, 3000, 4600]:
        compute = ExpenseKmLineCompute()
        compute.km = km
        compute.type_object = kmtype
        kmlines.append(compute)

    teltype = mk_expense_type(percentage=50)
    telline = ExpenseLineCompute()
    telline.ht = 2666
    telline.tva = 533
    telline.type_object = teltype

    km_lines_total = sum(l.total for l in kmlines)
    km_lines_rounded_total = int(sum(l.total_ht for l in kmlines))
    km_lines_linerounded_total = sum(int(l.total_ht) for l in kmlines)

    telline_total = telline.total
    telline_rounded_total = int(telline.total_tva) + int(telline.total_ht)

    last_rounded_total = int(km_lines_total + telline_total)
    byproduct_rounded_total = km_lines_rounded_total + telline_rounded_total
    byline_rounded_total = km_lines_linerounded_total + telline_rounded_total

    # Option 1
    assert last_rounded_total == byline_rounded_total
    # Option 2
    assert last_rounded_total == byproduct_rounded_total
