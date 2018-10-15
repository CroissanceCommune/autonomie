# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
import pytest
import datetime
from autonomie.forms.tasks.invoice import (
    get_add_edit_invoice_schema,
    get_add_edit_cancelinvoice_schema,
    get_add_edit_payment_schema,
)


NOW = datetime.datetime.now()


def test_paymentform_schema(
    dbsession,
    invoice,
    request_with_config,
    mode,
    bank,
    task_line,
    task_line_group,
    tva,
):
    task_line_group.lines = [task_line]
    invoice.line_groups = [task_line_group]
    from autonomie.forms.tasks.invoice import PaymentSchema
    request_with_config.context = invoice
    schema = PaymentSchema().bind(request=request_with_config)

    value = {
        'bank_remittance_id': '79.4',
        'amount': '12.53',
        'date': '2015-08-07',
        'bank_id': str(bank.id),
        'mode': mode.label,
        'resulted': True,
        'tva_id': str(tva.id),
    }
    expected_value = {
        'come_from': '',
        'bank_remittance_id': '79.4',
        'amount': 1253000,
        'date': datetime.date(2015, 8, 7),
        'bank_id': bank.id,
        'mode': mode.label,
        'resulted': True,
        'tva_id': tva.id,
    }
    assert schema.deserialize(value) == expected_value


def test_deferred_total_validator(
    invoice,
    request_with_config,
    mode,
    bank,
    task_line,
    task_line_group,
    tva,
):
    invoice.line_groups = [task_line_group]
    task_line_group.lines = [task_line]
    from autonomie.forms.tasks.invoice import PaymentSchema
    request_with_config.context = invoice
    schema = PaymentSchema().bind(request=request_with_config)

    value = {
        'bank_remittance_id': '79.4',
        'amount': '20.0',
        'date': '2015-08-07',
        'bank_id': str(bank.id),
        'mode': mode.label,
        'resulted': True,
        'tva_id': str(tva.id),
    }
    expected_value = {
        'bank_remittance_id': '79.4',
        'amount': 15500000,
        'date': datetime.date(2015, 8, 7),
        'bank_id': str(bank.id),
        'mode': mode.label,
        'resulted': True,
        'tva_id': tva.id,
    }
    schema.deserialize(value) == expected_value

    value = {
        'bank_remittance_id': '79.4',
        'amount': '21',
        'date': '2015-08-07',
        'bank_id': str(bank.id),
        'mode': mode.label,
        'resulted': True,
        'tva_id': str(tva.id),
    }
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_mode(mode):
    schema = get_add_edit_payment_schema(includes=('mode',))
    schema = schema.bind()

    value = {'mode': mode.label}
    assert schema.deserialize(value) == value

    value = {'mode': "error"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_amount():
    schema = get_add_edit_payment_schema(includes=('amount',))
    schema = schema.bind()

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {'amount': 12.5}
    assert schema.deserialize(value) == {'amount': 1250000}

    value = {'amount': 'a'}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_bank_remittance_id():
    schema = get_add_edit_payment_schema(includes=('bank_remittance_id',))
    schema = schema.bind()

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {'bank_remittance_id': "test"}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_date():
    schema = get_add_edit_payment_schema(includes=('date',))
    schema = schema.bind()
    value = {'date': NOW.isoformat()}
    assert schema.deserialize(value) == {'date': NOW}
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_tva_id(tva):
    schema = get_add_edit_payment_schema(includes=('tva_id',))
    schema = schema.bind()

    value = {'tva_id': tva.id}

    value = {'tva_id': tva.id + 1}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {}
    assert schema.deserialize(value) == value


def test_payment_bank_id(bank):
    schema = get_add_edit_payment_schema(includes=('bank_id',))
    schema = schema.bind()

    value = {'bank_id': bank.id}
    assert schema.deserialize(value) == value

    value = {'bank_id': bank.id + 1}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_user_id():
    schema = get_add_edit_payment_schema(includes=('user_id',))
    schema = schema.bind()

    value = {'user_id': 5}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_task_id():
    schema = get_add_edit_payment_schema(includes=('task_id',))
    schema = schema.bind()

    value = {'task_id': 5}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment(mode, tva, bank):
    schema = get_add_edit_payment_schema()
    schema = schema.bind()

    value = {
        'mode': mode.label,
        "amount": 12.5,
        "bank_remittance_id": u"Remittance",
        "date": NOW.isoformat(),
        "tva_id": tva.id,
        "bank_id": bank.id,
        "user_id": 5,
        "task_id": 5,
    }

    expected_value = {
        'mode': mode.label,
        "amount": 1250000,
        "bank_remittance_id": u"Remittance",
        "date": NOW,
        "tva_id": tva.id,
        "bank_id": bank.id,
        "user_id": 5,
        "task_id": 5,
    }
    result = schema.deserialize(value)

    for key, value in expected_value.items():
        assert result[key] == value


def test_cancelinvoice_invoice_id():
    schema = get_add_edit_cancelinvoice_schema(includes=('invoice_id',))
    schema = schema.bind()

    value = {'invoice_id': 5}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_cancelinvoice(request_with_config, config, cancelinvoice, tva, unity):
    schema = get_add_edit_cancelinvoice_schema()
    request_with_config.context = cancelinvoice
    schema = schema.bind(request=request_with_config)

    value = {
        "name": u"Avoir 1",
        'date': datetime.date.today().isoformat(),
        'address': u"adress",
        "description": u"description",
        "payment_conditions": u"Test",
        'invoice_id': 5,
        'financial_year': 2017,
        'line_groups': [
            {
                'task_id': 5,
                'title': u"title",
                'description': u"description",
                "order": 5,
                'lines': [
                    {
                        'cost': 15,
                        'tva': 20,
                        'description': u'description',
                        'unity': u"Mètre",
                        "quantity": 5,
                        "order": 2,
                    }
                ]
            }
        ],
    }
    expected_value = {
        "name": u"Avoir 1",
        'date': datetime.date.today(),
        'address': u"adress",
        "description": u"description",
        "payment_conditions": u"Test",
        'invoice_id': 5,
        'financial_year': 2017,
        'line_groups': [
            {
                'task_id': 5,
                'title': u"title",
                'description': u"description",
                "order": 5,
                'lines': [
                    {
                        'cost': 1500000,
                        'tva': 2000,
                        'description': u'description',
                        'unity': u"Mètre",
                        "quantity": 5.0,
                        "order": 2,
                    }
                ]
            }
        ],
    }
    # Check those values are valid
    result = schema.deserialize(value)
    for key, value in expected_value.items():
        assert result[key] == value


def test_invoice(config, invoice, request_with_config, tva, unity):
    schema = get_add_edit_invoice_schema()
    request_with_config.context = invoice
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    schema = schema.bind(request=request_with_config)

    value = {
        "name": u"Facture 1",
        'date': datetime.date.today().isoformat(),
        'address': u"adress",
        "description": u"description",
        "payment_conditions": u"Test",
        'estimation_id': 5,
        'financial_year': 2017,
        'line_groups': [
            {
                'task_id': 5,
                'title': u"title",
                'description': u"description",
                "order": 5,
                'lines': [
                    {
                        'cost': 15,
                        'tva': 20,
                        'description': u'description',
                        'unity': u"Mètre",
                        "quantity": 5,
                        "order": 2,
                    }
                ]
            }
        ],
    }
    expected_value = {
        "name": u"Facture 1",
        'date': datetime.date.today(),
        'address': u"adress",
        "description": u"description",
        "payment_conditions": u"Test",
        'estimation_id': 5,
        'financial_year': 2017,
        'line_groups': [
            {
                'task_id': 5,
                'title': u"title",
                'description': u"description",
                "order": 5,
                'lines': [
                    {
                        'cost': 1500000,
                        'tva': 2000,
                        'description': u'description',
                        'unity': u"Mètre",
                        "quantity": 5.0,
                        "order": 2,
                    }
                ]
            }
        ],
    }
    # Check those values are valid
    result = schema.deserialize(value)
    for key, value in expected_value.items():
        assert result[key] == value
