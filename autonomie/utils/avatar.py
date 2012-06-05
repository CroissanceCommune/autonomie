# -*- coding: utf-8 -*-
# * File Name : avatar.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : lun. 04 juin 2012 10:36:30 CEST
#
# * Project : Autonomie
#
"""
    avatar related utilities
"""
import logging
from pyramid.security import authenticated_userid

log = logging.getLogger(__name__)

def get_build_avatar(dbsession):
    """
        preferred to func.patial
    """
    def build_avatar(login, request):
        """
            Stores the avatar object in the session
        """
        log.debug("# Getting user auth datas #")
        user = get_user(login, dbsession)
        if user.is_admin():
            return ['admin']
        elif user.is_manager():
            return ['manager']
        else:
            return ['entrepreneur']
    return build_avatar

def get_avatar(request, dbsession):
    """
        Returns the current User object
    """
    login = authenticated_userid(request)
    avatar = get_user(login, dbsession)
    if not avatar:
        raise KeyError()
    return avatar

def get_user(login, dbsession):
    """
        return a user object
    """
    from autonomie.models.model import User
    return dbsession.query(User).filter_by(login=login).first()
