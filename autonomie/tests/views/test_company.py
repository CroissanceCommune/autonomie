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
from autonomie.models.user import User
from autonomie.models.company import Company

from autonomie.tests.base import BaseFunctionnalTest

APPSTRUCT = {
    'name':u"Compané $& test",
    "goal":u"Be the best",
    "contribution": 80,
        }

@pytest.fixture
def company(config, get_csrf_request_with_db):
    from autonomie.views.company import CompanyAdd
    config.add_route('company', '/')
    view = CompanyAdd(get_csrf_request_with_db())
    view.submit_success(APPSTRUCT)
    return getOne()

def getOne():
    return Company.query().filter(Company.name==APPSTRUCT['name']).first()


def test_company_index(config, content, get_csrf_request_with_db):
    from autonomie.views.company import company_index
    avatar = User.query().first()
    config.add_route('company', '/company/{cid}')
    config.add_static_view('static', 'autonomie:static')
    request = get_csrf_request_with_db()
    request._user = avatar
    request.user = avatar
    request.context = avatar.companies[0]
    response = company_index(request)
    assert avatar.companies[0].name == response['company'].name

def test_add(company):
    from autonomie.views.company import CompanyAdd
    for key, val in APPSTRUCT.items():
        assert getattr(company, key) == val

def test_success(company, get_csrf_request_with_db):
    from autonomie.views.company import CompanyEdit
    req = get_csrf_request_with_db()
    req.context = company
    appstruct = APPSTRUCT.copy()
    appstruct['phone'] = "+33 0606060606"
    appstruct['contribution'] = 70
    view = CompanyEdit(req)
    view.submit_success(appstruct)
    company = getOne()
    assert company.phone == "+33 0606060606"
    assert company.contribution == 70
