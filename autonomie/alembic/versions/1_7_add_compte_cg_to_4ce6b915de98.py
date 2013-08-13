"""1.7 : Add Treasury accounts attributes

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
    op.add_column("company", sa.Column("compte_cg_banque", sa.String(125),
        default=""))
    op.add_column("company", sa.Column("contribution", sa.Integer, default=0))
    op.add_column("customer",
            sa.Column("compte_cg", sa.String(125), default=""))
    op.add_column("customer",
            sa.Column("compte_tiers", sa.String(125), default=""))
    # Ajout du code produit au ligne des differents document
    for table in ("estimation_line", "cancelinvoice_line", "invoice_line"):
        op.add_column(table,
                sa.Column("product_code", sa.String(125), default=""))


def downgrade():
    op.drop_column("tva", "compte_cg")
    op.drop_column("company", "compte_cg_banque")
    op.drop_column("company", "contribution")
    op.drop_column("customer", "compte_cg")
    op.drop_column("customer", "compte_tiers")
    for table in ("estimation_line", "cancelinvoice_line", "invoice_line"):
        op.drop_column(table, "product_code")
