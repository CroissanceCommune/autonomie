# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
import pytest
import datetime


def test_paymentform_schema(
    dbsession,
    invoice,
    request_with_config,
    mode,
    bank,
    task_line,
    task_line_group,
):
    task_line_group.lines = [task_line]
    invoice.line_groups = [task_line_group]
    from autonomie.forms.tasks.invoice import PaymentSchema
    request_with_config.context = invoice
    schema = PaymentSchema().bind(request=request_with_config)

    value = {
        'remittance_amount': '79.4',
        'amount': '12.53',
        'date': '2015-08-07',
        'bank_id': str(bank.id),
        'mode': mode.label,
        'resulted': True,
    }
    expected_value = {
        'remittance_amount': '79.4',
        'amount': 7940000,
        'date': datetime.date(2015, 8, 7),
        'bank_id': str(bank.id),
        'mode': mode.label,
        'resulted': True,
    }
    schema.deserialize(value) == expected_value


def test_deferred_total_validator(
    invoice,
    request_with_config,
    mode,
    bank,
    task_line,
    task_line_group,
):
    invoice.line_groups = [task_line_group]
    task_line_group.lines = [task_line]
    from autonomie.forms.tasks.invoice import PaymentSchema
    request_with_config.context = invoice
    schema = PaymentSchema().bind(request=request_with_config)

    value = {
        'remittance_amount': '79.4',
        'amount': '17.53',
        'date': '2015-08-07',
        'bank_id': str(bank.id),
        'mode': mode.label,
        'resulted': True,
    }
    expected_value = {
        'remittance_amount': '79.4',
        'amount': 7940000,
        'date': datetime.date(2015, 8, 7),
        'bank_id': str(bank.id),
        'mode': mode.label,
        'resulted': True,
    }
    schema.deserialize(value) == expected_value

    value = {
        'remittance_amount': '79.4',
        'amount': '17.54',
        'date': '2015-08-07',
        'bank_id': str(bank.id),
        'mode': mode.label,
        'resulted': True,
    }
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
