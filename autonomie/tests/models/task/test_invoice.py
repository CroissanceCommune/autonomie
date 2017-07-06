# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime
import pytest
import colander
from colanderalchemy import SQLAlchemySchemaNode


NOW = datetime.datetime.now()


def test_payment_mode(mode):
    from autonomie.models.task.invoice import Payment
    schema = SQLAlchemySchemaNode(Payment, includes=('mode',))
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
    from autonomie.models.task.invoice import Payment
    schema = SQLAlchemySchemaNode(Payment, includes=('amount',))
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


def test_payment_remittance_amount():
    from autonomie.models.task.invoice import Payment
    schema = SQLAlchemySchemaNode(Payment, includes=('remittance_amount',))
    schema = schema.bind()

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {'remittance_amount': "test"}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_date():
    from autonomie.models.task.invoice import Payment
    schema = SQLAlchemySchemaNode(Payment, includes=('date',))
    schema = schema.bind()
    value = {'date': NOW.isoformat()}
    assert schema.deserialize(value) == {'date': NOW}
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_tva_id(tva):
    from autonomie.models.task.invoice import Payment
    schema = SQLAlchemySchemaNode(Payment, includes=('tva_id',))
    schema = schema.bind()

    value = {'tva_id': tva.id}

    value = {'tva_id': tva.id + 1}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {}
    assert schema.deserialize(value) == value


def test_payment_bank_id(bank):
    from autonomie.models.task.invoice import Payment
    schema = SQLAlchemySchemaNode(Payment, includes=('bank_id',))
    schema = schema.bind()

    value = {'bank_id': bank.id}
    assert schema.deserialize(value) == value

    value = {'bank_id': bank.id + 1}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_user_id():
    from autonomie.models.task.invoice import Payment
    schema = SQLAlchemySchemaNode(Payment, includes=('user_id',))
    schema = schema.bind()

    value = {'user_id': 5}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_task_id():
    from autonomie.models.task.invoice import Payment
    schema = SQLAlchemySchemaNode(Payment, includes=('task_id',))
    schema = schema.bind()

    value = {'task_id': 5}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment(mode, tva, bank):
    from autonomie.models.task.invoice import Payment
    schema = SQLAlchemySchemaNode(Payment)
    schema = schema.bind()

    value = {
        'mode': mode.label,
        "amount": 12.5,
        "remittance_amount": u"Remittance",
        "date": NOW.isoformat(),
        "tva_id": tva.id,
        "bank_id": bank.id,
        "user_id": 5,
        "task_id": 5,
    }

    expected_value = {
        'mode': mode.label,
        "amount": 1250000,
        "remittance_amount": u"Remittance",
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
    from autonomie.models.task.invoice import CancelInvoice
    schema = SQLAlchemySchemaNode(CancelInvoice, includes=('invoice_id',))
    schema = schema.bind()

    value = {'invoice_id': 5}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_cancelinvoice(tva, unity):
    from autonomie.models.task.invoice import CancelInvoice
    schema = SQLAlchemySchemaNode(CancelInvoice)
    schema = schema.bind()

    value = {
        "name": u"Avoir 1",
        'date': datetime.date.today().isoformat(),
        'address': u"adress",
        "description": u"description",
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


def test_invoice(tva, unity):
    from autonomie.models.task.invoice import Invoice
    schema = SQLAlchemySchemaNode(Invoice)
    schema = schema.bind()

    value = {
        "name": u"Facture 1",
        'date': datetime.date.today().isoformat(),
        'address': u"adress",
        "description": u"description",
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
