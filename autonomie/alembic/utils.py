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

from alembic import op
import sqlalchemy as sa


def force_rename_table(old, new):
    from autonomie.models import DBSESSION
    conn = DBSESSION.connection()
    if table_exists(old):
        if table_exists(new):
            op.drop_table(new)
        op.rename_table(old, new)


def table_exists(tbl):
    from autonomie.models import DBSESSION
    conn = DBSESSION.connection()
    ret = False
    try:
        conn.execute("select * from `%s`" % tbl)
        ret = True
    except:
        pass
    return ret


def rename_column(tbl, column_name, name, type_=sa.Integer, nullable=False,
                  autoincrement=False, **kw):
    if column_exists(tbl, column_name):
        if autoincrement:
            op.execute("Alter table `%s` change `%s` `%s` int(11) NOT NULL "
                       "AUTO_INCREMENT;" % (tbl, column_name, name))
        else:
            op.alter_column(tbl, column_name, name=name, type_=type_,
                            nullable=nullable, **kw)


def column_exists(tbl, column_name):
    from autonomie.models import DBSESSION
    conn = DBSESSION.connection()
    ret = False
    try:
        conn.execute("select %s from %s" % (column_name, tbl))
        ret = True
    except:
        pass
    return ret


def add_column(tbl, column):
    if not column_exists(tbl, column.name):
        op.add_column(tbl, column)


def disable_constraints():
    op.execute("SET FOREIGN_KEY_CHECKS=0;")


def enable_constraints():
    op.execute("SET FOREIGN_KEY_CHECKS=1;")
