# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
from autonomie.tests.tools import Dummy


def test_default_disable():
    from autonomie.forms.user.user import deferred_company_disable_default
    companies = [Dummy(employees=range(2))]
    user = Dummy(companies=companies)
    req = Dummy(context=user)
    assert not deferred_company_disable_default("", {'request': req})
    companies = [Dummy(employees=[1])]
    user = Dummy(companies=companies)
    req = Dummy(context=user)
    assert(deferred_company_disable_default("", {'request': req}))


def test_user_add_schema(pyramid_request):
    import colander
    from autonomie.forms.user.user import get_add_edit_schema

    appstruct = {
        'civilite': u'Monsieur',
        'lastname': u'Test lastname',
        'firstname': u"Firstname",
        'email': "a@a.fr",
        'add_login': "0",
    }
    schema = get_add_edit_schema()
    schema = schema.bind(request=pyramid_request)

    result = schema.deserialize(appstruct)

    assert 'email' in result
    # civilite
    with pytest.raises(colander.Invalid):
        appstruct = {
            'civilite': u"Not a valid one",
            'lastname': u'Test lastname',
            'firstname': u"Firstname",
            'email': "a@a.fr",
            'add_login': "0",
        }
        schema.deserialize(appstruct)
    # lastname
    with pytest.raises(colander.Invalid):
        appstruct = {
            'civilite': u'Monsieur',
            'firstname': u"Firstname",
            'email': "a@a.fr",
            'add_login': "0",
        }
        schema.deserialize(appstruct)
    # firstname
    with pytest.raises(colander.Invalid):
        appstruct = {
            'civilite': u'Monsieur',
            'lastname': u'Test lastname',
            'email': "a@a.fr",
            'add_login': "0",
        }
        schema.deserialize(appstruct)
    # email
    with pytest.raises(colander.Invalid):
        appstruct = {
            'civilite': u'Monsieur',
            'lastname': u'Test lastname',
            'firstname': u"Firstname",
            'add_login': "0",
        }
        schema.deserialize(appstruct)
    with pytest.raises(colander.Invalid):
        appstruct = {
            'civilite': u'Monsieur',
            'lastname': u'Test lastname',
            'firstname': u"Firstname",
            'email': "notanemail",
            'add_login': "0",
        }
        schema.deserialize(appstruct)
