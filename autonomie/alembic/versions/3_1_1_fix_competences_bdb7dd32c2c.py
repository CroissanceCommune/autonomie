"""3.1.1 : fix competences

Revision ID: bdb7dd32c2c
Revises: 59f05bb3051d
Create Date: 2015-10-13 09:44:07.621413

"""

# revision identifiers, used by Alembic.
revision = 'bdb7dd32c2c'
down_revision = '59f05bb3051d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from autonomie.models import competence
    from autonomie_base.models.base import DBSESSION

    for comp in competence.CompetenceOption.query():
        req = comp.requirement
        for deadline in competence.CompetenceDeadline.query():
            comp.requirements.append(
                competence.CompetenceRequirement(
                    deadline_id=deadline.id,
                    requirement=req,
                )
            )
        DBSESSION().merge(comp)


def downgrade():
    pass
