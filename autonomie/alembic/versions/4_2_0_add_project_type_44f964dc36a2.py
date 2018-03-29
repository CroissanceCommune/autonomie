"""4.2.0a : add project type

Revision ID: 44f964dc36a2
Revises: 1ad4b3e78299
Create Date: 2018-03-29 11:30:16.936487

"""

# revision identifiers, used by Alembic.
revision = '44f964dc36a2'
down_revision = '1ad4b3e78299'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    op.add_column(
        "project",
        sa.Column(
            'project_type_id', sa.Integer, sa.ForeignKey('project_type.id'),
        )
    )

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from autonomie.models.populate import populate_project_types
    populate_project_types(session)

    from autonomie.models.project.types import ProjectType
    default = ProjectType.get_by_name('default')

    op.execute("update project set project_type_id=%s" % default.id)

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
