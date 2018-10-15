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
import locale
from autonomie.utils import strings

class TestIt(unittest.TestCase):
    def test_format_amount(self):
        a = 1525
        b = 1525.3
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        self.assertEqual(strings.format_amount(a), "15,25")
        self.assertEqual(strings.format_amount(a, trim=False), "15,25")

        self.assertEqual(strings.format_amount(b), "15,25")
        self.assertEqual(strings.format_amount(b, trim=False), "15,25")

        c = 210000
        self.assertEqual(
            strings.format_amount(c, grouping=False),
            "2100,00"
        )
        self.assertEqual(
            strings.format_amount(c, grouping=True),
            "2&nbsp;100,00"
        )

        c = 21000000.0
        self.assertEqual(
            strings.format_amount(c, trim=False, precision=5),
            "210,00"
        )
        c = 21000004.0
        self.assertEqual(
            strings.format_amount(c, trim=False,precision=5),
            "210,00004"
        )
        c = 21000040.0
        self.assertEqual(
            strings.format_amount(c, trim=False,precision=5),
            "210,0004"
        )

        self.assertEqual(
            strings.format_amount(c, trim=True, precision=5),
            "210,00"
        )
        c = 21012000.0
        self.assertEqual(
            strings.format_amount(c, trim=False, precision=5),
            "210,12"
        )

    def test_format_name(self):
        self.assertEqual(strings.format_name(None, u"LastName"),
                                                         u"LASTNAME ")
        self.assertEqual(strings.format_name(u"Firstname", None),
                                                        u" Firstname")


def test_format_float():
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    from autonomie.utils.strings import format_float

    assert format_float(1.256, precision=2) == "1,26"
    res = format_float(1265.254, precision=2, html=False)
    assert res == "1\xe2\x80\xaf265,25" or res == "1 265,25"
    assert format_float(1265.254, precision=2) == "1&nbsp;265,25"
    assert format_float(1265.254, precision=2, grouping=False) == "1265,25"
    assert format_float(1.256, precision=None) == "1.256"
