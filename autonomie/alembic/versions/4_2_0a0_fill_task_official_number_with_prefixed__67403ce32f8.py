"""Fill task.official_number with prefixed number

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

    q = Task.query().filter(
        Task.official_number != None,  # noqa E711
        Task.type_.in_(('invoice', 'cancelinvoice')),
    )

    # The goal here is to have in official_numbre what would have appeared
    # on invoices (prefix + number if the invoice defines a prefix).
    for task in q:
        task.official_number = '{}{}'.format(
            task.prefix or '',
            task.official_number,
        )
        session.merge(task)

    session.flush()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
