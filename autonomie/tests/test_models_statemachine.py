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
from pyramid.security import Allow
from pyramid import testing
from autonomie.models.statemachine import TaskState
from autonomie.exception import Forbidden

def get_task():
    return MagicMock(CAEStatus='draft',
                    __acl__=[(Allow, "group:manager", ("edit",))],
                    statusPerson="toto")

class TestTaskState(BaseViewTest):
    def setUp(self):
        super(TestTaskState, self).setUp()
        self.state_machine = TaskState()
        self.state_machine.add_transition(
                'draft', 'wait', "edit", lambda task, user_id:(task, 2))

    def test_add_transition(self):
        self.state_machine.add_transition('wait', "valid")
        self.assertEqual(
                    self.state_machine.get_transition('wait', 'valid').name,
                                                            'valid')

    def test_process(self):
        self.config.testing_securitypolicy(userid='test',
                                            groupids="group:manager")
        request = testing.DummyRequest()
        task = get_task()
        process_result = self.state_machine.process(task,
                                                    request,
                                                    'test',
                                                    'wait')
        self.assertEqual(process_result, (task, 2))
        self.assertEqual(task.statusPerson, 'test')
        self.assertEqual(task.CAEStatus, 'wait')
        self.config.testing_securitypolicy(userid='test',
                                            groupids="group:pamanager")
        request = testing.DummyRequest()
        self.assertRaises(Forbidden, self.state_machine.process, task,
                                                    request, 'test',
                                                     'wait')
        self.assertRaises(Forbidden, self.state_machine.process, task,
                                                request, 'test',
                                                   'invalid')
