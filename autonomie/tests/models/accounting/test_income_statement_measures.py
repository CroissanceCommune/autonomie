# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest


@pytest.fixture
def income_statement_measure_type(dbsession):
    from autonomie.models.accounting.income_statement_measures import (
        IncomeStatementMeasureType,
    )
    type_ = IncomeStatementMeasureType(
        order=1,
        category="Test",
        label=u"label",
        account_prefix="706",
    )
    dbsession.add(type_)
    dbsession.flush()
    return type_


def test_get_next_order_by_category(income_statement_measure_type):
    from autonomie.models.accounting.income_statement_measures import (
        IncomeStatementMeasureType,
    )
    assert IncomeStatementMeasureType.get_next_order_by_category("Test") == 2
    assert IncomeStatementMeasureType.get_next_order_by_category("Other") == 0
