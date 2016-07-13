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
from decimal import (
    Decimal,
    ROUND_HALF_UP,
    ROUND_DOWN,
)

PRECISION_LEVEL = 2


def floor_to_precision(
    value,
    round_floor=False,
    precision=2,
    dialect_precision=5
):
    """
    floor a value in its int representation:
        >>> floor_to_thousand(296999)
        297000

        amounts are of the form : value * 10 ** dialect_precision it allows to
        store dialect_precision numbers after comma for intermediary amounts for
        totals we want precision numbers

    :param int value: The value to floor
    :param bool round_floor: Should be rounded down ?
    :param int precision: How much significant numbers we want ?
    :param int dialect_precision: The number of zeros that are concerning the
    floatting part of our value
    """
    if not isinstance(value, Decimal):
        value = Decimal(str(value))

    dividor = 10 ** (dialect_precision - precision)

    value = value / Decimal(dividor)
    return floor(value, round_floor) * dividor


def floor(value, round_floor=False):
    """
        floor a float value
        :param value: float value to be rounded
        :param bool round_floor: Should the data be floor rounded ?
        :return: an integer

        >>> floor(296.9999999)
        297
    """
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return int(dec_round(value, 0, round_floor))


def dec_round(dec, precision, round_floor=False):
    """
    Return a decimal object rounded to precision

    :param int precision: the number of decimals we want after the comma
    :param bool round_floor: Should the data be floor rounded ?
    """
    if round_floor:
        method = ROUND_DOWN
    else:
        method = ROUND_HALF_UP
    # On construit un nombre qui a le même nombre de 0 après la virgule que
    # ce que l'on veut en définitive
    precision_reference_tmpl = "%%.%df" % precision
    precision_reference = precision_reference_tmpl % 1
    precision = Decimal(precision_reference)
    return dec.quantize(precision, method)


def round(float_, precision, round_floor=False):
    """
    Return a float object rounded to precision
    :param float float_: the object to round
    :param int precision: the number of decimals we want after the comma
    :param bool round_floor: Should the data be floor rounded ?
    """
    dec = Decimal(float_)
    return float(dec_round(dec, precision, round_floor))


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


def convert_to_float(value, default=None):
    """
    Try to convert the given value object to a float
    """
    if isinstance(value, (str, unicode)):
        value = value.replace(',', '.')
    try:
        val = float(value)
    except ValueError as err:
        if default is not None:
            val = default
        else:
            raise err
    return val


# TVA related functions
def reverse_tva(total_ttc, tva, float_format=True):
    """
    Compute total_ht from total_ttc

    :param float total_ttc: ttc value in float format (by default)
    :param integer tva: the tva value in integer format (tva * 100)
    :param bool float_format: Is total_ttc in the float format (real ttc value)

    :returns: the value in integer format
    """
    # e.g : tva = 19.6 * 100 = 1960
    tva_dividor = max(int(tva), 0) + 100 * 100.0

    # First we translate the float value to an integer representation
    if float_format:
        total_ttc = amount(total_ttc, precision=5)

    # Representation in the integer representation
    result = floor(total_ttc * 10000 / tva_dividor)

    # We translate the result back to a float value
    if float_format:
        result = integer_to_amount(result, precision=5)

    return result


def compute_tva(total_ht, tva):
    """
        Compute the tva for the given ht total
    """
    return float(total_ht) * (max(int(tva), 0) / 10000.0)
