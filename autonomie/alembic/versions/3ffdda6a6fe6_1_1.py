"""1.1

Revision ID: 3ffdda6a6fe6
Revises: 432d76e49a9c
Create Date: 2012-08-28 23:25:12.403240

"""

# revision identifiers, used by Alembic.
revision = '3ffdda6a6fe6'
down_revision = '432d76e49a9c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('coop_task_status',
                    sa.Column('id', sa.Integer, autoincrement=True,
                                                        unique=True))
    op.alter_column('coop_project', sa.Column('status', sa.String(20),
                                        nullable=False, default=""))


def downgrade():
    pass
