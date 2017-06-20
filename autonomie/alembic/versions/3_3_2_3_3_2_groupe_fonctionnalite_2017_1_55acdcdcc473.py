"""3.3.2 : 3.3.2 groupe fonctionnalite 2017 1

Revision ID: 55acdcdcc473
Revises: 11219b4e619b
Create Date: 2017-06-20 13:21:41.795144

"""

# revision identifiers, used by Alembic.
revision = '55acdcdcc473'
down_revision = '11219b4e619b'

from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import rename_column


def update_database_structure():
    op.add_column(
        'customer',
        sa.Column('civilite', sa.String(10), default=''),
    )
    op.add_column(
        'customer',
        sa.Column('mobile', sa.String(20), default=''),
    )
    rename_column(
        "customer",
        'contactLastName',
        'lastname',
        sa.String(255)
    )
    rename_column(
        "customer",
        'contactFirstName',
        'firstname',
        sa.String(255)
    )
    rename_column(
        "customer",
        'intraTVA',
        'tva_intracomm',
        sa.String(50)
    )


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
