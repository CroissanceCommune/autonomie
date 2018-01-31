# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import datetime
from sqlalchemy import or_

from autonomie.utils.strings import month_name
from autonomie.models.accounting.income_statement_measures import (
    IncomeStatementMeasureGrid,
    IncomeStatementMeasureType,
)
from autonomie.forms.accounting import get_income_statement_measures_list_schema
from autonomie.views import BaseListView

logger = logging.getLogger(__name__)


class CompanyIncomeStatementMeasuresListView(BaseListView):
    schema = get_income_statement_measures_list_schema()
    use_paginate = False
    default_sort = 'month'
    sort_columns = {'month': 'month'}
    filter_button_label = u"Changer"

    title = u"Compte de résultat"

    def get_types(self, ids):
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

    def query(self):
        """
        Collect the grids we present in the output
        """
        query = self.request.dbsession.query(IncomeStatementMeasureGrid)
        query = query.join(IncomeStatementMeasureGrid.measures)
        query = query.filter(
            IncomeStatementMeasureGrid.company_id == self.context.id
        )
        return query

    def filter_year(self, query, appstruct):
        """
        Filter the current query by a given year
        """
        self.year = year = appstruct['year']
        logger.debug("Filtering by year : %s" % year)

        query = query.filter(
            IncomeStatementMeasureGrid.year == year
        )
        return query

    def _get_month_cell(self, type_id, month, grids):
        """
        Return the value to display in month related cells
        """
        grid = grids[month]
        result = None

        if grid is not None:
            measure = grid.get_measure_by_type(type_id)
            if measure is not None:
                result = measure.get_value()

        return result

    def _grid_by_month(self, month_grids):
        """
        """
        result = dict((month, None) for month in range(1, 13))
        for grid in month_grids:
            result[grid.month] = grid
        return result

    def more_template_vars(self, response_dict):
        """
        Add template datas in the response dictionnary
        """
        records = response_dict['records']
        response_dict['types'] = self.get_types(
            [rec.id for rec in records]
        )

        response_dict['month_names_dict'] = dict(
            (i, month_name(i)) for i in range(1, 13)
        )
        response_dict['current_year'] = datetime.date.today().year
        response_dict['selected_year'] = int(self.year)
        response_dict['grids'] = self._grid_by_month(records)
        response_dict['month_cell_factory'] = self._get_month_cell

        response_dict['ca'] = 15000
        return response_dict


def add_routes(config):
    config.add_route(
        "/companies/{id}/accounting/income_statement_measure_grids",
        "/companies/{id}/accounting/income_statement_measure_grids",
        traverse="/companies/{id}",
    )


def add_views(config):
    config.add_view(
        CompanyIncomeStatementMeasuresListView,
        route_name="/companies/{id}/accounting/income_statement_measure_grids",
        permission="view.accounting",
        renderer="/accounting/income_statement_measures.mako",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
