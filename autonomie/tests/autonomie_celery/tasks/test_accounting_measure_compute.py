# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_get_measure_compiler():
    from autonomie_celery.tasks.accounting_measure_compute import (
        get_measure_compiler,
        IncomeStatementMeasureCompiler,
        TreasuryMeasureCompiler
    )
    assert get_measure_compiler('general_ledger') == \
        IncomeStatementMeasureCompiler
    assert get_measure_compiler('analytical_balance') == TreasuryMeasureCompiler


def test_income_statement_measure_compiler(
    dbsession,
    general_upload,
    general_operations,
    income_measure_types,
    company,
):
    from autonomie_celery.tasks.accounting_measure_compute import (
        IncomeStatementMeasureCompiler,
    )
    compiler = IncomeStatementMeasureCompiler(general_upload, general_operations)
    assert compiler.measure_types.count() == len(income_measure_types) - 2

    grids = compiler.process_datas()
    grids = grids.values()
    grids = sorted(grids, key=lambda i: i.month)

    assert len(grids) == 2

    assert grids[0].month == 1
    assert grids[0].year == general_upload.date.year

    assert grids[1].month == 2
    assert grids[1].year == general_upload.date.year

    grid = grids[0]

    assert grid.company_id == company.id
    assert len(grid.measures) == 5
    assert grid.get_measure_by_type(income_measure_types[0].id).value == 1000
    assert grid.get_measure_by_type(income_measure_types[1].id).value == 2000
    assert grid.get_measure_by_type(income_measure_types[2].id).value == -1000
    assert grid.get_measure_by_type(income_measure_types[3].id).value == -1000
    assert grid.get_measure_by_type(income_measure_types[6].id).value == 5625


def test_treasury_measure_compiler(
    dbsession,
    analytical_upload,
    analytical_operations,
    treasury_measure_types,
    company,
):
    from autonomie_celery.tasks.accounting_measure_compute import (
        TreasuryMeasureCompiler,
    )
    compiler = TreasuryMeasureCompiler(analytical_upload, analytical_operations)
    assert compiler.measure_types.count() == len(treasury_measure_types)

    grids = compiler.process_datas()
    grids = grids.values()

    assert len(grids) == 1
    assert grids[0].date == analytical_upload.date

    grid = grids[0]
    assert grid.company_id == company.id
    assert len(grid.measures) == 3
    assert grid.get_measure_by_type(treasury_measure_types[0].id).value == 2000
    assert grid.get_measure_by_type(treasury_measure_types[1].id).value == -1000
    assert grid.get_measure_by_type(treasury_measure_types[5].id).value == -1000

