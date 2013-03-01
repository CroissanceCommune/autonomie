# -*- coding: utf-8 -*-
# * File Name : math_utils.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 01-03-2013
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Math utilities used for computing
"""
import math
from decimal import Decimal
from decimal import ROUND_DOWN

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
    return int(dec_round(value, 1))


def dec_round(dec, precision):
    """
        Return a decimal object rounded to precision
    """
    return dec.quantize(Decimal(str(10**-precision)), ROUND_DOWN)


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
