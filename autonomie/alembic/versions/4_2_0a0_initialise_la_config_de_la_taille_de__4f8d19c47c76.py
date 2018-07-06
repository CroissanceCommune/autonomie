"""Initialise la Config de la taille de troncature des libelles comptables

Revision ID: 4f8d19c47c76
Revises: 3d76b2ca290b
Create Date: 2018-06-27 16:52:39.342455

"""

# revision identifiers, used by Alembic.
revision = '4f8d19c47c76'
down_revision = '3d76b2ca290b'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    pass

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()
    from autonomie.models.config import Config
    Config.set('accounting_label_maxlength', 35)
    session.flush()


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
