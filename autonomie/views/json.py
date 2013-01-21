# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 06-09-2012
# * Last Modified :
#
# * Project :
#
"""
    Json API views
"""

def json_project(request):
    """
        Return a json representation of the project
    """
    return request.context.todict()

def includeme(config):
    """
        Configure the views for this module
    """
    for route_name in "project", "company", "client":
        config.add_view(json_project,
                        route_name=route_name,
                        renderer='json',
                        request_method='GET',
                        xhr=True,
                        permission='edit')
