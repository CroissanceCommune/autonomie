# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
import colander


@pytest.fixture
def income_measure_type_category(dbsession):
    from autonomie.models.accounting.income_statement_measures import (
        IncomeStatementMeasureTypeCategory,
    )
    cat = IncomeStatementMeasureTypeCategory(label=u"Produits")
    dbsession.add(cat)
    dbsession.flush()
    return cat


@pytest.fixture
def income_measure_type(dbsession, income_measure_type_category):
    from autonomie.models.accounting.income_statement_measures import (
        IncomeStatementMeasureType,
    )
    typ = IncomeStatementMeasureType(
        label="Label 1",
        category_id=income_measure_type_category.id,
        account_prefix="701",
    )
    dbsession.add(typ)
    dbsession.flush()
    typ.category = income_measure_type_category
    return typ


def test_label_validator(pyramid_request, income_measure_type):
    from autonomie.forms.accounting import deferred_label_validator

    pyramid_request.context = None
    label_validator = deferred_label_validator(
        None,
        kw={'request': pyramid_request}
    )

    with pytest.raises(colander.Invalid):
        label_validator(None, "Test : Test")

    with pytest.raises(colander.Invalid):
        label_validator(None, "Test ! Test")

    with pytest.raises(colander.Invalid):
        label_validator(None, "Label 1")

    with pytest.raises(colander.Invalid):
        label_validator(None, "Produits")

    assert label_validator(None, "Test") == None


def test_label_validator_with_context(
    pyramid_request,
    income_measure_type,
    income_measure_type_category
):
    from autonomie.forms.accounting import deferred_label_validator

    pyramid_request.context = income_measure_type
    label_validator = deferred_label_validator(
        None,
        kw={'request': pyramid_request}
    )

    with pytest.raises(colander.Invalid):
        label_validator(None, "Test : Test")

    with pytest.raises(colander.Invalid):
        label_validator(None, "Test ! Test")
    with pytest.raises(colander.Invalid):
        assert label_validator(None, "Produits") is None

    assert label_validator(None, "Label 1") is None
    assert label_validator(None, "Test") == None


def test_complex_total_validator():
    from autonomie.forms.accounting import complex_total_validator
    for value in (
        '{Salaires]',
        '[Salaires}',
        '{Salaires : Tout}',
        '100 * {Test ! }',
    ):
        with pytest.raises(colander.Invalid):
            complex_total_validator(None, value)
