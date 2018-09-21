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

from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from sqlalchemy.orm import (
    load_only,
    contains_eager,
    selectinload,
)

from autonomie.models.user.user import User
from autonomie.models.user.login import Login


logger = logging.getLogger(__name__)


def get_avatar(request):
    """
        Returns the current User object
    """
    logger.info("# Retrieving avatar #")
    login = request.unauthenticated_userid
    logger.info(u"  + Login : %s" % login)
    result = None
    if login is not None:
        logger.info("  + Returning the user")
        query = request.dbsession.query(User)
        query = query.join(Login)
        query = query.options(load_only("firstname", "lastname"))
        query = query.options(contains_eager(User.login).load_only('login').selectinload(Login._groups).load_only('name'))
        query = query.filter(Login.login == login)
        result = query.first()
        if result is None:
            forget(request)
            raise HTTPFound("/")
    else:
        logger.info("  + No user found")
    logger.debug(u"-> End of the avatar collection")
    return result


def get_current_company(request):
    """
    Extract the current company we're visiting

    :param obj request: the current pyramid request
    :returns: A Company instance
    """
    if hasattr(request.context, "get_company_id"):
        cid = request.context.get_company_id()
    else:
        cid = request.user.active_companies[0].id
    return cid
