# -*- coding: utf-8 -*-
# * File Name : avatar.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : jeu. 07 févr. 2013 16:39:15 CET
#
# * Project : Autonomie
#
"""
    avatar related utilities
"""
import logging
from pyramid.security import authenticated_userid

from autonomie.models.user import User

log = logging.getLogger(__name__)


def get_groups(login, request):
    """
        return the current user's groups
    """
    user = get_user(login, request)
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
    log.info("#  Get avatar  #")
    log.info(" -> the request object :")
    log.info("It's id : %s" % id(request))
    log.info(request)
    log.info(" -> the session :")
    log.info(request.session)
    log.info(" -> The db session")
    log.info(dbsession)
    login = authenticated_userid(request)
    get_user(login, request, dbsession)
    log.info("  ->> Returning the user")
    log.info(request._user)
    return request._user


def get_user(login, request, dbsession=None):
    """
        return a user object
    """
    if not dbsession:
        dbsession = request.dbsession
    if not hasattr(request, '_user'):
        log.info("  -> No _user attribute in the request")
        request._user = dbsession.query(User).filter_by(login=login).first()
    else:
        log.info("  -> Already has a _user as attribute in the request")
    return request._user
