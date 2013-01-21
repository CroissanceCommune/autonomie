# -*- coding: utf-8 -*-
# * File Name : unity.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 21-01-2013
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Models for work unit (days, ...)
"""
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from autonomie.models import default_table_args
from autonomie.models import DBBASE

class WorkUnit(DBBASE):
    """
        Work unit, used to build the price list
    """
    __tablename__ = "workunity"
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    label = Column(String(100))

