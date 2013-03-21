# -*- coding: utf-8 -*-
# * File Name : test_expense.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 12-03-2013
# * Last Modified :
#
# * Project :
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
from autonomie.views.expense import (RestExpenseLine, ExpensePage,
        RestExpenseKmLine, ExpenseKmLineJson, ExpenseLineJson)
from autonomie.views.forms.expense import ExpenseKmLineSchema, ExpenseLineSchema
from autonomie.tests.base import BaseFunctionnalTest


class BaseRest(BaseFunctionnalTest):
    def company(self):
        return Company.query().first()

    def user(self):
        return User.query().first()

    def sheet(self):
        request = self.get_csrf_request()
        request.context = self.company()
        request.matchdict = {'uid':self.user().id}
        page = ExpensePage(request)
        return page._expense()


class TestRestExpenseLine(BaseRest):
    def test_getOne(self):
        request = self.get_csrf_request()
        request.context = self.sheet()
        line = request.context.lines[0]
        request.matchdict = {'lid':line.id}
        view = RestExpenseLine(request)
        self.assertEqual(view.getOne(), line)
        request.matchdict = {'lid':0}
        view = RestExpenseLine(request)
        self.assertRaises(RestError, view.getOne)

    def test_post(self):
        request = self.get_csrf_request()
        request.context = self.sheet()
        appstruct = {'ht':'150.0',
                     'tva':'15',
                     'description':'Test',
                     'date':'2112-10-12',
                     'category':'1',
                     'code':'0001'}
        request.json_body = appstruct
        view = RestExpenseLine(request)
        view.post()
        sheet = self.sheet()
        line = sheet.lines[-1]
        self.assertEqual(line.tva, 1500)
        self.assertEqual(line.ht, 15000)
        self.assertEqual(line.date, date(2112, 10, 12))
        self.assertEqual(line.code, u"0001")
        self.assertEqual(line.category, u"1")
        self.assertTrue(isinstance(line, ExpenseLine))


class TestRestExpenseKmLine(BaseRest):
    def addOne(self):
        request = self.get_csrf_request()
        request.context = self.sheet()
        appstruct = {'km':'150.0',
                     'start':'point a',
                     'end':'point b',
                     'description':'Test',
                     'date':'2112-10-12',
                     'category':'1',
                     'code':'0004'}
        request.json_body = appstruct
        view = RestExpenseKmLine(request)
        view.post()

    def getOne(self):
        sheet = self.sheet()
        return sheet.kmlines[-1]

    def getIt(self):
        elem = self.getOne()
        request = self.get_csrf_request()
        request.context = self.sheet()
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
        self.assertEqual(line.code, u"0004")
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
                     "code":line.code}
        request = self.get_csrf_request()
        request.context = self.sheet()
        request.matchdict['lid'] = line.id
        request.json_body = appstruct
        view = RestExpenseKmLine(request)
        view.put()
        line = self.getOne()
        self.assertEqual(line.km, 1200)
        self.assertEqual(line.start, u"point a2")
        self.assertEqual(line.end, u"point b2")
        self.assertEqual(line.code, u"0004")
