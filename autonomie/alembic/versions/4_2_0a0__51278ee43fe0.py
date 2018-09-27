"""empty message

Revision ID: 51278ee43fe0
Revises: 587af17edabb
Create Date: 2018-09-26 15:05:23.492516

"""

# revision identifiers, used by Alembic.
revision = '51278ee43fe0'
down_revision = '587af17edabb'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    pass

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
