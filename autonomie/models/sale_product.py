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
    String,
    Float,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)
from sqlalchemy.ext.associationproxy import association_proxy
from autonomie.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie import forms


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

    products_rel = relationship(
        "SaleProductGroupRel",
        cascade='all, delete-orphan',
    )
    products = association_proxy("products_rel", "products")

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
            products=[product.__json__(request)
                      for product in self.products_rel],
            category_id=self.category_id,
        )


class SaleProductGroupRel(DBBASE):
    """
    The table used to configure the relationship between products and products
    groups
    """
    __table_args__ = default_table_args
    __tablename__ = 'product_product_group_rel'
    sale_product_id = Column(
        Integer,
        ForeignKey('sale_product.id'),
        primary_key=True,
        info={
            'colanderalchemy': {
                'validator': forms.get_deferred_select_validator(SaleProduct)
            }
        }
    )
    sale_product_group_id = Column(
        Integer,
        ForeignKey(
            'sale_product_group.id',
            name="fk_product_to_group_rel_group_id"
        ),
        primary_key=True,
        info={'colanderalchemy': {'missing': forms.colander.drop}}
    )
    sale_product = relationship(
        "SaleProduct",
        backref=backref(
            "group_association",
            cascade='all, delete-orphan',
        ),
        info={'colanderalchemy': {'exclude': True}},
    )
    quantity = Column(
        "quantity",
        Float(),
        default=1,
        info={'colanderalchemy': {'validator': forms.positive_validator}}
    )

    # The initialization method called by the association_proxy
    def __init__(self, product=None, product_id=None, quantity=None, **kwargs):
        if product is not None:
            self.sale_product = product
            if hasattr(product, 'quantity'):
                self.quantity = product.quantity
        if product_id is not None:
            self.sale_product_id = product_id
        if quantity is not None:
            self.quantity = quantity

    def __json__(self, request):
        res = self.sale_product.__json__(request)
        res['quantity'] = self.quantity
        res['product_id'] = self.sale_product_id
        return res

    @classmethod
    def find_or_create(cls, datas):
        """
        Method used to add/edit a relationship association

        Should be set as the objectify method if you used colanderalchemy to
        generate a formschema on the on of the related classes
        """
        rel_element = None

        if 'sale_product_group_id' in datas and "sale_product_id" in datas:
            # In case of edition, we try to retrieve the
            # group-product association object
            rel_element = SaleProductGroupRel.query().filter_by(
                sale_product_id=datas['sale_product_id'],
                sale_product_group_id=datas['sale_product_group_id']
            ).first()

        # We're not editing a relationship -> create a new one
        if rel_element is None:
            rel_element = SaleProductGroupRel()

        # Set the attributes on the relationship object
        for key, value in datas.items():
            setattr(rel_element, key, value)

        return rel_element
