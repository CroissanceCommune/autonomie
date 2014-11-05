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


def __current_test_ini_file():
    local_test_ini = os.path.join(HERE, '../../test.ini')
    if os.path.exists(local_test_ini):
        return local_test_ini
    return os.path.join(HERE, '../../travis.ini')


def launch_cmd(settings, cmd):
    """
        Main entry to launch os commands
    """
    command_line = cmd.format(**settings)
    return os.system(command_line)


def launch_sql_cmd(settings, cmd):
    """
        Main entry to launch sql commands
    """
    return launch_cmd(settings, "echo \"%s\"|{mysql_cmd}" % cmd)


def test_connect(settings):
    """
        test the db connection
    """
    cmd = "echo 'quit' | {mysql_cmd}"
    ret_code = launch_cmd(settings, cmd)

    if ret_code != 0:
        err_str = """
    actual err_code = %s\n
    You need to configure the test.ini file so that this script can connect\n
    to the Mysql database:

        ...\n
        testdb.mysql_cmd=mysql --defaults-file=/etc/mysql/debian.cnf\n
        ...\n
    or\n
        ...\n
        testdb.mysql_cmd=mysql -uroot -p<password>\n
        ...\n
        """ % ret_code

        print err_str
        sys.exit(err_str)


def create_sql_user(settings):
    """
        Create the sql test user
    """
    launch_sql_cmd(settings, 'CREATE USER {user}@localhost;')


def create_test_db(settings):
    """
        Create the test database and grant rights
    """
    launch_sql_cmd(settings, 'CREATE DATABASE IF NOT EXISTS "{db}" CHARACTER SET utf8 COLLATE utf8_bin;')


def grant_user(settings):
    """
        grant privileges on the test db to the test user
    """
    launch_sql_cmd(settings, "GRANT ALL PRIVILEGES on {db}.* to {user}@localhost "
                   "identified by '{password}'; FLUSH PRIVILEGES;")


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
    create_test_db(options)
    grant_user(options)


@fixture(scope='session')
def settings():
    _settings = appconfig('config:%s' % __current_test_ini_file(), "autonomie")
    return _settings

@fixture
def pyramid_request():
    return testing.DummyRequest()

@fixture
def config(request, pyramid_request, settings):
    """ returns a Pyramid `Configurator` object initialized
        with Kotti's default (test) settings.
    """
    os.environ['TZ'] = "Europe/Paris"
    from pyramid.registry import Registry
    from pyramid_beaker import set_cache_regions_from_settings
    registry = Registry()
    registry.settings = settings
    config = testing.setUp(registry=registry, settings=settings, request=pyramid_request)
    config.include('pyramid_mako')
    config.include('pyramid_chameleon')
    set_cache_regions_from_settings(settings)
    request.addfinalizer(testing.tearDown)

    from autonomie.utils.renderer import (
        set_deform_renderer,
        set_json_renderer,
        set_default_widgets,
    )
    set_deform_renderer()
    set_json_renderer(config)
    set_default_widgets()
    return config


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

    from autonomie.models.base import DBSESSION, DBBASE
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    _connection = engine.connect()
    DBSESSION.registry.clear()
    DBSESSION.configure(bind=_connection)
    DBBASE.metadata.bind = engine
    def drop_db():
        """
            drop the test database
        """
        options = get_test_options_from_settings(settings)
        cmd = "echo \"echo 'drop database {db};' | {mysql_cmd}\" | at now"
        launch_cmd(options, cmd)

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

    from autonomie.models.customer import Customer
    cust = Customer(
        code='C001',
        name='Client1',
        contactLastName=u'Client Lastname',
        address=u'15 rue Victore Hugo',
        zipCode='69003',
        city='Lyon',
    )
    session.add(cust)

    from autonomie.models.project import Project
    project = Project(
        name='Projet 1',
        code='P001',
        definition="Projet 1"
    )
    session.add(project)

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


@fixture(scope='session')
def content(connection, settings):
    """
    sets up some default content
    """
    from transaction import commit
    from autonomie.models.base import DBBASE, DBSESSION
    metadata = DBBASE.metadata

    metadata.drop_all(connection.engine)
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
    from autonomie.models.base import DBSESSION
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
    from autonomie import base_configure
    return base_configure({}, dbsession, **settings).make_wsgi_app()


@fixture
def app(wsgi_app):
    from webtest import TestApp
    return TestApp(wsgi_app)
