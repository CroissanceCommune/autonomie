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
from autonomie.models import DBSESSION
from autonomie.models.project import Project
from autonomie.models.task import EstimationLine
from autonomie.models.task import PaymentLine
from autonomie.models.task import InvoiceLine
from autonomie.models.task import TaskStatus
from autonomie.models.task import CancelInvoiceLine


TABLENAMES = ('estimation', 'invoice', 'cancelinvoice')

def migrate_projects_to_multiple_clients():
    """
        move project's client to the manytomany relationship
    """
    from autonomie.models.client import Client
    for proj in DBSESSION().query(Project):
        try:
            client = Client.get(proj.client_id)
            if client is not None:
                proj.clients.append(client)
                DBSESSION().merge(proj)
        except:
            continue


def purge_line_type(factory):
    """
        Supprimer les lignes orphelines pour le type factory
    """
    for line in factory.query():
        if line.task is None:
            DBSESSION().delete(line)


def purge_document_lines():
    """
        Purge the different line types
    """
    for i in (EstimationLine, PaymentLine, InvoiceLine, CancelInvoiceLine, TaskStatus):
        purge_line_type(i)

def add_constraints_to_document_lines():
    """
        Add foreign key constraints to document lines to allow cascaded
        deletion
    """
    for i in TABLENAMES:
        op.create_foreign_key("%s_line_ibfk_1" % i, "%s_line" % i, i,
            ['task_id'], ['id'], ondelete="CASCADE")
    op.create_foreign_key("estimation_payment_ibfk_1", "estimation_payment",
            "estimation", ['task_id'], ['id'], ondelete="CASCADE")
    op.create_foreign_key("task_status_ifbk_1", "task_status",
            "task", ["task_id"], ['id'], ondelete="CASCADE")
    op.create_foreign_key("discount_ifbk_1", "discount",
            "task", ["task_id"], ['id'], ondelete="CASCADE")


def upgrade():
    migrate_projects_to_multiple_clients()
    # Adding foreign keys constraints to existing tables
    # First removing wrong references
    purge_document_lines()
    # Add the keys
    add_constraints_to_document_lines()


def downgrade():
    op.execute("DELETE from project_client;")
    for i in TABLENAMES:
        op.execute("alter table %s_line drop foreign key %s_line_ifbk_1;" % (i,i))
    op.execute("alter table estimation_payment drop foreign key estimation_payment_ibfk_1")
    op.execute("alter table task_status drop foreign key task_status_ifbk_1")
    op.execute("alter table discount drop foreign key discount_ifbk_1")
