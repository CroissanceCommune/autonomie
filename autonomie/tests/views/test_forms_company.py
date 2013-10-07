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
