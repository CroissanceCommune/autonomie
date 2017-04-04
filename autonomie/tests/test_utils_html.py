# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2016 Croissance Commune
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Test for the forms package
"""
import colander
from autonomie.utils.html import (
    strip_whitespace,
    strip_linebreaks,
    strip_void_lines,
)


def test_strip_whitespace():
    value = "toto"
    assert strip_whitespace(value) == value
    value = "     toto\t   "
    assert strip_whitespace(value) == 'toto'
    value = "   to    toto \t toto"
    assert strip_whitespace(value) == "to    toto \t toto"
    assert strip_whitespace(None) is None
    assert strip_whitespace(colander.null) == colander.null


def test_strip_linebreaks():
    value = "\n toto \n <br /><br><br/>"
    assert strip_linebreaks(value) == "toto"
    assert strip_linebreaks(None) is None
    assert strip_linebreaks(colander.null) == colander.null


def test_strip_void_lines():
    value = "<div></div><p>toto</p><p> </p>"
    assert strip_void_lines(value) == "<div></div><p>toto</p>"
