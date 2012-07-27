# -*- coding: utf-8 -*-
# * File Name : test_models_types.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 27-07-2012
# * Last Modified :
#
# * Project :
#
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

