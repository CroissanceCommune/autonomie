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

from autonomie.compute.math_utils import (
    floor_to_precision,
    floor,
    amount,
    percent,
    percentage,
    convert_to_int,
    reverse_tva,
    compute_tva,
)


class TestMathUtils(unittest.TestCase):
    def test_floor(self):
        # Ref #727
        a = 292.65 * 100.0
        self.assertEqual(floor(a), 29265)
        a = 29264.91
        self.assertEqual(floor(a), 29265)
        self.assertEqual(floor(a, round_floor=True), 29264)
        a = 29264.5
        self.assertEqual(floor(a), 29265)

    def test_floor_to_precision(self):
        a = 299999
        self.assertEqual(floor_to_precision(a), 300000)
        a = 299455
        self.assertEqual(floor_to_precision(a), 299000)
        a = 299999
        self.assertEqual(floor_to_precision(a, round_floor=True), 299000)

    def test_amount(self):
        # Ref #727
        a = 192.65
        self.assertEqual(amount(a), 19265)
        a = 192.6555
        self.assertEqual(amount(a), 19266)
        self.assertEqual(amount(a, 4), 1926555)

    def test_percent(self):
        self.assertEqual(percent(30, 10), 300.0)
        self.assertEqual(percent(1, 3), 33.33)
        self.assertRaises(ZeroDivisionError, percent, 1, 0)
        self.assertEqual(percent(1, 0, 5), 5)

    def test_percentage(self):
        # Ref #32
        a = 0.25
        b = 10000
        self.assertEqual(percentage(a, b), 25)

    def test_convert_to_int(self):
        self.assertEqual(convert_to_int('25'), 25)
        self.assertEqual(convert_to_int('NOOK', 25), 25)
        self.assertRaises(ValueError, convert_to_int, 'NOOK')


def test_compute_tva():
    assert compute_tva(10000, 2000) == 2000


def test_reverse_tva():
    total_ttc = 1100.0
    tva = 10 * 100
    result = 1000
    assert reverse_tva(total_ttc, tva) == result
