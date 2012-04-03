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

from .base import BaseFunctionnalTest
from .base import BaseViewTest
#from webtest import TestRequest, TestResponse

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
    user.companies = [MagicMock(name=u'Test', id=100), MagicMock(name=u'Test2', id=101)]
    return user

def get_avatar2():
    user = MagicMock(name=u'test2')
    user.companies = [MagicMock(name=u'Test', id=100)]
    return user

class TestIndex(BaseViewTest):
    def test_index_view(self):
        from autonomie.views.index import index
        self.config.add_route('company', '/company/{cid}')
        self.config.add_static_view('static', 'autonomie:static')
        request = self.get_csrf_request()
        avatar = get_avatar()
        request.session['user'] = avatar
        response = index(request)
        self.assertEqual(avatar.companies, response['companies'])
        request.session['user'] = get_avatar2()
        response = index(request)
        self.assertEqual(response.status_int, 302)

class TestCompany(BaseFunctionnalTest):
    def test_company_index(self):
        from autonomie.views.company import company_index
        from autonomie.models.model import User
        avatar = self.session.query(User).first()
        self.config.add_route('company', '/company/{cid}')
        self.config.add_static_view('static', 'autonomie:static')
        request = self.get_csrf_request()
        request.matchdict['cid'] = 1
        request.session['user'] = avatar
        response = company_index(request)
        self.assertEqual(avatar.companies[0].name, response['company'].name )
        request.matchdict['cid'] = 0
        response = company_index(request)
        self.assertEqual(response.status_int, 403)

class TestSubscriber(BaseViewTest):
    def test_menu_scriber(self):
        from autonomie.views.subscribers import add_menu
        from pyramid.events import BeforeRender
        event = BeforeRender({})
        event['req'] = MagicMock(matchdict={'cid':'100'})
        add_menu(event)
        self.assertEqual(event['menu'][0]['label'], u'Clients')
        self.assertEqual(event['menu'][1]['label'], u'Devis - Factures')
