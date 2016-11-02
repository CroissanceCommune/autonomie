"""3.3.0 : Fix treasury percentage configuration

Revision ID: 11219b4e619b
Revises: 5706441c0f47
Create Date: 2016-11-02 17:26:43.351149

"""

# revision identifiers, used by Alembic.
revision = '11219b4e619b'
down_revision = '5706441c0f47'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    pass

def migrate_datas():
    from autonomie.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

    op.alter_column(
        "custom_invoice_book_entry_module",
        "percentage",
        type_=sa.Float(),
        nullable=False,
    )

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
