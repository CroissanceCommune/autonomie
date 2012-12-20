"""1.5 Client : multiline adress field

Revision ID: 70853b55768c
Revises: 23fd141c9484
Create Date: 2012-12-18 17:41:23.534086

"""

# revision identifiers, used by Alembic.
revision = '70853b55768c'
down_revision = '23fd141c9484'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column("customer", "address", type_=sa.Text)


def downgrade():
    op.alter_column("customer", "address", type_=sa.String(255))
