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

"""
    Test Documents (Tasks):
        Estimations
        Invoices
        CancelInvoices
        ManualInvoices
"""

import datetime
import unittest
import pytest
from zope.interface.verify import verifyObject
from pyramid import testing

from autonomie.models.task import Task
from autonomie.models.task import Estimation
from autonomie.models.task import Invoice
from autonomie.models.task import CancelInvoice
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
        customer_id=1)
CUSTOMER = dict(id=1, name=u"customer1", code=u"CLI1", company_id=1)

ESTIMATION = dict(
                phase_id=1,
                project_id=1,
                name=u"Devis 2",
                sequence_number=2,
                CAEStatus="draft",
                course="0",
                display_units="1",
                expenses=1500,
                deposit=20,
                exclusions=u"Notes",
                paymentDisplay=u"ALL",
                payment_conditions=u"Conditions de paiement",
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
                sequence_number=2,
                CAEStatus="draft",
                course="0",
                display_units="1",
                expenses=1500,
                deposit=20,
                payment_conditions=u"Conditions de paiement",
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de la facture",
                statusComment=u"Aucun commentaire",
                _number=u"invoicenumber")
CANCELINVOICE = dict(phase_id=1,
                project_id=1,
                owner_id=2,
                statusPerson=2,
                name=u"Avoir 2",
                sequence_number=2,
                CAEStatus="draft",
                course="0",
                display_units="1",
                expenses=1500,
                payment_conditions=u"Conditions de paiement",
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

class TestTaskModels(unittest.TestCase):
    def test_interfaces(self):
        self.assertTrue(verifyObject(ITask, Task()))
        self.assertTrue(verifyObject(IValidatedTask, Estimation()))
        self.assertTrue(verifyObject(IPaidTask, Invoice()))
        self.assertTrue(verifyObject(IPaidTask, CancelInvoice()))
        self.assertTrue(verifyObject(IInvoice, Invoice()))
        self.assertTrue(verifyObject(IInvoice, CancelInvoice()))

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

class TestStatusChange:
    def _forbidden_state_change(self, config, task, from_state, to_states):
        request = testing.DummyRequest()

        for st in to_states:
            task.CAEStatus = from_state
            with pytest.raises(Forbidden):
                task.set_status(st, request, 'test')

    def _allowed_state_change(self, config, task, from_state, to_states):
        request = testing.DummyRequest()
        for st in to_states:
            task.CAEStatus = from_state
            task.set_status(st, request, 'test')
            assert task.CAEStatus == st

    def test_status_change(self, config):
        config.testing_securitypolicy(userid='test', permissive=True)
        # Estimation
        task = get_task(factory=Estimation)
        status = 'draft'
        self._forbidden_state_change(
            config,
            task, status,
            ("geninv", "aboest", "invalid"))
        self._allowed_state_change(
            config,
            task, status,
            ('wait',))

        status = 'wait'
        self._forbidden_state_change(
            config,
            task, status,
            ("geninv", ))
        self._allowed_state_change(
            config,
            task, status,
            ("draft", 'invalid', 'valid',))

        status = 'valid'
        self._forbidden_state_change(
            config,
            task, status,
            ("draft", "invalid", )
            )
        self._allowed_state_change(
            config,
            task, status,
            ("aboest", ))

        status = 'geninv'
        self._forbidden_state_change(
            config,
            task, status,
            ("draft", "invalid", "valid", "aboest")
            )

#        # Invoice
        task = get_task(factory=Invoice)
        status = 'draft'
        self._forbidden_state_change(
            config,
            task, status,
            ("aboinv", "invalid"))
        self._allowed_state_change(
            config,
            task, status,
            ('wait',))

        status = 'wait'
        self._allowed_state_change(
            config,
            task, status,
            ("draft", 'invalid', 'valid',))

        status = 'valid'
        self._forbidden_state_change(
            config,
            task, status,
            ("draft", "invalid", )
            )

        status = "paid"
        self._forbidden_state_change(
            config,
            task, status,
            ("draft", "invalid", "valid", "aboinv", )
            )

        task = get_task(factory=CancelInvoice)
        status = "draft"
        self._allowed_state_change(
            config,
                task, status, ('delete',))

        status = "valid"
        self._forbidden_state_change(
            config,
            task, status,
            ("draft", ))



