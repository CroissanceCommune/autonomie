"""1.0

Revision ID: 432d76e49a9c
Revises: None
Create Date: 2012-08-28 23:24:03.771898

"""

# revision identifiers, used by Alembic.
revision = '432d76e49a9c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'coop_tva',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column("name", sa.String(8), nullable=False),
            sa.Column("value", sa.Integer),
            __table_args__={'mysql_engine': 'MyISAM', "mysql_charset":'utf8'})


def downgrade():
    # This one should not fail
    pass
