# -*- coding: utf-8 -*-
# * File Name : tva.py
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
    Model for tva amounts
"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from autonomie.models import DBBASE

class Tva(DBBASE):
    """
        `id` int(2) NOT NULL auto_increment,
        `name` varchar(8) NOT NULL,
        `value` int(5)
        `default` int(2) default 0 #rajouté par mise à jour 1.2
    """
    __tablename__ = 'tva'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset": 'utf8'}
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(8), nullable=False)
    value = Column("value", Integer)
    default = Column("default", Integer)

    @classmethod
    def query(cls):
        q = super(Tva, cls).query()
        return q.order_by('value')
