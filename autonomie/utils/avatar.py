# -*- coding: utf-8 -*-
# * File Name : avatar.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : mar. 26 juin 2012 16:10:45 CEST
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
    user = get_user(login, dbsession)
    if user.is_admin():
        return ['group:admin']
    elif user.is_manager():
        return ['group:manager']
    else:
        return ['group:entrepreneur']

def get_avatar(request, dbsession=None):
    """
        Returns the current User object
    """
    if not dbsession:
        dbsession = request.dbsession
    login = authenticated_userid(request)
    return get_user(login, dbsession)

def get_user(login, dbsession):
    """
        return a user object
    """
    from autonomie.models.model import User
    return dbsession.query(User).filter_by(login=login).first()
