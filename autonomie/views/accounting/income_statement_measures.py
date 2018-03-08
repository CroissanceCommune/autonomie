# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import datetime
from collections import OrderedDict
from sqlalchemy.orm import (
    joinedload,
)

from autonomie.compute import math_utils
from autonomie.utils.strings import (
    month_name,
    format_float,
)
from autonomie.models.accounting.income_statement_measures import (
    IncomeStatementMeasureGrid,
    IncomeStatementMeasureType,
    IncomeStatementMeasureTypeCategory,
)
from autonomie.forms.accounting import get_income_statement_measures_list_schema
from autonomie.views import BaseListView

logger = logging.getLogger(__name__)


class YearGlobalGrid(object):
    """
    Abstract class used to modelize the income statement and group all stuff
    """
    def __init__(self, grids, types, turnover):
        if not grids:
            self.is_void = True
        else:
            self.is_void = False
        self.categories = IncomeStatementMeasureTypeCategory.get_categories()
        # Month grids stored by month number
        self.grids = self._grid_by_month(grids)

        # Types by category id
        self.types = self._type_by_category(types)
        self.turnover = turnover

        # Totals by category_id, by month
        self.category_totals = self._get_default_category_totals()

        self.rows = self.compile_rows()

    @staticmethod
    def _grid_by_month(month_grids):
        """
        Store month grids by month
        """
        result = OrderedDict((month, None) for month in range(1, 13))
        for grid in month_grids:
            result[grid.month] = grid
        return result

    def _get_default_category_totals(self):
        """
        Build default dict used to store category totals

        :returns: A dict in the form
        {'category_id': {'month_number': 0, 'total': 0}}
        """
        month_dict = dict((month, 0) for month in range(1, 13))
        month_dict['total'] = 0
        return dict(
            (category.id, month_dict.copy())
            for category in self.categories
        )

    def _type_by_category(self, types):
        """
        Stores IncomeStatementMeasureType by category (to keep the display
        order)

        :param list types: List of IncomeStatementMeasureType
        :returns: A dict {'category.id': [IncomeStatementMeasureType]}
        :rtype: dict
        """
        result = dict((category.id, []) for category in self.categories)
        for type_ in types:
            result[type_.category.id].append(type_)
        return result

    def _collect_values_for_computation(self, month_number):
        """
        Collect total for the given categories and the given month number

        Sums are compiled while collecting rows and are stored as a dict matrix


                           month_number
            category_id    <value>

        Here, for a given column, we collect all values by category

        :param int month_number: The month number
        :returns: totals stored by category id
        :rtype: dict
        """
        result = {}
        for category in self.categories:
            total = self.category_totals[category.id][month_number]
            result[category.label] = total

        return result

    def compile_rows(self):
        """
        Pre-compute all row datas

        First collect datas collected from the general ledger file
        Then compile totals
        """
        result = []
        result = list(self.compute_rows())

        # After having collected all rows, we compile totals
        for type_, datas in result:
            if type_.computed_total:
                total = 0
                for month in range(1, 13):
                    values = self._collect_values_for_computation(
                        month
                    )
                    month_total = type_.compute_total(values)
                    total += month_total
                    datas[month - 1] = month_total

                datas[-2] = total
                percent = math_utils.percent(total, self.turnover, 0)
                datas[-1] = percent
        return result

    def _get_month_cell(self, grid, type_id):
        """
        Return the value to display in month related cells
        """
        result = 0

        if grid is not None:
            measure = grid.get_measure_by_type(type_id)
            if measure is not None:
                result = measure.get_value()

        return result

    def stream_headers(self):
        yield ""
        for i in range(1, 13):
            yield month_name(i)
        yield "Total"
        yield "% CA"

    def compute_rows(self):
        """
        Compute the main rows of the grid corresponding to the datas retrieved
        by celery
        also fill rows of computed_totals with 0

        :returns: generator yielding 2-uple (type, row) where type is a
        IncomeStatementMeasureType instance and row contains the datas of the
        grid row for the given type (15 columns).
        :rtype: tuple
        """
        for category in self.categories:
            for type_ in self.types[category.id]:
                    row = []
                    if not type_.computed_total:
                        sum = 0
                        for month, grid in self.grids.items():
                            value = self._get_month_cell(grid, type_.id)
                            sum += value
                            row.append(value)
                            self.category_totals[category.id][month] += value
                        self.category_totals[category.id]['total'] += sum

                        row.append(sum)
                        percent = math_utils.percent(sum, self.turnover, 0)
                        row.append(percent)

                    else:
                        row.extend([0 for i in range(0, 14)])

                    yield type_, row

    def format_datas(self):
        """
        Format all numeric datas to strings in localized formats
        """
        for row in self.rows:
            for index, data in enumerate(row[1]):
                row[1][index] = format_float(data, precision=2)


class CompanyIncomeStatementMeasuresListView(BaseListView):
    schema = get_income_statement_measures_list_schema()
    use_paginate = False
    default_sort = 'month'
    sort_columns = {'month': 'month'}
    filter_button_label = u"Changer"

    title = u"Compte de résultat"

    def get_types(self):
        """
        Collect active income statement measure types
        """
        clause = IncomeStatementMeasureType.active == True
        return IncomeStatementMeasureType.query().filter(clause).order_by(
            IncomeStatementMeasureType.order
        ).all()

    def query(self):
        """
        Collect the grids we present in the output
        """
        query = self.request.dbsession.query(IncomeStatementMeasureGrid)
        query = query.options(
            joinedload(IncomeStatementMeasureGrid.measures, innerjoin=True)
        )
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

    def more_template_vars(self, response_dict):
        """
        Add template datas in the response dictionnary
        """
        month_grids = response_dict['records']
        types = self.get_types()
        year_turnover = self.context.get_turnover(self.year)

        grid = YearGlobalGrid(month_grids, types, year_turnover)
        grid.format_datas()
        response_dict['grid'] = grid
        response_dict['current_year'] = datetime.date.today().year
        response_dict['selected_year'] = int(self.year)
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
