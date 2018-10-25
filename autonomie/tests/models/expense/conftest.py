# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest


@pytest.fixture
def mk_expense_type(dbsession):
    from autonomie.models.expense.types import (
        ExpenseKmType,
        ExpenseTelType,
        ExpenseType,
    )

    def builder(label="", code="", amount=None, percentage=None, year=2018):

        args = dict(
            label=label,
            code=code,
        )
        if amount is not None:
            factory = ExpenseKmType
            args.update(
                dict(
                    amount=amount,
                    year=year
                )
            )

        elif percentage is not None:
            factory = ExpenseTelType
            args.update(
                dict(
                    percentage=percentage
                )
            )

        else:
            factory = ExpenseType

        typ = factory(**args)
        dbsession.add(typ)
        dbsession.flush()
        return typ
    return builder
