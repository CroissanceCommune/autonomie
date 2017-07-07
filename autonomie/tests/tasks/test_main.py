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
import pytest

from autonomie.models.customer import Customer
from autonomie.models.project import Project, Phase
from autonomie.models.user import User
from autonomie.models.company import Company
from autonomie.models.task import Task


from autonomie.exception import Forbidden

TASK = dict(
    name=u"Test task",
    status="draft",
    date=datetime.date.today(),
    status_date=datetime.date.today(),
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
def task(project, user, customer, company, phase):
    task = Task(
        company,
        customer,
        project,
        phase,
        user,
    )
    for key, value in TASK.items():
        setattr(task, key, value)
    return task


class TestStatusChange:
    def _forbidden_state_change(self, config, task, from_state, to_states,
                                request):
        for st in to_states:
            task.status = from_state
            with pytest.raises(Forbidden):
                task.set_status(st, request, task.owner)

    def _allowed_state_change(self, config, task, from_state, to_states,
                              request):
        for st in to_states:
            task.status = from_state
            task.set_status(st, request, task.owner.id)
            assert task.status == st

    def test_status_change(self, config, task, request_with_config):
        config.testing_securitypolicy(userid='test', permissive=True)

        status = 'draft'
        self._forbidden_state_change(
            config,
            task,
            status,
            ("invalid"),
            request_with_config,
        )
        self._allowed_state_change(
            config,
            task, status,
            ('wait',),
            request_with_config,
        )

        status = 'wait'
        self._allowed_state_change(
            config,
            task, status,
            ("draft", 'invalid', 'valid',),
            request_with_config,
        )

        status = 'valid'
        self._forbidden_state_change(
            config,
            task, status,
            ("draft", "invalid", "wait"),
            request_with_config
        )


class TaskAvailableAction:
    pass
