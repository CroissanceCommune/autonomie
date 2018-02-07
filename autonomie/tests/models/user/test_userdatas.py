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
from autonomie.models.user.userdatas import (
    UserDatas,
    CompanyDatas,
    CaeSituationOption,
)


def get_userdatas(option):
    result = UserDatas(
        situation_situation=option,
        coordonnees_lastname="test",
        coordonnees_firstname="test",
        coordonnees_email1="test@test.fr",
        activity_companydatas=[CompanyDatas(
            title='test entreprise',
            name='test entreprise',
        )]
    )
    result.situation_situation_id = option.id
    return result

@pytest.fixture
def situation_option(dbsession):
    option = CaeSituationOption(label="Integre", is_integration=True)
    dbsession.add(option)
    dbsession.flush()
    return option

@pytest.fixture
def userdatas(dbsession, situation_option):
    model = get_userdatas(situation_option)
    dbsession.add(model)
    dbsession.flush()
    return model


def test_get_company(dbsession, user, company):
    company = user.get_company(company.id)
    assert company.name == company.name
    with pytest.raises(KeyError):
        user.get_company(company.id + 1)


def test_gen_existing_company(dbsession, userdatas, situation_option):
    companies = userdatas.gen_companies()
    company = companies[0]
    assert company.id is None
    dbsession.add(company)
    dbsession.flush()

    userdatas2 = get_userdatas(situation_option)
    dbsession.add(userdatas2)
    dbsession.flush()
    companies = userdatas2.gen_companies()
    company2 = companies[0]
    assert company2.id == company.id


def test_age(userdatas):
    import datetime
    today = datetime.date.today()

    birthday = today.replace(year=today.year - 55)
    userdatas.coordonnees_birthday = birthday
    assert userdatas.age == 55

    birthday = today.replace(year=today.year + 1)
    userdatas.coordonnees_birthday = birthday
    assert userdatas.age == -1


def test_salary_compute(dbsession, userdatas):
    userdatas.parcours_taux_horaire = 5
    userdatas.parcours_num_hours = 35
    dbsession.merge(userdatas)
    dbsession.flush()
    assert userdatas.parcours_salary == 175
    userdatas.parcours_taux_horaire = 5
    userdatas.parcours_num_hours = None
    dbsession.merge(userdatas)
    dbsession.flush()
    assert userdatas.parcours_salary == 0


def test_add_situation_change_handler(dbsession, userdatas):
    import datetime
    new_opt = CaeSituationOption(label=u"Sortie", is_integration=True)
    dbsession.add(new_opt)
    dbsession.flush()
    assert len(userdatas.situation_history) == 1
    userdatas.situation_situation_id = new_opt.id
    dbsession.merge(userdatas)
    dbsession.flush()
    today = datetime.date.today()
    assert len(userdatas.situation_history) == 2
    assert userdatas.situation_history[-1].situation_id == new_opt.id
    assert userdatas.situation_history[-1].date == today
