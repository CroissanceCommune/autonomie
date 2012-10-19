# -*- coding: utf-8 -*-
# * File Name : test_client.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-10-2012
# * Last Modified :
#
# * Project :
#
from autonomie.models.client import Client
from autonomie.views.client import ClientAdd, ClientEdit, client_view
from autonomie.tests.base import BaseFunctionnalTest

APPSTRUCT = {'name':'Company', 'contactLastName':u'Lastname',
                'contactFirstName':u'FirstName',
                    'address':'Address should be multiline'}
class Base(BaseFunctionnalTest):
    def addOne(self):
        self.config.add_route('client', '/')
        view = ClientAdd(self.get_csrf_request())
        view.submit_success(APPSTRUCT)

    def getOne(self):
        return Client.query().filter(Client.name=='Company').first()

class TestClientAdd(Base):
    def test_success(self):
        self.addOne()
        client = self.getOne()
        self.assertEqual(client.contactLastName, u'Lastname')
        self.assertEqual(client.contactFirstName, u'FirstName')
        self.assertEqual(client.address, "Address should be multiline")

class TestClientEdit(Base):
    def test_client_edit(self):
        self.addOne()
        client = self.getOne()
        req = self.get_csrf_request()
        req.context = client
        appstruct = APPSTRUCT.copy()
        appstruct['contactLastName'] = u"Changed Lastname"
        view = ClientEdit(req)
        view.submit_success(appstruct)
        client = Client.query().filter(Client.name=='Company').first()
        self.assertEqual(client.contactLastName, u'Changed Lastname')


