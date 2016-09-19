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
import string
from unidecode import unidecode


def force_ascii(value):
    """
        Return enforced ascii string
        éko=>ko
    """
    if not isinstance(value, unicode):
        if isinstance(value, str):
            value = force_unicode(value)
        else:
            value = unicode(value)
    value = unidecode(value)
    return value


def force_utf8(value):
    """
        return a utf-8 string
    """
    if isinstance(value, unicode):
        value = value.encode('utf-8')
    return value


def force_unicode(value):
    """
    return an utf-8 unicode entry
    """
    if isinstance(value, str):
        value = value.decode('utf-8')
    return value


def camel_case_to_name(name):
    """
    Used to convert a classname to a lowercase name
    """
    def convert_func(m):
        return "_" + m.group(0).lower()
    return name[0].lower() + re.sub(r'([A-Z])', convert_func, name[1:])


def gen_random_string(size=15):
    """
    Generate random string

        size

            size of the resulting string
    """
    return ''.join(random.choice(string.lowercase) for _ in range(size))


def random_tag_id(size=15):
    """
    Return a random string supposed to be used as tag id
    """
    return gen_random_string(size)


def to_utf8(datas):
    """
    Force utf8 string entries in the given datas
    """
    res = datas
    if isinstance(datas, dict):
        res = {}
        for key, value in datas.items():
            key = to_utf8(key)
            value = to_utf8(value)
            res[key] = value

    elif isinstance(datas, (list, tuple)):
        res = []
        for data in datas:
            res.append(to_utf8(data))

    elif isinstance(datas, unicode):
        res = datas.encode('utf-8')

    return res


def isint(val):
    """
    Return True if the result looks like an int
    """
    res = False

    if isinstance(val, int):
        res = True

    elif isinstance(val, (str, unicode)) and val.isdigit():
        res = True

    return res


def force_filename(val):
    """
    Transform a string to a valid filename
    """
    result = force_ascii(val)
    result = result.replace(' ', '_')

    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    result = "".join((char for char in result if char in valid_chars))

    return result
