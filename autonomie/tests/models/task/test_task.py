# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
import colander
from colanderalchemy import SQLAlchemySchemaNode


def test_task_line_description():
    from autonomie.models.task.task import TaskLine
    schema = SQLAlchemySchemaNode(TaskLine, includes=('description',))
    schema = schema.bind()
    value = {'description': "test\n"}
    assert schema.deserialize(value) == value
    value = {'description': "\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_cost():
    from autonomie.models.task.task import TaskLine
    schema = SQLAlchemySchemaNode(TaskLine, includes=('cost',))
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
    from autonomie.models.task.task import TaskLine
    schema = SQLAlchemySchemaNode(TaskLine, includes=('quantity',))
    schema = schema.bind()
    value = {'quantity': 1}
    assert schema.deserialize(value) == value
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_unity(unity):
    from autonomie.models.task.task import TaskLine
    schema = SQLAlchemySchemaNode(TaskLine, includes=('unity',))
    schema = schema.bind()
    value = {'unity': u"Mètre"}
    assert schema.deserialize(value) == value
    value = {'unity': u"Panies"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_tva(tva):
    from autonomie.models.task.task import TaskLine
    schema = SQLAlchemySchemaNode(TaskLine, includes=('tva',))
    schema = schema.bind()
    value = {'tva': 20.00}
    assert schema.deserialize(value) == {'tva': 2000}
    value = {'tva': 21.00}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_product_id(product):
    from autonomie.models.task.task import TaskLine
    schema = SQLAlchemySchemaNode(TaskLine, includes=('product_id',))
    schema = schema.bind()
    value = {'product_id': product.id}
    assert schema.deserialize(value) == value
    value = {'product_id': product.id + 1}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    assert schema.deserialize(value) == value


def test_task_line(unity, tva, product, product_without_tva):
    from autonomie.models.task.task import TaskLine
    schema = SQLAlchemySchemaNode(TaskLine)
    schema = schema.bind()
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
    from autonomie.models.task.task import TaskLineGroup
    schema = SQLAlchemySchemaNode(TaskLineGroup, includes=('lines',))
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
    from autonomie.models.task.task import TaskLineGroup
    schema = SQLAlchemySchemaNode(TaskLineGroup, includes=('task_id',))
    value = {'task_id': 5}
    assert schema.deserialize(value) == value
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_group(unity, tva):
    from autonomie.models.task.task import TaskLineGroup
    schema = SQLAlchemySchemaNode(TaskLineGroup)
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
    from autonomie.models.task.task import DiscountLine
    schema = SQLAlchemySchemaNode(DiscountLine, includes=('description',))
    value = {'description': u"description"}
    assert schema.deserialize(value) == value
    value = {"description": u"<br /><p></p>\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line_amount():
    from autonomie.models.task.task import DiscountLine
    schema = SQLAlchemySchemaNode(DiscountLine, includes=('amount',))
    value = {'amount': 12.50}
    assert schema.deserialize(value) == {'amount': 1250000}
    value = {'amount': 'a'}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line_tva(tva):
    from autonomie.models.task.task import DiscountLine
    schema = SQLAlchemySchemaNode(DiscountLine, includes=('tva',))
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
    from autonomie.models.task.task import DiscountLine
    schema = SQLAlchemySchemaNode(DiscountLine, includes=('task_id',))
    schema = schema.bind()
    value = {'task_id': 5}
    assert schema.deserialize(value) == value
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line(tva):
    from autonomie.models.task.task import DiscountLine
    schema = SQLAlchemySchemaNode(DiscountLine)
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
    from autonomie.models.task.task import Task
    schema = SQLAlchemySchemaNode(Task, includes=('description',))
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
    from autonomie.models.task.task import Task
    schema = SQLAlchemySchemaNode(Task, includes=('address',))
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
    from autonomie.models.task.task import Task
    schema = SQLAlchemySchemaNode(Task, includes=('mentions',))
    schema = schema.bind()
    value = {'mentions': [mention.id]}
    assert schema.deserialize(value) == value
    value = {'mentions': [mention.id + 1]}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_date():
    import datetime
    from autonomie.models.task.task import Task
    schema = SQLAlchemySchemaNode(Task, includes=('date',))
    schema = schema.bind()
    value = {'date': datetime.date.today().isoformat()}
    assert schema.deserialize(value) == {'date': datetime.date.today()}
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_groups(tva, unity):
    from autonomie.models.task.task import Task
    schema = SQLAlchemySchemaNode(Task, includes=('line_groups',))
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


def test_task(tva, unity):
    import datetime
    from autonomie.models.task.task import Task
    schema = SQLAlchemySchemaNode(Task)
    schema = schema.bind()
    value = {
        "name": u"Test task",
        'date': datetime.date.today().isoformat(),
        'address': u"adress",
        "description": u"description",
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
