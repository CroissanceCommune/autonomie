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
