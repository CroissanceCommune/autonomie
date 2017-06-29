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
    Handle the states of the objects
"""
from autonomie.exception import Forbidden


class State(object):
    """
        a state object with a name, permission and a callback callbacktion
        :param name: The state name
        :param permission: The permission needed to set this state
        :param callback: A callback function to call on state process
        :param status_attr: The attribute storing the model's status
        :param userid_attr: The attribute storing the status person's id
    """
    def __init__(
        self,
        name,
        permission,
        callback=None,
        status_attr=None,
        userid_attr=None
    ):
        self.name = name
        if not hasattr(permission, "__iter__"):
            permission = [permission]
        self.permissions = permission
        self.callback = callback
        self.status_attr = status_attr
        self.userid_attr = userid_attr

    def allowed(self, context, request):
        """
        return True if this state assignement on context is allowed
        in the current request

        :param obj context: An object with acl
        :param obj request: The Pyramid request object
        :returns: True/False
        :rtype: bool
        """
        res = False
        for permission in self.permissions:
            if request.has_permission(permission, context):
                res = True
                break

        return res

    def process(self, request, model, user_id, **kw):
        """
            process the expected actions after status change
        """
        if self.status_attr is not None:
            setattr(model, self.status_attr, self.name)
        if self.userid_attr:
            setattr(model, self.userid_attr, user_id)
        if self.callback:
            return self.callback(request, model, user_id=user_id, **kw)
        else:
            return model

    def __repr__(self):
        return (
            "< State %s allowed for %s (status_attr : %s, "
            "userid_attr : %s )>" % (
                self.name, self.permissions, self.status_attr, self.userid_attr
            )
        )


class StateMachine(object):
    """
        a state machine storing the transitions as:
            (state, new_state) : (permission, callback)
    """
    status_attr = "status"
    userid_attr = "user_id"

    def __init__(self, default_state='draft'):
        self.default_state = default_state
        self.transitions = dict()

    def add_transition(self, src_state_name, next_state):
        """
        Add a transition object

        :param str src_state_name: The name of the source state
        :param obj next_state: The next state object
        """
        self.transitions.setdefault(src_state_name, []).append(next_state)

    def process(self, model, request, user_id, new_state, **kw):
        """
        process the state change

        :param obj model: The model object
        :param obj request: The pyramid request object
        :param int user_id: The id of the user
        :param str new_state: The new state
        :param dict kw: params forwarded to the state's process function
        """
        state = getattr(model, self.status_attr)

        print("Looking for a new object : %s -> %s" % (state, new_state))
        state_obj = self.get_transition(state, new_state)
        if state_obj is None:
            raise Forbidden(
                u"No state object could be retrieved for %s" % new_state
            )
        elif not state_obj.allowed(model, request):
            raise Forbidden(
                u"Current user is not allowed to set the %s state" % new_state
            )
        else:
            return state_obj.process(request, model, user_id=user_id, **kw)

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

    def get_state(self, current_state, statename):
        """
        Return the state object with the given name that is in the next_actions
        of the current object

        :param str current_state: The actual state of the object
        :param str statename: The name of the state ('draft', 'wait', ...)
        :returns: The Associated state or None
        :rtype: State obj
        """
        next_states = self.get_next_states(current_state)
        result = None
        for state in next_states:
            if state.name == statename:
                result = state
                break
        return result
