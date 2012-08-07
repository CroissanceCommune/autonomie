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
import os
from hashlib import md5

from utils import gen_random_str
from utils import launch_cmd

def get_sql_grant_cmds(user, password, dbname):
    """
        return the change password command
    """
    grant = "grant all privileges on {0}.* to {1}@localhost identified by \
'{2}';".format(dbname, user, password)
    flush = "flush privileges;"
    return [grant, flush]

def get_sql_create_cmds(user, password, dbname):
    """
        Generates a database and adds a specific user
    """
    add_user = "CREATE USER {0} IDENTIFIED BY '{1}';".format(user, password)
    create_db = "CREATE DATABASE {0} CHARACTER SET utf8 COLLATE \
utf8_bin;".format(dbname)
    return [add_user, create_db]

def get_sql_connect_cmd():
    """
        Return the command used to connect to mysql as root
    """
    return "mysql --defaults-file=/etc/mysql/debian.cnf"

def get_bash_cmd(sql_cmd):
    """
        return the bash cmd to launch
    """
    root_cmd = get_sql_connect_cmd()
    topipe = 'echo "{0}"'.format(sql_cmd)
    return "{0} | {1}".format(topipe, root_cmd)

def gen_database(dbname="autonomie", user="autonomie"):
    """
        generates a database and a specific user and generates
        a random password
    """
    password = gen_random_str()
    if os.path.isdir("/var/lib/mysql/{0}".format(dbname)):
        print "The database {0} already exists, only modifying password".format(
                                                                        dbname)
        sql_cmds = get_sql_grant_cmds(user, password, dbname)
    else:
        sql_cmds = get_sql_create_cmds(user, password, dbname)
        sql_cmds.extend(get_sql_grant_cmds(user, password, dbname))

    for sql_cmd in sql_cmds:
        bash_cmd = get_bash_cmd(sql_cmd)
        launch_cmd(bash_cmd)
    return password

def adduser(login="admin.majerti", name="Majerti", firstname="Admin",
                                                    primary_group="1"):
    """
        Add a user to the database
    """
    password = gen_random_str(10)
    md5_pass = md5(password).hexdigest()
    cmd = "echo \"INSERT INTO egw_accounts (account_lid, account_pwd, account_firstname, \
account_lastname, account_status, account_primary_group, \
account_email) VALUES ('{0}', '{1}', '{2}', '{3}', 'A', '{4}', \
'equipe@majerti.fr');\" | mysql -uroot autonomie" .format(login, md5_pass,
                                                firstname, name, primary_group)
    launch_cmd(cmd)
    print "New password : {0}".format(password)

if __name__ == '__main__':
    print gen_database()

