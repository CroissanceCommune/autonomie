# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import colander
from sqlalchemy import extract

from autonomie.models.accounting.income_statement_measures import (
    IncomeStatementMeasureGrid,
    IncomeStatementMeasureType,
)
from autonomie.forms.accounting import get_income_statement_measures_list_schema
from autonomie.views import BaseListView

class CompanyIncomeStatementMeasuresListView(BaseListView):

    def get_types(self):
        """
        Collect measure types

        * Active ones
        * For which we have measures
        """
        clause = or_(
            IncomeStatementMeasureType.active == True,
            IncomeStatementMeasureType.id.in_(ids)
        )
        return IncomeStatementMeasureType.query().filter(clause).all()

    def get_grids(self):
        """
        Collect the grids we present in the output
        """
        pass


def add_routes(config):
    config.add_route(
        "/companies/{id}/accounting/income_statement_measure_grids",
        "/companies/{id}/accounting/income_statement_measure_grids",
        traverse="/companies/{id}",
    )
    config.add_route(
        "/income_statement_measure_grids/{id}",
        "/income_statement_measure_grids/{id}",
        traverse="/income_statement_measure_grids/{id}",
    )


def add_views(config):
    config.add_view(
        CompanyIncomeStatementMeasuresListView,
        route_name="/companies/{id}/accounting/income_statement_measure_grids",
        permission="view.accounting",
        renderer="/accounting/measures.mako",
    )
    config.add_view(
        CompanyStatementMeasuresListView,
        route_name="/income_statement_measure_grids/{id}",
        permission="view.accounting",
        renderer="/accounting/measures.mako",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
