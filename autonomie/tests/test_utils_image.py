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

"""
    Test image resizing
"""
import unittest
import os
from autonomie.tests.base import DATASDIR

from PIL import Image

from autonomie.utils.image import ImageResizer

class TestImageResize(unittest.TestCase):
    def getOne(self):
        return ImageResizer(5, 1)

    def test_resize_not_affect_equal(self):
        resizer = self.getOne()
        image = file(os.path.join(DATASDIR, 'entete5_1.png'), 'r')
        image2 = resizer.complete(image)
        self.assertEqual(image2, image)

    def test_resize_not_affect_less(self):
        resizer = self.getOne()
        image = file(os.path.join(DATASDIR, 'entete10_1.png'), 'r')
        image2 = resizer.complete(image)
        self.assertEqual(image2, image)

    def test_resize(self):
        resizer = self.getOne()
        image = file(os.path.join(DATASDIR, 'entete2_1.png'), 'r')
        image2 = resizer.complete(image)
        self.assertFalse(image==image2)
        img_obj2 = Image.open(image2)
        print img_obj2.size
        width, height = img_obj2.size
        self.assertEqual(width/height, 5)
