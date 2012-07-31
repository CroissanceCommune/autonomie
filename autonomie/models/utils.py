# -*- coding: utf-8 -*-
# * File Name : utils.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 28-06-2012
# * Last Modified :
#
# * Project :
#
"""
    Usefull functions
"""
import time
import datetime

DEFAULT_DATE = datetime.date(2000, 1, 1)

def format_to_taskdate(value):
    """
        format a datetime.date object to a 'taskdate' format:
        an integer composed from a string YYYYmmdd
        Sorry .... it's not my responsability
    """
    if value is None:
        return None
    elif isinstance(value, datetime.date):
        if value.year < 1900:
            value.year = 1901
        return int(value.strftime("%Y%m%d"))
    else:
        return int(value)

def format_from_taskdate(value):
    """
        return a datetime.date object from an integer in 'taskdate' format
    """
    if value:
        value = str(value)
        try:
            year = int(value[0:4])
            assert year > 1910
        except:
            year = 2000
        try:
            month = int(value[4:6])
            assert month in range(1,13)
        except:
            month = 1
        try:
            day = int(value[6:8])
            assert day in range(1,32)
        except:
            day = 1
        try:
            return datetime.date(year, month, day)
        except:
            return datetime.date(year, 1, 1)
    else:
        return DEFAULT_DATE

def get_current_timestamp():
    """
        returns current time
    """
    return int(time.time())
