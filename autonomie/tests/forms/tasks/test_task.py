# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
import colander

from autonomie.models.task.task import Task
from autonomie.forms.tasks.task import (
    get_add_edit_taskline_schema,
    get_add_edit_tasklinegroup_schema,
    get_add_edit_discountline_schema,
    get_add_edit_task_schema,
)


def test_task_line_description():
    schema = get_add_edit_taskline_schema(includes=('description',))
    schema = schema.bind()
    value = {'description': "test\n"}
    assert schema.deserialize(value) == {'description': 'test'}
    value = {'description': "\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_cost():
    schema = get_add_edit_taskline_schema(includes=('cost',))
    schema = schema.bind()
    value = {'cost': 12.50}
    assert schema.deserialize(value) == {'cost': 1250000}
    value = {'cost': 'a'}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_quantity():
    schema = get_add_edit_taskline_schema(includes=('quantity',))
    schema = schema.bind()
    value = {'quantity': 1}
    assert schema.deserialize(value) == value
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_unity(unity):
    schema = get_add_edit_taskline_schema(includes=('unity',))
    schema = schema.bind()
    value = {'unity': u"Mètre"}
    assert schema.deserialize(value) == value
    value = {'unity': u"Panies"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    schema.deserialize(value)


def test_task_line_tva(tva):
    schema = get_add_edit_taskline_schema(includes=('tva',))
    schema = schema.bind()
    value = {'tva': 20.00}
    assert schema.deserialize(value) == {'tva': 2000}
    value = {'tva': 21.00}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_product_id(config, request_with_config, estimation, product):
    schema = get_add_edit_taskline_schema(includes=('product_id',))
    request_with_config.context = estimation
    schema = schema.bind(request=request_with_config)
    value = {'product_id': product.id}
    assert schema.deserialize(value) == value
    value = {'product_id': product.id + 1}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    assert schema.deserialize(value) == value


def test_task_line(config, request_with_config, estimation,
                   unity, tva, product, product_without_tva):
    schema = get_add_edit_taskline_schema()
    request_with_config.context = estimation
    schema = schema.bind(request=request_with_config)
    value = {
        'description': u'test',
        'cost': 450,
        'quantity': 1,
        'unity': u'Mètre',
        'tva': 20.00,
        'product_id': product.id
    }
    assert schema.deserialize(value) == {
        'description': u'test',
        'cost': 45000000,
        'quantity': 1.0,
        'unity': u'Mètre',
        'tva': 2000,
        'product_id': product.id,
        'order': 1
    }
    value = {
        'description': u'test',
        'cost': 450,
        'quantity': 1,
        'unity': u'Mètre',
        'tva': 20.00,
        'product_id': product_without_tva.id
    }
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_group_lines(tva, unity):
    schema = get_add_edit_tasklinegroup_schema(includes=('lines',))
    schema = schema.bind()
    value = {'lines': []}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {'lines': [
        {
            'cost': 15,
            'tva': 20,
            'description': u'description',
            'unity': u"Mètre",
            "quantity": 5,
        }
    ]}
    assert schema.deserialize(value) == {'lines': [
        {
            'cost': 1500000,
            'tva': 2000,
            'description': u'description',
            'unity': u"Mètre",
            "quantity": 5.0,
            'order': 1
        }
    ]}


def test_task_line_group_task_id():
    schema = get_add_edit_tasklinegroup_schema(includes=('task_id',))
    value = {'task_id': 5}
    assert schema.deserialize(value) == value
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_group(unity, tva):
    schema = get_add_edit_tasklinegroup_schema()
    schema = schema.bind()
    value = {
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
    expected_value = {
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
    assert schema.deserialize(value) == expected_value


def test_discount_line_description():
    schema = get_add_edit_discountline_schema(includes=('description',))
    value = {'description': u"description"}
    assert schema.deserialize(value) == value
    value = {"description": u"<br /><p></p>\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line_amount():
    schema = get_add_edit_discountline_schema(includes=('amount',))
    schema = schema.bind()
    value = {'amount': 12.50}
    assert schema.deserialize(value) == {'amount': 1250000}
    value = {'amount': 'a'}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line_tva(tva):
    schema = get_add_edit_discountline_schema(includes=('tva',))
    schema = schema.bind()
    value = {'tva': 20.00}
    assert schema.deserialize(value) == {'tva': 2000}
    value = {'tva': 21.00}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line_task_id():
    schema = get_add_edit_discountline_schema(includes=('task_id',))
    schema = schema.bind()
    value = {'task_id': 5}
    assert schema.deserialize(value) == value
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line(tva):
    schema = get_add_edit_discountline_schema()
    schema = schema.bind()
    value = {
        'task_id': 5,
        'description': u"description",
        "amount": 5,
        "tva": 20.0
    }
    assert schema.deserialize(value) == {
        'task_id': 5,
        'description': u"description",
        "amount": 500000,
        "tva": 2000
    }


def test_task_description():
    schema = get_add_edit_task_schema(Task, includes=('description',))
    schema = schema.bind()
    value = {'description': u"description"}
    assert schema.deserialize(value) == value
    value = {"description": u"<br /><p></p>\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_address():
    schema = get_add_edit_task_schema(Task, includes=('address',))
    schema = schema.bind()
    value = {'address': u"address"}
    assert schema.deserialize(value) == value
    value = {"address": u"<br /><p></p>\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_mentions(mention):
    schema = get_add_edit_task_schema(Task, includes=('mentions',))
    schema = schema.bind()
    value = {'mentions': [mention.id]}
    assert schema.deserialize(value) == value
    value = {'mentions': [mention.id + 1]}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_date():
    import datetime
    schema = get_add_edit_task_schema(Task, includes=('date',))
    schema = schema.bind()
    value = {'date': datetime.date.today().isoformat()}
    assert schema.deserialize(value) == {'date': datetime.date.today()}
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_groups(tva, unity):
    schema = get_add_edit_task_schema(Task, includes=('line_groups',))
    schema = schema.bind()
    value = {'line_groups': []}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {'line_groups': [
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
    ]}
    expected_value = {'line_groups': [
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
    ]}
    assert schema.deserialize(value) == expected_value


def test_task_payment_conditions():
    schema = get_add_edit_task_schema(Task, includes=('payment_conditions',))
    schema = schema.bind()

    value = {'payment_conditions': u"À réception de facture"}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_isadmin():
    schema = get_add_edit_task_schema(Task, isadmin=False)
    assert 'status' not in schema
    schema = get_add_edit_task_schema(Task, isadmin=True)
    assert 'status' in schema


def test_task(tva, unity):
    import datetime
    schema = get_add_edit_task_schema(Task)
    schema = schema.bind()
    value = {
        "name": u"Test task",
        'date': datetime.date.today().isoformat(),
        'address': u"adress",
        "description": u"description",
        'payment_conditions': u"Test",
        "status_comment": "Test comment",
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
        "name": u"Test task",
        'date': datetime.date.today(),
        'address': u"adress",
        "description": u"description",
        'payment_conditions': u"Test",
        "status_comment": "Test comment",
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


def test_not_task_id_ref_bug_822():
    from autonomie.models.task import Estimation
    schema = get_add_edit_task_schema(Estimation)
    assert "id" not in schema
    schema = get_add_edit_task_schema(Estimation, includes=('id',))
    assert "id" not in schema
