# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
import pytest


def test_company_customer_schema():
    from autonomie.forms.customer import get_company_customer_schema
    schema = get_company_customer_schema()

    args = {
        "name": u"Test customer",
        "civilite": "Monsieur",
        "address": u"1 rue Victor Hugo",
        "lastname": "Lastname",
        "zip_code": "21000",
        "city": u"Paris",
    }
    result = schema.deserialize(args)
    assert result['name'] == u'Test customer'

    # mandatory fields
    for field in 'name', 'zip_code', 'city', 'lastname', 'address':
        wrong = args.copy()
        wrong.pop(field)
        with pytest.raises(colander.Invalid):
            schema.deserialize(wrong)

    wrong = args.copy()
    wrong['email'] = 'wrongmail'
    with pytest.raises(colander.Invalid):
        schema.deserialize(wrong)

    wrong = args.copy()
    wrong['civilite'] = 'wrongone'
    with pytest.raises(colander.Invalid):
        schema.deserialize(wrong)


def test_individual_customer_schema():
    from autonomie.forms.customer import get_individual_customer_schema
    schema = get_individual_customer_schema()

    args = {
        "civilite": "mr&mme",
        "address": u"1 rue Victor Hugo",
        "lastname": "Lastname",
        "zip_code": "21000",
        "city": u"Paris",
    }
    result = schema.deserialize(args)
    assert result['lastname'] == u'Lastname'

    # mandatory fields
    for field in (
        'lastname', 'civilite', 'zip_code',
        'city', 'address'
    ):
        wrong = args.copy()
        wrong.pop(field)
        with pytest.raises(colander.Invalid):
            schema.deserialize(wrong)
