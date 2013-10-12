"""1.5 Documents : Address field and client reference

Revision ID: 23fd141c9484
Revises: 2a7a5275c441
Create Date: 2012-12-18 13:39:38.807213

"""

# revision identifiers, used by Alembic.
revision = '23fd141c9484'
down_revision = '2a7a5275c441'

from alembic import op
import sqlalchemy as sa
from autonomie.models import DBSESSION
from autonomie.models.task import Invoice, CancelInvoice, Estimation


def upgrade():
    from autonomie.models.client import Client
    for table in ("estimation", "invoice", "cancelinvoice"):
        op.add_column(table, sa.Column("address", sa.Text, default=""))
        op.add_column(table,
                sa.Column("client_id",
                          sa.Integer,
                          sa.ForeignKey("customer.id")))

    for obj in (Invoice, CancelInvoice, Estimation):
        for doc in obj.query():
            if doc.project is not None and doc.project.client_id is not None:
                client = Client.get(doc.project.client_id)
                if client is not None:
                    doc.address = client.full_address
                    doc.client_id = client.id
            if len(doc._number) > 10:
                doc._number = doc._number[10:]
            DBSESSION.merge(doc)


def downgrade():
    for table in ("estimation", "invoice", "cancelinvoice"):
        op.drop_column(table, "address")
        op.drop_column(table, "client_id")

    for obj in (Invoice, CancelInvoice, Estimation):
        for doc in obj.query():
            if doc.project is not None and doc.client is not None:
                doc._number = "%s_%s_%s" % (doc.project.code, doc.client.code, doc._number)
                DBSESSION().merge(doc)


