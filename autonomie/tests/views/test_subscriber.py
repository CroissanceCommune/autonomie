# -*- coding: utf-8 -*-
# * File Name : test_views_subscriber.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 08-08-2012
# * Last Modified :
#
# * Project :
#


from mock import MagicMock
from autonomie.views.subscribers import get_cid
from autonomie.views.subscribers import get_companies

from autonomie.tests.base import BaseViewTest

def get_company(id):
    c = MagicMock()
    c.id = id
    return c

def get_user():
    user =  MagicMock()
    user.companies = [get_company(1)]
    user.is_contractor = lambda :True
    user.is_manager = lambda :False
    user.is_admin = lambda :False
    return user

def get_manager():
    user =  MagicMock()
    user.companies = [get_company(1)]
    user.is_contractor = lambda :False
    user.is_manager = lambda :True
    user.is_admin = lambda :False
    return user

def get_admin():
    user =  MagicMock()
    user.companies = [get_company(1)]
    user.is_contractor = lambda :False
    user.is_manager = lambda :False
    user.is_admin = lambda :True
    return user

def get_context():
    context = MagicMock()
    context.get_company_id = lambda :200
    return context


class TestSubscriber(BaseViewTest):
    def test_get_cid(self):
        request = MagicMock()
        request.user = get_user()
        request.context = get_context()
        self.assertEqual(get_cid(request), 1)
        request.user.companies.append(get_company(2))
        self.assertEqual(get_cid(request), 200)
        # ref bug :#522
        request.user = get_manager()
        self.assertEqual(get_cid(request), 200)
        request.user = get_admin()
        self.assertEqual(get_cid(request), 200)

    def test_get_companies(self):
        request = MagicMock()
        request.user = get_user()
        request.context = get_context()
        self.assertEqual(get_companies(request), request.user.companies)

