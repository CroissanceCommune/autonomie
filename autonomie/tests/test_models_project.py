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

from mock import MagicMock
from autonomie.models.project import Project
from .base import BaseTestCase

PROJECT = dict(name=u'project1',
               code=u"PRO1",
               company_id=1,
                )

EST_LIST1 = ["Devis 1", "Devis 3"]
EST_LIST2 = ["Devis 1", "Devis deoko"]
INV_LIST1 = ['Facture 1', "Facture d'acompte 2", "Facture 5"]
INV_LIST2 = ['Facture 1', "Facture d'acompte 1", "Facture d'acompte 2"]
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
