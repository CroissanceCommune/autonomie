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
from autonomie.models.expense import (
    ExpenseLine,
    ExpenseKmLine,
    ExpenseKmType,
    ExpenseTelType,

)

def test_ht_computing():
    # test based on a real world problem that raised the error
    kmtype = ExpenseKmType(amount=0.38, label="", code="")
    kmlines = []
    for km in [3000, 2800, 280, 200, 540, 2800, 3600, 3000, 3000, 4400, 2000, 3000, 4600]:
        kmlines.append(ExpenseKmLine(km=km, description="", type_object=kmtype))

    teltype = ExpenseTelType(percentage=50, label="", code="")
    telline = ExpenseLine(ht=2666, tva=533, description="", type_object=teltype)

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
