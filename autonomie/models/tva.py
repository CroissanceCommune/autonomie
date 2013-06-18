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
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from autonomie.models.base import DBBASE
from autonomie.models.base import default_table_args

class Tva(DBBASE):
    """
        `id` int(2) NOT NULL auto_increment,
        `name` varchar(8) NOT NULL,
        `value` int(5)
        `default` int(2) default 0 #rajouté par mise à jour 1.2
    """
    __tablename__ = 'tva'
    __table_args__ = default_table_args
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(8), nullable=False)
    value = Column("value", Integer)
    default = Column("default", Integer)
    compte_cg = Column("compte_cg", String(125), default="")

    @classmethod
    def query(cls):
        q = super(Tva, cls).query()
        return q.order_by('value')

    @classmethod
    def get_default(cls):
        return super(Tva, cls).query().filter(cls.default==1).first()

class Product(DBBASE):
    __tablename__ = 'product'
    __table_args__ = default_table_args
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(8), nullable=False)
    compte_cg = Column("compte_cg", String(125))
    tva_id = Column(Integer, ForeignKey("tva.id", ondelete="cascade"))
    tva = relationship("Tva",
            backref=backref("products", cascade="all, delete-orphan"))
