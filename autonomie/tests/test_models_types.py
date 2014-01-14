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

import os
import datetime
import time
from .base import BaseTestCase
from autonomie.models.types import CustomFileType
from autonomie.models.types import CustomDateType
from autonomie.models.types import CustomDateType2
from autonomie.models.types import CustomInteger

class TestCustomFileType(BaseTestCase):
    def test_bind(self):
        a = CustomFileType('test_', 255)
        cstruct1 = {'uid':'test_testfile.jpg', 'filename':'testfile.jpg'}
        self.assertEqual(a.process_bind_param(cstruct1, "nutt"),
                                                'testfile.jpg')

    def test_result(self):
        a = CustomFileType('test_', 255)
        cstruct1 = {'uid':'test_testfile.jpg', 'filename':'testfile.jpg'}
        self.assertEqual(a.process_result_value('testfile.jpg', 'nutt'),
                                            cstruct1)

class TestCustomDateType(BaseTestCase):
    def test_bind(self):
        os.environ['TZ'] = "Europe/Paris"
        a = CustomDateType()
        date = datetime.datetime(2012,1,1,1,1)
        self.assertEqual(a.process_bind_param(date, "nutt"),
                            1325376060)
        date = 1504545454
        self.assertEqual(a.process_bind_param(date, "nutt"),
                            1504545454)
        t = int(time.time())

        self.assertTrue(a.process_bind_param("", "nutt") >= t)
        self.assertTrue(a.process_bind_param("", "nutt") <= t + 6000)

    def test_result(self):
        os.environ['TZ'] = "Europe/Paris"
        a = CustomDateType()
        date = datetime.datetime(2012,1,1,1,1)
        timestamp = 1325376060
        self.assertEqual(a.process_result_value(timestamp, "nutt"),
                         date)

class TestCustomDateType2(BaseTestCase):
    def test_bind(self):
        a = CustomDateType2()
        date = datetime.date(2012, 11, 10)
        dbformat = 20121110
        self.assertEqual(a.process_bind_param(date, "Nutt"),
                         dbformat)

    def test_result(self):
        a = CustomDateType2()
        date = datetime.date(2012, 11, 10)
        dbformat = 20121110
        self.assertEqual(a.process_result_value(dbformat, "Nutt"),
                         date)

class TestCustomInterger(BaseTestCase):
    def test_bind(self):
        a = CustomInteger()
        vala = 1500
        valb = long(1500)
        self.assertEqual(a.process_bind_param(vala, "nutt"), valb)

    def test_result(self):
        a = CustomInteger()
        vala = long(1500)
        valb = 1500
        self.assertEqual(a.process_result_value(vala, "nutt"), valb)

