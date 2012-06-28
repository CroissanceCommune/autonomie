# -*- coding: utf-8 -*-
# * File Name :
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
    Custom types and usefull functions
"""
import time
import datetime

from sqlalchemy.types import TypeDecorator
from sqlalchemy.types import Integer as Integer_type
from sqlalchemy.types import String as String_type

from autonomie.models.utils import format_to_taskdate
from autonomie.models.utils import format_from_taskdate

class CustomDateType(TypeDecorator):
    """
        Custom date type used because our database is using
        integers to store date's timestamp
    """
    impl = Integer_type
    def process_bind_param(self, value, dialect):
        if value is None or not value:
            return int(time.time())
        elif isinstance(value, datetime.datetime):
            return int(time.mktime(value.timetuple()))
        elif isinstance(value, int):
            return value
        return time.mktime(value.timetuple())

    def process_result_value(self, value, dialect):
        if value:
            return datetime.datetime.fromtimestamp(float(value))
        else:
            return datetime.datetime.now()

class CustomDateType2(TypeDecorator):
    """
        Custom date type used because our database is using
        custom integers to store dates
        YYYYMMDD
    """
    impl = Integer_type
    def process_bind_param(self, value, dialect):
        return format_to_taskdate(value)

    def process_result_value(self, value, dialect):
        return format_from_taskdate(value)

class CustomFileType(TypeDecorator):
    """
        Custom Filetype used to glue deform fileupload tools with
        the database element
    """
    impl = String_type
    def __init__(self, prefix, *args, **kw):
        TypeDecorator.__init__(self, *args, **kw)
        self.prefix = prefix

    def process_bind_param(self, value, dialect):
        """
            process the insertion of the value
            write the file to persistent storage
        """
        ret_val = None
        if isinstance(value, dict):
            ret_val = value.get('filename', '')
        return ret_val

    def process_result_value(self, value, dialect):
        """
            Get the datas from database
        """
        if value:
            return dict(filename = value,
                        uid=self.prefix + value)
        else:
            return dict(filename="",
                        uid=self.prefix)

class CustomInteger(TypeDecorator):
    """
        Custom integer, allow long to int automatic conversion
    """
    impl = Integer_type
    def process_bind_param(self, value, dialect):
        """
            On insertion
        """
        if isinstance(value, long):
            value = int(value)
        return value

    def process_result_value(self, value, dialect):
        """
            On query
        """
        if isinstance(value, long):
            value = int(value)
        return value
