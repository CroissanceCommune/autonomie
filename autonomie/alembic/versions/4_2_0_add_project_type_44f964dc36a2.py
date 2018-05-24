"""4.2.0 : add project type

Revision ID: 44f964dc36a2
Revises: 1ad4b3e78299
Create Date: 2018-03-29 11:30:16.936487

"""

# revision identifiers, used by Alembic.
revision = '44f964dc36a2'
down_revision = '18591428772b'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    op.add_column(
        "project",
        sa.Column(
            'project_type_id', sa.Integer, sa.ForeignKey('project_type.id'),
        )
    )
    op.add_column("task_mention", sa.Column("help_text", sa.String(255)))
    op.alter_column(
        'project',
        'type',
        new_column_name='description',
        existing_type=sa.String(150),
        existing_nullable=True
    )
    op.add_column(
        'task',
        sa.Column(
            'business_type_id', sa.Integer, sa.ForeignKey('business_type.id')
        )
    )
    op.add_column(
        'task',
        sa.Column(
            'business_id', sa.Integer, sa.ForeignKey('business.id')
        )
    )
    op.add_column(
        "task",
        sa.Column(
            "version", sa.Integer,
        )
    )


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from autonomie.models.populate import populate_project_types
    populate_project_types(session)

    from autonomie.models.project.project import (
        Project,
    )
    from autonomie.models.project.business import Business
    from autonomie.models.project.types import (
        ProjectType,
        BusinessType,
    )

    from autonomie.models.populate import populate_project_types
    populate_project_types(session)

    default_ptype_id = ProjectType.get_default().id
    default_btype_id = BusinessType.get_default().id

    op.execute("update project set project_type_id=%s" % default_ptype_id)
    op.execute("update task set version='4.1'")
    op.execute("update task set business_type_id=%s" % default_btype_id)

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
