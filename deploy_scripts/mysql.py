#!/usr/bin/python
# -*- coding: utf-8 -*-
# * File Name : utils.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 10-07-2012
# * Last Modified :
#
# * Project : Autonomie Server handling
#
"""
    Usefull python tools to templatize, generate database and so on
"""
from .utils import gen_random_str
from .utils import launch_cmd

def get_sql_cmds(user, password, dbname):
    """
        Generates a database and adds a specific user
    """
    add_user = "CREATE USER {0} IDENTIFIED BY '{1}';".format(user, password)
    create_db = "CREATE DATABASE {0} CHARACTER SET utf8 COLLATE \
utf8_bin;".format(dbname)
    grant = "grant all privileges on {0}.* to {1}@localhost identified by \
'{2}';".format(dbname, user, password)
    return [add_user, create_db, grant]

def get_sql_connect_cmd():
    """
        Return the command used to connect to mysql as root
    """
    return "mysql --defaults-file=/etc/mysql/debian.cnf"

def get_cmds(user, password, dbname):
    """
        return the bash cmds to launch
    """
    root_cmd = get_sql_connect_cmd()
    for sql_cmd in get_sql_cmds(user, password, dbname):
        topipe = 'echo "{0}"'.format(sql_cmd)
        yield "{0} | {1}".format(topipe, root_cmd)

def gen_database(dbname="autonomie", user="autonomie"):
    """
        generates a database and a specific user and generates
        a random password
    """
    password = gen_random_str()
    for cmd in get_cmds(user, password, dbname):
        launch_cmd(cmd)
    return password

if __name__ == '__main__':
    print gen_database()

