# -*- coding: utf-8 -*-
# * File Name : test_views_forms_custom_types.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 29-08-2012
# * Last Modified :
#
# * Project :
#
import colander
from autonomie.views.forms.custom_types import AmountType
from autonomie.views.forms.custom_types import specialfloat
from autonomie.views.forms.custom_types import Integer
from autonomie.tests.base import BaseTestCase

class TestType(BaseTestCase):
    def test_amount_type(self):
        a = AmountType()
        self.assertEqual(a.serialize(None, 15000), "150.0")
        self.assertEqual(a.deserialize(None, "79.4"), 7940)

    def test_specialfloat(self):
        a = u"495, 4 5€"
        self.assertEqual(specialfloat( "", a), 495.45)

    def test_integer(self):
        i = Integer()
        self.assertEqual(colander.null, i.serialize(None, None))
        self.assertEqual("0", i.serialize(None, 0))
