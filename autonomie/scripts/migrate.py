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

"""
command line scripts for autonomie
"""
import os
import pkg_resources
import logging

from pyramid.threadlocal import get_current_registry
from zope.sqlalchemy import mark_changed

from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.environment import EnvironmentContext
from alembic.util import load_python_file
from alembic import autogenerate as autogen

from autonomie_base.models.base import DBSESSION
from autonomie.scripts.utils import command

SCRIPT_DIR = pkg_resources.resource_filename('autonomie', 'alembic')
DEFAULT_LOCATION = 'autonomie:alembic'


logger = logging.getLogger('alembic.autonomie')


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
    def __init__(self, location, sql_url=None):
        self.location = location
        self.config = self._make_config(sql_url)
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

    def _make_config(self, sql_url=None):
        """
            populate alembic's configuration
        """
        cfg = Config()
        cfg.set_main_option("script_location", self.location)
        settings = get_current_registry().settings
        if sql_url is None:
            cfg.set_main_option("sqlalchemy.url", settings['sqlalchemy.url'])
        else:
            cfg.set_main_option("sqlalchemy.url", sql_url)
        from autonomie import version
        autonomie_version = version().replace('.', '_')
        cfg.set_main_option(
            'file_template',
            autonomie_version + "_%%(slug)s_%%(rev)s"
        )
        return cfg

    def _make_script_dir(self, alembic_cfg):
        """
            build and cast the script_directory
        """
        script_dir = ScriptDirectory.from_config(alembic_cfg)
        script_dir.__class__ = ScriptDirectoryWithDefaultEnvPy
        return script_dir


def upgrade(sql_url=None):
    """
        upgrade the content of DEFAULT_LOCATION
    """
    pkg_env = PackageEnvironment(DEFAULT_LOCATION, sql_url)

    revision = pkg_env.script_dir.get_current_head()
    logger.info(u'Upgrading {0}:'.format(pkg_env.location))

    def upgrade_func(rev, context):
        rev = rev[0]
        if rev == revision:
            logger.info(u'Already up to date.')
            return []
        logger.info(u'Upgrading from {0} to {1}...'.format(
            rev, revision))
        return context.script._upgrade_revs(revision, rev)

    pkg_env.run_env(
        upgrade_func,
        starting_rev=None,
        destination_rev=revision,
        )

    fetch(revision)
    print


def downgrade(revision):
    """
        downgrade the content of DEFAULT_LOCATION
    """
    pkg_env = PackageEnvironment(DEFAULT_LOCATION)

    logger.info(u'Downgrading {0} to {1}:'.format(pkg_env.location, revision))

    def downgrade_func(rev, context):
        if rev == revision:
            logger.info(u'  - already reached.')
            return []
        logger.info(u'  - downgrading from {0} to {1}...'.format(
            rev, revision))
        return context.script._downgrade_revs(revision, rev)

    pkg_env.run_env(
        downgrade_func,
        starting_rev=None,
        destination_rev=revision,
        )

    fetch(revision)
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
        print(u"  - The Current Revision: {0}".format(rev))
        return []
    pkg_env.run_env(current_revision)
    print
    print migrate.__doc__


def fetch(revision=None):
    """
        fetch a revision without migrating
    """
    def do_stamp(rev, context, revision=revision):
        context.stamp(context.script, revision)
        mark_changed(DBSESSION())
        return []
    PackageEnvironment(DEFAULT_LOCATION).run_env(do_stamp)


def fetch_head():
    """
        fetch the latest revision
    """
    fetch(None)


def revision(message):
    command_args = dict(
        message=message,
        autogenerate=True,
        sql=False,
        head='head',
        splice=False,
        branch_label=None,
        version_path=None,
        rev_id=None,
        depends_on=None,
    )
    env = PackageEnvironment(DEFAULT_LOCATION)

    revision_context = autogen.RevisionContext(
        env.config,
        env.script_dir,
        command_args,
    )

    def get_rev(rev, context):
        # autogen._produce_migration_diffs(context, template_args, imports)
        revision_context.run_autogenerate(rev, context)
        return []

    env.run_env(
        get_rev,
        as_sql=False,
        revision_context=revision_context,
        template_args=revision_context.template_args,
    )
    scripts = [
        script for script in revision_context.generate_scripts()
    ]
    return scripts


def migrate():
    """Migrate autonomie's database
    Usage:
        migrate <config_uri> list
        migrate <config_uri> upgrade
        migrate <config_uri> fetch [--rev=<rev>]
        migrate <config_uri> revision [--m=<message>]
        migrate <config_uri> downgrade [--rev=<rev>]

    o list : all the revisions
    o upgrade : upgrade the app to the latest revision
    o revision : auto-generate a migration file with the given message
    o fetch : set the revision
    o downgrade : downgrade the database

    Options:
        -h --help     Show this screen.
    """
    def callback(arguments, env):
        args = ()
        if arguments['list']:
            func = list_all
        elif arguments['upgrade']:
            func = upgrade
        elif arguments['fetch']:
            args = (arguments['--rev'],)
            func = fetch
        elif arguments['revision']:
            args = (arguments['--m'],)
            func = revision
        elif arguments['downgrade']:
            args = (arguments['--rev'],)
            func = downgrade
        return func(*args)
    try:
        return command(callback, migrate.__doc__)
    finally:
        pass
