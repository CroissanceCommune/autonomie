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

from mock import Mock

from autonomie.forms import (
    merge_session_with_post,
    flatten_appstruct,
)


def test_merge_session_with_post():
    session = Mock()
    post = dict(id=12, name="Dupont", lastname="Jean",
                            accounts=['admin', 'user'])
    merge_session_with_post(session, post)
    assert session.name == 'Dupont'
    assert "admin" in session.accounts


def test_flatten_appstruct():
    appstruct = {'key1':'value1', 'key2': {'key3': 'value3'}}
    assert flatten_appstruct(appstruct) == {'key1': 'value1', 'key3': 'value3'}
