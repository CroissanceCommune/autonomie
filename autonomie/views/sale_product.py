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
    SaleProductGroup,
)
from autonomie.compute.math_utils import convert_to_float
from autonomie.resources import sale_product_js
from autonomie.views import BaseRestView


logger = logging.getLogger(__name__)


NO_GROUP_MESSAGE = u"""<h5>Aucun {label} n'a été configuré dans le catalogue.
</h5><a class='btn btn-default' href='{url}' title='Configurer le catalogue'
target='_blank'>Ajouter des {label}s</a>"""


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
    # Url utilisée pour charger l'ensemble des produits de l'entreprise (les
    # autres vues ne les renvoient que par catégorie)
    all_products_url = request.route_path(
        "sale_categories",
        id=context.id,
        _query=dict(action='products'),
    )
    contexturl = request.current_route_path()
    title = u"Configuration des produits"

    return {
        "title": title,
        "loadurl": loadurl,
        "contexturl": contexturl,
        "all_products_url": all_products_url,
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


def company_products_ajax_view(context, request):
    """
    Returns the products of the current company

    :param obj context: The context : The company object
    :param obj request: the Pyramid's request object
    """
    all_products = []
    for category in context.sale_catalog:
        all_products.extend(category.products)
    return dict(products=all_products)


def company_products_jstree_ajax_view(context, request):
    """
    Returns the catalog of products (stored by category) in the format expected
    by jstree

    :param obj context: The context : The company object
    :param obj request: the Pyramid's request object
    """
    void = True
    item_type = request.params.get('type', 'sale_product')

    if item_type == 'sale_product_group':
        category_child_attr = 'product_groups'
        label = u"ouvrage"
    elif item_type == 'sale_product':
        category_child_attr = 'products'
        label = u"produit"
    else:
        # Si on arrive ici c'est que quelqu'un joue au petit malin
        return dict(void_message=u"Erreur")

    jstree = []
    for category in context.sale_catalog:
        children = []
        category_datas = {
            "text": category.title,
            "children": children
        }

        children_models = getattr(category, category_child_attr)
        for child in children_models:
            void = False
            text = child.label
            if child.ref:
                text += u" ({0})".format(child.ref)

            children.append(
                {
                    "text": text,
                    "type": item_type,
                    "url": request.route_path(
                        item_type,
                        id=context.id,
                        cid=category.id,
                        pid=child.id,
                    ),
                    "id": child.id,
                })
        if children_models:
            jstree.append(category_datas)

    if void:
        message = NO_GROUP_MESSAGE.format(
            label=label,
            url=request.route_path('sale_categories', id=context.id)
        )
        result = dict(void_message=message)
    else:
        # We open the first node
        jstree[0]['state'] = {'opened': True}
        result = dict(jstree=jstree)

    return result


class RestCategories(BaseRestView):
    """
    Json api for SaleProductCategory
    """
    # Context is the company
    def collection_get(self):
        categories = SaleProductCategory.query()
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
        ).bind(request=self.request)


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
            excludes=('id',),
        ).bind(request=self.request)


class RestProductGroups(BaseRestView):
    """
    JSON rest api for product group configuration
    """
    # Context is the category
    def collection_get(self):
        return self.context.product_groups

    def pre_format(self, appstruct):
        """
        """
        # Since when serializing a multi select on the client side, we get a
        # list OR a string, we need to handle both cases
        if 'products' in appstruct:
            product_ids = appstruct.get('products')
            if not hasattr(product_ids, '__iter__'):
                product_ids = [product_ids]

            appstruct['products'] = product_ids

        if self.context.__name__ == 'sale_category':
            appstruct['category_id'] = self.context.id
        return appstruct

    @property
    def schema(self):
        return SQLAlchemySchemaNode(
            SaleProductGroup,
            # id passe par l'url
            excludes=('id', ),
        ).bind(request=self.request)


def add_routes(config):
    """
    Add module's related routes
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

    product_url = url + "/products"
    config.add_route(
        "sale_products",
        product_url,
        traverse="/sale_categories/{cid}",
    )

    product_url += "/{pid:\d+}"
    config.add_route(
        "sale_product",
        product_url,
        traverse="/sale_products/{pid}",
    )

    group_url = url + "/groups"
    config.add_route(
        "sale_product_groups",
        group_url,
        traverse="/sale_categories/{cid}",
    )

    group_url += "/{pid:\d+}"
    config.add_route(
        "sale_product_group",
        group_url,
        traverse="/sale_product_groups/{pid}",
    )


def includeme(config):
    """
    Pyramid's inclusion mechanism
    """
    add_routes(config)

    config.add_view(
        company_products_view,
        route_name="sale_categories",
        permission="list_sale_products",
        renderer="/sale/products.mako",
    )

    add_json_view = functools.partial(
        config.add_view,
        renderer='json',
        permission='add_sale_products',
        xhr=True,
    )

    add_json_view(
        company_products_options_ajax_view,
        route_name="sale_categories",
        request_param='action=options',
        permission="list_sale_products",
    )

    add_json_view(
        company_products_jstree_ajax_view,
        route_name="sale_categories",
        request_param='action=jstree',
        permission="list_sale_products",
    )

    add_json_view(
        company_products_ajax_view,
        route_name="sale_categories",
        request_param='action=products',
        permission="list_sale_products",
    )

    add_json_view(
        RestCategories,
        attr='collection_get',
        route_name='sale_categories',
        request_method="GET",
        permission="list_sale_products",
    )
    add_json_view(
        RestCategories,
        attr='post',
        route_name='sale_categories',
        request_method="POST",
        permission="add_sale_product",
    )
    add_json_view(
        RestCategories,
        attr='put',
        route_name='sale_category',
        request_method="PUT",
        permission="edit_sale_product"
    )
    add_json_view(
        RestCategories,
        attr='delete',
        route_name='sale_category',
        request_method="DELETE",
        permission="edit_sale_product"
    )

    add_json_view(
        RestProducts,
        attr='collection_get',
        route_name='sale_products',
        request_method="GET",
        permission="view_sale_product",
    )
    add_json_view(
        RestProducts,
        attr='post',
        route_name='sale_products',
        request_method="POST",
        permission="edit_sale_product",
    )
    add_json_view(
        RestProducts,
        attr='get',
        route_name='sale_product',
        request_method="GET",
        permission="view_sale_product",
    )
    add_json_view(
        RestProducts,
        attr='put',
        route_name='sale_product',
        request_method="PUT",
        permission="edit_sale_product",
    )
    add_json_view(
        RestProducts,
        attr='delete',
        route_name='sale_product',
        request_method="DELETE",
        permission="edit_sale_product",
    )

    add_json_view(
        RestProductGroups,
        attr='collection_get',
        route_name='sale_product_groups',
        request_method="GET",
        permission="view_sale_product",
    )
    add_json_view(
        RestProductGroups,
        attr='post',
        route_name='sale_product_groups',
        request_method="POST",
        permission="edit_sale_product",
    )
    add_json_view(
        RestProductGroups,
        attr='get',
        route_name='sale_product_group',
        request_method="GET",
        permission="view_sale_product",
    )
    add_json_view(
        RestProductGroups,
        attr='put',
        route_name='sale_product_group',
        request_method="PUT",
        permission="edit_sale_product",
    )
    add_json_view(
        RestProductGroups,
        attr='delete',
        route_name='sale_product_group',
        request_method="DELETE",
        permission="edit_sale_product",
    )
