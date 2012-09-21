# -*- coding: utf-8 -*-
# * File Name : test_views.py
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
# * Project :
#
"""
    Tests
"""
from mock import MagicMock
from pyramid import testing

from autonomie.tests.base import BaseFunctionnalTest
from autonomie.tests.base import BaseViewTest

class TestAuth(BaseFunctionnalTest):
    """
        Test the auth form and redirect
    """
    def test_redirect(self):
        login_url = "http://localhost/login?nextpage=%2F"
        res = self.app.get('/')
        self.assertEqual(res.status_int, 302)
        self.assertIn(login_url, dict(res.headerlist).values())

def get_avatar():
    user = MagicMock(name=u'test', companies=[])
    user.is_admin = lambda :False
    user.is_manager = lambda :False
    user.companies = [MagicMock(name=u'Test', id=100), MagicMock(name=u'Test2', id=101)]
    return user

def get_avatar2():
    user = MagicMock(name=u'test2')
    user.is_admin = lambda :False
    user.is_manager = lambda :False
    user.companies = [MagicMock(name=u'Test', id=100)]
    return user

class TestIndex(BaseViewTest):
    def test_index_view(self):
        from autonomie.views.index import index
        self.config.add_route('company', '/company/{id}')
        self.config.add_static_view('static', 'autonomie:static')
        request = self.get_csrf_request()
        avatar = get_avatar()
        request._user = avatar
        request.user = avatar
        response = index(request)
        self.assertEqual(avatar.companies, response['companies'])
        avatar = get_avatar2()
        request._user = avatar
        request.user = avatar
        response = index(request)
        self.assertEqual(response.status_int, 302)
