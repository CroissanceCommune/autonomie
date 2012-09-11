"""1.4 : taux de tva par ligne

Revision ID: 1987a6d83e5f
Revises: 1e7d7781a47b
Create Date: 2012-09-09 11:27:01.652369

"""

# revision identifiers, used by Alembic.
revision = '1987a6d83e5f'
down_revision = '1e7d7781a47b'

from alembic import op
import sqlalchemy as sa
from autonomie.models import DBSESSION
from autonomie.models.task.estimation import Estimation, EstimationLine
from autonomie.models.task.invoice import Invoice, InvoiceLine


def upgrade():
    # Devis
    op.add_column("estimation_line", "tva", sa.Integer, server_default=0)
    # Adding tva to the lines
    op.execute("""
    update estimation_line as l join estimation as e on e.id=l.task_id set l.tva=e.tva;
    """)
    # Moving dicounts to a discount table
    for est in Estimation.query().all():
        discount = est.discountHT
        tva = est.tva
        id_ = est.id
        op.execute("""
insert discount (description, amount, tva, task_id) values ("Remise", '%s', '%s', '%s')
    """% (discount, tva, id_))
    # Factures
    op.add_column("invoice_line", "tva", sa.Integer, server_default=0)
    # Adding tva to the lines
    op.execute("""
    update invoice_line as l join invoice as i on i.id=l.task_id set l.tva=e.tva;
    """)
    # Moving discounts to discount table
    for inv in Invoice.query().all():
        discount = inv.discountHT
        tva = inv.tva
        id_ = inv.id
        op.execute("""
insert discount (description, amount, tva, task_id) values ("Remise", '%s', '%s', '%s')
    """% (discount, tva, id_))
    # Avoirs
    op.execute("""
    update cancelinvoice_line as l join cancelinvoice as i on i.id=l.task_id set l.tva=e.tva;
    """)

def downgrade():
    pass
