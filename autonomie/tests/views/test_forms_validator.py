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

import unittest
import colander
from autonomie.views.forms.validators import validate_image_mime

class ValidatorsTest(unittest.TestCase):
    def test_validate_image_mime(self):
        form_datas = {'mimetype': 'application/pdf',
                  'filename': u'file.pdf',
                  'size': -1}
        self.assertRaises(colander.Invalid, validate_image_mime, "nutt",
                                                form_datas)
        form_datas = {'mimetype': 'image/png',
                'filename': u'file.png',
                'size': -1}
        self.assertEqual(None, validate_image_mime("nutt", form_datas))
