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

from autonomie.models.client import Client
from autonomie.views.client import ClientAdd, ClientEdit, client_view
from autonomie.tests.base import BaseFunctionnalTest

APPSTRUCT = {'name':'Company', 'contactLastName':u'Lastname',
             'contactFirstName':u'FirstName',
             'address':'Address should be multiline',
             'compte_cg':"Compte CG1515",
             'compte_tiers':"Compte Tiers"}


class Base(BaseFunctionnalTest):
    def addOne(self):
        self.config.add_route('client', '/')
        view = ClientAdd(self.get_csrf_request())
        view.submit_success(APPSTRUCT)

    def getOne(self):
        try:
            return Client.query().filter(Client.name=='Company').one()
        except:
            return None

class TestClientAdd(Base):
    def test_success(self):
        self.addOne()
        client = self.getOne()
        for attr, value in APPSTRUCT.items():
            self.assertEqual(getattr(client, attr), value)


class TestClientEdit(Base):
    def test_client_edit(self):
        self.addOne()
        client = self.getOne()
        req = self.get_csrf_request()
        req.context = client
        appstruct = APPSTRUCT.copy()
        appstruct['contactLastName'] = u"Changed Lastname"
        appstruct['compte_cg'] = "1"
        appstruct['compte_tiers'] = "2"
        view = ClientEdit(req)
        view.submit_success(appstruct)
        client = self.getOne()
        self.assertEqual(client.contactLastName, u'Changed Lastname')
        self.assertEqual(client.compte_cg, "1")
        self.assertEqual(client.compte_tiers, "2")
