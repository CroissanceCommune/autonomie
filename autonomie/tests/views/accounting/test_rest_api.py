# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_operation_post(config, get_csrf_request_with_db, company):
    from autonomie.views.accounting.rest_api import (
        AccountingOperationRestView,
    )
    params = {'datas': [
        {
            'analytical_account': u"0USER",
            "general_account": "GENERAL",
            "date": "2018-01-01",
            'label': u"LABEL",
            "debit": "15",
            "credit": "15",
            "balance": "25"
        }
    ]}
    request = get_csrf_request_with_db(post=params)
    view = AccountingOperationRestView(request)
    result = view.bulk_post()[0]

    assert result.analytical_account == u"0USER"
    assert result.general_account == u"GENERAL"
    assert result.debit == 15
    assert result.credit == 15
    assert result.balance == 25
    assert result.id == 1
    assert result.company_id == company.id
