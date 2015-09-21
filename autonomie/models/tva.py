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
    compte_a_payer = Column(String(125), default='')
    code = Column("code", String(125), default="")
    active = Column(Boolean(), default=True)

    @classmethod
    def query(cls, include_inactive=False):
        q = super(Tva, cls).query()
        if not include_inactive:
            q = q.filter(Tva.active == True)
        return q.order_by('value')

    @classmethod
    def by_value(cls, value):
        """
        Returns the Tva matching this value
        """
        return super(Tva, cls).query().filter(cls.value == value).one()

    @classmethod
    def get_default(cls):
        return super(Tva, cls).query().filter(cls.default == 1).first()

    def __json__(self, request):
        return dict(
            id=self.id,
            value=self.value,
            name=self.name,
            default=self.default == 1,
            products=[product.__json__(request) for product in self.products],
        )


class Product(DBBASE):
    __tablename__ = 'product'
    __table_args__ = default_table_args
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(125), nullable=False)
    compte_cg = Column("compte_cg", String(125))
    active = Column(Boolean(), default=True)
    tva_id = Column(Integer, ForeignKey("tva.id", ondelete="cascade"))
    tva = relationship(
        "Tva",
        backref=backref("products", cascade="all, delete-orphan")
    )

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
            q.filter(Product.active == True)
        return q.order_by('name')
