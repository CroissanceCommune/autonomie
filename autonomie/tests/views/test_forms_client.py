# -*- coding: utf-8 -*-
# * File Name : test_views_forms_client.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 04-09-2012
# * Last Modified :
#
# * Project :
#
import colander
from mock import MagicMock, Mock
from autonomie.views.forms.client import deferred_ccode_valid, \
                        get_client_from_request, get_company_id_from_request
from autonomie.models.client import Client
from autonomie.tests.base import BaseTestCase

class TestClient(BaseTestCase):
    def makeOne(self, context):
        request = MagicMock(context=context)
        return deferred_ccode_valid("nutt", {'request':request})

    def test_unique_ccode(self):
        # A IMDD exists in the database for the company with id 1
        company = Mock(id=1, __name__='company')
        validator = self.makeOne(company)
        self.assertRaises(colander.Invalid, validator, 'nutt', u'IMDD')
        self.assertNotRaises(validator, 'nutt', u'C002')

        company = Mock(id=2, __name__='company')
        validator = self.makeOne(company)
        self.assertNotRaises(validator, 'nutt', u'IMDD')

        # In edit mode, no error is raised for the current_client
        client = self.session.query(Client).first()
        client.__name__ = 'client'
        validator = self.makeOne(client)
        self.assertNotRaises(validator, 'nutt', u'IMDD')

    def test_get_client_from_request(self):
        context = Mock(__name__='client')
        req = MagicMock(context=context)
        self.assertEqual(get_client_from_request(req), context)
        context = Mock(__name__='other')
        req = MagicMock(context=context)
        self.assertEqual(get_client_from_request(req), None)

    def test_get_company_id_from_request(self):
        company = Mock(id=1, __name__='company')
        client = MagicMock(__name__='client', company=company)
        req = MagicMock(context=client)
        self.assertEqual(get_company_id_from_request(req), 1)
        req = MagicMock(context=company)
        self.assertEqual(get_company_id_from_request(req), 1)
        context = Mock(__name__='other')
        req = MagicMock(context=context)
        self.assertEqual(get_company_id_from_request(req), -1)

