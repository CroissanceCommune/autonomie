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

helper = sa.Table(
    "expensekm_type",
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('year', sa.Integer),
)


def update_database_structure():
    op.add_column('expensekm_type', sa.Column('year', sa.Integer, nullable=True))


def migrate_datas():
    connection = op.get_bind()
    year = datetime.date.today().year
    connection.execute(helper.update().values(year=year))


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.drop_column('expensekm_type', 'year')
