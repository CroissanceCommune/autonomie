# -*- coding: utf-8 -*-
# * File Name : views.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : mer. 06 juin 2012 09:44:31 CEST
#
# * Project : autonomie
#
"""
    Index view
"""
import logging

from pyramid.security import authenticated_userid
from pyramid.view import view_config
from pyramid.url import route_path
from pyramid.httpexceptions import HTTPFound

from autonomie.models import DBSESSION
from autonomie.models.model import User

log = logging.getLogger(__name__)

@view_config(route_name='index', renderer='index.mako')
def index(request):
    """
        Index page
    """
    userid = authenticated_userid(request)
    avatar = DBSESSION().query(User).filter_by(login=userid).one()
    companies = avatar.companies
    if len(companies) == 1:
        company = companies[0]
        return HTTPFound(route_path('company', request, id=company.id))
    else:
        for company in companies:
            company.url = route_path("company", request, id=company.id)
            company.icon = request.static_url("autonomie:static/company.png")
        return dict(title=u"Bienvenue dans Autonomie",
                    companies=avatar.companies)
