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
    Provide common tools for string handling
"""
import re
import random
from string import lowercase


def force_ascii(datas):
    """
        Return enforced ascii string
        éko=>ko
    """
    return "".join((i for i in datas if ord(i) < 128))


def force_utf8(value):
    """
        return a utf-8 string
    """
    if isinstance(value, unicode):
        value = value.encode('utf-8')
    return value


def camel_case_to_name(name):
    """
    Used to convert a classname to a lowercase name
    """
    convert_func = lambda m:"_" + m.group(0).lower()
    return name[0].lower() + re.sub(r'([A-Z])', convert_func, name[1:])


def gen_random_string(size=15):
    """
    Generate random string

        size

            size of the resulting string
    """
    return ''.join(random.choice(lowercase) for _ in range(size))
