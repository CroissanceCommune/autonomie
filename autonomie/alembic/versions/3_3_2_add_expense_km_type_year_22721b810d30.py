"""3.3.2 : add expense_km_type year

Revision ID: 22721b810d30
Revises: 55acdcdcc473
Create Date: 2017-09-05 18:07:51.101638

"""

# revision identifiers, used by Alembic.
revision = '22721b810d30'
down_revision = '55acdcdcc473'

import datetime
from alembic import op
import sqlalchemy as sa


def update_database_structure():
    op.add_column('expensekm_type', sa.Column('year', sa.Integer, nullable=True))


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()
    from autonomie.models.expense import ExpenseKmType
    year = datetime.date.today().year
    for type_ in ExpenseKmType.query():
        type_.year = year
        session.merge(type_)


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.drop_column('expensekm_type', 'year')
