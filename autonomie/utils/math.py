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
# * Project :
#
"""
    Provide common functions for mathematic operations
"""
def integer_to_amount(val):
    """
        Format an amount (stored as integer in the db)
        :param val: value returned by the database
        :return: a float object
    """
    return val / 100.0
