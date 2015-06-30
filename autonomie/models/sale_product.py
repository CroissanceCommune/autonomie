# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Models related to product management
"""
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    Table,
    String,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)
from autonomie.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie import forms


#PRODUCT_GROUP = Table(
#    'product_group_rel',
#    DBBASE.metadata,
#    Column("product_id", Integer, ForeignKey('sale_product.id')),
#    Column("product_group_id", Integer, ForeignKey('product_group.id')),
#    mysql_charset=default_table_args['mysql_charset'],
#    mysql_engine=default_table_args['mysql_engine'],
#)


class SaleProductCategory(DBBASE):
    """
    A product category allowing to group products
    """
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    title = Column(
        String(255),
        nullable=False,
        info={
            "colanderalchemy": {'title': u"Titre"}
        }
    )
    description = Column(Text(), default="")
    parent_id = Column(ForeignKey('sale_product_category.id'))
    children = relationship(
        "SaleProductCategory",
        primaryjoin="SaleProductCategory.id==SaleProductCategory.parent_id",
        backref=backref("parent", remote_side=[id]),
        cascade="all",
        info={'colanderalchemy': forms.EXCLUDED},
    )
    company_id = Column(
        ForeignKey('company.id'),
        info={
            'export': {'exclude': True},
        }
    )
    company = relationship(
        "Company",
        backref=backref(
            'products',
            order_by="SaleProductCategory.title",
        ),
        info={
            'export': {'exclude': True},
        }
    )

    def __json__(self, request):
        """
        Json repr of our model
        """
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            parent_id=self.parent_id,
            company_id=self.company_id,
            product_groups=[item.__json__(request) for item in self.children],
            products=[item.__json__(request) for item in self.products],
        )


class SaleProduct(DBBASE):
    """
    A product model
    """
    __table_args__ = default_table_args
    __tablename__ = 'sale_product'
    id = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=False)
    ref = Column(String(100), nullable=True)
    description = Column(Text(), default='')
    tva = Column(Integer, default=0)
    value = Column(Integer, default=0)
    unity = Column(String(100), default='')

    category_id = Column(ForeignKey('sale_product_category.id'))
    category = relationship(
        SaleProductCategory,
        backref=backref('products'),
        info={'colanderalchemy': forms.EXCLUDED},
    )

    def __json__(self, request):
        """
        Json repr of our model
        """
        return dict(
            id=self.id,
            label=self.label,
            ref=self.ref,
            description=self.description,
            tva=self.tva,
            value=self.value,
            unity=self.unity,
            category_id=self.category_id,
        )
