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
from autonomie.models.company import Company
from .base import BaseTestCase

TEST = dict(name=u"Test",
            logo=u"logo.png",
            header=u"header.png",
            id=1)


class TestCompanyModel(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.company = Company(name=u"Test", id=1)
        self.company.logo = dict(filename=u"logo.png")
        self.company.header = dict(filename=u"header.png")

    def test_get_path(self):
        self.assertEqual(self.company.get_path(), "company/1")
        self.assertEqual(self.company.get_logo_filepath(), "company/1/logo/logo.png")
        self.assertEqual(self.company.get_header_filepath(), "company/1/header/header.png")

    def test_get_company_id(self):
        self.assertEqual(self.company.get_company_id(), 1)
