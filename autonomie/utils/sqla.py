# -*- coding: utf-8 -*-
# * File Name : sqla.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 08-09-2010
# * Last Modified :
#
# * Project :
#
"""
    SqlAlchemy utilities
"""
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm import class_mapper

def get_columns(sqla_obj):
    """
        Return the columns from an sqlalchemy object
        (only the primary one, not the related ones)
    """
    return [pro.columns[0] for pro in class_mapper(sqla_obj).iterate_properties
            if isinstance(pro, ColumnProperty)]
