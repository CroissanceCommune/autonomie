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
from mock import MagicMock
from sqlalchemy import (
        Column,
        Integer,
        String,
        )
from autonomie.export import csvtools
from autonomie.models import DBBASE

class DummyModel(DBBASE):
    __tablename__ = 'test'
    id = Column('id', Integer, primary_key=True)
    col1 = Column(String(8))
    col2 = Column(String(8), info={'label':"Column 2"})


class TestCsvTools(unittest.TestCase):

    def test_collect_labels(self):
        labels = csvtools.collect_labels(DummyModel)
        expected_labels = ["id", "col1", "Column 2"]
        self.assertTrue(set(labels).difference(set(expected_labels)) == set([]))

    def test_collect_keys(self):
        keys = csvtools.collect_keys(DummyModel)
        expected_keys = ['id', 'col1', 'col2']
        self.assertTrue(set(keys).difference(set(expected_keys)) == set([]))

    def test_should_be_exported(self):
        col = MagicMock(info={'options':{'csv_exclude':True}})
        self.assertFalse(csvtools.should_be_exported(col))
        col = MagicMock(info={'options':{}})
        self.assertTrue(csvtools.should_be_exported(col))

