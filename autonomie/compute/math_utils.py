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
    Math utilities used for computing
"""
import math
from decimal import Decimal
from decimal import ROUND_HALF_UP

PRECISION_LEVEL = 2


def floor(value):
    """
        floor a float value
        :param value: float value to be rounded
        :return: an integer

        >>> floor(296.9999999)
        297
        >>> floor(296.9985265)
        296
    """
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return int(dec_round(value, 0))


def dec_round(dec, precision):
    """
    Return a decimal object rounded to precision

    :param int precision: the number of decimals we want after the comma
    """
    # On construit un nombre qui a le même nombre de 0 après la virgule que
    # ce que l'on veut en définitive
    precision_reference_tmpl = "%%.%df" % precision
    precision_reference = precision_reference_tmpl % 1
    precision = Decimal(precision_reference)
    return dec.quantize(precision, ROUND_HALF_UP)


def amount(value, precision=2):
    """
        Convert a float value as an integer amount to store it in a database
        :param value: float value to convert
        :param precision: number of dot translation to make

        >>> amount(195.65)
        19565
    """
    converter = math.pow(10, precision)
    result = floor(value * converter)
    return result


def integer_to_amount(value, precision=2):
    """
        Convert an integer value to a float with precision numbers after comma
    """
    flat_point = Decimal(str(math.pow(10, -precision)))
    val = Decimal(str(value)) * flat_point
    return float(Decimal(str(val)).quantize(flat_point, ROUND_HALF_UP))


def percentage(value, _percent):
    """
        Return the value of the "percent" percent of the original "value"
    """
    return int(float(value) * (float(_percent)/100.0))


def percent(part, total, default=None):
    """
        Return the percentage of total represented by part
        if default is provided, the ZeroDivisionError is handled
    """
    if default is not None and total == 0:
        return default
    value = part * 100.0 / total
    return float(dec_round(Decimal(str(value)), 2))


def convert_to_int(value, default=None):
    """
    try to convert the given value to an int
    """
    try:
        val = int(value)
    except ValueError as err:
        if default:
            val = default
        else:
            raise err
    return val

