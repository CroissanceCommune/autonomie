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
"""
Expense computing tool
"""
from autonomie.compute import math_utils


class ExpenseCompute(object):
    lines = ()
    kmlines = ()

    def get_lines_by_type(self):
        """
        Return expense lines grouped by treasury code
        """
        ret_dict = {}
        for line in self.lines:
            ret_dict.setdefault(line.type_object.code, []).append(line)
        for line in self.kmlines:
            ret_dict.setdefault(line.type_object.code, []).append(line)

        return ret_dict.values()

    @property
    def total(self):
        return sum(
            [line.total for line in self.lines]
        ) + sum(
            [line.total for line in self.kmlines]
        )


class ExpenseLineCompute(object):
    """
    Expense lines related computation tools
    """
    type_object = None

    def _compute_value(self, val):
        result = 0
        if self.type_object is not None:
            if self.type_object.type == 'expensetel':
                percentage = self.type_object.percentage
                val = val * percentage / 100.0
            result = math_utils.floor(val)
        return result

    @property
    def total(self):
        return self.total_ht + self.total_tva

    @property
    def total_ht(self):
        return self._compute_value(self.ht)

    @property
    def total_tva(self):
        return self._compute_value(self.tva)


class ExpenseKmLineCompute(object):
    type_object = None

    @property
    def total(self):
        indemnity = self.type_object.amount
        return math_utils.floor(indemnity * self.km)

    @property
    def ht(self):
        # Deprecated function kept for compatibility
        return self.total

    @property
    def total_ht(self):
        return self.total

    @property
    def total_tva(self):
        return 0
