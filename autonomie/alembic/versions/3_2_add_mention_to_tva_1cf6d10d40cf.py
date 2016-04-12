"""3.2 : Add mention to tva

Revision ID: 1cf6d10d40cf
Revises: 3c1321f40c0c
Create Date: 2016-04-12 15:26:57.422710

"""

# revision identifiers, used by Alembic.
revision = '1cf6d10d40cf'
down_revision = '3c1321f40c0c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('tva', sa.Column('mention', sa.Text(), default=''))


def downgrade():
    op.drop_column('tva', 'mention')
