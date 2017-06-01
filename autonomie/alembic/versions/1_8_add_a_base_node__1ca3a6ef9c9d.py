"""1.8 : Add a base node class

Revision ID: 1ca3a6ef9c9d
Revises: 1aa7e3b02b04
Create Date: 2013-12-12 18:05:09.712208

"""

# revision identifiers, used by Alembic.
revision = '1ca3a6ef9c9d'
down_revision = '1aa7e3b02b04'

import datetime
from alembic import op
import sqlalchemy as sa

from autonomie.models.node import Node


def format_date(value):
    if value:
        return datetime.datetime.fromtimestamp(float(value))
    return datetime.datetime.now()

def upgrade():

    from autonomie_base.models.base import DBSESSION


    session = DBSESSION()
    from alembic.context import get_bind

    request = "select id, type_, name, creationDate, updateDate from task"
    conn = get_bind()
    result = conn.execute(request)
    index = 0
    max_id = -1
    for id_, type_, name, creationDate, updateDate in result:
        creationDate = format_date(creationDate)
        updateDate = format_date(updateDate)
        index += 1
        node = Node(
                id=id_,
                created_at=creationDate,
                updated_at=updateDate,
                name=name,
                type_=type_
                )
        session.add(node)
        if index % 50 == 0:
            session.flush()
        if id_ > max_id:
            max_id = id_

    request = "select id, name, creationDate, updateDate from project ORDER BY id DESC"
    result = conn.execute(request).fetchall()

    # We disable foreign key constraints check
    op.execute("SET FOREIGN_KEY_CHECKS=0;")
    index = 0
    for id_, name, creationDate, updateDate in result:
        new_id = id_ + max_id
        creationDate = format_date(creationDate)
        updateDate = format_date(updateDate)
        index += 1
        node = Node(
                id=new_id,
                created_at=creationDate,
                updated_at=updateDate,
                name=name,
                type_='project'
                )
        session.add(node)

        # We update the foreignkeys
        for table in ('estimation', 'invoice', 'cancelinvoice', 'phase', 'project_customer'):
            op.execute("update {0} set project_id={1} where project_id={2}".format(table, new_id, id_))

        # We update the project id
        op.execute("update project set id={0} where id={1};".format(new_id, id_))
        if index % 50 == 0:
            session.flush()
    op.execute("SET FOREIGN_KEY_CHECKS=1;")


def downgrade():
    op.execute("drop table {0};".format(Node.__tablename__))
