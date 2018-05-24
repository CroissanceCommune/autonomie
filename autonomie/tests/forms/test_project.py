# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
import colander
import datetime


def test_add_project_schema(customer, project_type):
    from autonomie.forms.project import get_add_project_schema
    schema = get_add_project_schema()

    args = {
        "name": u"Test project",
        "project_type_id": str(project_type.id),
        "customers": [str(customer.id)]
    }
    result = schema.deserialize(args)
    assert result['name'] == u"Test project"
    assert result['project_type_id'] == project_type.id
    assert result['customers'] == [customer.id]

    for field in 'name', 'customers', "project_type_id":
        wrong = args.copy()
        wrong.pop(field)
        with pytest.raises(colander.Invalid):
            schema.deserialize(wrong)


def test_add_step2_project_schema():
    from autonomie.forms.project import get_add_step2_project_schema
    schema = get_add_step2_project_schema()

    args = {
        "description": u"Descr",
        "code": u"PROJ",
        "starting_date": "2016-02-01",
        "ending_date": "2016-02-02",
    }

    result = schema.deserialize(args)
    assert result['description'] == u"Descr"
    assert result['code'] == u"PROJ"
    assert result['starting_date'] == datetime.date(2016, 2, 1)

    args['starting_date'] = "2016-02-03"
    with pytest.raises(colander.Invalid):
        schema.deserialize(args)


def test_edit_project_schema(customer, project_type):
    from autonomie.forms.project import get_edit_project_schema
    schema = get_edit_project_schema()

    args = {
        'name': u"Other name",
        "customers": [str(customer.id)],
        "project_type_id": str(project_type.id),
    }
    result = schema.deserialize(args)

    assert result['name'] == u"Other name"
