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

"""
    Tests
"""
from mock import MagicMock

def test_redirect(app):
    login_url = "http://localhost/login?nextpage=%2F"
    resp = app.get('/')
    assert resp.status_int == 302
    assert login_url in dict(resp.headerlist).values()

def test_xhr_redirect(app):
    login_url = "http://localhost/login?nextpage=%2F"
    resp = app.get('/', xhr=True)
    assert resp.status_int == 200
    assert resp.json['redirect'] == login_url


def test_check_login(app, config):
    login_url = "http://localhost/api/v1/login"
    resp = app.get(login_url, xhr=True)
    assert resp.json['status'] == 'error'
    assert resp.json['datas'].has_key('login_form')


#def get_avatar():
#    user = MagicMock(name=u'test', companies=[])
#    user.is_admin = lambda :False
#    user.is_manager = lambda :False
#    user.companies = [MagicMock(name=u'Test', id=100), MagicMock(name=u'Test2', id=101)]
#    return user
#
#
#def get_avatar2():
#    user = MagicMock(name=u'test2')
#    user.is_admin = lambda :False
#    user.is_manager = lambda :False
#    user.companies = [MagicMock(name=u'Test', id=100)]
#    return user
#
#
#def test_index_view(config, get_csrf_request):
#    from autonomie.views.index import index
#    config.add_route('company', '/company/{id}')
#    config.add_route('manage', '/manage/')
#    config.add_static_view('static', 'autonomie:static')
#    request = get_csrf_request()
#    avatar = get_avatar()
#    request._user = avatar
#    request.user = avatar
#    response = index(request)
#    assert avatar.companies == response['companies']
#    avatar = get_avatar2()
#    request._user = avatar
#    request.user = avatar
#    response = index(request)
#    assert response.status_int == 302
