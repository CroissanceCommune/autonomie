#-*-coding:utf-8-*-
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
    # Ajout et modification de la structure de données existantes
    op.execute("alter table project modify archived BOOLEAN;")

    for name in ('ht', 'tva', 'ttc'):
        col = sa.Column(name, sa.Integer, default=0)
        op.add_column('task', col)
    col = sa.Column("project_id", sa.Integer, sa.ForeignKey('project.id'))
    op.add_column("task", col)
    col = sa.Column("customer_id", sa.Integer, sa.ForeignKey('customer.id'))
    op.add_column("task", col)
    col = sa.Column("_number", sa.String(10))
    op.add_column("task", col)
    col = sa.Column("sequence_number", sa.Integer)
    op.add_column("task", col)

    col = sa.Column("display_units", sa.Integer, default=0)
    op.add_column("task", col)


    # Migration des donnees vers la nouvelle structure
    from alembic.context import get_bind
    conn = get_bind()

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

    # Migration des customer_id et project_id au niveau de la table Task

    for type_ in "invoice", "cancelinvoice", "estimation":
        request = "select id, customer_id, project_id, number, sequenceNumber, displayedUnits from %s;" % type_
        result = conn.execute(request)

        for index, (id, c_id, p_id, number, seq_number, display) in enumerate(result):
            request = "update task set project_id=%s, customer_id=%s, _number=%s, sequence_number=%s, display_units=%s where id=%s;" % (p_id, c_id, number, seq_number, display, id,)
            op.execute(request)
            if index % 50 == 0:
                session.flush()


def downgrade():
    op.execute("alter table project modify archived VARCHAR(255);")

    for name in ('ht', 'tva', 'ttc'):
        op.drop_column('task', name)
