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
from autonomie.models.task import Invoice, CancelInvoice
from autonomie.models import DBSESSION

def upgrade():
    for table in "invoice", "cancelinvoice":
        op.add_column(table, sa.Column("financial_year", sa.Integer,
            nullable=False))
    for invoice in Invoice.query():
        invoice.financial_year = invoice.taskDate.year
        DBSESSION.merge(invoice)
    for cancelinvoice in CancelInvoice.query():
        cancelinvoice.financial_year = cancelinvoice.taskDate.year
        DBSESSION.merge(cancelinvoice)


def downgrade():
    for table in "invoice", "cancelinvoice":
        op.drop_column(table, "financial_year")
