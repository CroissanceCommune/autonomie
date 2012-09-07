"""1.4 : Adding polymorphic identity to documents

Revision ID: 3f52b6b0ed7c
Revises: 2cc9251fb0bb
Create Date: 2012-08-29 15:30:31.817382

"""

# revision identifiers, used by Alembic.
revision = '3f52b6b0ed7c'
down_revision = '2cc9251fb0bb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""
alter table coop_task add column type_ VARCHAR(30) NOT NULL;
update coop_task as t join coop_estimation as e on t.IDTask=e.IDTask set type_='estimation';
update coop_task as t join coop_invoice as i on t.IDTask=i.IDTask set type_='invoice';
update coop_task as t join coop_cancelinvoice as c on t.IDTask=c.IDTask set type_='cancelinvoice';
update coop_task set type_='task' where type_='';
""")


def downgrade():
    pass
