"""3.2.2 : Add bank code journal

Revision ID: 25a21d2410b7
Revises: 18504ec02955
Create Date: 2016-05-13 10:26:13.049549

"""

# revision identifiers, used by Alembic.
revision = '25a21d2410b7'
down_revision = '18504ec02955'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'bank_account',
        sa.Column('code_journal', sa.String(120), nullable=False)
    )
    req = "select config_value from config where config_name='receipts_code_journal';"
    from alembic.context import get_bind
    from autonomie.models.base import DBSESSION
    conn = get_bind()
    res = conn.execute(req).scalar()
    if res is not None:
        req = "update bank_account set code_journal='%s'" % res
        conn.execute(req)
        session = DBSESSION()
        from zope.sqlalchemy import mark_changed
        mark_changed(session)



def downgrade():
    op.drop_column('bank_account', 'code_journal')
