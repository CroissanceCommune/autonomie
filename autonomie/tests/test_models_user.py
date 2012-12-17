# -*- coding: utf-8 -*-
# * File Name : test_models_user.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 27-07-2012
# * Last Modified :
#
# * Project :
#
from .base import BaseTestCase
from autonomie.models.user import User
TEST1 = dict(login="user1_login", firstname="user1_firstname",
                    lastname="user1_lastname", email="user1@test.fr",
                    primary_group=1)
TEST2 = dict(login="user2_login", firstname="user2_firstname",
                    lastname="user2_lastname", email="user2@test.fr",
                    primary_group=2)
TEST3 = dict(login="user3_login", firstname="user3_firstname",
                    lastname="user3_lastname", email="user3@test.fr",
        primary_group=3)

class TestUserModel(BaseTestCase):
    def test_account(self):
        a = User(**TEST1)
        a.set_password('pwd')
        self.assertTrue(a.auth("pwd"))
        strange = "#;\'\\\" $25; é ö ô è à ù"
        a.set_password(strange)
        self.assertFalse(a.auth("pwd"))
        self.assertTrue(a.auth(strange))

    def test_get_company(self):
        user1 = User.get(3)
        cid = 1
        company = user1.get_company(cid)
        self.assertEqual(company.name, u'Laveur de K-ro')
        self.assertRaises(KeyError, user1.get_company, 3000)

    def test_role(self):
        a = User(**TEST1)
        self.assertTrue(a.is_admin())
        self.assertFalse(a.is_manager())
        a = User(**TEST2)
        self.assertTrue(a.is_manager())
        self.assertFalse(a.is_admin())
        a = User(**TEST3)
        self.assertTrue(a.is_contractor())
        self.assertFalse(a.is_admin())

