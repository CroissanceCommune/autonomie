"""1.1 : Adding id to status table and adding project status

Revision ID: 3ffdda6a6fe6
Revises: 432d76e49a9c
Create Date: 2012-08-28 23:25:12.403240

"""

# revision identifiers, used by Alembic.
revision = '3ffdda6a6fe6'
down_revision = "432d76e49a9c"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""
alter table coop_task_status DROP INDEX statusCode;
""")
    op.execute("""
alter table coop_task_status DROP INDEX IDTask;
""")
    op.execute("""
alter table coop_task_status add column id int(11) primary key auto_increment not null;
            """)
    op.alter_column('coop_project', 'status', type_=sa.String(20),
                                        nullable=False, server_default="")


def downgrade():
    pass
