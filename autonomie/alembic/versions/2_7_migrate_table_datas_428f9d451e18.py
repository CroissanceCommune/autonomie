"""2.7 : migrate table datas

Revision ID: 428f9d451e18
Revises: 1b94920692a3
Create Date: 2015-03-05 17:42:12.124252

"""

# revision identifiers, used by Alembic.
revision = '428f9d451e18'
down_revision = '1b94920692a3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("alter table project modify archived BOOLEAN;")

    for name in ('ht', 'tva', 'ttc'):
        col = sa.Column(name, sa.Integer, default=0)
        op.add_column('task', col)

    from autonomie.models.base import DBSESSION
    session = DBSESSION()

    from autonomie.models.task import (
        Invoice,
        CancelInvoice,
        Estimation,
    )
    index = 0
    for factory in (Invoice, CancelInvoice, Estimation,):
        for document in factory.query().all():
            document.ttc = document.total()
            document.ht = document.total_ht()
            document.tva = document.tva_amount()
            session.merge(document)
            index += 1
        if index % 50 == 0:
            session.flush()


def downgrade():
    op.execute("alter table project modify archived VARCHAR(255);")

    for name in ('ht', 'tva', 'ttc'):
        op.drop_column('task', name)
