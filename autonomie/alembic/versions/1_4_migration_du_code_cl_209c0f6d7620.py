"""1.4 : Migration du code client

Revision ID: 209c0f6d7620
Revises: 14b76f64614c
Create Date: 2012-09-04 14:51:43.270844

Add an id column to the coop_customer table and migrate :
- projects-client relationships to this new id
- manual invoice to client relationships to this new id

"""

# revision identifiers, used by Alembic.
revision = '209c0f6d7620'
down_revision = '14b76f64614c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""
alter table coop_customer drop primary key;
""")
    op.execute("""
alter table coop_customer add column id int(11) auto_increment not null FIRST, add primary key(id);
""")
    op.execute("""
update coop_project as p join coop_customer as c on p.customerCode=c.code set p.customerCode=c.id;
""")
    op.execute("""
alter table coop_project change customerCode client_id int(11) default null;
""")
    op.execute("""
update symf_facture_manuelle as s join coop_customer as c on s.client_id=c.code set s.client_id=c.id;
""")
    op.execute("""
alter table symf_facture_manuelle change client_id client_id int(11) default null;
""")


def downgrade():
    pass
