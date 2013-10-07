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
            assert month in range(1, 13)
        except:
            month = 1
        try:
            day = int(value[6:8])
            assert day in range(1, 32)
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
