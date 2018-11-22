# -*- coding: utf-8 -*-
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
    wrong = args.copy()
    wrong.pop('name')
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
        "civilite": "M. et Mme",
        "address": u"1 rue Victor Hugo",
        "lastname": "Lastname",
        "zip_code": "21000",
        "city": u"Paris",
    }
    result = schema.deserialize(args)
    assert result['lastname'] == u'Lastname'

    # mandatory fields
    for field in ('lastname', 'civilite'):
        wrong = args.copy()
        wrong.pop(field)
        with pytest.raises(colander.Invalid):
            schema.deserialize(wrong)
