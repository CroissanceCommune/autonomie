"""3.2 : add workplace field

Revision ID: 37a35699b280
Revises: 1cf6d10d40cf
Create Date: 2016-04-13 08:12:36.522976

"""

# revision identifiers, used by Alembic.
revision = '37a35699b280'
down_revision = '1cf6d10d40cf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('task', sa.Column('workplace', sa.Text, default=''))


def downgrade():
    pass
