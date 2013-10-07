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

import time
import datetime
import locale
from autonomie.tests.base import BaseTestCase
from autonomie.views import render_api

class TestIt(BaseTestCase):
    def test_its_in(self):
        for i in dir(render_api):
            if i.startswith('format_'):
                self.assertTrue(hasattr(render_api.api, i))

    def test_format_amount(self):
        a = 1525
        b = 1525.3
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        self.assertEqual(render_api.format_amount(a), "15,25")
        self.assertEqual(render_api.format_amount(a, False), "15,25")
        self.assertEqual(render_api.format_amount(b), "15,25")
        self.assertEqual(render_api.format_amount(b, False), "15,253")

    def test_format_name(self):
        self.assertEqual(render_api.format_name(None, u"LastName"),
                                                         u" LASTNAME")
        self.assertEqual(render_api.format_name(u"Firstname", None),
                                                        u"Firstname ")
