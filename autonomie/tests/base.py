# -*- coding: utf-8 -*-
# * File Name : base.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 13-03-2012
# * Last Modified :
#
# * Project : autonomie
#
import os
import unittest

from pyramid import testing
from mock import Mock

from paste.deploy.loadwsgi import appconfig
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

import autonomie.models
from autonomie.models import DBBASE  # base declarative object
from sqlalchemy.orm import scoped_session

here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, '../../', 'test.ini'),
                                                          "autonomie")
TMPDIR = os.path.join(here, 'tmp')
DATASDIR = os.path.join(here, 'datas')

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        cls.connection = cls.engine.connect()
        cls.DBSession = scoped_session(sessionmaker(bind=cls.connection))
        autonomie.models.DBSESSION = cls.DBSession

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
        csrf_token = Mock()
        csrf_token.return_value = def_csrf
        request.session.get_csrf_token = csrf_token
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
