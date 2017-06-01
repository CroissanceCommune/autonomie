"""1.6 : Migrate code compta

Revision ID: 29299007fe7d
Revises: 4a4eba558244
Create Date: 2013-02-11 12:04:50.322459

"""

# revision identifiers, used by Alembic.
revision = '29299007fe7d'
down_revision = '4a4eba558244'

import logging
from alembic import op
import sqlalchemy as sa

from autonomie_base.models.base import DBSESSION
from autonomie.models.user import User


def upgrade():
    logger = logging.getLogger("alembic.migrate_code_compta")
    op.add_column("company", sa.Column("code_compta", sa.String(30), default=0))
    dbsession = DBSESSION()
    for user in User.query():
        code_compta = user.code_compta
        companies = user.companies
        if code_compta not in [u"0", None, u""]:
            if len(companies) == 1:
                company = companies[0]
                company.code_compta = code_compta
                dbsession.merge(company)
            else:
                logger.warn(u"User {0} has a code_compta and multiple \
companies".format(user.id))


def downgrade():
    op.drop_column("company", "code_compta")
