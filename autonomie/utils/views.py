# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 24-04-2012
# * Last Modified :
#
# * Project :
#
"""
    View utilities
"""
from pyramid.url import current_route_url
def get_page_url(request, page):
    """
        Return a url generator for pagination
    """
    args = request.GET
    args['page'] = str(page)
    return current_route_url(request, page=page, _query=args)


