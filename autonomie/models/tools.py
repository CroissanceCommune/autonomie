# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from sqlalchemy import inspect


def get_excluded_colanderalchemy(title):
    """
    Return colanderalchemy for excluded field but with title set (for other sqla
    inspection based modules like py3o inspection or ods generation)
    """
    return {'exclude': True, title: title}


def set_attribute(instance, key, value, initiator=None):
    """Set the value of an attribute, firing history events.

    This function is copied from the attributes module but adds the
    "initiator" argument.

    Mike Bayer's code provided on the sqlalchemy mailling list

    """
    state = inspect(instance)
    dict_ = state.dict
    state.manager[key].impl.set(state, dict_, value, initiator)
