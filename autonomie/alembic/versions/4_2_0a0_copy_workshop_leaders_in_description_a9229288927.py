"""copy workshop.leaders in description

Revision ID: a9229288927
Revises: 470feca21286
Create Date: 2018-07-12 11:06:03.897458

"""

# revision identifiers, used by Alembic.
revision = 'a9229288927'
down_revision = '470feca21286'

import json

from alembic import op
import sqlalchemy as sa
from zope.sqlalchemy import mark_changed

def update_database_structure():
    pass

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()

    from alembic.context import get_bind
    conn = get_bind()

    for row in list(conn.execute('SELECT id, leaders FROM workshop')):
        if not row.leaders:
            continue

        try:
            leaders_list = json.loads(row.leaders)
        except ValueError:
            # This should not happen, but some dumps we use have a bare string
            # in leaders field.
            leaders_list = [row.leaders]

        req = sa.text("""
            UPDATE workshop SET
            description=CONCAT(
              'Formateurs: ',
              IFNULL(:leaders, ''),
              ' ',
              IFNULL(description, '')
            )
            WHERE id=:id_
            """)
        conn.execute(
            req,
            leaders=', '.join(leaders_list),
            id_=row.id,
        )
    mark_changed(session)
    session.flush()


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
