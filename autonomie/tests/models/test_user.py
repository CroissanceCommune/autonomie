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
from autonomie.models.user import (
    User,
    UserDatas,
    CompanyDatas,
    CaeSituationOption,
)
TEST1 = dict(
    login="user1_login",
    firstname="user1_firstname",
    lastname="user1_lastname",
    email="user1@test.fr",
)
TEST2 = dict(
    login="user2_login",
    firstname="user2_firstname",
    lastname="user2_lastname",
    email="user2@test.fr",
)
TEST3 = dict(
    login="user3_login",
    firstname="user3_firstname",
    lastname="user3_lastname",
    email="user3@test.fr",
)

def get_userdatas():
    option = CaeSituationOption(label="Integre", is_integration=True)
    return UserDatas(
        situation_situation=option,
        coordonnees_lastname="test",
        coordonnees_firstname="test",
        coordonnees_email1="test@test.fr",
        activity_companydatas=[CompanyDatas(
            title='test entreprise',
            name='test entreprise',
        )]
    )

@pytest.fixture
def userdatas(dbsession):
    model = get_userdatas()
    dbsession.add(model)
    dbsession.flush()
    return model


def test_account(dbsession):
    a = User(**TEST1)
    a.set_password('pwd')
    assert a.auth("pwd")
    strange = "#;\'\\\" $25; é ö ô è à ù"
    a.set_password(strange)
    assert not a.auth("pwd")
    assert a.auth(strange)

def test_get_company(dbsession, user, company):
    company = user.get_company(company.id)
    assert company.name == company.name
    with pytest.raises(KeyError):
        user.get_company(company.id + 1)

def test_gen_account_with_duplicate_login(dbsession, userdatas):
    # First add a user account
    u, l, p = userdatas.gen_user_account()
    dbsession.add(u)
    dbsession.flush()
    assert l == 'test@test.fr'
    userdatas2 = get_userdatas()
    dbsession.add(userdatas2)
    dbsession.flush()
    u, l, p = userdatas2.gen_user_account()
    assert l == '0_test@test.fr'

def test_gen_existing_company(dbsession, userdatas):
    companies = userdatas.gen_companies()
    company = companies[0]
    assert company.id == None
    dbsession.add(company)
    dbsession.flush()

    userdatas2 = get_userdatas()
    dbsession.add(userdatas2)
    dbsession.flush()
    companies = userdatas2.gen_companies()
    company2 = companies[0]
    assert company2.id == company.id
