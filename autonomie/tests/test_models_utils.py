# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 31-07-2012
# * Last Modified :
#
# * Project :
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
