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
import pytest
from autonomie.models.sale_product import (
    SaleProduct,
    SaleProductGroup,
    SaleProductCategory,
)
from autonomie.models.company import Company


@pytest.fixture
def company(content):
    c = Company.query().first()
    c.__name__ = 'company'
    return c


@pytest.fixture
def sale_product_category(dbsession, company):
    c = SaleProductCategory(
        title=u"Catégorie",
        description=u"Description",
        company=company,
    )
    c.__name__ = 'sale_category'
    dbsession.add(c)
    dbsession.flush()
    return c


@pytest.fixture
def sale_product(dbsession, sale_product_category):
    p = SaleProduct(
        label="Produit",
        ref="PROD",
        description=u"Produit",
        tva=2000,
        value=100.0,
        unity=u"m²",
        category=sale_product_category,
    )
    p.__name__ = 'sale_product'
    dbsession.add(p)
    dbsession.flush()
    return p


@pytest.fixture
def sale_product_group(dbsession, sale_product, sale_product_category):
    g = SaleProductGroup(
        category_id=sale_product_category.id,
        ref=u"GROU",
        label=u"Groupe",
        description=u"Nouveau groupe",
        title=u"Groupe",
        products=[sale_product]
    )
    g.__name__ = 'sale_product_group'
    dbsession.add(g)
    dbsession.flush()
    return g


def test_add_category(company, get_csrf_request_with_db):
    from autonomie.views.sale_product import RestCategories
    category_appstruct = {
        'title': u"Titre",
    }
    request = get_csrf_request_with_db()
    request.context = company
    request.json_body = category_appstruct
    view = RestCategories(request)
    view.post()
    category = company.sale_catalog[-1]
    assert category.title == u"Titre"


def test_edit_category(sale_product_category, get_csrf_request_with_db):
    from autonomie.views.sale_product import RestCategories
    appstruct = {
        'id': sale_product_category.id,
        'title': u"Nouveau titre",
    }
    request = get_csrf_request_with_db()
    request.context = sale_product_category
    request.json_body = appstruct
    view = RestCategories(request)
    view.put()
    assert sale_product_category.title == u"Nouveau titre"


def test_add_product(sale_product_category, get_csrf_request_with_db):
    from autonomie.views.sale_product import RestProducts
    product_appstruct = {
        'label': u"Produit",
        'ref': u"PROD",
        'description': u'Description',
        'tva': 2000,
        'value': 100.05,
        'unity': u'm²'
    }
    request = get_csrf_request_with_db()
    request.context = sale_product_category
    request.json_body = product_appstruct
    view = RestProducts(request)
    view.post()
    product = sale_product_category.products[-1]
    for key, value in product_appstruct.items():
        assert getattr(product, key) == value


def test_edit_product(sale_product, get_csrf_request_with_db):
    from autonomie.views.sale_product import RestProducts
    product_appstruct = {
        'id': sale_product.id,
        'label': u"Prod",
        'tva': 1000,
        'value': 100.025,
    }
    request = get_csrf_request_with_db()
    request.context = sale_product
    request.json_body = product_appstruct
    view = RestProducts(request)
    view.put()
    assert sale_product.tva == 1000
    assert sale_product.value == 100.025
    assert sale_product.label == u'Prod'


def test_edit_appstruct_with_commas(sale_product, get_csrf_request_with_db):
    from autonomie.views.sale_product import RestProducts
    product_appstruct = {
        'id': sale_product.id,
        'label': u"Prod",
        'tva': 1000,
        'value': 100.025,
    }
    request = get_csrf_request_with_db()
    request.context = sale_product
    request.json_body = product_appstruct
    view = RestProducts(request)
    result = view.put()
    assert result == sale_product


def test_add_product_group(sale_product_category, sale_product,
                           get_csrf_request_with_db):
    from autonomie.views.sale_product import RestProductGroups
    product_group_appstruct = {
        'label': u"Ouvrage",
        'ref': u"OUV",
        'title': u"Mur intérieur",
        'description': u'Mur isolation enduit à la chaux',
        'products': [{'quantity': 1.524, 'id': sale_product.id}]
    }
    request = get_csrf_request_with_db()
    request.context = sale_product_category
    request.json_body = product_group_appstruct
    view = RestProductGroups(request)
    view.post()
    group = sale_product_category.product_groups[-1]
    product_group_appstruct.pop('products', None)
    product_group_appstruct.pop('products_rel', None)
    for key, value in product_group_appstruct.items():
        assert getattr(group, key) == value
    assert group.products_rel[-1].sale_product_id == sale_product.id
    assert group.products_rel[-1].quantity == 1.524


def test_edit_product_group(sale_product_category, sale_product,
                            sale_product_group, get_csrf_request_with_db):
    from autonomie.views.sale_product import RestProductGroups
    product_group_appstruct = {
        'label': u"Ouvrage Nouveau label",
        'title': u"Nouveau titre",
        'products': [
            {
                'quantity': 1.254,
                'id': sale_product.id,
            },
        ]
    }
    request = get_csrf_request_with_db()
    request.context = sale_product_group
    request.json_body = product_group_appstruct
    view = RestProductGroups(request)
    view.put()
    assert sale_product_group.label == u"Ouvrage Nouveau label"
    assert sale_product_group.title == u"Nouveau titre"
    assert len(sale_product_group.products_rel) == 1
    assert sale_product_group.products_rel[-1].quantity == 1.254
