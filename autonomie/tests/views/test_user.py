# -*- coding: utf-8 -*-
# * File Name : test_user.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 23-10-2012
# * Last Modified :
#
# * Project :
#

from autonomie.views.user import (UserAccount, user_delete, UserDisable,
        UserAdd, UserEdit)
from autonomie.tests.base import BaseFunctionnalTest
from autonomie.models.user import User
from autonomie.models.company import Company

USER = dict(login=u'test_user', lastname=u'lastname__\xe9\xe9',
                 firstname=u'firstname__éé')
PWD = "Tést$!Pass"
COMPANIES = ['company 1', 'company 2']
APPSTRUCT = {'user':USER, 'password':{'pwd':PWD}, 'companies':COMPANIES}

class Base(BaseFunctionnalTest):
    def addone(self):
        self.config.add_route("user", "/users/{id:\d+}" )
        request = self.get_csrf_request()
        view = UserAdd(request)
        view.submit_success(APPSTRUCT)

    def getone(self):
        return User.query().filter(User.login==USER['login']).first()

class TestUserAccount(Base):
    def test_success(self):
        self.addone()
        req = self.get_csrf_request()
        req.user = self.getone()
        view = UserAccount(req)
        view.submit_success({'pwd':u"Né^PAs$$ù"})
        self.assertEqual(req.user.auth(u"Né^PAs$$ù"), True)

class TestUserDelete(Base):
    def test_func(self):
        self.config.add_route('users', '/')
        self.addone()
        self.session.commit()
        req = self.get_csrf_request()
        req.context = self.getone()
        user_delete(req)
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
        appstruct = {'user':APPSTRUCT, 'password':{'pwd':PWD},
                'companies':['company1', 'company2']}
        self.addone()
        user = self.getone()
        self.assertTrue(user.auth(PWD))
        self.assertEqual(len(user.companies), 2)

class TestUserEdit(Base):
    def test_success(self):
        pass
