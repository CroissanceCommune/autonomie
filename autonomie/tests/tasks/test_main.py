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

from autonomie.models.customer import Customer
from autonomie.models.project import Project, Phase
from autonomie.models.user import User
from autonomie.models.company import Company
from autonomie.models.task import Estimation
from autonomie.models.task import Invoice
from autonomie.models.task import CancelInvoice
from autonomie.models.task.interfaces import IValidatedTask
from autonomie.models.task.interfaces import IPaidTask
from autonomie.models.task.interfaces import IInvoice


from autonomie.exception import Forbidden

TASK = dict(
    name=u"Test task",
    CAEStatus="draft",
    date=datetime.date.today(),
    statusDate=datetime.date.today(),
    description=u"Test task description"
)


@pytest.fixture
def phase(content):
    return Phase.query().first()


@pytest.fixture
def user(content):
    return User.query().first()


@pytest.fixture
def company(content):
    return Company.query().first()


@pytest.fixture
def customer(content):
    res = Customer.query().first()
    return res


@pytest.fixture
def project(content):
    return Project.query().first()


@pytest.fixture
def invoice(project, user, customer, company, phase):
    task = Invoice(
        company,
        customer,
        project,
        phase,
        user,
    )
    for key, value in TASK.items():
        setattr(task, key, value)
    return task


@pytest.fixture
def cancelinvoice(project, user, customer, company, phase):
    task = CancelInvoice(
        company,
        customer,
        project,
        phase,
        user,
    )
    for key, value in TASK.items():
        setattr(task, key, value)
    return task


@pytest.fixture
def estimation(project, user, customer, company, phase):
    est = Estimation(
        company,
        customer,
        project,
        phase,
        user,
    )
    for key, value in TASK.items():
        setattr(est, key, value)
    return est


def test_interfaces(estimation, invoice, cancelinvoice):
    assert(verifyObject(IValidatedTask, estimation))
    assert(verifyObject(IPaidTask, invoice))
    assert(verifyObject(IPaidTask, cancelinvoice))
    assert(verifyObject(IInvoice, invoice))
    assert(verifyObject(IInvoice, invoice))


def test_task_status(estimation, invoice, cancelinvoice):
    #Estimations
    task = estimation
    assert(task.is_draft())
    assert(task.is_editable())
    assert(not(task.is_valid()))
    assert(not(task.has_been_validated()))
    assert(not(task.is_waiting()))
    task.CAEStatus = "wait"
    assert(task.is_waiting())
    assert(not(task.is_valid()))
    assert(not(task.is_editable()))
    assert(task.is_editable(manage=True))
    for i in ("valid", "geninv"):
        task.CAEStatus = i
        assert(task.has_been_validated())
        assert(not(task.is_editable()))
    # Invoices
    task = invoice
    assert(task.is_draft())
    assert(task.is_editable())
    assert(not(task.is_valid()))
    assert(not(task.has_been_validated()))
    assert(not(task.is_waiting()))
    task.CAEStatus = "wait"
    assert(task.is_waiting())
    assert(not(task.is_valid()))
    assert(not(task.is_editable()))
    assert(task.is_editable(manage=True))
    for i in ("valid", ):
        task.CAEStatus = i
        assert(task.has_been_validated())
        assert(not(task.is_editable()))
    task.CAEStatus = "paid"
    assert(task.is_paid())
    # CancelInvoice
    task = cancelinvoice
    assert(task.is_draft())
    assert(task.is_editable())
    assert(not(task.is_valid()))
    assert(not(task.has_been_validated()))
    assert(not(task.is_waiting()))
    task.CAEStatus = "wait"
    assert(task.is_waiting())
    assert(not(task.is_valid()))
    assert(not(task.is_editable()))
    assert(task.is_editable(manage=True))
    task.CAEStatus = "valid"
    assert(task.is_valid())
    assert(not(task.is_editable()))


class TestStatusChange:
    def _forbidden_state_change(self, config, task, from_state, to_states):
        request = testing.DummyRequest()

        for st in to_states:
            task.CAEStatus = from_state
            with pytest.raises(Forbidden):
                task.set_status(st, request, task.owner)

    def _allowed_state_change(self, config, task, from_state, to_states):
        request = testing.DummyRequest()
        for st in to_states:
            task.CAEStatus = from_state
            task.set_status(st, request, task.owner.id)
            assert task.CAEStatus == st

    def test_status_change(self, config, estimation, invoice, cancelinvoice):
        config.testing_securitypolicy(userid='test', permissive=True)
        # Estimation
        task = estimation
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
        task = invoice
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

        task = cancelinvoice
        request = testing.DummyRequest()
        task.CAEStatus = 'draft'
        task.set_status("delete", request, 'test')

        status = "valid"
        self._forbidden_state_change(
            config,
            task, status,
            ("draft", ))
