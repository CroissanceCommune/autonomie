# -*- coding: utf-8 -*-
# * File Name : test_models_project.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 23-08-2012
# * Last Modified :
#
# * Project :
#
from mock import MagicMock
from autonomie.models.project import Project
from .base import BaseTestCase

PROJECT = dict(name=u'project1',
               code=u"PRO1",
               id_company=1,
               code_client=u"CLI1")

EST_LIST1 = ["Devis 1", "Devis 3"]
EST_LIST2 = ["Devis 1", "Devis deoko"]
INV_LIST1 = ['Facture 1', "Facture d'accompte 2", "Facture 5"]
INV_LIST2 = ['Facture 1', "Facture d'accompte 1", "Facture d'accompte 2"]
CINV_LIST1 = ["Avoir 1", "Avoir 4"]

def get_project():
    return Project(**PROJECT)

def get_mocks(_list):
    mocks = []
    for i in _list:
        mock = MagicMock()
        mock.number = i
        mocks.append(mock)
    return mocks

class TestProjectModel(BaseTestCase):
    def get_number(self):
        test_str = "Devis 5"
        self.assertEqual(Project.get_number(test_str, "Devis "), 5)
        self.assertEqual(Project.get_number(test_str, "Devistoto"), 0)

    def test_get_next_estimation_number(self):
        for elist, result in ((EST_LIST1, 4),  (EST_LIST2, 3)):
            p1 = get_project()
            for i in get_mocks(elist):
                p1.estimations.append(i)
            self.assertEqual(p1.get_next_estimation_number(), result)

    def test_get_next_invoice_number(self):
        for ilist, result in ((INV_LIST1, 6), ([], 1), (INV_LIST2, 4)):
            p1 = get_project()
            for i in get_mocks(ilist):
                p1.invoices.append(i)
            self.assertEqual(p1.get_next_invoice_number(), result)

    def test_get_next_cancelinvoice_number(self):
        for clist, result in ((CINV_LIST1, 5), ([], 1)):
            p1 = get_project()
            for i in get_mocks(clist):
                p1.cancelinvoices.append(i)
            self.assertEqual(p1.get_next_cancelinvoice_number(), result)
