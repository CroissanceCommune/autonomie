# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime
import colander
import pytest
from autonomie.forms.tasks.estimation import (
    get_add_edit_estimation_schema,
    get_add_edit_paymentline_schema,
)


def test_payment_line_description():
    schema = get_add_edit_paymentline_schema(includes=('description',))
    schema = schema.bind()
    value = {'description': "test\n"}
    assert schema.deserialize(value) == value
    value = {'description': "\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_line_amount():
    schema = get_add_edit_paymentline_schema(includes=('amount',))
    schema = schema.bind()

    value = {'amount': 12.5}
    assert schema.deserialize(value) == {'amount': 1250000}

    value = {'amount': 'a'}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_line_date():
    import datetime
    schema = get_add_edit_paymentline_schema(includes=('date',))
    schema = schema.bind()
    value = {'date': datetime.date.today().isoformat()}
    assert schema.deserialize(value) == {'date': datetime.date.today()}
    value = {}
    assert schema.deserialize(value) == value


def test_payment_line_task_id():
    schema = get_add_edit_paymentline_schema(includes=('task_id',))
    value = {'task_id': 5}
    assert schema.deserialize(value) == value
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_payment_line():
    schema = get_add_edit_paymentline_schema()
    schema = schema.bind()

    value = {
        'task_id': 5,
        'date': datetime.date.today().isoformat(),
        'amount': 12.5,
        'description': u"Description"
    }
    expected_value = {
        'task_id': 5,
        'date': datetime.date.today(),
        'amount': 1250000,
        'description': u"Description",
        'order': 1
    }
    assert schema.deserialize(value) == expected_value


def test_estimation_signed_status():
    schema = get_add_edit_estimation_schema(includes=('signed_status',))
    schema = schema.bind()

    value = {'signed_status': u"signed"}
    assert schema.deserialize(value) == value

    value = {'signed_status': u"error"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_estimation_deposit():
    schema = get_add_edit_estimation_schema(includes=('deposit',))
    schema = schema.bind()

    value = {'deposit': 15}
    assert schema.deserialize(value) == value

    value = {'deposit': 150}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {'deposit': -1}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_estimation_paymentDisplay():
    schema = get_add_edit_estimation_schema(includes=('paymentDisplay',))
    schema = schema.bind()

    value = {'paymentDisplay': u'SUMMARY'}
    assert schema.deserialize(value) == value

    value = {}
    assert schema.deserialize(value) == {'paymentDisplay': u'NONE'}

    value = {'paymentDisplay': u'ERROR'}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_estimation_payment_lines():
    schema = get_add_edit_estimation_schema(includes=('payment_lines',))
    schema = schema.bind()

    value = {'payment_lines': []}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {'payment_lines': [
        {
            'task_id': 5,
            'date': datetime.date.today().isoformat(),
            'amount': 12.5,
            'description': u"Description"
        }
    ]}
    expected_value = {
        'payment_lines': [
            {
                'task_id': 5,
                'date': datetime.date.today(),
                'amount': 1250000,
                'description': u"Description",
                'order': 1
            }
        ]
    }
    assert schema.deserialize(value) == expected_value


def test_estimation(
    config, unity, tva, product, request_with_config, estimation
):
    schema = get_add_edit_estimation_schema()
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )

    request_with_config.context = estimation
    schema = schema.bind(request=request_with_config)

    value = {
        "name": u"Devis 1",
        'date': datetime.date.today().isoformat(),
        'address': u"adress",
        "description": u"description",
        "paymentDisplay": u"SUMMARY",
        "payment_conditions": u"Réception de facture",
        "deposit": 5,
        "signed_status": "signed",
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
                        "product_id": product.id
                    }
                ]
            }
        ],
        'payment_lines': [
            {
                'task_id': 5,
                'date': datetime.date.today().isoformat(),
                'amount': 12.5,
                'description': u"Description",
                "order": 8
            }
        ],
    }
    expected_value = {
        "name": u"Devis 1",
        'date': datetime.date.today(),
        'address': u"adress",
        "description": u"description",
        "paymentDisplay": u"SUMMARY",
        "deposit": 5,
        "signed_status": "signed",
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
                        "product_id": product.id
                    }
                ]
            }
        ],
        'payment_lines': [
            {
                'task_id': 5,
                'date': datetime.date.today(),
                'amount': 1250000,
                'description': u"Description",
                "order": 8
            }
        ],
    }
    # Check those values are valid
    result = schema.deserialize(value)
    for key, value in expected_value.items():
        assert result[key] == value


def test_validate_estimation_base_fail(estimation, request_with_config):
    from autonomie.forms.tasks.estimation import validate_estimation
    request_with_config.context = estimation
    with pytest.raises(colander.Invalid):
        validate_estimation(estimation, request_with_config)


def test_validate_full_estimation(
    dbsession,
    estimation,
    request_with_config,
    task_line_group,
    task_line,
    payment_line
):

    from autonomie.forms.tasks.estimation import validate_estimation
    estimation.date = datetime.date.today()
    estimation.description = u"Description"
    estimation.paymentDisplay = u"SUMMARY"
    estimation.deposit = 5
    estimation.signed_status = "signed"
    task_line_group.task_id = estimation.id
    payment_line.task_id = estimation.id
    estimation.line_groups = [task_line_group]
    estimation.payment_conditions = "Test"
    estimation.payment_lines = [payment_line]
    request_with_config.context = estimation
    validate_estimation(estimation, request_with_config)
