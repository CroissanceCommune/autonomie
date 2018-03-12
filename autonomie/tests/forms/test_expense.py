# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
import datetime


@pytest.fixture
def expensetype(dbsession):
    from autonomie.models.expense.types import ExpenseType
    type_ = ExpenseType(label=u"Restauration", code=u"CODE")

    dbsession.add(type_)
    dbsession.flush()
    return type_


@pytest.fixture
def expensekmtype(dbsession):
    from autonomie.models.expense.types import ExpenseKmType
    type_ = ExpenseKmType(
        label=u"voiture",
        year=datetime.date.today().year,
        amount=1.55,
        code="CODEKM"
    )

    dbsession.add(type_)
    dbsession.flush()
    return type_


def test_add_sheet_schema(dbsession, pyramid_request, user, company):
    import colander
    from autonomie.models.expense.sheet import ExpenseSheet
    from autonomie.forms.expense import get_add_edit_sheet_schema

    sheet = ExpenseSheet(
        month=1, year=2017, user_id=user.id, company_id=company.id
    )
    dbsession.add(sheet)
    dbsession.flush()

    schema = get_add_edit_sheet_schema()
    pyramid_request.context = company
    pyramid_request.user = user
    schema = schema.bind(request=pyramid_request)

    result = schema.deserialize({'month': 2, 'year': 2016})

    assert 'month' in result

    with pytest.raises(colander.Invalid):
        schema.deserialize({'month': 2})

    with pytest.raises(colander.Invalid):
        schema.deserialize({'month': 22, 'year': 2017})

    with pytest.raises(colander.Invalid):
        schema.deserialize({'month': 2, 'year': -1})

    with pytest.raises(colander.Invalid):
        schema.deserialize({'month': 1, 'year': 2017})


def test_add_edit_line_schema(dbsession, pyramid_request, expensetype):
    import colander
    from autonomie.models.expense.sheet import (
        ExpenseLine,
    )
    from autonomie.forms.expense import get_add_edit_line_schema

    schema = get_add_edit_line_schema(ExpenseLine)
    schema = schema.bind(request=pyramid_request)

    result = schema.deserialize({
        'ht': '15.52',
        'tva': '1.55',
        'type_id': expensetype.id,
    })

    assert result['ht'] == 1552

    with pytest.raises(colander.Invalid):
        schema.deserialize({
            'ht': 'ab',
            'tva': '1.55',
            'type_id': expensetype.id,
        })

    with pytest.raises(colander.Invalid):
        schema.deserialize({
            'tva': '1.55',
            'type_id': expensetype.id,
        })

    with pytest.raises(colander.Invalid):
        schema.deserialize({
            'ht': '15.52',
            'type_id': expensetype.id,
        })

    with pytest.raises(colander.Invalid):
        schema.deserialize({
            'ht': '15.52',
            'tva': '1.55',
        })


def test_add_edit_kmline_schema(dbsession, pyramid_request, expensetype,
                                expensekmtype):
    import colander
    from autonomie.models.expense.sheet import (
        ExpenseKmLine,
    )
    from autonomie.forms.expense import get_add_edit_line_schema

    schema = get_add_edit_line_schema(ExpenseKmLine)
    schema = schema.bind(request=pyramid_request)

    result = schema.deserialize({
        'km': '2',
        'type_id': expensekmtype.id,
    })

    assert result['km'] == 200

    with pytest.raises(colander.Invalid):
        schema.deserialize({
            'km': '2',
            'type_id': expensetype.id,
        })

    with pytest.raises(colander.Invalid):
        schema.deserialize({
            'type_id': expensekmtype.id,
        })

    with pytest.raises(colander.Invalid):
        schema.deserialize({
            'km': '2',
        })

    expensekmtype.year = 1980
    dbsession.merge(expensekmtype)
    dbsession.flush()
    schema = get_add_edit_line_schema(ExpenseKmLine)
    schema = schema.bind(request=pyramid_request)

    with pytest.raises(colander.Invalid):
        result = schema.deserialize({
            'km': '2',
            'type_id': expensekmtype.id,
        })
