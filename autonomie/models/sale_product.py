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
    Float,
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


PRODUCT_TO_GROUP_REL_TABLE = Table(
    "product_product_group_rel",
    DBBASE.metadata,
    Column(
        "sale_product_id",
        Integer,
        ForeignKey('sale_product.id', ondelete='cascade')
    ),
    Column(
        "sale_product_group_id",
        Integer,
        ForeignKey(
            'sale_product_group.id',
            ondelete='cascade',
            name="fk_product_to_group_rel_group_id"
        )
    ),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


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
    company_id = Column(
        ForeignKey('company.id'),
        info={
            'export': {'exclude': True},
        }
    )
    company = relationship(
        "Company",
        backref=backref(
            'sale_catalog',
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
            company_id=self.company_id,
            product_groups=[item.__json__(request)
                            for item in self.product_groups],
            products=[item.__json__(request)
                      for item in self.products],
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
    value = Column(Float(), default=0)
    quantity = Column(Float(), default=1)
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
            quantity=self.quantity,
            unity=self.unity,
            category_id=self.category_id,
            category=self.category.title,
        )


class SaleProductGroup(DBBASE):
    """
    A product group model
    """
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=False)
    ref = Column(String(100), nullable=True)

    title = Column(String(255), default="")
    description = Column(Text(), default='')

    products = relationship(
        "SaleProduct",
        secondary=PRODUCT_TO_GROUP_REL_TABLE,
        info={
            'colanderalchemy': {
                # Permet de sélectionner des éléments existants au lieu
                # d'insérer des nouveaux à chaque fois
                'children': forms.get_sequence_child_item(SaleProduct),
            }
        }
    )

    category_id = Column(ForeignKey('sale_product_category.id'))
    category = relationship(
        SaleProductCategory,
        backref=backref('product_groups'),
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
            title=self.title,
            description=self.description,
            products=[product.__json__(request) for product in self.products],
            category_id=self.category_id,
        )
