"""4.2.0 merge

Revision ID: 15fb49b9cb37
Revises: ('4ab29f6cdd50', '2e4c3172fc54')
Create Date: 2018-06-13 12:13:49.353601

"""

# revision identifiers, used by Alembic.
revision = '15fb49b9cb37'
down_revision = ('4ab29f6cdd50', '2e4c3172fc54')

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
