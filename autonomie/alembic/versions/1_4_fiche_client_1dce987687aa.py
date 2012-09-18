"""1_4_fiche_client

Revision ID: 1dce987687aa
Revises: 1987a6d83e5f
Create Date: 2012-09-19 00:06:34.416770

"""

# revision identifiers, used by Alembic.
revision = '1dce987687aa'
down_revision = '1987a6d83e5f'

from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import add_column
from autonomie.alembic.utils import column_exists


def upgrade():
    if not column_exists("customer", "fax"):
        op.add_column("customer", sa.Column("fax", sa.String(50),
                                                            nullable=True))
    if not column_exists("customer", "function"):
        op.add_column("customer", sa.Column("function", sa.String(255),
                                                            nullable=True))

def downgrade():
    pass
