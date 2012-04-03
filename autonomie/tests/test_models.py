# -*- coding: utf-8 -*-
# * File Name : test_models.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 26-03-2012
# * Last Modified :
#
# * Project :
#

from .base import BaseTestCase

class TestModels(BaseTestCase):
    def test_account(self):
        from autonomie.models.model import User
        a = User(login="user2_login",
                 firstname="user2_firstname",
                 lastname="user2_lastname",
                 email="user2@test.fr")
        a.set_password('pwd')
        self.assertTrue(a.auth("pwd"))
        strange = "#;\'\\\" $25; é ö ô è à ù"
        a.set_password(strange)
        self.assertFalse(a.auth("pwd"))
        self.assertTrue(a.auth(strange))

    def test_get_company(self):
        from autonomie.models.model import User
        user1 = self.session.query(User).filter_by(lastname='user1_lastname').one()
        cid = '1'
        company = user1.get_company(cid)
        self.assertEqual(company.name, 'company1')
        self.assertRaises(KeyError, user1.get_company, 3000)

    def test_get_client(self):
        from autonomie.models.model import User
        user1 = self.session.query(User).filter_by(lastname='user1_lastname').one()
        cid = '1'
        company = user1.get_company(cid)
        client = company.get_client('C001')
        self.assertEqual(client.name, 'Client1')
        self.assertRaises(KeyError, company.get_client, "BADC")

    def test_get_project(self):
        from autonomie.models.model import User
        user1 = self.session.query(User).filter_by(lastname='user1_lastname').one()
        cid = '1'
        company = user1.get_company(cid)
        project = company.get_project('1')
        self.assertEqual(project.code_client, 'C001')
        self.assertRaises(KeyError, company.get_project, "15")

        self.assertEqual(project.client.name, 'Client1')


