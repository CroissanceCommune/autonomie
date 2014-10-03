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
import os
from autonomie.scripts.utils import command
from autonomie.models import DBSESSION
from autonomie.models.user import User

PWD_LENGTH = 10

def get_pwd():
    """
        Return a random password
    """
    return os.urandom(PWD_LENGTH)

def get_value(arguments, key, default):
    """
        Return the value for key in arguments or default
    """
    val = arguments.get('--%s' % key)
    if not val:
        val = default
    return val

def add_admin(arguments):
    """
        Add an admin user to the database
    """
    login = get_value(arguments, 'user', 'admin.majerti')
    password = get_value(arguments, 'pwd', get_pwd())
    firstname = get_value(arguments, 'firstname', 'Admin')
    lastname = get_value(arguments, 'lastname', 'Majerti')
    email = get_value(arguments, 'email', 'admin@example.com')
    user = User(login=login,
                firstname=firstname,
                primary_group=1,  #is an admin
                lastname=lastname,
                email=email
            )
    user.set_password(password)
    db = DBSESSION()
    db.add(user)
    db.flush()
    print u"Creating account %s with password %s" % (login, unicode(password))
    return user

def add_admin_cmd():
    """Create an admin account in Autonomie
    Usage:
        autonomie-admin <config_uri> add [--user=<user>] [--pwd=<password>] [--firstname=<firstname>] [--lastname=<lastname>] [--email=<email>]

    Options:
        -h --help     Show this screen.
    """
    try:
        return command(add_admin, add_admin_cmd.__doc__)
    finally:
        pass
