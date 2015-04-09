"""2.7 : add round_floor

Revision ID: 577f50e908d1
Revises: 428f9d451e18
Create Date: 2015-04-09 13:03:42.805671

"""

# revision identifiers, used by Alembic.
revision = '577f50e908d1'
down_revision = '428f9d451e18'

from alembic import op
import sqlalchemy as sa


def upgrade():
    col = sa.Column('round_floor', sa.Boolean(), default=False)
    op.add_column('task', col)


def downgrade():
    pass
