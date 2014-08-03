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
import datetime
from autonomie.export import base, csvtools, excel
from sqlalchemy import (
        Column,
        Integer,
        String,
        DateTime,
        )

from autonomie.models import DBBASE
from autonomie.tests.base import Dummy

class DummyModel(DBBASE):
    __tablename__ = 'test'
    id = Column(
        'id',
        Integer,
        primary_key=True,
        info={'export':{'exclude':True}}
    )
    col1 = Column(
        String(8)
    )
    col2 = Column(
        String(8),
        info={'export':{'label':"Column 2"}}
    )
    col3 = Column(
        String(8),
        info={'export':{'label':"main_label", 'csv': {'label':'Csv label'}}},
    )
    col4 = Column(
        String(8),
        info={'export':{
            'label':"not now",
            'csv': {'label':'Csv label'},
            'excel': {'label': 'Excel label',
                      'formatter': lambda x:2*x },
        }
        },
    )
    col5 = Column(
        DateTime(),
    )

col5_val = datetime.datetime(2014, 07, 05, 12, 45)


def test_collect_headers_csv():
    a = csvtools.SqlaCsvExporter(DummyModel)
    labels = [h['label'] for h in a.headers]
    assert labels == ['col1', "Column 2", 'Csv label', 'Csv label', 'col5']

def test_collect_headers_excel():
    b = excel.SqlaXlsExporter(DummyModel)
    labels = [h['label'] for h in b.headers]
    assert labels == ['col1', "Column 2", 'main_label', 'Excel label', 'col5']


def test_format_row_csv():
    a = csvtools.SqlaCsvExporter(DummyModel)
    a.add_row(Dummy(col1=1, col2=1, col3=1, col4=1, col5=col5_val))
    for i in ['col1', "Column 2", 'Csv label', 'Csv label']:
        assert i in a._datas[0].keys()

def test_format_row_excel():
    a = excel.SqlaXlsExporter(DummyModel)
    a.add_row(Dummy(col1=1, col2=2, col3=3, col4=4, col5=col5_val))
    assert a._datas == [
        [1,2,3,8, u'05/07/2014 à 12:45'],
    ]
