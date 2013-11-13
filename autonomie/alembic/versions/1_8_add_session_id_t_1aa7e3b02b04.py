"""1.8 : Add session id to user

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

def downgrade():
    op.drop_column("accounts", "session_id")
    op.drop_column("expensetel_type", "initialize")
