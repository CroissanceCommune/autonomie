"""4.2.0 Remove Workshop.leaders field

Revision ID: 1e4eb742df36
Revises: a9229288927
Create Date: 2018-07-18 11:00:25.084656

"""

# revision identifiers, used by Alembic.
revision = '1e4eb742df36'
down_revision = 'a9229288927'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def update_database_structure():
    op.drop_column('workshop', 'leaders')

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.add_column('workshop', sa.Column('leaders', mysql.TEXT(), nullable=True))
