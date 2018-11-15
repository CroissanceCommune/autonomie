"""4.2.0 Add workshop.description

Revision ID: 470feca21286
Revises: 2793f8d2e33e
Create Date: 2018-07-12 10:19:33.474797

"""

# revision identifiers, used by Alembic.
revision = '470feca21286'
down_revision = '2793f8d2e33e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def update_database_structure():
    op.add_column('workshop', sa.Column('description', sa.Text(), nullable=True))

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.drop_column('workshop', 'description')
