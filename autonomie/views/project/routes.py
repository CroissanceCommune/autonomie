# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os


COMPANY_PROJECTS_ROUTE = "/companies/{id}/projects"
PROJECT_ROUTE = "/projects"
PROJECT_ITEM_ROUTE = os.path.join(PROJECT_ROUTE, "{id}")
PROJECT_ITEM_ESTIMATION_ROUTE = os.path.join(PROJECT_ITEM_ROUTE, 'estimations')
PROJECT_ITEM_PHASE_ROUTE = os.path.join(PROJECT_ITEM_ROUTE, 'phases')
PROJECT_ITEM_GENERAL_ROUTE = os.path.join(PROJECT_ITEM_ROUTE, 'general')
PROJECT_ITEM_INVOICE_ROUTE = os.path.join(PROJECT_ITEM_ROUTE, 'invoices')
PROJECT_ITEM_INVOICE_EXPORT_ROUTE = PROJECT_ITEM_INVOICE_ROUTE + ".{extension}"
PROJECT_ITEM_BUSINESS_ROUTE = os.path.join(PROJECT_ITEM_ROUTE, 'businesses')
PHASE_ROUTE = "/phases"
PHASE_ITEM_ROUTE = os.path.join(PHASE_ROUTE, "{id}")


def includeme(config):
    config.add_route(
        COMPANY_PROJECTS_ROUTE,
        COMPANY_PROJECTS_ROUTE,
        traverse='/companies/{id}',
    )
    for route in (
        PROJECT_ITEM_ROUTE,
        PROJECT_ITEM_PHASE_ROUTE,
        PROJECT_ITEM_GENERAL_ROUTE,
        PROJECT_ITEM_ESTIMATION_ROUTE,
        PROJECT_ITEM_INVOICE_ROUTE,
        PROJECT_ITEM_INVOICE_EXPORT_ROUTE,
        PROJECT_ITEM_BUSINESS_ROUTE,
    ):
        config.add_route(route, route, traverse='/projects/{id}')
    config.add_route(
        PHASE_ITEM_ROUTE,
        PHASE_ITEM_ROUTE,
        traverse='/phases/{id}',
    )
