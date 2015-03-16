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
from sqlalchemy.orm import undefer_group


def upgrade():
    # Ajout et modification de la structure de données existantes
    op.execute("alter table project modify archived BOOLEAN;")


    for name in ('ht', 'tva', 'ttc'):
        col = sa.Column(name, sa.Integer, default=0)
        op.add_column('task', col)

    for col in (
        sa.Column("project_id", sa.Integer, sa.ForeignKey('project.id')),
        sa.Column("customer_id", sa.Integer, sa.ForeignKey('customer.id')),
        sa.Column("_number", sa.String(10)),
        sa.Column("sequence_number", sa.Integer),
        sa.Column("display_units", sa.Integer, default=0),
        sa.Column('expenses', sa.Integer, default=0),
        sa.Column('expenses_ht', sa.Integer, default=0),
        sa.Column('address', sa.Text, default=""),
        sa.Column('payment_conditions', sa.Text, default=""),
        sa.Column("official_number", sa.Integer, default=None),
    ):
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
    # Migration des customer_id et project_id au niveau de la table Task
    index = 0

    for type_ in "invoice", "cancelinvoice", "estimation":
        conditions = "paymentConditions"
        if type_ == "cancelinvoice":
            conditions = "reimbursementConditions"

        request = "select id, customer_id, project_id, number, \
sequenceNumber, displayedUnits, expenses, expenses_ht, address, %s \
from %s;" % (conditions, type_)
        result = conn.execute(request)

        for index, (id, c_id, p_id, number, seq_number, display, expenses,
                    expenses_ht, address, conditions) in enumerate(result):

            request = sa.text(u"update task set \
project_id=:p_id, \
customer_id=:c_id, \
_number=:number, \
sequence_number=:seq_number, \
display_units=:display, \
expenses=:expenses, \
expenses_ht=:expenses_ht, \
address=:address, \
payment_conditions=:conditions \
where id=:id;"
                             )

            conn.execute(
                request,
                p_id=p_id,
                c_id=c_id,
                number=number,
                seq_number=seq_number,
                display=display,
                expenses=expenses,
                expenses_ht=expenses_ht,
                address=address,
                conditions=conditions,
                id=id,
            )
            if index % 50 == 0:
                session.flush()

    for type_ in ('invoice', 'cancelinvoice'):
        request = "select id, officialNumber from %s" % (type_,)
        result = conn.execute(request)

        for index, (id, official_number) in enumerate(result):
            request = sa.text(u"update task set \
official_number=:official_number \
where id=:id;"
                             )
            conn.execute(
                request,
                official_number=official_number,
                id=id,
            )
            if index % 50 == 0:
                session.flush()

    for factory in (Invoice, CancelInvoice, Estimation,):
        for document in factory.query().options(undefer_group('edit')):
            document.ttc = document.total()
            document.ht = document.total_ht()
            document.tva = document.tva_amount()
            session.merge(document)
            index += 1
        if index % 50 == 0:
            session.flush()

    # Drop old constraints
    for table in ('estimation', 'invoice', 'cancelinvoice'):
        for num in [2,3,4]:
            key = "%s_ibfk_%s" % (table, num,)
            cmd = "ALTER TABLE %s DROP FOREIGN KEY %s;" % (table, key)
            try:
                print(cmd)
                conn.execute(cmd)
            except:
                print("Error while droping a foreignkey : %s %s" % (table, key))

        for column in ('customer_id', 'project_id', 'number', \
                       'sequenceNumber', 'displayedUnits', 'expenses', \
                       'expenses_ht', 'address'):
            op.drop_column(table, column)

    op.drop_column('cancelinvoice', 'reimbursementConditions')
    op.drop_column('estimation', 'paymentConditions')
    op.drop_column('invoice', 'paymentConditions')

    for table in ('invoice', 'cancelinvoice'):
        op.drop_column(table, 'officialNumber')



def downgrade():
    op.execute("alter table project modify archived VARCHAR(255);")

    for name in ('ht', 'tva', 'ttc'):
        op.drop_column('task', name)
