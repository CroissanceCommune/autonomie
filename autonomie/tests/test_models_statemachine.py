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
from .base import BaseViewTest
from mock import MagicMock
from pyramid.security import Allow, ALL_PERMISSIONS, Authenticated, Deny
from pyramid import testing
from autonomie.models.statemachine import StateMachine
from autonomie.exception import Forbidden

class DummyStates(StateMachine):
    status_attr = "CAEStatus"
    userid_attr = "statusPerson"


class TestStateMachine(BaseViewTest):
    def get_model(self):
        return MagicMock(status='draft',
                    user_id="toto")

    def setUp(self):
        super(TestStateMachine, self).setUp()
        self.state_machine = StateMachine()
        self.state_machine.add_transition(
                'draft', 'wait', "edit", lambda model, user_id:(model, 2))

    def test_add_transition(self):
        self.state_machine.add_transition('wait', "valid")
        self.assertEqual(
                    self.state_machine.get_transition('wait', 'valid').name,
                                                            'valid')

    def test_process_failure(self):
        self.config.testing_securitypolicy(userid='test',
                                            groupids=["group:pabon"],
                                            permissive=False)
        request = testing.DummyRequest()
        model = self.get_model()
        self.assertRaises(Forbidden, self.state_machine.process, model,
                                                    request, 'test',
                                                     'wait')
        self.assertRaises(Forbidden, self.state_machine.process, model,
                                                request, 'test',
                                                   'invalid')


    def test_process_caestate(self):
        self.state_machine.add_transition(
              'draft', 'delete', 'edit', lambda model, user_id:(model, user_id),
                cae=False)
        self.config.testing_securitypolicy(userid='test',
                                         permissive=True)
        request = testing.DummyRequest()
        model = self.get_model()
        process_result = self.state_machine.process(model,
                                                    request,
                                                    5,
                                                    'delete')
        self.assertEqual(process_result, (model, 5))
        # Because delete state has a False cae attr, it doesn't affect the model
        # object
        self.assertEqual(model.status, 'draft')


class TestCustomStateMachine(BaseViewTest):
    def get_model(self):
        return MagicMock(CAEStatus='draft',
                         statusPerson="toto")

    def setUp(self):
        super(TestCustomStateMachine, self).setUp()
        self.state_machine = DummyStates()
        self.state_machine.add_transition(
                'draft', 'wait', "edit", lambda model, user_id:(model, 2))

    def test_affected_attrs(self):
        self.config.testing_securitypolicy(userid='test',
                                        permissive=True)
        request = testing.DummyRequest()
        model = self.get_model()
        process_result = self.state_machine.process(model,
                                                    request,
                                                    5,
                                                    'wait')
        self.assertEqual(model.statusPerson, 5)
        self.assertEqual(model.CAEStatus, 'wait')
