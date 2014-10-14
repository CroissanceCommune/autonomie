"""2.3.1 : 2.3.1 header and logo in db

Revision ID: 40c1f95213d0
Revises: 42c3d2634645
Create Date: 2014-10-13 10:45:40.840370

"""

# revision identifiers, used by Alembic.
revision = '40c1f95213d0'
down_revision = '42c3d2634645'

from alembic import op
import sqlalchemy as sa


def upgrade():
    for i in ('header_id', 'logo_id',):
        col = sa.Column(i, sa.Integer, sa.ForeignKey('file.id'))
        op.add_column('company', col)


def downgrade():
    op.drop_column('company', sa.Column('logo_id'))
    op.drop_column('company', sa.Column('header_id'))
