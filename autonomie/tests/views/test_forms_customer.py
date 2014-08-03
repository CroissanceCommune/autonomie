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
from autonomie.models.customer import (
    Customer,
    deferred_ccode_valid,
)

from autonomie.tests.base import BaseTestCase

class TestCustomer(BaseTestCase):
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

        # In edit mode, no error is raised for the current_customer
        customer = self.session.query(Customer).first()
        customer.__name__ = 'customer'
        validator = self.makeOne(customer)
        self.assertNotRaises(validator, 'nutt', u'IMDD')
