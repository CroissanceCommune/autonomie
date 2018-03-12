# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
import colander


def test_company_schema(company, pyramid_request):
    from autonomie.forms.user.company import get_company_association_schema
    schema = get_company_association_schema()
    schema = schema.bind(request=pyramid_request)

    assert schema.deserialize({'companies': [company.name]}) == \
        {'companies': [company.name]}

    with pytest.raises(colander.Invalid):
        schema.deserialize({'companies': ["Wrong company"]})
