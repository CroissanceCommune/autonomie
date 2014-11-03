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
from autonomie.models.types import CustomFileType
from autonomie.models.types import CustomDateType
from autonomie.models.types import CustomDateType2
from autonomie.models.types import CustomInteger

def test_bind_customfiletype():
    a = CustomFileType('test_', 255)
    cstruct1 = {'uid':'test_testfile.jpg', 'filename':'testfile.jpg'}
    assert a.process_bind_param(cstruct1, "nutt") == 'testfile.jpg'

def test_result_customfiletype():
    a = CustomFileType('test_', 255)
    cstruct1 = {'uid':'test_testfile.jpg', 'filename':'testfile.jpg'}
    assert a.process_result_value('testfile.jpg', 'nutt') == cstruct1

def test_bind_customdatetype():
    os.environ['TZ'] = "Europe/Paris"
    a = CustomDateType()
    date = datetime.datetime(2012,1,1,1,1)
    assert a.process_bind_param(date, "nutt") == 1325376060
    date = 1504545454
    assert a.process_bind_param(date, "nutt") == 1504545454
    t = int(time.time())

    assert a.process_bind_param("", "nutt") >= t
    assert a.process_bind_param("", "nutt") <= t + 6000

def test_result_customdatetype():
    os.environ['TZ'] = "Europe/Paris"
    a = CustomDateType()
    date = datetime.datetime(2012,1,1,1,1)
    timestamp = 1325376060
    assert a.process_result_value(timestamp, "nutt") == date

def test_bind_customdatetype2():
    a = CustomDateType2()
    date = datetime.date(2012, 11, 10)
    dbformat = 20121110
    assert a.process_bind_param(date, "Nutt") == dbformat

def test_result_customdatetype2():
    a = CustomDateType2()
    date = datetime.date(2012, 11, 10)
    dbformat = 20121110
    assert a.process_result_value(dbformat, "Nutt") == date

def test_bind():
    a = CustomInteger()
    vala = 1500
    valb = long(1500)
    assert a.process_bind_param(vala, "nutt") == valb

def test_result():
    a = CustomInteger()
    vala = long(1500)
    valb = 1500
    assert a.process_result_value(vala, "nutt") == valb
