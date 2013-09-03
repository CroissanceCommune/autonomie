# -*- coding: utf-8 -*-
# * File Name : test_views_company.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 09-08-2012
# * Last Modified :
#
# * Project :
#

from autonomie.views.company import (company_index, company_view, CompanyEdit,
        CompanyAdd)
from autonomie.models.user import User
from autonomie.models.company import Company

from autonomie.tests.base import BaseFunctionnalTest

APPSTRUCT = {
    'name':u"Compané $& test",
    "goal":u"Be the best",
    "compte_cg_banque": u"compte0652589",
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
        self.assertEqual(company.compte_cg_banque, APPSTRUCT['compte_cg_banque'])
        self.assertEqual(company.contribution, APPSTRUCT['contribution'])

class TestCompanyEdit(Base):
    def test_success(self):
        self.addOne()
        company = self.getOne()
        req = self.get_csrf_request()
        req.context = company
        appstruct = APPSTRUCT.copy()
        appstruct['phone'] = "+33 0606060606"
        appstruct['compte_cg_banque'] = u"Autre compte cg"
        appstruct['contribution'] = 70
        view = CompanyEdit(req)
        view.submit_success(appstruct)
        company = self.getOne()
        self.assertEqual(company.phone, "+33 0606060606")
        self.assertEqual(company.compte_cg_banque, u"Autre compte cg")
        self.assertEqual(company.contribution, 70)
