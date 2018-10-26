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
    mk_expense_type,
):
    typ = mk_expense_type(label="test")
    from autonomie.views.expenses.rest_api import RestExpenseLineView
    request = get_csrf_request_with_db(post={
        'description': u"Test",
        "category": "1",
        "ht": "50",
        "tva": "10",
        "type_id": typ.id,
    })
    request.context = full_expense_sheet
    view = RestExpenseLineView(request)
    line = view.post()

    assert line.ht == 5000
    assert line.tva == 1000
    assert line.category == "1"
    assert line.description == u"Test"
    assert line.type_object == typ


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


def test_add_kmline(
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    mk_expense_type,
):
    typ = mk_expense_type(amount=0.184)
    from autonomie.views.expenses.rest_api import RestExpenseKmLineView
    request = get_csrf_request_with_db(post={
        'description': u"Test",
        "category": "1",
        "start": "Start point",
        "end": "End point",
        "km": "50",
        "type_id": typ.id,
    })
    request.context = full_expense_sheet
    view = RestExpenseKmLineView(request)
    line = view.post()

    assert line.km == 5000
    assert line.category == "1"
    assert line.description == u"Test"
    assert line.start == u"Start point"
    assert line.end == u"End point"
    assert line.type_object == typ


def test_edit_kmline(
    dbsession,
    get_csrf_request_with_db,
    expense_kmline,
):
    from autonomie.views.expenses.rest_api import RestExpenseKmLineView
    request = get_csrf_request_with_db(post={
        'description': u"Test Modify",
        "category": "2",
        "km": "55",
    })
    request.context = expense_kmline
    view = RestExpenseKmLineView(request)
    view.put()

    assert expense_kmline.km == 5500
    assert expense_kmline.category == "2"
    assert expense_kmline.description == u"Test Modify"
    assert expense_kmline.start == u"Dijon"


def test_line_type_required(
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
):
    from autonomie.views.expenses.rest_api import RestExpenseKmLineView
    from autonomie.utils.rest import RestError
    request = get_csrf_request_with_db(post={
        'description': u"Test",
        "category": "1",
        "start": "Start point",
        "end": "End point",
        "km": "50",
        "type_id": -1,
    })
    request.context = full_expense_sheet
    view = RestExpenseKmLineView(request)
    with pytest.raises(RestError) as exc:
        view.post()
    assert exc.value.code == 400


def test_bookmark_view(
    dbsession,
    get_csrf_request_with_db,
    mk_expense_type,
    user
):
    typ = mk_expense_type(label="base")
    from autonomie.views.expenses.rest_api import RestBookMarkView
    request = get_csrf_request_with_db(
        post={
            'type_id': typ.id,
            "tva": "20",
            "ht": "100",
            "description": u"Bookmark"
        }
    )
    request.user = user
    view = RestBookMarkView(request)
    view.post()
    bookmarks = user.session_datas['expense']['bookmarks']
    bookmark = bookmarks[1]
    assert bookmark['ht'] == 100
    assert bookmark['tva'] == 20
    assert bookmark['description'] == "Bookmark"
    assert bookmark['type_id'] == typ.id
    assert bookmark['id'] == 1


def test_forbidden_sheet_status(
    config,
    user,
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
):
    from autonomie.utils.rest import RestError
    from autonomie.views.expenses.rest_api import RestExpenseSheetStatusView
    config.add_route('/expenses/{id}', '/{id}')
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=False,
    )
    request = get_csrf_request_with_db(
        post={
            "submit": "valid",
            "comment": "Test status comment",
        }
    )
    request.context = full_expense_sheet
    request.user = user
    request.is_xhr = True

    view = RestExpenseSheetStatusView(request)
    with pytest.raises(RestError) as forbidden_exc:
        view.__call__()
    assert forbidden_exc.value.code == 403


def test_sheet_status_valid(
    config,
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    user,
):
    from autonomie.views.expenses.rest_api import RestExpenseSheetStatusView
    config.add_route('/expenses/{id}', '/{id}')
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True,
    )
    request = get_csrf_request_with_db(
        post={
            "submit": "valid",
            "comment": "Test status comment",
        }
    )
    request.context = full_expense_sheet
    request.user = user
    request.is_xhr = True

    view = RestExpenseSheetStatusView(request)
    result = view.__call__()
    assert result == {'redirect': u'/{0}'.format(full_expense_sheet.id)}
    assert full_expense_sheet.status == 'valid'
    assert full_expense_sheet.communications[0].content == \
        u"Test status comment"
    assert full_expense_sheet.communications[0].user_id == user.id


def test_sheet_justified(
    config,
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    user,
):
    from autonomie.views.expenses.rest_api import (
        RestExpenseSheetJustifiedStatusView,
    )
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True,
    )
    request = get_csrf_request_with_db(
        post={
            "submit": "true",
            "comment": "Test status comment",
        }
    )
    request.context = full_expense_sheet
    request.user = user
    request.is_xhr = True

    view = RestExpenseSheetJustifiedStatusView(request)
    result = view.__call__()
    assert result['status'] == 'success'
    assert result['datas']['justified'] == True
    assert full_expense_sheet.justified
    assert full_expense_sheet.communications[0].content == \
        u"Test status comment"
    assert full_expense_sheet.communications[0].user_id == user.id
    request = get_csrf_request_with_db(
        post={
            "submit": "false",
            "comment": "2nd Test status comment",
        }
    )
    request.context = full_expense_sheet
    request.user = user
    request.is_xhr = True

    result = view.__call__()
    assert result['status'] == 'success'
    assert result['datas']['justified'] == False
    assert not full_expense_sheet.justified
    assert full_expense_sheet.communications[1].content == \
        u"2nd Test status comment"
    assert full_expense_sheet.communications[1].user_id == user.id
