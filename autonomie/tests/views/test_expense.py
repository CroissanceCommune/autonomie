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
from autonomie.views.forms.expense import ExpenseKmLineSchema, ExpenseLineSchema
from autonomie.tests.base import (
        BaseFunctionnalTest,
        BaseViewTest,
        )


class BaseExpense(BaseFunctionnalTest):
    def company(self):
        return Company.query().first()

    def user(self):
        return User.query().first()

    def sheet(self, request):
        year = date.today().year
        month = date.today().month
        cid = self.company().id
        uid = self.user().id
        return get_expense_sheet(request, year, month, cid, uid)


class TestExpenseSheet(BaseExpense):
    def get_type(self):
        type_ = ExpenseType(label=u"Restauration", code="000065588")
        self.session.add(type_)
        self.session.flush()
        return type_

    def test_reset_success(self):
        self.config.add_route('user_expenses', '/')
        request = self.get_csrf_request()
        sheet = self.sheet(request)
        type_ = self.get_type()
        sheet.lines.append(ExpenseLine(tva=1960, ht=150, type_object=type_))
        self.session.merge(sheet)
        self.session.flush()
        request.context = sheet
        view = ExpenseSheetView(request)
        view.reset_success(appstruct={})


class TestRestExpenseLine(BaseExpense):
    def test_getOne(self):
        request = self.get_csrf_request()
        request.context = self.sheet(request)
        line = request.context.lines[0]
        request.matchdict = {'lid':line.id}
        view = RestExpenseLine(request)
        self.assertEqual(view.getOne(), line)
        request.matchdict = {'lid':0}
        view = RestExpenseLine(request)
        self.assertRaises(RestError, view.getOne)

    def test_post(self):
        request = self.get_csrf_request()
        request.context = self.sheet(request)
        appstruct = {'ht':'150.0',
                     'tva':'15',
                     'description':'Test',
                     'date':'2112-10-12',
                     'category':'1',
                     'type_id':5}
        request.json_body = appstruct
        view = RestExpenseLine(request)
        view.post()
        sheet = self.sheet(request)
        line = sheet.lines[-1]
        self.assertEqual(line.tva, 1500)
        self.assertEqual(line.ht, 15000)
        self.assertEqual(line.date, date(2112, 10, 12))
        self.assertEqual(line.type_id, 5)
        self.assertEqual(line.category, u"1")
        self.assertTrue(isinstance(line, ExpenseLine))


class TestRestExpenseKmLine(BaseExpense):
    def addOne(self):
        request = self.get_csrf_request()
        request.context = self.sheet(request)
        appstruct = {'km':'150.0',
                     'start':'point a',
                     'end':'point b',
                     'description':'Test',
                     'date':'2112-10-12',
                     'category':'1',
                     'type_id':1}
        request.json_body = appstruct
        view = RestExpenseKmLine(request)
        view.post()

    def getOne(self):
        request = self.get_csrf_request()
        sheet = self.sheet(request)
        return sheet.kmlines[-1]

    def getIt(self):
        elem = self.getOne()
        request = self.get_csrf_request()
        request.context = self.sheet(request)
        request.matchdict['lid'] = elem.id
        view = RestExpenseKmLine(request)
        return view.getOne()

    def test_get(self):
        self.addOne()
        elem = self.getOne()
        line = self.getIt()
        self.assertEqual(line.id, elem.id)

    def test_post(self):
        self.addOne()
        line = self.getOne()
        self.assertEqual(line.km, 15000)
        self.assertEqual(line.start, u"point a")
        self.assertEqual(line.end, u"point b")
        self.assertEqual(line.date, date(2112, 10, 12))
        self.assertEqual(line.type_id, 1)
        self.assertEqual(line.category, u"1")
        self.assertTrue(isinstance(line, ExpenseKmLine))

    def test_put(self):
        self.addOne()
        line = self.getOne()
        appstruct = {'km':'12.0',
                     "start":"point a2",
                     "end":"point b2",
                     "date":line.date.isoformat(),
                     "description":line.description,
                     "category":line.category,
                     "type_id":line.type_id}
        request = self.get_csrf_request()
        request.context = self.sheet(request)
        request.matchdict['lid'] = line.id
        request.json_body = appstruct
        view = RestExpenseKmLine(request)
        view.put()
        line = self.getOne()
        self.assertEqual(line.km, 1200)
        self.assertEqual(line.start, u"point a2")
        self.assertEqual(line.end, u"point b2")
        self.assertEqual(line.type_id, 1)


class TestBookMarkHandler(BaseViewTest):
    def get_handler(self, user):
        req = self.get_csrf_request()
        req.user = user
        return BookMarkHandler(req)

    def get_user(self):
        return User.query().first()

    def test_init(self):
        user = self.get_user()
        handler = self.get_handler(user)
        self.assertEqual(handler.bookmarks, {})

        user.session_datas = {'expense':
            {'bookmarks':
                {1:
                    {'description':u'test', 'ht': 2.25, 'tva': 1.2}
                }
            }}
        handler = self.get_handler(user)
        self.assertEqual(handler.bookmarks,
                        {1: {'description':u'test', 'ht': 2.25, 'tva': 1.2}})

    def test_next_id(self):
        user = self.get_user()
        user.session_datas = {'expense':
            {'bookmarks':
                {"1":
                    {'description':u'test 1', 'ht': 2.25, 'tva': 1.2},
                 2:
                    {'description':u'test 2', 'ht': 2.5, 'tva': 1.25},

                }
            }}
        handler = self.get_handler(user)
        self.assertEqual(handler._next_id(), 3)

    def test_store(self):
        user = self.get_user()
        handler = self.get_handler(user)
        a = {'description':u'test 1', 'ht': 2.25, 'tva': 1.2}
        handler.store(a)
        self.session.flush()
        b = {'description':u'test 2', 'ht': 2.5, 'tva': 1.25}
        handler.store(b)
        self.session.flush()
        c = {'description':u'test 3', 'ht': 2.5, 'tva': 1.25}
        handler.store(c)
        self.session.flush()
        user = self.get_user()
        self.assertEqual(user.session_datas.keys(), ['expense'])
        self.assertEqual(len(user.session_datas['expense']['bookmarks']), 3)

        self.assertEqual(user.session_datas['expense']['bookmarks'][3], c)
