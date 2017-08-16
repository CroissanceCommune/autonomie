# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

# NOTE : fixture can be found in the associated conftest.py file
import pytest


def test_get_sheet(dbsession, get_csrf_request_with_db, full_expense_sheet):
    from autonomie.views.expenses.rest_api import RestExpenseSheetView
    request = get_csrf_request_with_db()
    request.context = full_expense_sheet
    view = RestExpenseSheetView(request)
    result = view.get()
    assert len(result.lines) == 2
    assert len(result.kmlines) == 1


def test_add_sheet(
    dbsession,
    get_csrf_request_with_db,
    user,
    company
):
    from autonomie.views.expenses.rest_api import RestExpenseSheetView
    request = get_csrf_request_with_db(post={
        'month': 10,
        'year': 2016,
    })
    request.context = company
    request.user = user
    view = RestExpenseSheetView(request)
    result = view.post()
    assert result.month == 10
    assert result.user_id == user.id
    assert result.company_id == company.id


def test_add_sheet_fail(
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    company,
    user
):
    from autonomie.utils.rest import RestError
    from autonomie.views.expenses.rest_api import RestExpenseSheetView
    request = get_csrf_request_with_db(post={
        'month': 10,
        'year': 2015,
    })
    request.context = company
    request.user = user
    view = RestExpenseSheetView(request)
    with pytest.raises(RestError) as invalid_exc:
        view.post()

    assert invalid_exc.value.code == 400


def test_edit_sheet(
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    company
):
    from autonomie.views.expenses.rest_api import RestExpenseSheetView
    request = get_csrf_request_with_db(post={
        'month': 8,
        'year': 2005,
    })
    request.context = full_expense_sheet
    view = RestExpenseSheetView(request)
    result = view.put()
    assert result.year == 2005
    assert result.month == 8


def test_add_line(
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    expense_type,
):
    from autonomie.views.expenses.rest_api import RestExpenseLineView
    request = get_csrf_request_with_db(post={
        'description': u"Test",
        "category": "1",
        "ht": "50",
        "tva": "10",
        "type_id": expense_type.id,
    })
    request.context = full_expense_sheet
    view = RestExpenseLineView(request)
    line = view.post()

    assert line.ht == 5000
    assert line.tva == 1000
    assert line.category == "1"
    assert line.description == u"Test"


def test_edit_line(
    dbsession,
    get_csrf_request_with_db,
    expense_line,
):
    from autonomie.views.expenses.rest_api import RestExpenseLineView
    request = get_csrf_request_with_db(post={
        'description': u"Test Modify",
        "category": "2",
        "ht": "55",
        "tva": "11",
    })
    request.context = expense_line
    view = RestExpenseLineView(request)
    view.put()

    assert expense_line.ht == 5500
    assert expense_line.tva == 1100
    assert expense_line.category == "2"
    assert expense_line.description == u"Test Modify"
