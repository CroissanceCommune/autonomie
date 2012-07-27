# -*- coding: utf-8 -*-
# * File Name : test_models_company.py
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
