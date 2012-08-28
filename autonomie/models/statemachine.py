# -*- coding: utf-8 -*-
# * File Name : statemachine.py
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
    Handle the states of the objects
"""
from pyramid.security import has_permission
from autonomie.exception import Forbidden

class State(object):
    """
        a state object with a name, permission and a callback callbacktion
        name:the state name
        permission: the permission needed to set this state
        callback: a callback function to call on state process
        cae_state: True if this state is a CAE state
                                 (it should be set as CAEStatus on the object)
    """
    def __init__(self, name, permission=None, callback=None, cae_state=True):
        self.name = name
        self.permission = permission or "edit"
        self.callback = callback
        self.cae_state = cae_state

    def allowed(self, context, request):
        """
            return True if this state assignement is allowed
            in the current request
        """
        return has_permission(self.permission, context, request)

    def process(self, task, user_id, **kw):
        """
            process the expected actions after status change
        """
        if self.cae_state:
            task.statusPerson = user_id
            task.CAEStatus = self.name
        if self.callback:
            return self.callback(task, user_id=user_id, **kw)
        else:
            return task

class TaskState(object):
    """
        a state machine storing the transitions as:
            (state, new_state) : (permission, callback)
    """
    def __init__(self, default_state='draft', transition_dict=None):
        self.default_state = default_state
        self.transitions = dict()
        if transition_dict:
            self.load_transitions_from_dict(transition_dict)

    def load_transitions_from_dict(self, transition_dict):
        """
            allows to load a bulk of transitions from a dictionnary
            {'state
        """
        for state, new_states in transition_dict.items():
            for new_state in new_states:
                if not hasattr(new_state, '__iter__'):
                    new_state = [new_state]
                self.add_transition(state, *new_state)

    def add_transition(self, state, next_, perm=None, callback=None, cae=True):
        """
            adds a transition to the state machine
        """
        state_obj = State(next_, perm, callback, cae)
        self.transitions.setdefault(state, []).append(state_obj)

    def process(self, task, request, user_id, new_state, **kw):
        """
            process the state change
        """
        state = task.CAEStatus

        state_obj = self.get_transition(state, new_state)
        if state_obj is None:
            raise Forbidden()
        elif not state_obj.allowed(task, request):
            raise Forbidden()
        else:
            return state_obj.process(task, user_id=user_id, **kw)

    def get_transition(self, state, new_state):
        """
            Return the State transition object from state to new_state
        """
        available_states = self.transitions.get(state, [])
        for state_obj in available_states:
            if state_obj.name == new_state:
                return state_obj
        return None

    def get_next_status(self, state):
        """
            return the name of the next available status
        """
        return [st_obj.name for st_obj in self.transitions.get(state, [])]

    def get_next_states(self, state):
        """
            return the next state objects after state
        """
        return self.transitions.get(state, [])
