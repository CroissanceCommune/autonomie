# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 11-09-2012
# * Last Modified :
#
# * Project :
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
