"""4.2.0 Remove Task.prefix column

Revision ID: 4ab29f6cdd50
Revises: 67403ce32f8
Create Date: 2018-06-09 19:48:51.640677

"""

# revision identifiers, used by Alembic.
revision = '4ab29f6cdd50'
down_revision = '67403ce32f8'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def update_database_structure():
    op.drop_column('task', 'prefix')

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.add_column('task', sa.Column('prefix', mysql.VARCHAR(length=15), nullable=True))
