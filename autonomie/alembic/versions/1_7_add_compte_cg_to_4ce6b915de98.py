"""1.7 : Add Treasury accounts attributes

Revision ID: 4ce6b915de98
Revises: 29299007fe7d
Create Date: 2013-06-18 16:20:25.690811

"""

# revision identifiers, used by Alembic.
revision = '4ce6b915de98'
down_revision = '29299007fe7d'

import logging
from alembic import op
import sqlalchemy as sa
from autonomie.models import DBSESSION
from autonomie.models.task import Invoice


def upgrade():
    logger = logging.getLogger("alembic.add_compte_cg")
    op.add_column("tva", sa.Column("compte_cg", sa.String(125), default=""))
    op.add_column("company", sa.Column("compte_cg_banque", sa.String(125),
        default=""))
    op.add_column("company", sa.Column("contribution", sa.Integer))
    op.add_column("customer",
            sa.Column("compte_cg", sa.String(125), default=""))
    op.add_column("customer",
            sa.Column("compte_tiers", sa.String(125), default=""))
    # Ajout du code produit au ligne des factures
    op.add_column("invoice_line",
            sa.Column("product_id", sa.Integer, default=""))
    # Ajout d'un tag "exporte" aux factures
    op.add_column("invoice",
            sa.Column("exported",
                sa.Boolean()))
    # Les factures deja validees sont considerees comme exportees
    logger.warn(u"On tag des factures comme exportees")
    for invoice in Invoice.query():
        if invoice.has_been_validated():
            invoice.exported = True
            DBSESSION().merge(invoice)
            logger.warn(u"officialNumber : {0.officialNumber} \
{0.financial_year}".format(invoice))



def downgrade():
    op.drop_column("tva", "compte_cg")
    op.drop_column("company", "compte_cg_banque")
    op.drop_column("company", "contribution")
    op.drop_column("customer", "compte_cg")
    op.drop_column("customer", "compte_tiers")
    op.drop_column("invoice_line", "product_id")
    op.drop_column("invoice", "exported")
