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

from autonomie.utils.session import get_session_factory
from autonomie.tests.base import BaseTestCase
from pyramid_beaker.tests import TestPyramidBeakerSessionObject
from pyramid import testing

class TestSession(TestPyramidBeakerSessionObject):
    def test_longtimeout(self):
        settings = {"session.longtimeout":350, "session.timeout":35}
        sessionfactory = get_session_factory(settings)
        request = testing.DummyRequest(cookies={'remember_me':'ok'})
        session = sessionfactory(request)
        self.assertEqual(session.timeout, 350)

    def test_notlongtimeout(self):
        settings = {"session.longtimeout":350, "session.timeout":35}
        sessionfactory = get_session_factory(settings)
        request = testing.DummyRequest()
        session = sessionfactory(request)
        self.assertEqual(session.timeout, 35)
