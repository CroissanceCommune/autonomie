# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os


BUSINESSES_ROUTE = "/businesses"
BUSINESS_ITEM_ROUTE = os.path.join(BUSINESSES_ROUTE, "{id}")
BUSINESS_ITEM_ESTIMATION_ROUTE = os.path.join(
    BUSINESS_ITEM_ROUTE, "estimations"
)
BUSINESS_ITEM_INVOICE_ROUTE = os.path.join(BUSINESS_ITEM_ROUTE, "invoices")
BUSINESS_ITEM_FILE_ROUTE = os.path.join(BUSINESS_ITEM_ROUTE, "files")


def includeme(config):
    for route in (
        BUSINESS_ITEM_ROUTE,
        BUSINESS_ITEM_ESTIMATION_ROUTE,
        BUSINESS_ITEM_INVOICE_ROUTE,
        BUSINESS_ITEM_FILE_ROUTE,
    ):
        config.add_route(route, route, traverse="/businesses/{id}")
