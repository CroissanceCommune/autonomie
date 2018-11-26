"""4.2.0 Revision merge

Revision ID: 3d5b6e485203
Revises: ('c48c967f7f7', '5362502b508c')
Create Date: 2018-11-26 09:54:25.191623

"""

# revision identifiers, used by Alembic.
revision = '3d5b6e485203'
down_revision = ('c48c967f7f7', '5362502b508c')

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
