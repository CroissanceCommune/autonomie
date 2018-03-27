# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


class TestYearGlobalGrid:
    def get_global_grid(self, grids=(), types=[], turnover=10000):
        from autonomie.views.accounting.income_statement_measures import (
            YearGlobalGrid,
        )
        return YearGlobalGrid(
            grids=grids,
            types=types,
            turnover=turnover
        )

    def test__get_default_category_totals(
        self, income_measure_type_categories, income_measure_types
    ):
        grid = self.get_global_grid(types=income_measure_types)
        category_totals = grid._get_default_category_totals()

        assert category_totals.keys() == [
            c.id for c in income_measure_type_categories
        ]
        month_dict = category_totals.values()[0]
        assert len(month_dict.keys()) == 13

        for value in month_dict.values():
            assert value == 0

    def test_compile_rows(
        self, income_measure_type_categories, income_measure_types,
        income_measure_grid,
    ):
        global_grid = self.get_global_grid(
            types=income_measure_types,
            grids=[income_measure_grid],
            turnover=10000
        )
        print(global_grid.rows)

        assert global_grid.rows[0] == (
            income_measure_types[0],
            [0, 0, 8000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8000, 80]
        )
        assert global_grid.rows[1] == (
            income_measure_types[1],
            [0, 0, 2000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2000, 20]
        )
        assert global_grid.rows[2] == (
            income_measure_types[2],
            [0, 0, -1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1000, -10]
        )
        assert global_grid.rows[3] == (
            income_measure_types[3],
            [0, 0, -500, 0, 0, 0, 0, 0, 0, 0, 0, 0, -500, -5]
        )
        assert global_grid.rows[4] == (
            income_measure_types[4],
            [0, 0, 8500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8500, 85]
        )
        assert global_grid.rows[5] == (
            income_measure_types[5],
            [0, 0, -15, 0, 0, 0, 0, 0, 0, 0, 0, 0, -15, -0.15]
        )
        assert global_grid.rows[6] == (
            income_measure_types[6],
            [0, 0, 9000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9000, 90]
        )
