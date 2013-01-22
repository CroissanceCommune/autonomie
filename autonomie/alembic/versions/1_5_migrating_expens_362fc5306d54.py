"""1.5 : Migrating expenses

Revision ID: 362fc5306d54
Revises: 1212f113f03b
Create Date: 2013-01-22 17:44:54.317539

"""

# revision identifiers, used by Alembic.
revision = '362fc5306d54'
down_revision = '1212f113f03b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    for table in "invoice", "estimation", "cancelinvoice":
        op.add_column(table, sa.Column("expenses_ht", sa.Integer, default=0))


def downgrade():
    op.drop_column("invoice", "expenses_ht")
