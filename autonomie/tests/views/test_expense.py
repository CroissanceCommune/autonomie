# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    tests autonomie.views.expense
"""
import pytest

from datetime import date
from autonomie.models.user import User
from autonomie.models.company import Company
from autonomie.models.treasury import (ExpenseType, ExpenseKmType,
                ExpenseSheet, ExpenseLine, ExpenseKmLine)
from autonomie.utils.rest import RestError
from autonomie.views.expense import (
        RestExpenseLine,
        get_expense_sheet,
        RestExpenseKmLine,
        ExpenseKmLineJson,
        ExpenseLineJson,
        ExpenseSheetView,
        get_bookmarks,
        BookMarkHandler,
        )
from autonomie.forms.expense import ExpenseKmLineSchema, ExpenseLineSchema
from autonomie.tests.base import (
        BaseFunctionnalTest,
        BaseViewTest,
        )


@pytest.fixture
def company(content):
    return Company.query().first()


@pytest.fixture
def user(content):
    return User.query().first()


@pytest.fixture
def expensetype(dbsession):
    type_ = ExpenseType(label=u"Restauration", code="000065588")
    dbsession.add(type_)
    dbsession.flush()
    return type_


@pytest.fixture
def expensekmtype(dbsession):
    type_ = ExpenseKmType(label=u"Restauration", code="000065588", amount=0.625)
    dbsession.add(type_)
    dbsession.flush()
    return type_


@pytest.fixture
def sheet(user, company, get_csrf_request_with_db, expensetype):
    request = get_csrf_request_with_db()
    year = date.today().year
    month = date.today().month
    return get_expense_sheet(request, year, month, company.id, user.id)

def test_reset_success(config, dbsession, get_csrf_request_with_db, sheet, expensetype):
    config.add_route('user_expenses', '/')
    request = get_csrf_request_with_db()
    sheet.lines.append(ExpenseLine(tva=1960, ht=150, type_object=expensetype))
    dbsession.merge(sheet)
    dbsession.flush()
    request.context = sheet
    view = ExpenseSheetView(request)
    view.reset_success(appstruct={})


def test_get_line(dbsession, get_csrf_request_with_db, sheet, expensetype):
    request = get_csrf_request_with_db()
    request.context = sheet
    sheet.lines.append(ExpenseLine(tva=1960, ht=150, type_object=expensetype))
    dbsession.merge(sheet)
    dbsession.flush()
    line = request.context.lines[-1]
    request.matchdict = {'lid':line.id}
    view = RestExpenseLine(request)
    assert view.getOne() == line
    request.matchdict = {'lid':0}
    view = RestExpenseLine(request)
    with pytest.raises(RestError):
        view.getOne()

def test_post_line(get_csrf_request_with_db, sheet, expensetype):
    request = get_csrf_request_with_db()
    request.context = sheet
    appstruct = {'ht':'150.0',
                    'tva':'15',
                    'description':'Test',
                    'date':'2112-10-12',
                    'category':'1',
                    'type_id': expensetype.id}
    request.json_body = appstruct
    view = RestExpenseLine(request)
    view.post()
    line = sheet.lines[-1]
    assert line.tva == 1500
    assert line.ht == 15000
    assert line.date == date(2112, 10, 12)
    assert line.type_id == expensetype.id
    assert line.category == u"1"
    assert isinstance(line, ExpenseLine)


@pytest.fixture
def sheet_with_kmline(get_csrf_request_with_db, sheet, expensekmtype):
    request = get_csrf_request_with_db()
    request.context = sheet
    appstruct = {'km':'150.0',
                    'start':'point a',
                    'end':'point b',
                    'description':'Test',
                    'date':'2112-10-12',
                    'category':'1',
                    'type_id': expensekmtype.id}
    request.json_body = appstruct
    view = RestExpenseKmLine(request)
    view.post()
    return sheet

def test_get_kmline(get_csrf_request_with_db, sheet_with_kmline):
    """
    Check the rest api return the same line object
    """
    line = sheet_with_kmline.kmlines[-1]
    request = get_csrf_request_with_db()
    request.context = sheet_with_kmline
    request.matchdict['lid'] = line.id
    view = RestExpenseKmLine(request)
    rest_line = view.getOne()
    assert line.id == rest_line.id

def test_post_kmline(get_csrf_request_with_db, sheet_with_kmline, expensekmtype):
    line = sheet_with_kmline.kmlines[-1]
    assert line.km == 15000
    assert line.start == u"point a"
    assert line.end == u"point b"
    assert line.date == date(2112, 10, 12)
    assert line.type_id == expensekmtype.id
    assert line.category == u"1"
    assert isinstance(line, ExpenseKmLine)

def test_put_kmline(get_csrf_request_with_db, sheet_with_kmline, expensekmtype):
    line = sheet_with_kmline.kmlines[-1]
    appstruct = {'km':'12.0',
                    "start":"point a2",
                    "end":"point b2",
                    "date":line.date.isoformat(),
                    "description":line.description,
                    "category":line.category,
                    "type_id":line.type_id}
    request = get_csrf_request_with_db()
    request.context = sheet_with_kmline
    request.matchdict['lid'] = line.id
    request.json_body = appstruct
    view = RestExpenseKmLine(request)
    view.put()
    assert line.km == 1200
    assert line.start == u"point a2"
    assert line.end == u"point b2"
    assert line.type_id == expensekmtype.id


@pytest.fixture
def bookmark_handler(get_csrf_request_with_db, user):
    req = get_csrf_request_with_db()
    req.user = user
    return BookMarkHandler(req)


def test_bookmark_handler_init(bookmark_handler, user, pyramid_request):
    assert bookmark_handler.bookmarks == {}

    user.session_datas = {'expense':
        {'bookmarks':
            {1:
                {'description':u'test', 'ht': 2.25, 'tva': 1.2}
            }
        }}
    bookmark_handler.refresh()
    assert bookmark_handler.bookmarks == \
                    {1: {'description':u'test', 'ht': 2.25, 'tva': 1.2}}

def test_bookmark_handler_next_id(bookmark_handler, user):
    user.session_datas = {'expense':
        {'bookmarks':
            {"1":
                {'description':u'test 1', 'ht': 2.25, 'tva': 1.2},
                2:
                {'description':u'test 2', 'ht': 2.5, 'tva': 1.25},

            }
        }}
    bookmark_handler.refresh()
    assert bookmark_handler._next_id() == 3

def test_bookmark_handler_store(dbsession, bookmark_handler, user):
    a = {'description':u'test 1', 'ht': 2.25, 'tva': 1.2}
    bookmark_handler.store(a)
    dbsession.flush()
    b = {'description':u'test 2', 'ht': 2.5, 'tva': 1.25}
    bookmark_handler.store(b)
    dbsession.flush()
    c = {'description':u'test 3', 'ht': 2.5, 'tva': 1.25}
    bookmark_handler.store(c)
    dbsession.flush()
    assert user.session_datas.keys() == ['expense']
    assert len(user.session_datas['expense']['bookmarks']) == 3
    assert user.session_datas['expense']['bookmarks'][3] == c
