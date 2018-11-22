"""4.2.0 Make customer's datas nullable

Revision ID: c48c967f7f7
Revises: d777c5e2750
Create Date: 2018-11-20 18:26:58.418620

"""

# revision identifiers, used by Alembic.
revision = 'c48c967f7f7'
down_revision = 'd777c5e2750'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    op.alter_column(
        'customer',
        'lastname',
        nullable=True,
        existing_type=sa.String(255)
    )
    op.alter_column(
        'customer',
        'address',
        nullable=True,
        existing_type=sa.String(255)
    )
    op.alter_column(
        'customer',
        'zip_code',
        nullable=True,
        existing_type=sa.String(20)
    )
    op.alter_column(
        'customer',
        'city',
        nullable=True,
        existing_type=sa.String(255)
    )

def upgrade():
    update_database_structure()

def downgrade():
    pass
