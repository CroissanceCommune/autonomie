# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 08-09-2010
# * Last Modified :
#
# * Project :
#
import unittest
from mock import MagicMock
from sqlalchemy import (
        Column,
        Integer,
        String,
        )
from autonomie.utils import csvtools
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

