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

def make_expense_nodes(conn, session):
    from autonomie.models.node import Node
    req = "select max(id) from node"
    result = conn.execute(req).fetchall()
    max_id = result[0][0]
    print("The new max_id is : %s" % max_id)

    request = "select id, month, year from expense_sheet"
    result = conn.execute(request)

    op.execute("SET FOREIGN_KEY_CHECKS=0;")

    from autonomie.models.treasury import get_expense_sheet_name

    for index, (id, month,year) in enumerate(result):
        max_id += 1
        new_id = max_id
        name = get_expense_sheet_name(month, year)
        node = Node(
            id=new_id,
            name=name,
            type_='expensesheet',
        )
        session.add(node)
        # Update relationships
        for key, table in ("sheet_id", "baseexpense_line"), ("expense_sheet_id", "communication"):
            op.execute("update {0} set {2}={1} where {2}={3}".format(table, new_id, key, id))
        op.execute("update expense_sheet set id={0} where id={1}".format(new_id, id))
        if index % 50 == 0:
            session.flush()
    op.execute("SET FOREIGN_KEY_CHECKS=1;")


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

    col = sa.Column("sortie_type_id", sa.Integer, sa.ForeignKey('type_sortie_option.id'))
    op.add_column("user_datas", col)
    op.execute("alter table user_datas modify parcours_num_hours float DEFAULT NULL")
    op.execute("alter table external_activity_datas modify hours float DEFAULT NULL")
    op.execute("alter table external_activity_datas modify brut_salary float DEFAULT NULL")

    col = sa.Column("cgv", sa.Text, default="")
    op.add_column("company", col)

    col = sa.Column('_acl', sa.Text)
    op.add_column("job", col)


    # Migration des donnees vers la nouvelle structure
    from alembic.context import get_bind
    conn = get_bind()
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()

    # Expenses will be nodes
    make_expense_nodes(conn, session)

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
