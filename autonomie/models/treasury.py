# -*- coding: utf-8 -*-
# * File Name : treasury.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 04-02-2013
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Treasury related models
"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from autonomie.models.base import DBBASE
from autonomie.models.base import default_table_args

class TurnoverProjection(DBBASE):
    """
        Turnover projection
        :param company_id: The company this projection is related to
        :param month: The month number this projection is made for
        :param year: The year this projection is made for
    """
    __tablename__ = 'turnover_projection'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="cascade"))
    month = Column(Integer)
    year = Column(Integer)
    comment = Column(Text, default="")
    value = Column(Integer)
    company = relationship("Company",
            backref=backref("turnoverprojections",
                order_by="TurnoverProjection.month",
                cascade="all, delete-orphan"))
