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
from autonomie.tests.base import (
    Dummy,
)
from autonomie.models.user import User

PWD = u"Tést$!Pass"
COMPANIES = ['company 1', 'company 2']

APPSTRUCT = {
    "login": u'test_user',
    "lastname": u'lastname__\xe9\xe9',
    "firstname": u'firstname__éé',
    "email": u"Test@example.com",
    'pwd': u"Tést$!Pass",
    'companies':COMPANIES,
}


@pytest.fixture
def user(config, get_csrf_request_with_db):
    from autonomie.views.user import PermanentUserAddView
    appstruct = APPSTRUCT.copy()
    config.add_route("user", "/users/{id:\d+}")
    request = get_csrf_request_with_db()
    request.context = Dummy(__name__='root')
    view = PermanentUserAddView(request)
    view.submit_success(appstruct)
    user = getone()
    return user

def getone():
    return User.query().filter(User.login==APPSTRUCT['login']).first()


def test_myaccount_success(config, get_csrf_request_with_db, user):
    from autonomie.views.user import UserAccountView
    config.add_route('account', '/account')
    req = get_csrf_request_with_db()
    req.context = user
    view = UserAccountView(req)
    view.submit_success({'pwd':u"Né^PAs$$ù"})
    assert user.auth(u"Né^PAs$$ù")


def test_delete(config, dbsession, get_csrf_request_with_db, user):
    from autonomie.views.user import user_delete
    config.add_route('users', '/')
    req = get_csrf_request_with_db()
    req.context = user
    user_delete(user, req)
    dbsession.flush()
    assert getone() is None

def test_disable(config, get_csrf_request_with_db, user):
    from autonomie.views.user import UserDisable
    config.add_route('users', '/')
    appstruct = {'disable':True, 'companies':True}
    req = get_csrf_request_with_db()
    req.context = user
    view = UserDisable(req)
    view.submit_success(appstruct)
    assert not user.enabled()
    for company in user.companies:
        assert 'N' == company.active

def test_success(user):
    assert user.email == APPSTRUCT['email']
    assert user.auth(PWD)
    assert len(user.companies) == 2
