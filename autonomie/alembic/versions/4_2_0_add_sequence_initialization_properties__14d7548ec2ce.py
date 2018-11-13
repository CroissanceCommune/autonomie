"""4.2.0 Add sequence initialization properties to Company

Revision ID: 14d7548ec2ce
Revises: 15fb49b9cb37
Create Date: 2018-06-14 14:11:04.229997

"""

# revision identifiers, used by Alembic.
revision = '14d7548ec2ce'
down_revision = '15fb49b9cb37'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def update_database_structure():
    op.add_column('company', sa.Column('month_company_sequence_init_date', sa.Date(), nullable=True))
    op.add_column('company', sa.Column('month_company_sequence_init_value', sa.Integer(), nullable=True))

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.drop_column('company', 'month_company_sequence_init_value')
    op.drop_column('company', 'month_company_sequence_init_date')
