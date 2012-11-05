# -*- coding: utf-8 -*-
# * File Name : holiday.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 20-10-2012
# * Last Modified :
#
# * Project :
#
"""
    Holiday model used to store employee's holiday declaration
"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from autonomie.models import DBBASE
from autonomie.models import default_table_args

class Holiday(DBBASE):
    """
        Holidays table
        Stores the start and end date for holiday declaration
        user_id
        start_date
        end_date
    """
    __tablename__ = "holiday"
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey('accounts.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    user = relationship("User",
                        backref=backref("holidays",
                                        order_by="Holiday.start_date"),
                        primaryjoin="Holiday.user_id==User.id"
                        )
