#-*-coding:utf-8-*-
"""1.4 : Migration des statuts des documents vers le nouveau workflow

Revision ID: 14b76f64614c
Revises: 3f52b6b0ed7c
Create Date: 2012-08-31 15:09:19.368084

"""

# revision identifiers, used by Alembic.
revision = '14b76f64614c'
down_revision = '3f52b6b0ed7c'

import datetime
from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import table_exists

def get_ht(lines, discountHT):
    ht = 0
    for line in lines:
        cost, quantity = line
        ht += float(cost) * float(quantity)
    ht -= discountHT
    return ht

def get_date(value):
    try:
        return datetime.datetime.fromtimestamp(float(value))
    except:
        return datetime.datetime.now()

def upgrade():
    from autonomie.models import DBSESSION
    from autonomie.models.task import Payment
    from alembic.context import get_bind
    conn = get_bind()
    result = conn.execute("""
select invoice.IDTask, invoice.tva, invoice.discountHT, invoice.expenses, invoice.paymentMode, task.statusDate from coop_invoice as invoice join coop_task as task on task.IDTask=invoice.IDTask where task.CAEStatus='paid';
""").fetchall()
    dbsession = DBSESSION
    for i in result:
        id_, tva, discountHT, expenses, paymentMode, statusDate = i
        lines = conn.execute("""
select cost, quantity from coop_invoice_line where IDTask='%s'""" % id_).fetchall()
        totalht = get_ht(lines, discountHT)
        tva_amount = int(float(totalht) * (max(int(tva), 0) / 10000.0))
        ttc = tva_amount + totalht
        total = ttc + expenses
        date = datetime.datetime.fromtimestamp(float(statusDate))
        # Adding one payment for each invoice that has been marked as "paid"
        conn.execute("""
insert into payment (mode, amount, date, task_id) VALUE ('%s', '%s', '%s', '%s')"""%(paymentMode, total, date, id_))

    # Using direct sql allows to enforce CAEStatus modifications
    # Ref #573
    # Ref #551
    op.execute("""
update coop_task as t join coop_invoice as inv on t.IDTask=inv.IDTask set CAEStatus='resulted' WHERE t.CAEStatus='paid';
""")
    op.execute("""
update coop_task set CAEStatus='resulted' where CAEStatus='gencinv';
""")
    op.execute("""
update coop_task set CAEStatus='valid' where CAEStatus='sent' OR CAEStatus='recinv';
""")
    if table_exists("coop_cancel_invoice"):
        op.execute("""
update coop_task as t join coop_cancel_invoice as est on t.IDTask=est.IDTask SET t.CAEStatus='valid' WHERE t.CAEStatus='paid';
""")

def downgrade():
    pass
