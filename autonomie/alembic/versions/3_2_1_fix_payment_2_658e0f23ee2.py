"""3.2.1 : fix_payment_2

Revision ID: 658e0f23ee2
Revises: 3017103d60c0
Create Date: 2016-04-26 18:20:10.010347

"""

# revision identifiers, used by Alembic.
revision = '658e0f23ee2'
down_revision = '3017103d60c0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from sqlalchemy import Date, cast
    from datetime import date
    from autonomie.models.task.invoice import Payment
    from autonomie.models.base import DBSESSION as db

    for payment in db().query(Payment).filter(cast(Payment.created_at, Date) == date.today):
        try:
            payment.amount = payment.amount/1000
            db().merge(payment)
        except:
            print(u"Erreur payment : %s (%s)" % payment.id, payment.amount)

    from zope.sqlalchemy import mark_changed
    mark_changed(db())


def downgrade():
    pass
