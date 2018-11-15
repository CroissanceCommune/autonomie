"""4.2.0 Alembic merge

(suite rebase jd-workshops sur master)

Revision ID: 1729bb7ed957
Revises: ('3885e8260693', '30fe999bc58e')
Create Date: 2018-11-02 09:33:32.730752

"""

# revision identifiers, used by Alembic.
revision = '1729bb7ed957'
down_revision = ('3885e8260693', '2ed5c14be058')

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
