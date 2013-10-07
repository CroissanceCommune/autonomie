# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
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
