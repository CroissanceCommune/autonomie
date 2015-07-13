"""2.9 : Migrate task lines

Revision ID: 2192101f133b
Revises: 465776bbb019
Create Date: 2015-06-29 11:57:26.726124

"""

# revision identifiers, used by Alembic.
revision = '2192101f133b'
down_revision = '36b1d9c38c43'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from autonomie.models.task import (
        TaskLine,
        TaskLineGroup,
        Task,
        Estimation,
        CancelInvoice,
        Invoice,
    )
    from autonomie.models.base import (
        DBSESSION,
    )

    session = DBSESSION()

    index = 0
    query = Task.query()
    query = query.with_polymorphic([Invoice, CancelInvoice, Estimation])
    query = query.filter(
        Task.type_.in_(['invoice', 'estimation', 'cancelinvoice'])
    )
    for task in query:
        group = TaskLineGroup(task_id=task.id, order=0)

        for line in task.lines:

            tline = TaskLine(
                group=group,
                order=line.rowIndex,
                description=line.description,
                cost=line.cost,
                tva=line.tva,
                quantity=line.quantity,
            )

            if hasattr(line, 'product_id'):
                tline.product_id = line.product_id
            session.add(tline)

            if index % 100 == 0:
                session.flush()

    op.alter_column(
        table_name='estimation_payment',
        column_name='rowIndex',
        new_column_name='order',
        type_=sa.Integer,
    )


def downgrade():
    pass
