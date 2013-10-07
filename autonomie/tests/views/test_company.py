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


from autonomie.views.company import (company_index, company_view, CompanyEdit,
        CompanyAdd)
from autonomie.models.user import User
from autonomie.models.company import Company

from autonomie.tests.base import BaseFunctionnalTest

APPSTRUCT = {
    'name':u"Compané $& test",
    "goal":u"Be the best",
    "contribution": 80
        }

class Base(BaseFunctionnalTest):
    def addOne(self):
        self.config.add_route('company', '/')
        view = CompanyAdd(self.get_csrf_request())
        view.submit_success(APPSTRUCT)

    def getOne(self):
        return Company.query().filter(Company.name==APPSTRUCT['name']).first()


class TestCompany(BaseFunctionnalTest):
    def test_company_index(self):
        avatar = User.get(3)
        self.config.add_route('company', '/company/{cid}')
        self.config.add_static_view('static', 'autonomie:static')
        request = self.get_csrf_request()
        request._user = avatar
        request.user = avatar
        request.context = avatar.companies[0]
        response = company_index(request)
        self.assertEqual(avatar.companies[0].name, response['company'].name )

class TestCompanyAdd(Base):
    def test_success(self):
        self.addOne()
        company = self.getOne()
        self.assertEqual(company.goal, APPSTRUCT['goal'])
        self.assertEqual(company.name, APPSTRUCT['name'])
        self.assertEqual(company.contribution, APPSTRUCT['contribution'])

class TestCompanyEdit(Base):
    def test_success(self):
        self.addOne()
        company = self.getOne()
        req = self.get_csrf_request()
        req.context = company
        appstruct = APPSTRUCT.copy()
        appstruct['phone'] = "+33 0606060606"
        appstruct['contribution'] = 70
        view = CompanyEdit(req)
        view.submit_success(appstruct)
        company = self.getOne()
        self.assertEqual(company.phone, "+33 0606060606")
        self.assertEqual(company.contribution, 70)
