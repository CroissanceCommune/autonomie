"""empty message

Revision ID: 21136a900c10
Revises: ('4f011ed2a459', '5280341abe1a')
Create Date: 2018-10-26 09:47:25.503072

"""

# revision identifiers, used by Alembic.
revision = '21136a900c10'
down_revision = ('4f011ed2a459', '5280341abe1a')

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
