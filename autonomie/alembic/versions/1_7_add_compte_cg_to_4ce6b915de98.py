"""1.7 : Add compte_cg to tva

Revision ID: 4ce6b915de98
Revises: 29299007fe7d
Create Date: 2013-06-18 16:20:25.690811

"""

# revision identifiers, used by Alembic.
revision = '4ce6b915de98'
down_revision = '29299007fe7d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("tva", sa.Column("compte_cg", sa.String(125), default=""))


def downgrade():
    op.drop_column("tva", "compte_cg")
