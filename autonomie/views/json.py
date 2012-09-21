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

from pyramid.view import view_config

@view_config(route_name='company', renderer='json', request_method='GET',
            xhr=True, permission='edit')
@view_config(route_name='client', renderer='json', request_method='GET',
            xhr=True, permission='edit')
@view_config(route_name='project', renderer='json', request_method='GET',
            xhr=True, permission='edit')
def json_project(request):
    """
        Return a json representation of the project
    """
    return request.context.todict()
