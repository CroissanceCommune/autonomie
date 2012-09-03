"""Migration des factures 'paid' vers le nouveau format

Revision ID: 14b76f64614c
Revises: 3f52b6b0ed7c
Create Date: 2012-08-31 15:09:19.368084

"""

# revision identifiers, used by Alembic.
revision = '14b76f64614c'
down_revision = '3f52b6b0ed7c'

from alembic import op
import sqlalchemy as sa
from autonomie.models import DBSESSION
from autonomie.models import model
from autonomie.models.task import Payment


def upgrade():
    sess = DBSESSION()
    for i in sess.query(model.Invoice)\
            .filter(model.Invoice.CAEStatus=='paid').all():
        amount = i.total()
        mode = i.paymentMode
        date = i.statusDate
        payment = Payment(mode=mode, amount=amount, date=date)
        i.payments.append(payment)
        i.CAEStatus = 'resulted'
        sess.merge(i)
    # We ensure all cancel invoice have a correct status
    for i in sess.query(model.CancelInvoice)\
        .filter(model.CancelInvoice.CAEStatus.in_(('paid', 'sent', 'recinv'))):
        i.CAEStatus = 'valid'
        sess.merge(i)
    sess.flush()


def downgrade():
    pass
