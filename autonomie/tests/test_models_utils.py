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

import datetime
import unittest

from autonomie.models.utils import format_to_taskdate
from autonomie.models.utils import format_from_taskdate

class TestUtils(unittest.TestCase):
    def test_format_to_taskdate(self):
        date1 = datetime.date(2012, 1, 10)
        date2 = datetime.date(2012, 12, 10)
        date3 = datetime.date(2012, 7, 1)
        # bug #529
        date4 = datetime.date(2012, 7, 31)
        self.assertEqual(format_to_taskdate(date1), 20120110)
        self.assertEqual(format_to_taskdate(date2), 20121210)
        self.assertEqual(format_to_taskdate(date3), 20120701)
        self.assertEqual(format_to_taskdate(date4), 20120731)

    def test_format_from_taskdate(self):
        date1 = datetime.date(2012, 1, 10)
        date2 = datetime.date(2012, 12, 10)
        date3 = datetime.date(2012, 7, 1)
        # bug #529
        date4 = datetime.date(2012, 7, 31)
        self.assertEqual(format_from_taskdate(20120110), date1)
        self.assertEqual(format_from_taskdate(20121210), date2)
        self.assertEqual(format_from_taskdate(20120701), date3)
        self.assertEqual(format_from_taskdate(20120731), date4)
