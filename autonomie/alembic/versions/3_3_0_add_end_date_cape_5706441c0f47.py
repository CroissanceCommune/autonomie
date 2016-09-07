"""3.3.0 : add_end_date_cape

Revision ID: 5706441c0f47
Revises: 2b6ac7b172d3
Create Date: 2016-09-07 11:47:52.522342

"""

# revision identifiers, used by Alembic.
revision = '5706441c0f47'
down_revision = '2b6ac7b172d3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "date_convention_cape_datas",
        sa.Column('end_date', sa.Date())
    )


def downgrade():
    op.drop_column("date_convention_cape_datas", 'end_date')
