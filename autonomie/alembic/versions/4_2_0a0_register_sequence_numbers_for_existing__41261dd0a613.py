"""register sequence numbers for existing invoices

Revision ID: 41261dd0a613
Revises: 1e1a970ad004
Create Date: 2018-06-13 13:55:52.816292

"""

# revision identifiers, used by Alembic.
revision = '41261dd0a613'
down_revision = '1e1a970ad004'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    pass

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()
    # Fill SequenceNumber for existing invoices
    op.execute("""
    INSERT INTO task_sequence_number (`task`, `index`, `sequence`)
      SELECT task.id, official_number, 'invoice_year' from task
        LEFT JOIN invoice on task.id = invoice.id
        LEFT JOIN cancelinvoice on cancelinvoice.id = task.id
        WHERE task.official_number IS NOT NULL
    ;""")


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
