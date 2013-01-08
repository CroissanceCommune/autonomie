# -*- coding: utf-8 -*-
# * File Name : test_header_resize.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 08-01-2013
# * Last Modified :
#
# * Project :
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
