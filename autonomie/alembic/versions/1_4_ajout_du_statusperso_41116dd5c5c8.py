"""1.4 : Ajout du statusPerson dans task_status

Revision ID: 41116dd5c5c8
Revises: 1dce987687aa
Create Date: 2012-09-22 00:09:52.242524

"""

# revision identifiers, used by Alembic.
revision = '41116dd5c5c8'
down_revision = '1dce987687aa'

from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import column_exists


def upgrade():
    if not column_exists('task_status', 'statusPerson'):
        op.execute("""
alter table task_status add column statusPerson INT(11)
""")

def downgrade():
    pass
