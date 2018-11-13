"""4.2.0 clear old treasury modules Config

Revision ID: 3519f2dab802
Revises: 2e4c3172fc54
Create Date: 2018-06-18 18:32:20.882990

"""

# revision identifiers, used by Alembic.
revision = '3519f2dab802'
down_revision = '2e4c3172fc54'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    pass

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    from autonomie.models.config import Config
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

    deprecated_conf_keys = [
        'compte_cgscop',
        'compte_cg_debiteur',
        'compte_cg_organic',
        'compte_cg_debiteur_organic',
        'compte_cg_assurance',
        'taux_assurance',
        'taux_cgscop',
        'taux_contribution_organic',
        'sage_assurance',
        'sage_cgscop',
        'sage_organic',
    ]
    q = Config.query().filter(Config.name.in_(deprecated_conf_keys))
    q.delete(synchronize_session=False)
    session.flush()

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass  # Nothing can be done, data is lost
