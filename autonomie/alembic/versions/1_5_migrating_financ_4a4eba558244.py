"""1.5 : Migrating financial year

Revision ID: 4a4eba558244
Revises: 362fc5306d54
Create Date: 2013-01-23 10:43:59.972288

"""

# revision identifiers, used by Alembic.
revision = '4a4eba558244'
down_revision = '362fc5306d54'

from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import column_exists

def upgrade():
    from autonomie.models.task import Invoice, CancelInvoice, ManualInvoice
    from autonomie_base.models.base import DBSESSION
    for table in "invoice", "cancelinvoice", "manualinv":
        if not column_exists(table, "financial_year"):
            op.add_column(table, sa.Column("financial_year", sa.Integer,
                                                        nullable=False))
    for type_ in (Invoice, CancelInvoice, ManualInvoice):
        for document in type_.query():
            document.financial_year = document.taskDate.year
            DBSESSION.merge(document)


def downgrade():
    for table in "invoice", "cancelinvoice", "manualinv":
        op.drop_column(table, "financial_year")
