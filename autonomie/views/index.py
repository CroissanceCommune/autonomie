# -*- coding: utf-8 -*-
# * File Name : views.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : lun. 11 juin 2012 16:20:06 CEST
#
# * Project : autonomie
#
"""
    Index view
"""
import logging

from pyramid.view import view_config
from pyramid.url import route_path
from pyramid.httpexceptions import HTTPFound


log = logging.getLogger(__name__)

@view_config(route_name='index', renderer='index.mako')
def index(request):
    """
        Index page
    """
    avatar = request.user
    companies = avatar.companies
    if len(companies) == 1:
        company = companies[0]
        return HTTPFound(route_path('company', request, id=company.id,
                                            _query=dict(action='index')))
    else:
        for company in companies:
            company.url = request.route_path("company", id=company.id,
                                            _query=dict(action='index'))
        return dict(title=u"Bienvenue dans Autonomie",
                    companies=avatar.companies)
