# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#
import pytest
from colander import Invalid
from mock import MagicMock
from autonomie.forms.user import (
    auth,
    get_password_schema,
    deferred_company_disable_default,
)
from autonomie.models.user import User


@pytest.fixture
def user(dbsession):
    user = User(login='test_forms_user',
                lastname='lastname__éé',
                firstname='firstname__éé',
               email="a@a.fr")
    user.set_password(u"Tést$!Pass")
    dbsession.add(user)
    dbsession.flush()
    return user

def test_unique_login(user):
    assert User.unique_login("test_forms_user") == False
    assert User.unique_login("Test_forms_user") == True

def test_auth(user):
    form = get_password_schema()
    appstruct = {'login':'test_forms_user', 'password':u"Tést$!Pass"}
    auth(form, appstruct)
    appstruct = {'login':'test_forms_user', 'password':u"Tést$"}
    with pytest.raises(Invalid):
        auth(form, appstruct)

def test_default_disable():
    companies = [MagicMock(employees=range(2))]
    user = MagicMock(companies=companies)
    req = MagicMock(context=user)
    assert not deferred_company_disable_default("", {'request': req})
    companies = [MagicMock(employees=[1])]
    user = MagicMock(companies=companies)
    req = MagicMock(context=user)
    assert(deferred_company_disable_default("", {'request': req}))
