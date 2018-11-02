"""Add Event.signup_mode

Revision ID: 3fa09c31c2ac
Revises: 1729bb7ed957
Create Date: 2018-11-02 15:03:10.055199

"""

# revision identifiers, used by Alembic.
revision = '3fa09c31c2ac'
down_revision = '1729bb7ed957'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from zope.sqlalchemy import mark_changed

def update_database_structure():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('signup_mode', sa.String(length=100), nullable=False))

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    #from alembic.context import get_bind
    #conn = get_bind()
    op.execute(
        "UPDATE event SET signup_mode = 'closed' WHERE signup_mode = '';"
    )
    mark_changed(session)



def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
     op.drop_column('event', 'signup_mode')
     ### end Alembic commands ###
