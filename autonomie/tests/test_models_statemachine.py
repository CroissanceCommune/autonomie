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
    Test the state machine
"""
from mock import MagicMock
from pyramid import testing
from autonomie.models.statemachine import StateMachine, State
from autonomie.exception import Forbidden

import pytest


@pytest.fixture(scope='function')
def state_machine():
    wait = State(
        'wait',
        "edit",
        status_attr='status',
        callback=lambda req, model, user_id: (model, 2),
    )
    invalid = State(
        'invalid',
        ('edit', 'manage'),
        status_attr='status',
        userid_attr='statusPerson',
        callback=lambda req, model, user_id: (model, 2),
    )
    state_machine = StateMachine()
    state_machine.add_transition('draft', wait)
    state_machine.add_transition('wait', invalid)
    return state_machine


@pytest.fixture
def state():
    return State("invalid", permission=("edit", "manage"))


@pytest.fixture(scope='function')
def model():
    return MagicMock(
        status='draft',
        statusPerson="toto"
    )


class DummyStates(StateMachine):
    status_attr = "status"
    userid_attr = "statusPerson"


def test_add_transition(state_machine, state):
    state_machine.add_transition('wait', state)
    assert state_machine.get_transition('wait', 'invalid').name == 'invalid'


def test_process_failure(config, state_machine, model):
    config.testing_securitypolicy(
        userid='test',
        groupids=["group:pabon"],
        permissive=False
    )
    request = testing.DummyRequest()

    with pytest.raises(Forbidden):
        state_machine.process(model, request, 'test', 'wait')

    with pytest.raises(Forbidden):
        state_machine.process(model, request, 'test', 'invalid')


def test_allowed(config, state, model):
    config.testing_securitypolicy(userid="test", permissive=True,)
    request = testing.DummyRequest()
    assert state.allowed(model, request)


def test_not_allowed(config, state, model):
    config.testing_securitypolicy(userid="test", permissive=False,)
    request = testing.DummyRequest()
    assert not state.allowed(model, request,)


def test_process_caestate(config, state_machine, model):
    delete = State(
        'delete',
        'edit',
        callback=lambda r, mode, user_id: (model, user_id),
    )
    state_machine.add_transition('draft', delete)
    config.testing_securitypolicy(userid='test', permissive=True)
    request = testing.DummyRequest()
    process_result = state_machine.process(
        model,
        request,
        5,
        'delete',
    )
    assert process_result == (model, 5)
    # Because delete state has a False cae attr, it doesn't affect the model
    # object
    assert model.status == 'draft'


def test_affected_attrs(config, state_machine, model):
    config.testing_securitypolicy(
        userid='test',
        permissive=True,
    )
    request = testing.DummyRequest()
    state_machine.process(
        model,
        request,
        5,
        'wait',
    )
    # Should not have changed
    assert model.statusPerson == 'toto'
    # Should have changed
    assert model.status == 'wait'
