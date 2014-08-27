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


from autonomie.views.user import (
    user_delete,
    UserAccountView,
    UserDisable,
    PermanentUserAddView,
#    PermanentUserEditView,
)
from autonomie.tests.base import (
    BaseFunctionnalTest,
    Dummy,
)
from autonomie.models.user import User

PWD = "Tést$!Pass"
COMPANIES = ['company 1', 'company 2']

APPSTRUCT = {
    "login": u'test_user',
    "lastname": u'lastname__\xe9\xe9',
    "firstname": u'firstname__éé',
    "email": u"Test@example.com",
    'pwd': "Tést$!Pass",
    'companies':COMPANIES,
}


class Base(BaseFunctionnalTest):
    def addone(self):
        appstruct = APPSTRUCT.copy()
        self.config.add_route("user", "/users/{id:\d+}")
        request = self.get_csrf_request()
        request.context = Dummy(__name__='root')
        view = PermanentUserAddView(request)
        view.submit_success(appstruct)

    def getone(self):
        return User.query().filter(User.login==APPSTRUCT['login']).first()

class TestUserAccount(Base):
    def test_success(self):
        self.config.add_route('account', '/account')
        self.addone()
        req = self.get_csrf_request()
        req.user = self.getone()
        view = UserAccountView(req)
        view.submit_success({'pwd':u"Né^PAs$$ù"})
        self.assertEqual(req.user.auth(u"Né^PAs$$ù"), True)


class TestUserDelete(Base):
    def test_func(self):
        self.config.add_route('users', '/')
        self.addone()
        self.session.commit()
        req = self.get_csrf_request()
        u = self.getone()
        req.context = u
        user_delete(u, req)
        self.session.commit()
        self.assertEqual(None, self.getone())

class TestUserDisable(Base):
    def test_success(self):
        self.config.add_route('users', '/')
        self.addone()
        user = self.getone()
        appstruct = {'disable':True, 'companies':True}
        req = self.get_csrf_request()
        req.context = user
        view = UserDisable(req)
        view.submit_success(appstruct)
        self.assertFalse(user.enabled())
        for company in user.companies:
            self.assertEqual('N', company.active)

class TestUserAdd(Base):
    def test_success(self):
        self.addone()
        user = self.getone()
        self.assertEqual(user.email, APPSTRUCT['email'])
        self.assertTrue(user.auth(PWD))
        self.assertEqual(len(user.companies), 2)
