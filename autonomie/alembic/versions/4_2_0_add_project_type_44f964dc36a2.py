"""4.2.0 : add project type

Revision ID: 44f964dc36a2
Revises: 1ad4b3e78299
Create Date: 2018-03-29 11:30:16.936487

"""

# revision identifiers, used by Alembic.
revision = '44f964dc36a2'
down_revision = '18591428772b'
import logging
from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import column_exists

logger = logging.getLogger('alembic.add_project_type')

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
    if column_exists("task", "name"):
        op.drop_column("task", "name")
    if column_exists("task", "type_"):
        op.drop_column("task", "type_")


def _add_business_to_all_invoices(session):
    """
    Add a Business entry to all invoices
    """
    from autonomie.models.task import (
        Estimation, Invoice,
    )
    logger.debug(u"Adding business to estimations")
    for e in Estimation.query().options(
        sa.orm.load_only('id', 'name', 'business_type_id', 'project_id')
    ):
        invoices = Invoice.query().options(
            sa.orm.load_only('id')
        ).filter_by(estimation_id=e.id).all()
        if invoices:
            business = e.gen_business()
            for invoice in invoices:
                op.execute(
                    u"update task set business_id=%s where id=%s" % (
                        business.id,
                        invoice.id
                    )
                )
                op.execute(
                    u"update task join cancelinvoice as c on c.id=task.id "
                    u"set task.business_id=%s where c.invoice_id=%s" % (
                        business.id,
                        invoice.id
                    )
                )

    logger.debug(u"Adding business to direct invoices")
    for invoice in Invoice.query().options(
        sa.orm.load_only('id', 'name', 'business_type_id', 'project_id')
    ).filter_by(estimation_id=None).all():
        business = invoice.gen_business()

        op.execute(
            u"update task join cancelinvoice as c on c.id=task.id "
            u"set task.business_id=%s where c.invoice_id=%s" % (
                business.id,
                invoice.id
            )
        )

    session.flush()


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from autonomie.models.populate import populate_project_types
    populate_project_types(session)

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

    _add_business_to_all_invoices(session)


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
