# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 02-08-2012
# * Last Modified :
#
# * Project :
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
