# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
from sqlalchemy.orm.exc import NoResultFound

from autonomie.models.user.user import User


@pytest.fixture
def other_user(dbsession):
    user = User(
        lastname=u"Lastname2",
        firstname=u"Firstname2",
        email="login2@c.fr",
    )
    dbsession.add(user)
    dbsession.flush()
    return user


@pytest.fixture
def other_company(dbsession, other_user):
    from autonomie.models.company import Company
    company = Company(
        name=u"Company2",
        email=u"company2@c.fr",
        code_compta="0USER2",
    )
    company.employees = [other_user]
    dbsession.add(company)
    dbsession.flush()
    other_user.companies = [company]
    other_user = dbsession.merge(other_user)
    dbsession.flush()
    return company


def test_find_user(dbsession, user, other_user, login):
    assert User.find_user("login") == user
    assert User.find_user("nonexistinglogin") is None
    assert User.find_user("Lastname Firstname") == user
    assert User.find_user("Lastname2 Firstname2") == other_user
    assert User.find_user("LASTNAME2 FIRSTNAME2") == other_user


def test_find_user_complex_lastname(dbsession, other_user):
    other_user.lastname = "Part1 Part2"
    other_user = dbsession.merge(other_user)
    dbsession.flush()
    assert User.find_user("Part1 Part2 Firstname2") == other_user


def test_get_company(dbsession, user, company, other_company):
    assert user.get_company(company.id) == company
    with pytest.raises(NoResultFound):
        # Non belonging
        user.get_company(other_company.id)

    with pytest.raises(NoResultFound):
        # Non existing
        user.get_company(other_company.id + 1000)


def test_has_userdatas(dbsession, user, userdatas, other_user):
    assert user.has_userdatas() == True
    assert other_user.has_userdatas() == False


def test_sync_user_to_userdatas(dbsession, user, userdatas):
    user.lastname = 'New Lastname'
    user.firstname = 'New Firstname'
    user.email = 'newemail@mail.fr'
    dbsession.merge(user)
    dbsession.flush()
    assert userdatas.coordonnees_lastname == 'New Lastname'
    assert userdatas.coordonnees_firstname == 'New Firstname'
    assert userdatas.coordonnees_email1 == 'newemail@mail.fr'


def test_sync_userdatas_to_user(dbsession, user, userdatas):
    userdatas.coordonnees_lastname = 'New Lastname'
    userdatas.coordonnees_firstname = 'New Firstname'
    userdatas.coordonnees_email1 = 'newemail@mail.fr'
    dbsession.merge(userdatas)
    dbsession.flush()
    assert user.lastname == 'New Lastname'
    assert user.firstname == 'New Firstname'
    assert user.email == 'newemail@mail.fr'
