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


def test_add_expense(
    config,
    dbsession,
    get_csrf_request_with_db,
    company,
    user,
):
    from autonomie.views.expenses.expense import ExpenseSheetAddView
    config.add_route('/expenses/{id}', "/{id}")
    request = get_csrf_request_with_db(
        post={'month': '10', 'year': '2017', 'submit': 'submit'}
    )
    request.context = company
    request.matchdict = {'uid': user.id}
    view = ExpenseSheetAddView(request)
    result = view.__call__()
    print(result)
    assert result.code == 302


def test_add_redirect(
    config,
    dbsession,
    get_csrf_request_with_db,
    company,
    user,
    expense_sheet,
):
    from autonomie.views.expenses.expense import ExpenseSheetAddView
    config.add_route('/expenses/{id}', "/{id}")
    request = get_csrf_request_with_db(
        post={'month': '10', 'year': '2015', 'submit': 'submit'}
    )
    request.context = company
    request.matchdict = {'uid': user.id}
    view = ExpenseSheetAddView(request)
    result = view.__call__()
    assert result.location == "/{id}".format(id=expense_sheet.id)


def test_duplicate(
    config,
    dbsession,
    get_csrf_request_with_db,
    company,
    user,
    full_expense_sheet,
    mk_expense_type,
):
    from autonomie.views.expenses.expense import ExpenseSheetDuplicateView
    config.add_route('/expenses/{id}', "/{id}")
    request = get_csrf_request_with_db(
        post={'month': '10', 'year': '2017', 'submit': 'submit'}
    )
    # https://github.com/CroissanceCommune/autonomie/issues/774
    mk_expense_type(label='KM', code='KM', amount=0.184, year=2017)

    request.context = full_expense_sheet
    view = ExpenseSheetDuplicateView(request)
    result = view.__call__()
    assert result.location != "/{id}".format(id=full_expense_sheet.id)

    from autonomie.models.expense.sheet import ExpenseSheet
    id = int(result.location[1:])
    new_sheet = ExpenseSheet.get(id)
    assert new_sheet.month == 10
    assert new_sheet.year == 2017
    assert new_sheet.company_id == company.id
    assert new_sheet.user_id == user.id
    assert len(new_sheet.lines) == len(full_expense_sheet.lines)
    assert len(new_sheet.kmlines) == len(full_expense_sheet.kmlines)


def test_duplicate_redirect(
    config,
    dbsession,
    get_csrf_request_with_db,
    company,
    user,
    full_expense_sheet,
):
    from autonomie.views.expenses.expense import ExpenseSheetDuplicateView
    config.add_route('/expenses/{id}', "/{id}")
    request = get_csrf_request_with_db(
        post={'month': '10', 'year': '2015', 'submit': 'submit'}
    )
    request.context = full_expense_sheet
    view = ExpenseSheetDuplicateView(request)
    result = view.__call__()
    assert result.location == "/{id}".format(id=full_expense_sheet.id)


def test_payment_view(
    config,
    dbsession,
    get_csrf_request_with_db,
    company,
    user,
    full_expense_sheet,
    bank,
    mode,
):
    from autonomie.views.expenses.expense import ExpenseSheetPaymentView
    from collections import OrderedDict
    config.add_route('/expenses/{id}', "/{id}")
    request = get_csrf_request_with_db(
        post=OrderedDict([
            ('amount', str(125.4 + 120 + 36/2)),
            ('mode', mode.label),
            ('__start__', 'date:mapping'),
            ('date', "2017-05-02"),
            ('__end__', 'date:mapping'),
            ("bank_id", str(bank.id)),
            ('submit', 'submit'),
        ])
    )
    request.context = full_expense_sheet
    request.user = user
    view = ExpenseSheetPaymentView(request)
    result = view.__call__()
    assert result.location == "/{id}".format(id=full_expense_sheet.id)
    assert full_expense_sheet.topay() == 0
    assert full_expense_sheet.paid_status == 'resulted'
