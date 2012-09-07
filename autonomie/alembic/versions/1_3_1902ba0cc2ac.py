"""1.3 : Ajout du code compta pour les comptes entrepreneurs

Revision ID: 1902ba0cc2ac
Revises: 1f548f8115e8
Create Date: 2012-08-28 23:34:15.096157

"""

# revision identifiers, used by Alembic.
revision = '1902ba0cc2ac'
down_revision = '1f548f8115e8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("egw_accounts", sa.Column("code_compta", sa.String(30),
                                        default=0))


def downgrade():
    pass
