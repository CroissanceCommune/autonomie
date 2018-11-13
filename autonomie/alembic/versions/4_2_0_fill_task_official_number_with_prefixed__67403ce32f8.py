"""4.2.0 Fill task.official_number with prefixed number

Revision ID: 67403ce32f8
Revises: 29e53cf4579a
Create Date: 2018-06-06 19:07:15.271943

"""

# revision identifiers, used by Alembic.
revision = '67403ce32f8'
down_revision = '29e53cf4579a'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    pass

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

    from autonomie.models.task import Task
    op.execute("""
    UPDATE task
      LEFT JOIN invoice on task.id = invoice.id
      LEFT JOIN cancelinvoice on cancelinvoice.id = task.id
      SET official_number = CONCAT(IFNULL(prefix, ''), official_number)
      WHERE (cancelinvoice.id IS NOT NULL) OR (invoice.id IS NOT NULL)
    ;""")

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
