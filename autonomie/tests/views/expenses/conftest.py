# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime
from pytest import fixture


@fixture
def expense_kmline(dbsession, mk_expense_type):
    typ = mk_expense_type(
        label="KM",
        code="KM",
        amount=1.254,
        year=2018
    )
    from autonomie.models.expense.sheet import ExpenseKmLine
    item = ExpenseKmLine(
        description=u"Aller retour",
        category="1",
        type_id=typ.id,
        km=10000,
        start="Dijon",
        end="Lyon",
    )
    dbsession.add(item)
    dbsession.flush()
    return item


@fixture
def expense_telline(dbsession, mk_expense_type):
    typ = mk_expense_type(percentage=50)
    from autonomie.models.expense.sheet import ExpenseLine
    item = ExpenseLine(
        description=u"Test expense",
        category="1",
        type_id=typ.id,
        ht=3000,
        tva=600,
    )
    dbsession.add(item)
    dbsession.flush()
    return item


@fixture
def expense_line(dbsession, mk_expense_type):
    typ = mk_expense_type(label="Base type")
    from autonomie.models.expense.sheet import ExpenseLine
    item = ExpenseLine(
        description=u"Test expense",
        category="2",
        type_id=typ.id,
        ht=10000,
        tva=2000,
    )
    dbsession.add(item)
    dbsession.flush()
    return item


@fixture
def expense_sheet(
    dbsession,
    company,
    user,
):
    from autonomie.models.expense.sheet import ExpenseSheet
    item = ExpenseSheet(
        month=10,
        year=2015,
        company_id=company.id,
        user_id=user.id,
    )
    dbsession.add(item)
    dbsession.flush()
    return item


@fixture
def full_expense_sheet(
    dbsession,
    expense_sheet,
    expense_line,
    expense_kmline,
    expense_telline,
):
    expense_sheet.lines.append(expense_line)
    expense_sheet.lines.append(expense_telline)
    expense_sheet.kmlines.append(expense_kmline)
    dbsession.add(expense_sheet)
    dbsession.flush()
    return expense_sheet
