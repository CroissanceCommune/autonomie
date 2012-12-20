"""1.5 Project : Multiple clients per project

Revision ID: 1cc9ff114346
Revises: 70853b55768c
Create Date: 2012-12-20 10:22:18.381606

"""

# revision identifiers, used by Alembic.
revision = '1cc9ff114346'
down_revision = '70853b55768c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from autonomie.models import DBSESSION
    from autonomie.models.project import Project
    from autonomie.models.client import Client
    for proj in DBSESSION().query(Project):
        try:
            client = Client.get(proj.client_id)
            if client is not None:
                proj.clients.append(client)
                DBSESSION().merge(proj)
        except:
            continue


def downgrade():
    op.execute("DELETE from project_client;")
