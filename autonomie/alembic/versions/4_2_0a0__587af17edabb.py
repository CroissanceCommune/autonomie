"""empty message

Revision ID: 587af17edabb
Revises: 8714471b524
Create Date: 2018-09-26 14:59:36.612490

"""

# revision identifiers, used by Alembic.
revision = '587af17edabb'
down_revision = '8714471b524'

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
