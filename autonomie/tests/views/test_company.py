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
from autonomie.tests.tools import DummyForm
from autonomie.models.company import Company

DATAS = {
    'name': u"Compané $& test",
    "goal": u"Be the best",
    "contribution": "80",
    "submit": "submit",
}


def test_company_index(config, content, get_csrf_request_with_db, user,
                       company):
    from autonomie.views.company import company_index
    config.add_route('company', '/company/{cid}')
    config.add_static_view('static', 'autonomie:static')
    request = get_csrf_request_with_db()
    request._user = user
    request.user = user
    request.context = company
    response = company_index(request)
    assert user.companies[0].name == response['company'].name


class TestCompanyAdd:

    def test_before(self, get_csrf_request_with_db):
        pyramid_request = get_csrf_request_with_db()
        pyramid_request.params['user_id'] = 1
        pyramid_request.referrer = "/test"
        from autonomie.views.company import CompanyAdd

        view = CompanyAdd(pyramid_request)
        form = DummyForm()
        view.before(form)
        assert form.appstruct['user_id'] == 1
        assert form.appstruct['come_from'] == "/test"

    def test_add(self, config, get_csrf_request_with_db):
        from autonomie.views.company import CompanyAdd

        config.add_route('company', 'company')

        post = DATAS.copy()
        req = get_csrf_request_with_db(post=post)
        view = CompanyAdd(req)
        view.__call__()

        company = Company.query().filter_by(name=u"Compané $& test").first()
        assert company is not None
        assert company.goal == u"Be the best"
        assert company.contribution == 80

    def test_come_from(self, config, get_csrf_request_with_db, user):
        from autonomie.views.company import CompanyAdd

        post = DATAS.copy()
        post['come_from'] = "/test"
        req = get_csrf_request_with_db(post=post)
        req.referrer = "/test"

        view = CompanyAdd(req)
        result = view.__call__()

        assert result.location == "/test"

        company = Company.query().filter_by(name=u"Compané $& test").first()
        assert company is not None
        assert company.goal == u"Be the best"
        assert company.contribution == 80

    def test_user_id(self, config, get_csrf_request_with_db, user):
        from autonomie.views.company import CompanyAdd

        post = DATAS.copy()
        post['user_id'] = str(user.id)
        req = get_csrf_request_with_db(post=post)
        req.referrer = "/test"

        view = CompanyAdd(req)
        view.__call__()

        company = Company.query().filter_by(name=u"Compané $& test").first()
        assert company is not None
        assert user in company.employees


class TestCompanyEdit:
    def test_edit(self, config, company, get_csrf_request_with_db):
        config.add_route('company', 'company')
        from autonomie.views.company import CompanyEdit
        appstruct = DATAS.copy()
        appstruct['phone'] = "+33 0606060606"
        appstruct['contribution'] = "70"
        req = get_csrf_request_with_db(post=appstruct)
        req.context = company

        view = CompanyEdit(req)
        view.__call__()

        assert company.phone == "+33 0606060606"
        assert company.contribution == 70
