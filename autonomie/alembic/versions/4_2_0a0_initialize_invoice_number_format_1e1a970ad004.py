"""initialize invoice number format

Revision ID: 1e1a970ad004
Revises: 44f964dc36a2
Create Date: 2018-06-06 12:29:45.046659

"""

# revision identifiers, used by Alembic.
revision = '1e1a970ad004'
down_revision = '44f964dc36a2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def update_database_structure():
    pass


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    from autonomie.models.config import Config

    session = DBSESSION()

    Config.query().filter_by(
        app='autonomie',
        name='invoice_number_template'
    ).delete()

    prefix = session.query(Config.value).filter_by(
        app='autonomie',
        name='invoiceprefix',
    ).scalar() or ''

    default_format = Config(
        app='autonomie',
        name='invoice_number_template',
        value=prefix + '{SEQYEAR}'
    )
    session.add(default_format)
    session.flush()


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
