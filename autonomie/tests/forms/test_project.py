# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
import colander


def test_add_edit_project_schema(customer):
    from autonomie.forms.project import get_add_edit_project_schema
    schema = get_add_edit_project_schema()

    args = {
        "name": u"Test project",
        "code": u"PROJ",
        "starting_date": "2016-02-01",
        "ending_date": "2016-02-02",
        "customers": [str(customer.id)]
    }
    result = schema.deserialize(args)
    assert result['name'] == u"Test project"

    for field in 'name', 'customers':
        wrong = args.copy()
        wrong.pop(field)
        with pytest.raises(colander.Invalid):
            schema.deserialize(wrong)

    args['starting_date'] = "2016-02-03"
    with pytest.raises(colander.Invalid):
        schema.deserialize(args)
