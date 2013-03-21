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
        :param name: The state name
        :param permission: The permission needed to set this state
        :param callback: A callback function to call on state process
        :param model_state: True if this state is a CAE state
        :param status_attr: The attribute storing the model's status
        :param userid_attr: The attribute storing the status person's id
    """
    def __init__(self, name, permission=None, callback=None, model_state=True,
            status_attr="status", userid_attr="user_id"):
        self.name = name
        self.permission = permission or "edit"
        self.callback = callback
        self.model_state = model_state
        self.status_attr = status_attr
        self.userid_attr = userid_attr

    def allowed(self, context, request):
        """
            return True if this state assignement is allowed
            in the current request
        """
        return has_permission(self.permission, context, request)

    def process(self, model, user_id, **kw):
        """
            process the expected actions after status change
        """
        if self.model_state:
            setattr(model, self.status_attr, self.name)
            setattr(model, self.userid_attr, user_id)
        if self.callback:
            return self.callback(model, user_id=user_id, **kw)
        else:
            return model

    def __repr__(self):
        return "< State %s allowed for %s (ModelState : %s)>" % (
                self.name, self.permission, self.model_state,)


class StateMachine(object):
    """
        a state machine storing the transitions as:
            (state, new_state) : (permission, callback)
    """
    status_attr = "status"
    userid_attr = "user_id"
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
        state_obj = State(next_, perm, callback, cae, self.status_attr,
                                                    self.userid_attr)
        self.transitions.setdefault(state, []).append(state_obj)

    def process(self, model, request, user_id, new_state, **kw):
        """
            process the state change
        """
        state = getattr(model, self.status_attr)

        state_obj = self.get_transition(state, new_state)
        if state_obj is None:
            raise Forbidden()
        elif not state_obj.allowed(model, request):
            raise Forbidden()
        else:
            return state_obj.process(model, user_id=user_id, **kw)

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

    def get_next_states(self, state=None):
        """
            return the next state objects after state
        """
        if state is None:
            return self.transitions.get(self.default_state, [])
        else:
            return self.transitions.get(state, [])
