# -*- coding: utf-8 -*-
# * File Name : test_forms_user.py
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
from colander import Invalid
from mock import MagicMock
from autonomie.views.forms.user import (is_useredit_form, unique_login, auth,
        PasswordChangeSchema, deferred_company_disable_default)
from autonomie.models.user import User

from colander import SchemaNode

from autonomie.tests.base import BaseTestCase

def adduser(dbsession):
    user = User(login='test_forms_user',
                lastname='lastname__éé',
                firstname='firstname__éé')
    user.set_password(u"Tést$!Pass")
    dbsession.add(user)
    dbsession.flush()
    return user

class TestFormsUser(BaseTestCase):
    def test_isuseredit_form(self):
        req = MagicMock(context=MagicMock(__name__='user'))
        self.assertTrue(is_useredit_form(req))
        req = MagicMock(context=MagicMock(__name__='other'))
        self.assertFalse(is_useredit_form(req))

    def test_unique_login(self):
        adduser(self.session)
        self.assertRaises(Invalid, unique_login, "nutt", "test_forms_user")
        unique_login("nutt", "other unused login")

    def test_auth(self):
        adduser(self.session)
        form = PasswordChangeSchema()
        appstruct = {'login':'test_forms_user', 'password':u"Tést$!Pass"}
        auth(form, appstruct)
        appstruct = {'login':'test_forms_user', 'password':u"Tést$"}
        self.assertRaises(Invalid, auth, form, appstruct)

    def default_disable(self):
        companies = [MagicMock(employees=range(2))]
        user = MagicMock(companies=companies)
        req = MagicMock(user=user)
        self.assertFalse(deferred_default_company_disable("", {'request', req}))
        companies = [MagicMock(employees=[1])]
        user = MagicMock(companies=companies)
        req = MagickMock(user=user)
        self.assertTrue(deferred_default_company_disable("", {'request', req}))
