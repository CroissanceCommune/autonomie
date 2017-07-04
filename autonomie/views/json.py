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
    Json API views
"""


def json_model_view(request):
    """
        Return a json representation of a model
    """
    return request.context


def includeme(config):
    """
        Configure the views for this module
    """
    for route_name in "project", "company", "customer":
        config.add_view(
            json_model_view,
            route_name=route_name,
            renderer='json',
            request_method='GET',
            xhr=True,
            permission='view_%s' % route_name
        )

    config.add_view(
        json_model_view,
        route_name="job",
        renderer="json",
        request_method="GET",
        xhr=True,
        permission="view",
    )
