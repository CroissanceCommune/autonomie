"""4.2.0 Alembic merge

Following rebase of master into jd-workshops

Revision ID: d777c5e2750
Revises: ('118382521263', '2ab20c4414aa')
Create Date: 2018-11-09 11:36:05.772943

"""

# revision identifiers, used by Alembic.
revision = 'd777c5e2750'
down_revision = ('4a7a603b00f7', '2ab20c4414aa')

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
