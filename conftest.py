# -*- coding: utf-8 -*-
# * File Name : conftest.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 12-03-2012
# * Last Modified :
#
# * Project :
#
import sys
from os.path import dirname, join
import os.path
import shlex
import subprocess

from paste.deploy.loadwsgi import appconfig
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from autonomie.models.initialize import initialize_sql
from autonomie.tests.base import TMPDIR


HERE = dirname(__file__)


def __current_test_ini_file():
    local_test_ini = os.path.join(HERE, 'test.ini')
    if os.path.exists(local_test_ini):
        return local_test_ini
    return os.path.join(HERE, 'travis.ini')


SETTINGS = appconfig('config:%s' % __current_test_ini_file(), "autonomie")
PREFIX = "testdb."

OPTIONS = dict((key[len(PREFIX):], SETTINGS[key])
            for key in SETTINGS if key.startswith(PREFIX))

if HERE:
    OPTIONS['sampledb'] = join(HERE, OPTIONS['sampledb'])
    OPTIONS['sampledatas'] = join(HERE, OPTIONS['sampledatas'])
    OPTIONS['updatedir'] = join(HERE, OPTIONS['updatedir'])
    OPTIONS.setdefault('mysql_cmd', 'mysql_cmd')
    os.putenv('SHELL', '/bin/bash')


def launch_cmd(cmd):
    """
        Main entry to launch os commands
    """
    command_line = cmd.format(**OPTIONS)
    print "Launching : %s" % command_line
    return os.system(command_line)


def launch_sql_cmd(cmd):
    """
        Main entry to launch sql commands
    """
    return launch_cmd("echo \"%s\"|{mysql_cmd}" % cmd)


def create_sql_user():
    """
        Create the sql test user
    """
    launch_sql_cmd('CREATE USER {user}@localhost;')


def create_test_db():
    """
        Create the test database and grant rights
    """
    launch_sql_cmd('CREATE DATABASE IF NOT EXISTS "{db}" CHARACTER SET utf8 COLLATE utf8_bin;')


def grant_user():
    """
        grant privileges on the test db to the test user
    """
    launch_sql_cmd("GRANT ALL PRIVILEGES on {db}.* to {user}@localhost "
                   "identified by '{password}'; FLUSH PRIVILEGES;")


def dump_sample():
    """
        dump sample datas in our test database
    """
    from autonomie.scripts import fake_database
    fake_database.fake_database_fill({})
    from transaction import commit
    commit()
    launch_cmd("mysqldump -uroot testautonomie > /tmp/test.sql")

def drop_db():
    """
        drop the test database
    """
    cmd = "echo \"echo 'drop database {db};' | {mysql_cmd}\" | at now"
    launch_cmd(cmd)


def drop_sql_datas():
    """
        Drop all the test db created stuff
    """
    print "Dropping test datas : keeping it clean"
    drop_db()


def test_connect():
    """
        test the db connection
    """
    cmd = "echo 'quit' | {mysql_cmd}"
    ret_code = launch_cmd(cmd)

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


def initialize_test_database():
    """
        dump sample datas as a test database
    """
    if __current_test_ini_file().endswith('travis.ini'):
        return
    print "Initializing test database"
    test_connect()
    create_sql_user()
    create_test_db()
    grant_user()


def migrate_database(settings, key):
    """
        migrate the database
    """
    from autonomie.scripts.migrate import upgrade
    upgrade(settings[key])


def pytest_sessionstart():
    """
        Py.test setup
    """
    from py.test import config

    # Only run database setup on master (in case of xdist/multiproc mode)
    if not hasattr(config, 'slaveinput'):
        initialize_test_database()

        engine = engine_from_config(SETTINGS, prefix='sqlalchemy.')
        print 'Creating the tables on the test database %s' % engine

        config = Configurator(settings=SETTINGS)
        config.begin()
        config.commit()

        initialize_sql(engine)
        dump_sample()


def pytest_sessionfinish():
    """
        py.test teardown
    """
    from py.test import config
    if __current_test_ini_file().endswith('travis.ini'):
        return

    if not hasattr(config, 'slaveinput'):
        drop_sql_datas()
        launch_cmd('rm -rf "%s"' % TMPDIR)
