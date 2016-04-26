"""3.2.1 : fix payment 5 number

Revision ID: 3017103d60c0
Revises: 37a35699b280
Create Date: 2016-04-26 17:07:38.330713

"""

# revision identifiers, used by Alembic.
revision = '3017103d60c0'
down_revision = '37a35699b280'

from alembic import op
import sqlalchemy as sa


def format_remittance(value):
    try:
        value = int(value) / 100.0
    except:
        value = value
    return str(value)


def upgrade():
    from autonomie.models.task import Payment
    from autonomie.models.base import DBSESSION as db

    table = Payment.__tablename__
    op.execute(
        "Alter table {table} CHANGE amount amount BIGINT(20)".format(
            table=table
        )
    )

    for entry in db().query(Payment.id, Payment.amount, Payment.remittance_amount):
        id_, amount, remittance = entry
        query = "update {table} set amount={amount}, remittance_amount={remittance} where id={id}".format(
            table=table,
            amount=amount*1000,
            remittance=format_remittance(remittance),
            id=id_,
        )
        op.execute(query)
        from zope.sqlalchemy import mark_changed
        mark_changed(db())



def downgrade():
    pass
