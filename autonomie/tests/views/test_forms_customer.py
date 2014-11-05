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
import pytest
import colander
from mock import MagicMock, Mock
from autonomie.models.customer import (
    Customer,
    deferred_ccode_valid,
)
from autonomie.models.company import Company

def makeOne(context):
    request = MagicMock(context=context)
    return deferred_ccode_valid("nutt", {'request':request})

def test_unique_ccode(dbsession, content):
    # A IMDD exists in the database for the company with id 1
    company = Company.query().first()
    company.__name__ = 'company'
    validator = makeOne(company)
    with pytest.raises(colander.Invalid):
        validator('nutt', u'C001')
    validator('nutt', u'C002')

    company = Mock(id=2, __name__='company')
    validator = makeOne(company)
    validator('nutt', u'C001')

    # In edit mode, no error is raised for the current_customer
    customer = dbsession.query(Customer).first()
    customer.__name__ = 'customer'
    validator = makeOne(customer)
    validator('nutt', u'C001')
