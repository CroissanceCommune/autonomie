"""4.2.0 change task.official_number int->str

Revision ID: 29e53cf4579a
Revises: 41261dd0a613
Create Date: 2018-06-06 18:11:23.345748

"""

# revision identifiers, used by Alembic.
revision = '29e53cf4579a'
down_revision = '41261dd0a613'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def update_database_structure():
    op.alter_column('task', 'official_number',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=255),
               existing_nullable=True)


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.alter_column('task', 'official_number',
               existing_type=sa.String(length=255),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=True)
