# -*- coding: utf-8 -*-
# * File Name : company.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 27-03-2012
# * Last Modified :
#
# * Project : autonomie
#
"""
    Views for the company handling
    Entry point for the main users
"""
import logging
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden

log = logging.getLogger(__name__)
@view_config(route_name='company', renderer='company_index.mako')
def company_index(request):
    """
        index page for the company shows latest news :
            - last validated estimation/invoice
            - To be relaunched bill
    """
    cid = request.matchdict.get('cid')
    avatar = request.session['user']
    try:
        company = avatar.get_company(cid)
        ret_val = dict(title=u"Autonomie", company=company)
    except KeyError:
        ret_val = HTTPForbidden()
    return ret_val
