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
