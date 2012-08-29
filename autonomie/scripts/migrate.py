# -*- coding: utf-8 -*-
# * File Name : scripts.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 28-08-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
command line scripts for autonomie
"""
import os
import pkg_resources

from pyramid.threadlocal import get_current_registry
from zope.sqlalchemy import mark_changed

from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.environment import EnvironmentContext
from alembic.util import load_python_file

from autonomie.models import DBSESSION
from autonomie.scripts.utils import command

SCRIPT_DIR = pkg_resources.resource_filename('autonomie', 'alembic')
DEFAULT_LOCATION = 'autonomie:alembic'

class ScriptDirectoryWithDefaultEnvPy(ScriptDirectory):
    """
        Wrapper for the ScriptDirectory object
        enforce the env.py script
    """
    @property
    def env_py_location(self):
        return os.path.join(SCRIPT_DIR, 'env.py')

    def run_env(self):
        dir_, filename = self.env_py_location.rsplit(os.path.sep, 1)
        load_python_file(dir_, filename)

class PackageEnvironment(object):
    """
        package environment
        Here we use one but it could be usefull when handling plugins'
        migrations
    """
    def __init__(self, location):
        self.location = location
        self.config = self._make_config()
        self.script_dir = self._make_script_dir(self.config)

    @property
    def pkg_name(self):
        return self.location.split(':')[0]

    @property
    def version_table(self):
        """
            Return the name of the table hosting alembic's current revision
        """
        return '{0}_alembic_version'.format(self.pkg_name)

    def run_env(self, fn, **kw):
        """
            run alembic's context
        """
        with EnvironmentContext(
            self.config,
            self.script_dir,
            fn=fn,
            version_table=self.version_table,
            **kw
            ):
            self.script_dir.run_env()

    def _make_config(self):
        """
            populate alembic's configuration
        """
        cfg = Config()
        cfg.set_main_option("script_location", self.location)
        settings = get_current_registry().settings
        cfg.set_main_option("sqlalchemy.url", settings['sqlalchemy.url'])
        return cfg

    def _make_script_dir(self, alembic_cfg):
        """
            build and cast the script_directory
        """
        script_dir = ScriptDirectory.from_config(alembic_cfg)
        script_dir.__class__ = ScriptDirectoryWithDefaultEnvPy
        return script_dir

def upgrade():
    """
        upgrade the content of DEFAULT_LOCATION
    """
    pkg_env = PackageEnvironment(DEFAULT_LOCATION)

    revision = pkg_env.script_dir.get_current_head()
    print(u'Upgrading {0}:'.format(pkg_env.location))

    def upgrade_func(rev, context):
        if rev == revision:
            print(u'  - already up to date.')
            return []
        print(u'  - upgrading from {0} to {1}...'.format(
            rev, revision))
        return context.script._upgrade_revs(revision, rev)

    pkg_env.run_env(
        upgrade_func,
        starting_rev=None,
        destination_rev=revision,
        )
    print

def list_all():
    """
        list all available revisions
    """
    pkg_env = PackageEnvironment(DEFAULT_LOCATION)
    print(u'{0}:'.format(pkg_env.pkg_name))

    for script in pkg_env.script_dir.walk_revisions():
        print(u"  - {0} -> {1}: {2}".format(
            script.down_revision,
            script.revision,
            script.doc,
            ))

    def current_revision(rev, context):
        """
            print the current revision
        """
        print(u"  - current revision: {0}".format(rev))
        return []
    pkg_env.run_env(current_revision)
    print

def stamp(revision):
    """
        fetch a revision without migrating
    """
    def do_stamp(rev, context, revision=revision):
        current = context._current_rev()
        if revision is None:
            revision = context.script.get_current_head()
        elif revision == 'None':
            revision = None
        context._update_current_rev(current, revision)
        mark_changed(DBSESSION())
        return []
    PackageEnvironment(DEFAULT_LOCATION).run_env(do_stamp)


def migrate():
    __doc__ = """Migrate autonomie's database
    Usage:
        migrate <config_uri> list_all
        migrate <config_uri> upgrade
        migrate <config_uri> stamp [--rev=<rev>]

    o stamp : join a specific migration revision without launching migration
              scripts
    o list_all : all the revisions
    o upgrade : upgrade the app to the latest revision

    Options:
        -h --help     Show this screen.
    """
    def callback(arguments):
        args = ()
        if arguments['list_all']:
            func = list_all
        elif arguments['upgrade']:
            func = upgrade
        elif arguments['stamp']:
            args = (arguments['--rev'],)
            func = stamp
        return func(*args)
    try:
        return command(callback, __doc__)
    finally:
        pass
