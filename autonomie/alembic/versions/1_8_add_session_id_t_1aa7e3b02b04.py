"""1.8 : add session id to user, initialize to expenses, drop comments from expensesheets

Revision ID: 1aa7e3b02b04
Revises: 2b29f533fdfc
Create Date: 2013-11-06 17:00:23.318821

"""

# revision identifiers, used by Alembic.
revision = '1aa7e3b02b04'
down_revision = '2b29f533fdfc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    col = sa.Column('session_id',
            sa.String(256),
            default=None)
    op.add_column("accounts", col)

    col = sa.Column("initialize", sa.Boolean, default=False)
    op.add_column("expensetel_type", col)
    op.drop_column("expense_sheet", "comments")

def downgrade():
    op.drop_column("accounts", "session_id")
    op.drop_column("expensetel_type", "initialize")
    col = sa.Column("comments", sa.Text)
    op.add_column("expense_sheet", col)
