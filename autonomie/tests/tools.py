# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from pyramid.compat import is_nonstr_iter
from pyramid.security import (
    Allow,
    Everyone,
)


class Dummy(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def check_acl(acl, permission, principals=()):
    """
    Test if the given acl list in the form
    ((Deny/Allow, <principals>, <permissions>),)

    Allow permission

    :param list acl: acl in the pyramid form
    :param permission: The permission to check
    :param principals: If specified the principals to check for
    """
    if not is_nonstr_iter(principals):
        principals = [principals]
    for ace in acl:
        ace_action, ace_principal, ace_permissions = ace
        if ace_principal in principals or ace_principal == Everyone:
            if not is_nonstr_iter(ace_permissions):
                ace_permissions = [ace_permissions]
            if permission in ace_permissions:
                if ace_action == Allow:
                    return True
                else:
                    return False
    return False
