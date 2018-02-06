# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
from autonomie.models.user.login import Login

def test_auth(dbsession):
    """
    Test user authentication
    """
    a = Login(login="Testuser")
    a.set_password('pwd')
    assert a.auth("pwd") is True
    strange = "#;\'\\\" $25; é ö ô è à ù"
    a.set_password(strange)
    assert not a.auth("pwd")
    assert a.auth(strange) is True

    a.active = False
    assert not a.auth(strange)


def test_unique_login(dbsession, login):

    assert Login.unique_login(login.login) == False
    assert Login.unique_login("test2") == True
    assert Login.unique_login(login.login, login.id) == True


def test_unique_user_id(dbsession, login):
    assert Login.unique_user_id(login.user_id) == False
    assert Login.unique_user_id("other login") == True
    assert Login.unique_login(1, login.id) == True


def test_id_from_login(dbsession, login):
    assert Login.id_from_login(login.login) == login.id
    with pytest.raises(Exception):
        Login.id_from_login("wrong login")


def test_find_by_login(dbsession, login):
    assert Login.find_by_login(login.login).id == login.id
