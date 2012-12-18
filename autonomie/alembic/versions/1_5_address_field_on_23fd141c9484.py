"""1.5 : Address field on documents

Revision ID: 23fd141c9484
Revises: 2a7a5275c441
Create Date: 2012-12-18 13:39:38.807213

"""

# revision identifiers, used by Alembic.
revision = '23fd141c9484'
down_revision = '2a7a5275c441'

from alembic import op
import sqlalchemy as sa


def upgrade():
    for table in ("estimation", "invoice", "cancelinvoice"):
        op.add_column(table, sa.Column("address", sa.Text, default=""))

    from autonomie.models import DBSESSION
    from autonomie.models.task import Invoice, CancelInvoice, Estimation
    for obj in (Invoice, CancelInvoice, Estimation):
        for doc in obj.query():
            if doc.project is not None and doc.project.client is not None:
                doc.address = doc.project.client.full_address
                DBSESSION.merge(doc)



def downgrade():
    for table in ("estimation", "invoice", "cancelinvoice"):
        op.drop_column(table, "address")


