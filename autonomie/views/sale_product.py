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
View for product configuration
"""
import logging
import functools

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.tva import Tva
from autonomie.models.task import WorkUnit
from autonomie.models.sale_product import (
    SaleProductCategory,
    SaleProduct,
)
from autonomie.compute.math_utils import convert_to_float
from autonomie.resources import sale_product_js
from autonomie.views import BaseRestView


logger = logging.getLogger(__name__)


def company_products_view(context, request):
    """
    The view for company products configuration

    :param obj context: The context : The company object
    :param obj request: the Pyramid's request object
    """
    sale_product_js.need()
    loadurl = request.route_path(
        "sale_categories",
        id=context.id,
        _query=dict(action='options'),
    )
    contexturl = request.current_route_path()
    title = u"Configuration des produits"

    return {
        "title": title,
        "loadurl": loadurl,
        "contexturl": contexturl
    }


def company_products_options_ajax_view(context, request):
    """
    The view for company products options load

    :param obj context: The context : The company object
    :param obj request: the Pyramid's request object
    """
    return dict(
        tvas=Tva.query().all(),
        unities=WorkUnit.query().all()
    )


class RestCategories(BaseRestView):
    """
    Json api for SaleProductCategory
    """
    # Context is the company
    def collection_get(self):
        categories = SaleProductCategory.query().filter(
            SaleProductCategory != None
        )
        categories = categories.filter_by(company_id=self.context.id)
        return {'categories': categories.all()}

    def pre_format(self, appstruct):
        """
        Force the company_id in the appstruct
        """
        logger.info("Preformatting the appstruct")
        if self.context.__name__ == 'company':
            appstruct['company_id'] = self.context.id
        return appstruct

    # Context is a SaleProductCategory Object
    @property
    def schema(self):
        return SQLAlchemySchemaNode(
            SaleProductCategory,
            includes=('parent_id', 'title', 'company_id'),
        )


class RestProducts(BaseRestView):
    """
    Json api for products configuration
    """
    # Context is the category
    def collection_get(self):
        return self.context.products

    def pre_format(self, appstruct):
        value = appstruct.get('value', 0)
        appstruct['value'] = convert_to_float(value, 0)
        if self.context.__name__ == 'sale_category':
            appstruct['category_id'] = self.context.id
        return appstruct

    @property
    def schema(self):
        return SQLAlchemySchemaNode(
            SaleProduct,
            excludes=('id'),
        )


def includeme(config):
    """
    Pyramid's inclusion mechanism
    """
    url = "/companies/{id:\d+}/sale_categories"
    config.add_route(
        "sale_categories",
        url,
        traverse="/companies/{id}",
    )

    url += "/{cid:\d+}"
    config.add_route(
        "sale_category",
        url,
        traverse="/sale_categories/{cid}",
    )

    url += "/products"
    config.add_route(
        "sale_products",
        url,
        traverse="/sale_categories/{cid}",
    )

    url += "/{pid:\d+}"
    config.add_route(
        "sale_product",
        url,
        traverse="/sale_products/{pid}",
    )

    config.add_view(
        company_products_view,
        route_name="sale_categories",
        permission="edit",
        renderer="/sale/products.mako",
    )
    add_json_view = functools.partial(
        config.add_view,
        renderer='json',
        permission='edit',
        xhr=True,
    )

    add_json_view(
        company_products_options_ajax_view,
        route_name="sale_categories",
        request_param='action=options',
    )

    add_json_view(
        RestCategories,
        attr='collection_get',
        route_name='sale_categories',
        request_method="GET",
    )
    add_json_view(
        RestCategories,
        attr='post',
        route_name='sale_categories',
        request_method="POST"
    )
    add_json_view(
        RestCategories,
        attr='put',
        route_name='sale_category',
        request_method="PUT"
    )
    add_json_view(
        RestCategories,
        attr='delete',
        route_name='sale_category',
        request_method="DELETE"
    )

    add_json_view(
        RestProducts,
        attr='collection_get',
        route_name='sale_products',
        request_method="GET",
    )
    add_json_view(
        RestProducts,
        attr='post',
        route_name='sale_products',
        request_method="POST"
    )
    add_json_view(
        RestProducts,
        attr='get',
        route_name='sale_product',
        request_method="GET",
    )
    add_json_view(
        RestProducts,
        attr='put',
        route_name='sale_product',
        request_method="PUT"
    )
