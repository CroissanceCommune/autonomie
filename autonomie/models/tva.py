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
from sqlalchemy import (
        Column,
        Integer,
        String,
        ForeignKey,
        Boolean,
        )
from sqlalchemy.orm import (
        relationship,
        backref,
        )

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
    active = Column(Boolean(), default=True)

    @classmethod
    def query(cls, include_inactive=False):
        q = super(Tva, cls).query()
        if not include_inactive:
            q = q.filter(Tva.active==True)
        return q.order_by('value')

    @classmethod
    def get_default(cls):
        return super(Tva, cls).query().filter(cls.default==1).first()

    def __json__(self, request):
        return dict(
                id=self.id,
                value=self.value,
                name=self.name,
                products=[product.__json__(request) \
                        for product in self.products]
                )

class Product(DBBASE):
    __tablename__ = 'product'
    __table_args__ = default_table_args
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(125), nullable=False)
    compte_cg = Column("compte_cg", String(125))
    active = Column(Boolean(), default=True)
    tva_id = Column(Integer, ForeignKey("tva.id", ondelete="cascade"))
    tva = relationship("Tva",
            backref=backref("products", cascade="all, delete-orphan"))

    def __json__(self, request):
        return dict(
                id=self.id,
                name=self.name,
                compte_cg=self.compte_cg
                )

    @classmethod
    def query(cls, include_inactive=False):
        q = super(Product, cls).query()
        if not include_inactive:
            q.filter(Product.active==True)
        return q.order_by('name')
