#-*-coding:utf-8-*-
"""Migration des statuts des documents vers le nouveau workflow

Revision ID: 14b76f64614c
Revises: 3f52b6b0ed7c
Create Date: 2012-08-31 15:09:19.368084

"""

# revision identifiers, used by Alembic.
revision = '14b76f64614c'
down_revision = '3f52b6b0ed7c'

from alembic import op
from autonomie.models import DBSESSION
from autonomie.models import model
from autonomie.models.task import Payment


def upgrade():
    sess = DBSESSION()
    for i in sess.query(model.Invoice)\
            .filter(model.Invoice.CAEStatus=='paid').all():
        # On ajoute une entrée de paiement pour chaque factures existantes
        amount = i.total()
        mode = i.paymentMode
        date = i.statusDate
        payment = Payment(mode=mode, amount=amount, date=date, IDTask=i.id)
        sess.merge(payment)
    # Using direct sql allows to enforce CAEStatus modifications
    # Ref #573
    # Ref #551
    op.execute("""
update coop_task as t join coop_invoice as inv on t.IDTask=inv.IDTask set CAEStatus='resulted' WHERE t.CAEStatus='paid';
update coop_task set CAEStatus='resulted' where CAEStatus='gencinv';
update coop_task set CAEStatus='valid' where CAEStatus='sent' OR CAEStatus='recinv';
update coop_task as t join coop_cancel_invoice as est on t.IDTask=est.IDTask SET t.CAEStatus='valid' WHERE t.CAEStatus='paid';
""")

def downgrade():
    pass
