"""4.2.0 add task's notes

Revision ID: 3885e8260693
Revises: 4f011ed2a459
Create Date: 2018-10-29 14:05:21.266035

"""

# revision identifiers, used by Alembic.
revision = '3885e8260693'
down_revision = '4f011ed2a459'

from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import column_exists


def update_database_structure():
    if not column_exists('task', 'notes'):
        op.add_column('task', sa.Column('notes', sa.Text(), nullable=True))


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    cnx = op.get_bind()
    cnx.execute("UPDATE task LEFT OUTER JOIN estimation USING (id) SET task.notes=estimation.exclusions")


def clean_database():
    if column_exists('estimation', 'exclusions'):
        op.drop_column('estimation', 'exclusions',)


def upgrade():
    update_database_structure()
    migrate_datas()
    clean_database()


def downgrade():
    pass
