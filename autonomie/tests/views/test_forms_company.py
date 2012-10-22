# -*- coding: utf-8 -*-
# * File Name : test_forms_company.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 22-10-2012
# * Last Modified :
#
# * Project :
#
from mock import MagicMock
from autonomie.views.forms.company import get_upload_options_from_request

from autonomie.tests.base import BaseViewTest

class TestCompany(BaseViewTest):
    def test_get_upload_options_from_request(self):
        req = self.get_csrf_request()
        company = MagicMock()
        company.get_path = lambda :"25"
        req.context = company
        self.assertEqual(get_upload_options_from_request(req, "logo"),
                                    ("/tmp/25/logo", "/assets/25/logo"))
        self.assertEqual(get_upload_options_from_request(req, "header"),
                                    ("/tmp/25/header", "/assets/25/header"))

