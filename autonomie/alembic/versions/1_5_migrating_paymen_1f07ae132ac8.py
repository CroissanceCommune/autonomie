#-*-coding:utf-8-*-
"""1.5 : Migrating payment modes

Revision ID: 1f07ae132ac8
Revises: 1cc9ff114346
Create Date: 2012-12-31 10:22:14.636420

"""

# revision identifiers, used by Alembic.
revision = '1f07ae132ac8'
down_revision = '1cc9ff114346'

from alembic import op
import sqlalchemy as sa
from autonomie.models.task.invoice import PaymentMode, Payment
from autonomie_base.models.base import DBSESSION


def upgrade():
    for payment in Payment.query():
        if payment.mode in (u"cheque", u"CHEQUE"):
            payment.mode = u"par chèque"
        elif payment.mode in (u"virement", u"VIREMENT"):
            payment.mode = u"par virement"
        elif payment.mode in (u"liquide", u"LIQUIDE"):
            payment.mode = u"en liquide"
        else:
            payment.mode = "mode de paiement inconnu"
        DBSESSION().merge(payment)

    for mode in (u"par chèque", u"par virement", u"en liquide"):
        pmode = PaymentMode(label=mode)
        DBSESSION().add(pmode)


def downgrade():
    for p in PaymentMode.query():
        DBSESSION().delete(p)
    for p in Payment.query():
        if p.mode == u"par chèque":
            p.mode = u"cheque"
        elif p.mode == u"par virement":
            p.mode = u"virement"
        elif p.mode == u"en liquide":
            p.mode = u"liquide"
        else:
            p.mode = "inconnu"
        DBSESSION().merge(p)
