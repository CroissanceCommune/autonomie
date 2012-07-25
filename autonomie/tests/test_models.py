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

import datetime
from .base import BaseTestCase

TEST1 = dict(login="user1_login", firstname="user1_firstname",
                    lastname="user1_lastname", email="user1@test.fr",
                    primary_group=1)
TEST2 = dict(login="user2_login", firstname="user2_firstname",
                    lastname="user2_lastname", email="user2@test.fr",
                    primary_group=2)
TEST3 = dict(login="user3_login", firstname="user3_firstname",
                    lastname="user3_lastname", email="user3@test.fr",
        primary_group=3)

TEST_TASK = dict(name=u"Test task",
                 CAEStatus="draft",
                 taskDate=datetime.date.today(),
                 statusDate=datetime.date.today(),
                 description=u"Test task description")

class TestUserModel(BaseTestCase):
    def test_account(self):
        from autonomie.models.user import User
        a = User(**TEST1)
        a.set_password('pwd')
        self.assertTrue(a.auth("pwd"))
        strange = "#;\'\\\" $25; é ö ô è à ù"
        a.set_password(strange)
        self.assertFalse(a.auth("pwd"))
        self.assertTrue(a.auth(strange))

    def test_get_company(self):
        from autonomie.models.user import User
        user1 = User.get(1)
        cid = 1
        company = user1.get_company(cid)
        self.assertEqual(company.name, 'company1')
        self.assertRaises(KeyError, user1.get_company, 3000)

    def test_role(self):
        from autonomie.models.user import User
        a = User(**TEST1)
        self.assertTrue(a.is_admin())
        self.assertFalse(a.is_manager())
        a = User(**TEST2)
        self.assertTrue(a.is_manager())
        self.assertFalse(a.is_admin())
        a = User(**TEST3)
        self.assertTrue(a.is_contractor())
        self.assertFalse(a.is_admin())

class TestCustomFileType(BaseTestCase):
    def test_customfiletype(self):
        from autonomie.models.types import CustomFileType
        a = CustomFileType('test_', 255)
        cstruct1 = {'uid':'test_testfile.jpg', 'filename':'testfile.jpg'}
        self.assertEqual(a.process_bind_param(cstruct1, "nutt"),
                                                'testfile.jpg')
        self.assertEqual(a.process_result_value('testfile.jpg', 'nutt'),
                                            cstruct1)

class TestCompanyModel(BaseTestCase):
    def test_get_path(self):
        from autonomie.models.company import Company
        c = Company.get(1)
        self.assertEqual(c.get_path(), "company/1")
        self.assertEqual(c.get_logo_filepath(), "company/1/logo/logo.png")
        self.assertEqual(c.get_header_filepath(), "company/1/header/header.png")

    def test_get_company_id(self):
        from autonomie.models.company import Company
        c = Company.get(1)
        self.assertEqual(c.get_company_id(), 1)

class TestTaskModels(BaseTestCase):
    def test_interfaces(self):
        from autonomie.models.task import ITask
        from autonomie.models.task import IValidatedTask
        from autonomie.models.task import IPaidTask
        from autonomie.models.task import Task
        from autonomie.models.task import Estimation
        from autonomie.models.task import Invoice
        from autonomie.models.task import CancelInvoice
        from zope.interface.verify import verifyObject
        self.assertTrue(verifyObject(ITask, Task()))
        self.assertTrue(verifyObject(IValidatedTask, Estimation()))
        self.assertTrue(verifyObject(IPaidTask, Invoice()))
        self.assertTrue(verifyObject(IPaidTask, CancelInvoice()))

    def _get_task(self):
        from autonomie.models.task import Task
        from autonomie.models.user import User
        user = User(**TEST1)
        task = Task(**TEST_TASK)
        task.statusPersonAccount = user
        task.owner = user
        return task

    def test_task(self):
        task = self._get_task()
        self.assertEqual(task.get_status_suffix(),
                u" par user1_firstname user1_lastname le {:%d/%m/%Y}".format(
                                                        datetime.date.today()))



