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
    Command to add an admin to autonomie
"""
import logging
import os
from sqlalchemy.orm.exc import NoResultFound
from autonomie.scripts.utils import (
    command,
    get_value,
)
from autonomie_base.models.base import DBSESSION
from autonomie.forms.user.user import User
from autonomie.forms.user.login import Login


PWD_LENGTH = 10


def get_pwd():
    """
        Return a random password
    """
    return os.urandom(PWD_LENGTH).encode('base-64')


def user_add_command(arguments, env):
    """
        Add a user in the database
    """
    logger = logging.getLogger(__name__)

    login = get_value(arguments, 'user', 'admin.majerti')
    login = login.decode('utf-8')
    logger.debug(u"Adding a user {0}".format(login))

    password = get_value(arguments, 'pwd', get_pwd())
    password = password.decode('utf-8')

    login = Login(login=login)
    login.set_password(password)

    group = get_value(arguments, 'group', None)
    if group:
        try:
            login.groups.append(group)
        except NoResultFound:
            print(
                u"""

ERROR : group %s doesn't exist, did you launched the syncdb command :

    autonomie-admin <fichier.ini> syncdb
                """ % (
                    group,
                )
            )
            return

    db = DBSESSION()
    db.add(login)
    db.flush()


    firstname = get_value(arguments, 'firstname', 'Admin')
    lastname = get_value(arguments, 'lastname', 'Majerti')
    email = get_value(arguments, 'email', 'admin@example.com')
    user = User(
        login=login,
        firstname=firstname,
        lastname=lastname,
        email=email
    )
    db.add(user)
    db.flush()
    print(u"""
    User Account created :
          ID        : {0.id}
          Login     : {0.login.login}
          Firstname : {0.firstname}
          Lastname  : {0.lastname}
          Email     : {0.email}
          Groups    : {0.login.groups}
          """.format(user))

    if 'pwd' not in arguments:
        print(u"""
          Password  : {0}""".format(password)
              )

    logger.debug(u"-> Done")
    return user


def test_mail_command(arguments, env):
    """
    Test tool for mail sending
    """
    from autonomie_base.mail import send_mail
    dest = get_value(arguments, 'to', 'autonomie@majerti.fr')
    request = env['request']
    subject = u"Test d'envoi de mail"
    body = u"""Il semble que le test d'envoi de mail a réussi.
    Ce test a été réalisé depuis le script autonomie-admin

Bonne et belle journée !!!"""
    send_mail(
        request,
        [dest],
        body,
        subject
    )


def syncdb_command(arguments, env):
    """
    Populate the database
    """
    from autonomie.models.populate import populate_database
    populate_database()


def autonomie_admin_cmd():
    """Autonomie administration tool
    Usage:
        autonomie-admin <config_uri> useradd [--user=<user>] [--pwd=<password>] [--firstname=<firstname>] [--lastname=<lastname>] [--email=<email>] [--group=<group>]
        autonomie-admin <config_uri> testmail [--to=<mailadress>]
        autonomie-admin <config_uri> syncdb

    o useradd : Add a user in the database
    o testmail : Send a test mail to the given address
    o syncdb : Populate the database with the initial datas

    Options:

        -h --help     Show this screen.
    """
    def callback(arguments, env):
        if arguments['useradd']:
            func = user_add_command
        elif arguments['testmail']:
            func = test_mail_command
        elif arguments['syncdb']:
            func = syncdb_command
        return func(arguments, env)
    try:
        return command(callback, autonomie_admin_cmd.__doc__)
    finally:
        pass
