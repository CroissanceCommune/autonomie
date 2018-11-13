"""4.2.0 Rename Payment.remittance_amount -> Payment.bank_remittance_id

Revision ID: 50caf9dd4cd6
Revises: 4f8d19c47c76
Create Date: 2018-06-29 19:16:41.424052

"""

# revision identifiers, used by Alembic.
revision = '50caf9dd4cd6'
down_revision = '4f8d19c47c76'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from autonomie.alembic.utils import rename_column


def update_database_structure():
    rename_column(
        'payment',
        'remittance_amount',
        'bank_remittance_id',
        type_=mysql.VARCHAR(length=255),
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
        rename_column(
        'payment',
        'bank_remittance_id',
        'remittance_amount',
        type_=mysql.VARCHAR(length=255),
    )
