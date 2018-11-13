"""4.2.0 Update civility value from mr&mme to M. et Mme

Revision ID: 4a7a603b00f7
Revises: 3885e8260693
Create Date: 2018-11-10 17:00:58.886950

"""

# revision identifiers, used by Alembic.
revision = '4a7a603b00f7'
down_revision = '118382521263'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    pass

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()
    op.execute('update customer set civilite="M. et Mme" where civilite="mr&mme"')
    from zope.sqlalchemy import mark_changed
    mark_changed(session)

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
