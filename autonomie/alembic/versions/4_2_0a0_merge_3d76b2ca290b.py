"""empty message

Revision ID: 3d76b2ca290b
Revises: ('14d7548ec2ce', '18b00b9e3b46')
Create Date: 2018-06-25 15:42:40.769490

"""

# revision identifiers, used by Alembic.
revision = '3d76b2ca290b'
down_revision = ('14d7548ec2ce', '18b00b9e3b46')

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
