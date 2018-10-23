"""ajout d'une reference aux fichiers pdf des factures

Revision ID: 5280341abe1a
Revises: 18b6a30326e2
Create Date: 2018-10-23 17:24:38.059904

"""

# revision identifiers, used by Alembic.
revision = '5280341abe1a'
down_revision = '18b6a30326e2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def update_database_structure():
    op.add_column('task', sa.Column('pdf_file_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_task_pdf_file_id'), 'task', 'file', ['pdf_file_id'], ['id'])

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.drop_constraint(op.f('fk_task_pdf_file_id'), 'task', type_='foreignkey')
    op.drop_column('task', 'pdf_file_id')
