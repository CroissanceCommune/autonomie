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

import os
import unittest

from pyramid import testing
from mock import Mock

from paste.deploy.loadwsgi import appconfig
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from autonomie.utils.widgets import ActionMenu

import autonomie.models.base
from autonomie.models.base import DBBASE  # base declarative object
from sqlalchemy.orm import scoped_session

here = os.path.dirname(__file__)
base_dir = os.path.join(here, '../..')

def __current_test_ini_file():
    local_test_ini = os.path.join(base_dir, 'test.ini')
    if os.path.exists(local_test_ini):
        return local_test_ini
    return os.path.join(base_dir, 'travis.ini')
settings = appconfig('config:%s' % __current_test_ini_file(), "autonomie")
TMPDIR = os.path.join(here, 'tmp')
DATASDIR = os.path.join(here, 'datas')

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        cls.connection = cls.engine.connect()
        cls.DBSession = scoped_session(sessionmaker(bind=cls.connection))
        autonomie.models.base.DBSESSION = cls.DBSession

    def setUp(self):
        # begin a non-ORM transaction
        self.trans = self.connection.begin()
        # Get a new session
        self.session = self.DBSession()
        DBBASE.session = self.session

    def tearDown(self):
        # rollback - everything that happened with the
        # dbsession above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.trans.rollback()
        self.session.close()

    def assertNotRaises(self, func, *args):
        func(*args)

class BaseViewTest(BaseTestCase):
    """
        Base class for testing views
    """
    def setUp(self):
        super(BaseViewTest, self).setUp()
        self.config = testing.setUp(request=testing.DummyRequest())

    def make_session(self, request, **options):
        from pyramid_beaker import BeakerSessionFactoryConfig
        return BeakerSessionFactoryConfig(**options)(request)

    def get_csrf_request(self, post={}):
        """
            Insert a dummy csrf token in the posted datas
        """
        def_csrf = 'default_csrf'
        if not  u'csrf_token' in post.keys():
            post.update({'csrf_token': def_csrf})
        request = testing.DummyRequest(post)
        request.session = self.make_session(request)
        request.dbsession = self.session
        request.config = {}
        csrf_token = Mock()
        csrf_token.return_value = def_csrf
        request.session.get_csrf_token = csrf_token
        request.actionmenu = ActionMenu()
        return request

class BaseFunctionnalTest(BaseViewTest):
    @classmethod
    def setUpClass(cls):
        from autonomie import main
        cls.app = main({}, **settings)
        super(BaseFunctionnalTest, cls).setUpClass()

    def setUp(self):
        from webtest import TestApp
        self.app = TestApp(self.app)
        self.config = testing.setUp()
        super(BaseFunctionnalTest, self).setUp()

def printstatus(obj):
    """
        print an object's status regarding the sqla's session
    """
    from sqlalchemy.orm import object_session
    from sqlalchemy.orm.util import has_identity
    if object_session(obj) is None and not has_identity(obj):
        print "Sqlalchemy status : transient"
    elif object_session(obj) is not None and not has_identity(obj):
        print "Sqlalchemy status : pending"
    elif object_session(obj) is None and has_identity(obj):
        print "Sqlalchemy status : detached"
    elif object_session(obj) is not None and has_identity(obj):
        print "Sqlalchemy status : persistent"
    else:
        print "Unknown Status"

