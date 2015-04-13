"""2.7.1 : add_columns

Revision ID: 36b1d9c38c43
Revises: 577f50e908d1
Create Date: 2015-04-09 16:52:36.065153

"""

# revision identifiers, used by Alembic.
revision = '36b1d9c38c43'
down_revision = '577f50e908d1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    col = sa.Column('activity_id', sa.Integer(), sa.ForeignKey('company_activity.id'))
    op.add_column('company_datas', col)
    col = sa.Column('archived', sa.Boolean(), default=False, server_default="0")
    op.add_column('customer', col)

    # Migration de accompagnement_header.png en activity_header.png
    op.execute('update config_files set key="activity_header_img.png" where \
key="accompagnement_header.png";')


def downgrade():
    op.drop_column('customer', 'archived')
