# -*- coding: utf-8 -*-
# * File Name : avatar.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : sam. 04 sept. 2010 23:10:12 CEST
#
# * Project : Autonomie
#
"""
    avatar related utilities
"""
import logging
from pyramid.security import authenticated_userid

log = logging.getLogger(__name__)

def get_groups(login, request):
    """
        return the current user's groups
    """
    dbsession = request.dbsession
    user = get_user(login, request)
    if user.is_admin():
        log.debug(" + User is an admin")
        return ['group:admin']
    elif user.is_manager():
        log.debug(" + User is a manager")
        return ['group:manager']
    else:
        log.debug(" + User is a contractor")
        return ['group:entrepreneur']

def get_avatar(request, dbsession=None):
    """
        Returns the current User object
    """
    login = authenticated_userid(request)
    user = get_user(login, request, dbsession)
    return request._user

def get_user(login, request, dbsession=None):
    """
        return a user object
    """
    if not dbsession:
        dbsession = request.dbsession
    if not hasattr(request, '_user'):
        from autonomie.models.model import User
        request._user = dbsession.query(User).filter_by(login=login).first()
    return request._user
