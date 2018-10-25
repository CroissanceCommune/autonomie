# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
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
from autonomie.models.expense.sheet import (
    ExpenseKmLine,
    ExpenseSheet,
)


def test_expensekm_duplicate_ref_7774(mk_expense_type):
    kmtype = mk_expense_type(amount=1, year=2018)
    line = ExpenseKmLine(description="", km="", type_object=kmtype)

    sheet = ExpenseSheet(year=2019, month=1)
    assert line.duplicate(sheet) is None

    kmtype2019 = mk_expense_type(amount=1, year=2019)
    assert line.duplicate(sheet).type_object == kmtype2019
