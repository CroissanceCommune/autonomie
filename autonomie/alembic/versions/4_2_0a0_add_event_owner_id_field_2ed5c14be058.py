"""Add Event.owner_id field

Revision ID: 2ed5c14be058
Revises: 1e4eb742df36
Create Date: 2018-07-18 19:31:04.311893

"""

# revision identifiers, used by Alembic.
revision = '2ed5c14be058'
down_revision = '1e4eb742df36'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def update_database_structure():
    op.add_column('event', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_event_owner_id'), 'event', 'accounts', ['owner_id'], ['id'])

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.drop_constraint(op.f('fk_event_owner_id'), 'event', type_='foreignkey')
    op.drop_column('event', 'owner_id')
