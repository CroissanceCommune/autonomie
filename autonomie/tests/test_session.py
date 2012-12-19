# -*- coding: utf-8 -*-
# * File Name : test_session.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-12-2012
# * Last Modified :
#
# * Project :
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
