# -*- coding: utf-8 -*-
# * File Name : add_admin.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 04-10-2012
# * Last Modified :
#
# * Project :
#
"""
    Command to add an admin to autonomie
"""
import os
from transaction import commit
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
    user = User(login=login,
                firstname=firstname,
                primary_group=1,  #is an admin
                lastname=lastname)
    user.set_password(password)
    db = DBSESSION()
    db.add(user)
    db.flush()
    commit()
    print u"Creating account %s with password %s" % (login, unicode(password))
    return user

def add_admin_cmd():
    """Create an admin account in Autonomie
    Usage:
        autonomie-admin <config_uri> add [--user=<user>] [--pwd=<password>] [--firstname=<firstname>] [--lastname=<lastname>]

    Options:
        -h --help     Show this screen.
    """
    try:
        return command(add_admin, add_admin_cmd.__doc__)
    finally:
        pass
