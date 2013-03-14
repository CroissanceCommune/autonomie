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
from autonomie.models.statemachine import TaskStates
from autonomie.exception import Forbidden

def get_task():
    return MagicMock(CAEStatus='draft',
                    statusPerson="toto")

class TestTaskState(BaseViewTest):
    def setUp(self):
        super(TestTaskState, self).setUp()
        self.state_machine = TaskStates()
        self.state_machine.add_transition(
                'draft', 'wait', "edit", lambda task, user_id:(task, 2))

    def test_add_transition(self):
        self.state_machine.add_transition('wait', "valid")
        self.assertEqual(
                    self.state_machine.get_transition('wait', 'valid').name,
                                                            'valid')

    def test_process_ok(self):
        self.config.testing_securitypolicy(userid='test',
                                        permissive=True)
        request = testing.DummyRequest()
        task = get_task()
        process_result = self.state_machine.process(task,
                                                    request,
                                                    'test',
                                                    'wait')
        self.assertEqual(process_result, (task, 2))
        self.assertEqual(task.statusPerson, 'test')
        self.assertEqual(task.CAEStatus, 'wait')

    def test_process_failure(self):
        self.config.testing_securitypolicy(userid='test',
                                            groupids=["group:pabon"],
                                            permissive=False)
        request = testing.DummyRequest()
        task = get_task()
        self.assertRaises(Forbidden, self.state_machine.process, task,
                                                    request, 'test',
                                                     'wait')
        self.assertRaises(Forbidden, self.state_machine.process, task,
                                                request, 'test',
                                                   'invalid')


    def test_process_caestate(self):
        self.state_machine.add_transition(
              'draft', 'delete', 'edit', lambda task, user_id:(task, user_id),
                cae=False)
        self.config.testing_securitypolicy(userid='test',
                                         permissive=True)
        request = testing.DummyRequest()
        task = get_task()
        process_result = self.state_machine.process(task,
                                                    request,
                                                    'test',
                                                    'delete')
        self.assertEqual(process_result, (task, 'test'))
        # Because delete state has a False cae attr, it doesn't affect the task
        # object
        self.assertEqual(task.CAEStatus, 'draft')
