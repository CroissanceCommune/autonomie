# -*- coding: utf-8 -*-
# * File Name : test_views_render_api.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 31-08-2012
# * Last Modified :
#
# * Project :
#
import time
import datetime
import locale
from .base import BaseTestCase
from autonomie.views import render_api

class TestIt(BaseTestCase):
    def test_its_in(self):
        for i in dir(render_api):
            if i.startswith('format_'):
                self.assertTrue(hasattr(render_api.api, i))

    def test_format_amount(self):
        a = 1525
        b = 1525.3
        locale.setlocale(locale.LC_ALL, 'fr_FR')
        self.assertEqual(render_api.format_amount(a), "15,25")
        self.assertEqual(render_api.format_amount(a, False), "15,25")
        self.assertEqual(render_api.format_amount(b), "15,25")
        self.assertEqual(render_api.format_amount(b, False), "15,253")
