"""4.1 : compte de resultats

Revision ID: 13a25f46e412
Revises: 4299e583631c
Create Date: 2018-01-06 12:52:36.054138

"""

# revision identifiers, used by Alembic.
revision = '13a25f46e412'
down_revision = '4299e583631c'

from alembic import op
import sqlalchemy as sa
from autonomie.alembic import utils

def update_database_structure():
    utils.add_column(
        "accounting_operation_upload", sa.Column("filetype", sa.String(50))
    )
    utils.add_column(
        "accounting_operation", sa.Column("date", sa.Date())
    )
    if utils.column_exists('accounting_operation', 'datetime'):
        op.drop_column('accounting_operation', 'datetime')


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from autonomie.models.accounting.operations import AccountingOperationUpload
    for entry in AccountingOperationUpload.query():
        entry.filetype = "analytical_balance"
        session.merge(entry)
        session.flush()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.drop_column(
        "accounting_operation_upload", "filetype"
    )
