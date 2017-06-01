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
import os
import sys
from pytest import fixture
from paste.deploy.loadwsgi import appconfig
from pyramid import testing
from mock import Mock
from pyramid_beaker import BeakerSessionFactoryConfig
from sqlalchemy import engine_from_config

from autonomie.utils.widgets import ActionMenu

HERE = os.path.dirname(__file__)
DATASDIR = os.path.join(HERE, 'datas')
TMPDIR = os.path.join(HERE, 'tmp')


def __current_test_ini_file():
    local_test_ini = os.path.join(HERE, '../../test.ini')
    if os.path.exists(local_test_ini):
        return local_test_ini
    return os.path.join(HERE, '../../travis.ini')


def launch_cmd(cmd):
    """
        Main entry to launch os commands
    """
    print("Launching : %s" % cmd)
    return os.system(cmd)


def test_connect(settings):
    """
        test the db connection
    """
    cmd = settings['connect']
    ret_code = launch_cmd(cmd)

    if ret_code != 0:

        err_str = """
    actual err_code = %s\n

    1- You need to configure the test.ini file so that this script can connect\n
    to the Mysql database:

        ...\n
        testdb.sql_cmd=mysql --defaults-file=/etc/mysql/debian.cnf\n
        ...\n
    or\n
        ...\n
        testdb.sql_cmd=mysql -uroot -p<password>\n
        ...\n


    2- Ensure mysql server is started and reachable with the given configuration
        """ % ret_code

        print err_str
        sys.exit(err_str)


def create_sql_user(settings):
    """
        Create the sql test user
    """
    launch_cmd(settings['adduser'])


def create_test_db(settings):
    """
        Create the test database and grant rights
    """
    launch_cmd(settings['adddb'])


def get_test_options_from_settings(settings):
    prefix = "testdb."
    options = {}
    for key in settings:
        if key.startswith(prefix):
            options[key[len(prefix):]] = settings[key]
    return options


def initialize_test_database(settings):
    """
        dump sample datas as a test database
    """
    if __current_test_ini_file().endswith('travis.ini'):
        return
    options = get_test_options_from_settings(settings)
    os.putenv('SHELL', '/bin/bash')
    test_connect(options)
    create_sql_user(options)
    launch_cmd(options['drop'])
    create_test_db(options)


@fixture(scope='session')
def settings():
    _settings = appconfig('config:%s' % __current_test_ini_file(), "autonomie")
    _settings["autonomie.ftpdir"] = DATASDIR
    return _settings

@fixture(scope='session')
def registry(settings):
    from pyramid.registry import Registry
    registry = Registry()
    registry.settings = settings
    return registry


@fixture
def pyramid_request(registry, settings):
    from pyramid_services import (
        find_service,
        find_service_factory,
        AdapterRegistry,
    )
    from functools import partial
    request = testing.DummyRequest()
    request.registry = registry
    request.find_service = partial(find_service, request)
    request.find_service_factory = partial(find_service_factory, request)
    request.service_cache = AdapterRegistry()
    return request


@fixture
def config(request, pyramid_request, settings, registry):
    """ returns a Pyramid `Configurator` object initialized
        with Kotti's default (test) settings.
    """
    os.environ['TZ'] = "Europe/Paris"
    from pyramid_beaker import set_cache_regions_from_settings
    config = testing.setUp(
        registry=registry,
        settings=settings,
        request=pyramid_request
    )
    config.include('pyramid_services')
    config.include('pyramid_mako')
    config.include('pyramid_chameleon')
    set_cache_regions_from_settings(settings)
    request.addfinalizer(testing.tearDown)

    from autonomie import setup_services
    setup_services(config, settings)
    from autonomie.utils.renderer import customize_renderers
    customize_renderers(config)
    return config


@fixture
def request_with_config(config, pyramid_request):
    return pyramid_request


@fixture(scope='session')
def connection(request, settings):
    """ sets up a SQLAlchemy engine and returns a connection
        to the database.

        :param settings: the settings of the test (given by the testing fixture)
        :returns: a sqlalchemy connection object
    """
    # the following setup is based on `kotti.resources.initialize_sql`,
    # except that it explicitly binds the session to a specific connection
    # enabling us to use savepoints independent from the orm, thus allowing
    # to `rollback` after using `transaction.commit`...
    initialize_test_database(settings)

    from autonomie_base.models.base import DBSESSION, DBBASE
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    _connection = engine.connect()
    DBSESSION.registry.clear()
    DBSESSION.configure(bind=_connection)
    DBBASE.metadata.bind = engine
    def drop_db():
        """
            drop the test database
        """
        if __current_test_ini_file().endswith('travis.ini'):
            return
        db_settings = get_test_options_from_settings(settings)
        launch_cmd(db_settings['drop'])

    request.addfinalizer(drop_db)
    return _connection


def populate_db(session):
    from autonomie.models.user import User
    user = User(
        login='user1_login',
        firstname='user1_firstname',
        lastname="user1_lastname",
        email="user1@test.fr"
    )
    user.set_password('o')
    session.add(user)

    from autonomie.models.project import Project
    project = Project(
        name='Projet 1',
        code='P001',
        definition="Projet 1"
    )
    session.add(project)

    from autonomie.models.customer import Customer
    cust = Customer(
        code='C001',
        name='Client1',
        contactLastName=u'Client Lastname',
        address=u'15 rue Victore Hugo',
        zipCode='69003',
        city='Lyon',
    )
    cust.projects.append(project)
    session.add(cust)

    from autonomie.models.project import Phase
    phase = Phase(name='Phase de test')
    phase.project = project
    session.add(phase)


    from autonomie.models.company import Company
    c = Company(
        name="company1",
        goal="Company of user1",
        phone='0457858585',
    )
    c.employees.append(user)
    c.customers.append(cust)
    c.projects.append(project)
    session.add(c)
    from autonomie.scripts import fake_database
    fake_database.set_configuration()


@fixture(scope='session')
def content(connection, settings):
    """
    sets up some default content
    """
    from transaction import commit
    from autonomie_base.models.base import DBBASE, DBSESSION
    metadata = DBBASE.metadata

    metadata.drop_all(connection.engine)
    from autonomie.models.initialize import _adjust_for_engine
    _adjust_for_engine(connection.engine)
    metadata.create_all(connection.engine)

    populate_db(DBSESSION())

    commit()


@fixture
def dbsession(config, content, connection, request):
    """ returns a db session object and sets up a db transaction
        savepoint, which will be rolled back after the test.

        :returns: a SQLA session
    """
    from transaction import abort
    trans = connection.begin()          # begin a non-orm transaction
    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)
    from autonomie_base.models.base import DBSESSION
    return DBSESSION()


@fixture
def get_csrf_request(pyramid_request):
    """
    Build a testing request builder with a csrf token

    :returns: a function to be called with params/cookies/post optionnal
    arguments
    """
    def func(params=None, cookies=None, post=None):
        params = params or {}
        post = post or {}
        params.update(post)
        cookies = cookies or {}
        def_csrf = 'default_csrf'
        if not  u'csrf_token' in post.keys():
            post.update({'csrf_token': def_csrf})
        pyramid_request.params = params
        pyramid_request.POST = post
        pyramid_request.cookies = cookies
        pyramid_request.session = BeakerSessionFactoryConfig()(pyramid_request)
        pyramid_request.config = {}
        csrf_token = Mock()
        csrf_token.return_value = def_csrf
        pyramid_request.session.get_csrf_token = csrf_token
        pyramid_request.actionmenu = ActionMenu()
        return pyramid_request
    return func


@fixture
def get_csrf_request_with_db(pyramid_request, dbsession):
    """
    Build a testing request builder with a csrf token and a db session object

    :returns: a function to be called with params/cookies/post optionnal
    arguments
    """
    def func(params=None, cookies=None, post=None):
        cookies = cookies or {}
        params = params or {}
        post = post or {}
        params.update(post)
        def_csrf = 'default_csrf'
        if not  u'csrf_token' in post.keys():
            post.update({'csrf_token': def_csrf})
        pyramid_request.params = params
        pyramid_request.POST = post
        pyramid_request.cookies = cookies
        pyramid_request.session = BeakerSessionFactoryConfig()(pyramid_request)
        pyramid_request.dbsession = dbsession
        pyramid_request.config = {}
        csrf_token = Mock()
        csrf_token.return_value = def_csrf
        pyramid_request.session.get_csrf_token = csrf_token
        pyramid_request.actionmenu = ActionMenu()
        return pyramid_request
    return func


@fixture
def wsgi_app(settings, dbsession):
    from autonomie import base_configure, prepare_config
    config = prepare_config(**settings)
    return base_configure(config, dbsession, **settings).make_wsgi_app()


@fixture
def app(wsgi_app):
    from webtest import TestApp
    return TestApp(wsgi_app)
