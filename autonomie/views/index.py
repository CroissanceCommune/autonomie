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
    Index view
"""
import logging

from pyramid.httpexceptions import HTTPFound


log = logging.getLogger(__name__)


def index(request):
    """
        Index page
    """
    user = request.user
    companies = user.companies
    if request.has_permission('manage')
        return HTTPFound(request.route_path('manage'))
    elif len(companies) == 1:
        company = companies[0]
        return HTTPFound(request.route_path('company', id=company.id,
                                            _query=dict(action='index')))
    else:
        for company in companies:
            company.url = request.route_path(
                "company",
                id=company.id,
                _query=dict(action='index')
            )
        return dict(
            title=u"Bienvenue dans Autonomie",
            companies=user.companies
        )


def includeme(config):
    """
        Adding the index view on module inclusion
    """
    config.add_route("index", "/")
    config.add_view(
        index,
        route_name='index',
        renderer='index.mako',
        permission='view'
    )
