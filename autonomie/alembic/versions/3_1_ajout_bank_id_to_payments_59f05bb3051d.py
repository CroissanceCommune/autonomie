"""3.1 : Ajout bank_id to payments

Revision ID: 59f05bb3051d
Revises: 54de05a93319
Create Date: 2015-08-19 13:09:12.384701

"""

# revision identifiers, used by Alembic.
revision = '59f05bb3051d'
down_revision = '2192101f133b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('payment', sa.Column('bank_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('payment', 'bank_id')
