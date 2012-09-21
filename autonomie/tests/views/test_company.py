# -*- coding: utf-8 -*-
# * File Name : test_views_company.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 09-08-2012
# * Last Modified :
#
# * Project :
#

from autonomie.views.company import CompanyViews
from autonomie.models.model import User

from autonomie.tests.base import BaseFunctionnalTest


class TestCompany(BaseFunctionnalTest):
    def test_company_index(self):
        avatar = self.session.query(User).first()
        self.config.add_route('company', '/company/{cid}')
        self.config.add_static_view('static', 'autonomie:static')
        request = self.get_csrf_request()
        request._user = avatar
        request.user = avatar
        request.context = avatar.companies[0]
        response = CompanyViews(request).company_index()
        self.assertEqual(avatar.companies[0].name, response['company'].name )
# TODO : Company is now set in the context
#        view is not handling the acls anymore
#        request.matchdict['cid'] = 0
#        response = CompanyViews(request).company_index()
#        self.assertEqual(response.status_int, 403)
