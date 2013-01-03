# -*- coding: utf-8 -*-
# * File Name : test_models_tasks.py
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
"""
    Test Documents (Tasks):
        Estimations
        Invoices
        CancelInvoices
        ManualInvoices
"""

import datetime
from zope.interface.verify import verifyObject
from autonomie.tests.base import BaseTestCase

from autonomie.models.task import Task
from autonomie.models.task import Estimation
from autonomie.models.task import Invoice
from autonomie.models.task import CancelInvoice
from autonomie.models.task import ManualInvoice
from autonomie.models.task.interfaces import ITask
from autonomie.models.task.interfaces import IValidatedTask
from autonomie.models.task.interfaces import IPaidTask
from autonomie.models.task.interfaces import IInvoice

from autonomie.models.user import User

from autonomie.exception import Forbidden

TASK = dict(name=u"Test task",
                 CAEStatus="draft",
                 taskDate=datetime.date.today(),
                 statusDate=datetime.date.today(),
                 description=u"Test task description")

USER = dict(id=2,
            login=u"test_user1",
            firstname=u"user1_firstname",
            lastname=u"user1_lastname")

USER2 = dict(login=u"test_user2")

PROJECT = dict(id=1, name=u'project1', code=u"PRO1", company_id=1,
        client_id=1)
CLIENT = dict(id=1, name=u"client1", code=u"CLI1", company_id=1)

ESTIMATION = dict(
                phase_id=1,
                project_id=1,
                name=u"Devis 2",
                sequenceNumber=2,
                CAEStatus="draft",
                course="0",
                displayedUnits="1",
                expenses=1500,
                deposit=20,
                exclusions=u"Notes",
                paymentDisplay=u"ALL",
                paymentConditions=u"Conditions de paiement",
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description du devis",
                manualDeliverables=1,
                statusComment=u"Aucun commentaire",
                _number=u"estnumber")
INVOICE = dict(phase_id=1,
                project_id=1,
                owner_id=2,
                statusPerson=2,
                name=u"Facture 2",
                sequenceNumber=2,
                CAEStatus="draft",
                course="0",
                displayedUnits="1",
                expenses=1500,
                deposit=20,
                paymentConditions=u"Conditions de paiement",
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de la facture",
                statusComment=u"Aucun commentaire",
                _number=u"invoicenumber")
CANCELINVOICE = dict(phase_id=1,
                project_id=1,
                owner_id=2,
                statusPerson=2,
                name=u"Avoir 2",
                sequenceNumber=2,
                CAEStatus="draft",
                course="0",
                displayedUnits="1",
                expenses=1500,
                paymentConditions=u"Conditions de paiement",
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de l'avoir",
                statusComment=u"Aucun commentaire",
                _number=u"cancelinvoicenumber")

def get_user(datas=USER):
    user = User(**datas)
    return user

def get_task(factory):
    user = get_user()
    task = factory(**TASK)
    task.statusPersonAccount = user
    task.owner = user
    return task

class TestTaskModels(BaseTestCase):
    def test_interfaces(self):
        self.assertTrue(verifyObject(ITask, Task()))
        self.assertTrue(verifyObject(IValidatedTask, Estimation()))
        self.assertTrue(verifyObject(IPaidTask, Invoice()))
        self.assertTrue(verifyObject(IPaidTask, CancelInvoice()))
        self.assertTrue(verifyObject(IInvoice, Invoice()))
        self.assertTrue(verifyObject(IInvoice, CancelInvoice()))
        self.assertTrue(verifyObject(IInvoice, ManualInvoice()))

    def test_task_status(self):
        task = get_task(factory=Task)
        #Estimations
        task = get_task(factory=Estimation)
        self.assertTrue(task.is_draft())
        self.assertTrue(task.is_editable())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.has_been_validated())
        self.assertFalse(task.is_waiting())
        task.CAEStatus = "wait"
        self.assertTrue(task.is_waiting())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.is_editable())
        self.assertTrue(task.is_editable(manage=True))
        for i in ("valid", "geninv"):
            task.CAEStatus = i
            self.assertTrue(task.has_been_validated())
            self.assertFalse(task.is_editable())
        # Invoices
        task = get_task(factory=Invoice)
        self.assertTrue(task.is_draft())
        self.assertTrue(task.is_editable())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.has_been_validated())
        self.assertFalse(task.is_waiting())
        task.CAEStatus = "wait"
        self.assertTrue(task.is_waiting())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.is_editable())
        self.assertTrue(task.is_editable(manage=True))
        for i in ("valid", ):
            task.CAEStatus = i
            self.assertTrue(task.has_been_validated())
            self.assertFalse(task.is_editable())
        task.CAEStatus = "paid"
        self.assertTrue(task.is_paid())
        # CancelInvoice
        task = get_task(factory=CancelInvoice)
        self.assertTrue(task.is_draft())
        self.assertTrue(task.is_editable())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.has_been_validated())
        self.assertFalse(task.is_waiting())
        task.CAEStatus = "wait"
        self.assertTrue(task.is_waiting())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.is_editable())
        self.assertTrue(task.is_editable(manage=True))
        task.CAEStatus = "valid"
        self.assertTrue(task.is_valid())
        self.assertFalse(task.is_editable())

    def test_status_change(self):
        # Estimation
        task = get_task(factory=Estimation)
        for st in ("geninv", "aboest", "invalid"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        self.assertEqual(task.validate_status("nutt", "wait"), "wait")
        task.CAEStatus = "wait"
        for st in ("draft", "geninv", ):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        self.assertEqual(task.validate_status("nutt", "invalid"), "invalid")
        self.assertEqual(task.validate_status("nutt", "valid"), "valid")
        task.CAEStatus = "valid"
        for st in ("draft", "invalid", ):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        for st in ("geninv", "aboest"):
            self.assertEqual(task.validate_status("nutt", st), st)
        task.CAEStatus = "geninv"
        for st in ("draft", "invalid", "valid", "aboest"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)

        # Invoice
        task = get_task(factory=Invoice)
        for st in ("aboinv", "invalid"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        self.assertEqual(task.validate_status("nutt", "wait"), "wait")
        task.CAEStatus = "wait"
        for st in ("draft", ):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        self.assertEqual(task.validate_status("nutt", "invalid"), "invalid")
        self.assertEqual(task.validate_status("nutt", "valid"), "valid")
        task.CAEStatus = "valid"
        for st in ("draft", "invalid"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        for st in ("aboinv", "paid"):
            self.assertEqual(task.validate_status("nutt", st), st)
        task.CAEStatus = "paid"
        for st in ("draft", "invalid", "valid", "aboinv", ):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)

        # CancelInvoice
        task = get_task(factory=CancelInvoice)
        # Removing Direct validation of the cancelinvoice
        task.CAEStatus = "valid"
        for st in ("draft",):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
