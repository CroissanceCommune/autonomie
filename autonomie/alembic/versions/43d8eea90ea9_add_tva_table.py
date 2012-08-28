"""add_tva_table

Revision ID: 43d8eea90ea9
Revises: None
Create Date: 2012-08-28 20:25:31.089175

"""

# revision identifiers, used by Alembic.
revision = '43d8eea90ea9'
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
    op.drop_table('coop_tva')
