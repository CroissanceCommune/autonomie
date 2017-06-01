"""3.2.1 : fix payment 3

Revision ID: 18504ec02955
Revises: 658e0f23ee2
Create Date: 2016-04-26 18:35:37.775710

"""

# revision identifiers, used by Alembic.
revision = '18504ec02955'
down_revision = '658e0f23ee2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from sqlalchemy import Date, cast
    from datetime import date
    from autonomie.models.task.invoice import Payment
    from autonomie_base.models.base import DBSESSION as db

    for payment in db().query(Payment).filter(cast(Payment.created_at, Date) == date.today()):
        try:
            payment.remittance_amount = float(payment.remittance_amount) / 100000.0
            db().merge(payment)
        except:
            print(u"Erreur payment : %s (%s)" % (payment.id, payment.remittance_amount))

    from zope.sqlalchemy import mark_changed
    mark_changed(db())


def downgrade():
    pass
