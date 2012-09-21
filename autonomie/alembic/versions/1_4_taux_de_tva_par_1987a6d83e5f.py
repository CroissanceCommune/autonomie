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
from autonomie.models.task.estimation import Estimation
from autonomie.models.task.invoice import Invoice
from autonomie.alembic.utils import add_column
from autonomie.alembic.utils import column_exists


def upgrade():
    # Devis
    op.add_column("estimation_line",
                    sa.Column("tva", sa.Integer))
    # Adding tva to the lines
    op.execute("""
    update estimation_line as l join estimation as e on e.id=l.task_id set l.tva=e.tva;
    """)
    # Moving dicounts to a discount table
    for est in Estimation.query().all():
        id_ = est.id
        op.execute("""
insert discount (description, amount, tva, task_id) select "Remise", discountHT, tva, id from estimation where estimation.id='%s' and estimation.discountHT!= 0 and estimation.discountHT is not null ;
    """% (id_))
    # Factures
    op.add_column("invoice_line",
                    sa.Column("tva", sa.Integer))
    # Adding tva to the lines
    op.execute("""
    update invoice_line as l join invoice as i on i.id=l.task_id set l.tva=i.tva;
    """)
    # Moving discounts to discount table
    for inv in Invoice.query().all():
        id_ = inv.id
        op.execute("""
insert discount (description, amount, tva, task_id) select "Remise", discountHT, tva, id from invoice where invoice.id='%s' and invoice.discountHT!= 0 and invoice.discountHT is not null ;
    """% (id_))
    # Avoirs
    add_column("cancelinvoice_line",
                    sa.Column("tva", sa.Integer))
    if column_exists("cancelinvoice", "tva"):
        # If the column exists, there may be some cancelinvoices
        op.execute("""
    update cancelinvoice_line as l join cancelinvoice as i on i.id=l.task_id set l.tva=i.tva;
    """)

def downgrade():
    pass
