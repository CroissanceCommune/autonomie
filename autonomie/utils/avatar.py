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

from sqlalchemy.orm import undefer_group

from autonomie.models.user import User

log = logging.getLogger(__name__)


def get_groups(login, request):
    """
        return the current user's groups
    """
    user = request.user
    if user is None:
        return None
    res = []
    for group in user.groups:
        res.append('group:{0}'.format(group))

    return res


def get_avatar(request):
    """
        Returns the current User object
    """
    log.info("Get avatar")
    login = request.unauthenticated_userid
    if login is not None:
        log.info("  + Returning the user")
        query = request.dbsession.query(User).options(undefer_group('edit'))
        user = query.filter_by(login=login).first()
        return user
