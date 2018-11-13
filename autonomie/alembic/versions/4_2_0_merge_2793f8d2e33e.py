"""4.2.0 Revision merge

Revision ID: 2793f8d2e33e
Revises: ('50caf9dd4cd6', '2a66d798c55d')
Create Date: 2018-07-11 14:43:11.369728

"""

# revision identifiers, used by Alembic.
revision = '2793f8d2e33e'
down_revision = ('50caf9dd4cd6', '2a66d798c55d')

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
