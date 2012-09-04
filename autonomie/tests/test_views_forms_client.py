# -*- coding: utf-8 -*-
# * File Name : test_views_forms_client.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 04-09-2012
# * Last Modified :
#
# * Project :
#
import colander
from mock import Mock
from autonomie.views.forms.client import deferred_ccode_valid
from .base import BaseTestCase

class TestClient(BaseTestCase):
    def test_unique_ccode(self):
        # A C001 exists in the database for the company with id 1
        company = Mock(id=1)
        validator = deferred_ccode_valid("nutt", {'company':company})
        self.assertRaises(colander.Invalid, validator, 'nutt', u'C001')
        self.assertNotRaises(validator, 'nutt', u'C002')

        company = Mock(id=2)
        validator = deferred_ccode_valid("nutt", {'company':company})
        self.assertNotRaises(validator, 'nutt', u'C001')
