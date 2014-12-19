# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Test the csv import view module
"""
import pytest
from autonomie.views.csv_import import (
    get_preferences_obj,
    load_preferences,
    get_preference,
)


@pytest.fixture
def config(dbsession):
    from autonomie.models.config import Config
    c = Config(
        name='csv_import',
        value='{"test en action": {"PR\\u00e9nom": "coordonnees_firstname"}}'
    )
    dbsession.add(c)
    dbsession.flush()
    return c

def test_get_preferences_obj(config):
    assert get_preferences_obj().value is not None

def test_get_new_preference_obj():
    assert get_preferences_obj().value is None

def test_load_preferences(config):
    assert load_preferences(get_preferences_obj()).keys() == [u"test en action"]

def test_get_preference(config):
    assert get_preference('test en action') == {u'PRénom': 'coordonnees_firstname'}
