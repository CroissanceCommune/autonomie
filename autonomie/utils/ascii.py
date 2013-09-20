# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 21-03-2013
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Provide common tools for string handling
"""
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
