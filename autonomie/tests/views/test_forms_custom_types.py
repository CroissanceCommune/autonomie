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

import colander
from autonomie.forms.custom_types import AmountType
from autonomie.forms.custom_types import specialfloat
from autonomie.forms.custom_types import Integer
from autonomie.tests.base import BaseTestCase

class TestType(BaseTestCase):
    def test_amount_type(self):
        a = AmountType()
        self.assertEqual(a.serialize(None, 15000), "150.0")
        self.assertEqual(a.deserialize(None, u"79.4"), 7940)
        self.assertEqual(a.deserialize(None, u"292,65"), 29265)

    def test_specialfloat(self):
        a = u"495, 4 5€"
        self.assertEqual(specialfloat( "", a), 495.45)

    def test_integer(self):
        i = Integer()
        self.assertEqual(colander.null, i.serialize(None, None))
        self.assertEqual("0", i.serialize(None, 0))
