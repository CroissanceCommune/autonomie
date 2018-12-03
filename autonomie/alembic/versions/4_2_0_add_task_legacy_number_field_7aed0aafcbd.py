"""4.2.0 Add task.legacy_number field

Revision ID: 7aed0aafcbd
Revises: 3d5b6e485203
Create Date: 2018-11-30 17:18:22.260814

"""

# revision identifiers, used by Alembic.
revision = '7aed0aafcbd'
down_revision = '3d5b6e485203'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from zope.sqlalchemy import mark_changed

def update_database_structure():
    op.add_column('task', sa.Column('legacy_number', sa.Boolean(), nullable=False))

def migrate_datas():
    """We tolerate duplicate invoice number for invoices issued so far.

    That means that coops have to migrate to real unique invoice number
    template before then.
    """
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()
    conn.execute("UPDATE task set legacy_number = 1")
    mark_changed(session)


def upgrade():
    update_database_structure()
    migrate_datas()

def downgrade():
    op.drop_column('task', 'legacy_number')
