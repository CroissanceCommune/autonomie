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

from mock import MagicMock
from autonomie.panels.menu import get_cid
from autonomie.panels.menu import get_companies


def get_company(id):
    c = MagicMock()
    c.id = id
    return c

def get_user():
    user =  MagicMock()
    user.companies = [get_company(1)]
    user.is_contractor = lambda :True
    user.is_manager = lambda :False
    user.is_admin = lambda :False
    return user

def get_manager():
    user =  MagicMock()
    user.companies = [get_company(1)]
    user.is_contractor = lambda :False
    user.is_manager = lambda :True
    user.is_admin = lambda :False
    return user

def get_admin():
    user =  MagicMock()
    user.companies = [get_company(1)]
    user.is_contractor = lambda :False
    user.is_manager = lambda :False
    user.is_admin = lambda :True
    return user

def get_context():
    context = MagicMock()
    context.get_company_id = lambda :200
    return context


def test_get_cid():
    request = MagicMock()
    request.user = get_user()
    request.context = get_context()
    assert get_cid(request) == 1
    request.user.companies.append(get_company(2))
    assert get_cid(request) == 200
    # ref bug :#522
    request.user = get_manager()
    assert get_cid(request, submenu=True) == 200
    request.user = get_admin()
    assert get_cid(request, submenu=True) == 200

def test_get_companies(config, pyramid_request):
    config.testing_securitypolicy(userid="test", permissive=False)
    pyramid_request.user = get_user()
    pyramid_request.context = get_context()
    assert get_companies(pyramid_request) == pyramid_request.user.companies

