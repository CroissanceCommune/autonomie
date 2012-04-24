# -*- coding: utf-8 -*-
# * File Name : base.py
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
    Base views with commonly used utilities
"""
from functools import partial

from webhelpers import paginate
from pyramid.httpexceptions import HTTPForbidden

from autonomie.models import DBSESSION
from autonomie.utils.views import get_page_url

class BaseView(object):
    """
        Base View object
    """
    def __init__(self, request):
        self.request = request
        self.dbsession = DBSESSION()

    def get_company_id(self):
        """
            Return current company Id
        """
        return self.request.matchdict.get('cid')

    def get_avatar(self):
        """
            Return the user's avatar
        """
        return self.request.session['user']

    def get_current_company(self):
        """
            Returns the current company
        """
        #FIXME : Handle admin or not here ?
        try:
            company = self.get_avatar().get_company(self.get_company_id())
        except KeyError:
            raise HTTPForbidden()
        return company

class ListView(BaseView):
    """
        Base view object for listing elements
    """
    columns = ()
    def _get_pagination_args(self):
        """
            Returns arguments for element listing
        """
        search = self.request.params.get("search", "")
        sort = self.request.params.get('sort', 'name')
        if sort not in self.columns:
            sort = "name"

        direction = self.request.params.get("direction", 'asc')
        if direction not in ['asc', 'desc']:
            direction = 'asc'

        items_per_page = int(self.request.params.get('nb', 10))

        current_page = int(self.request.params.get("page", 1))
        return search, sort, direction, current_page, items_per_page

    def _get_pagination(self, records, current_page, items_per_page):
        """
            return a pagination object
        """
        page_url = partial(get_page_url, request=self.request)
        return paginate.Page(records,
                             current_page,
                             url=page_url,
                             items_per_page=items_per_page)
