# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 27-08-2012
# * Last Modified :
#
# * Project :
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
