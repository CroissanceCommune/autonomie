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
from pytest import fixture
from mock import MagicMock
from autonomie.models.project import Project

PROJECT = dict(name=u'project1',
               code=u"PRO1",
               company_id=1,
                )

EST_LIST = ["Devis 1", "Devis deoko"]
INV_LIST = ['Facture 1', "Facture d'acompte 2", "Facture 5"]
CINV_LIST = ["Avoir 1", "Avoir 4"]

@fixture()
def project():
    p = Project(**PROJECT)
    for i in EST_LIST:
        p.tasks.append(MagicMock(number=i, type_='estimation'))
    for i in INV_LIST:
        p.tasks.append(MagicMock(number=i, type_='invoice'))
    for i in CINV_LIST:
        p.tasks.append(MagicMock(number=i, type_='cancelinvoice'))
    return p


def test_get_number():
    test_str = "Devis 5"
    assert Project.get_number(test_str, "Devis ") == 5
    assert Project.get_number(test_str, "Devistoto") == 0

def test_get_next_estimation_number(project):
    assert project.get_next_estimation_number() == 3

def test_get_next_invoice_number(project):
    assert project.get_next_invoice_number() == 6
    project.tasks = []
    assert project.get_next_invoice_number() == 1

def test_get_next_cancelinvoice_number(project):
    print(project.tasks)
    assert project.get_next_cancelinvoice_number() == 5
