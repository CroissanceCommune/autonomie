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

def downgrade():
    for table in ("estimation", "invoice", "cancelinvoice"):
        op.drop_column(table, "address")
