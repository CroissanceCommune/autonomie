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
import pytest
import os
from autonomie.tests.conftest import DATASDIR

from PIL import Image

from autonomie.utils.image import (
    ImageResizer,
    ImageRatio,
)

@pytest.fixture
def ratio():
    return ImageRatio(5, 1)


@pytest.fixture
def resizer():
    return ImageResizer(800, 200)


def test_ratio_not_affect_equal(ratio):
    image = file(os.path.join(DATASDIR, 'entete5_1.png'), 'r')
    image2 = ratio.complete(image)
    assert Image.open(image2).size == Image.open(image).size


def test_ratio_not_affect_less(ratio):
    image = file(os.path.join(DATASDIR, 'entete10_1.png'), 'r')
    image2 = ratio.complete(image)
    assert Image.open(image2).size == Image.open(image).size


def test_ratio(ratio):
    image = file(os.path.join(DATASDIR, 'entete2_1.png'), 'r')
    image2 = ratio.complete(image)
    img_obj2 = Image.open(image2)
    width, height = img_obj2.size
    assert width/height == 5


def test_resize_width(resizer):
    image = file(os.path.join(DATASDIR, 'entete2_1.png'), 'r')
    image2 = resizer.complete(image)
    assert Image.open(image2).size[0] == 400
    assert Image.open(image2).size[1] == 200


def test_resize_height(resizer):
    image = file(os.path.join(DATASDIR, 'entete5_1.png'), 'r')
    image2 = resizer.complete(image)
    assert Image.open(image2).size[0] == 800
    assert Image.open(image2).size[1] == 160


def test_resize_cmyk_bug880(resizer):
    image = file(os.path.join(DATASDIR, 'cmyk.jpg'), 'r')
    result = resizer.complete(image)
    assert Image.open(result).size[0] <= 200
    assert Image.open(result).mode == "RGB"
