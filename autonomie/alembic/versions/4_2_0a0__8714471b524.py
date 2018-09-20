"""empty message

Revision ID: 8714471b524
Revises: 182bf34f7989
Create Date: 2018-09-20 09:38:21.607117

"""

# revision identifiers, used by Alembic.
revision = '8714471b524'
down_revision = '182bf34f7989'

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
