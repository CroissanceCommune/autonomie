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
    from autonomie.models.task.task import (
        TaskLine,
        TaskLineGroup,
        Task
    )
    from autonomie.models.base import (
        DBSESSION,
    )

    session = DBSESSION()

    index = 0
    for task in Task.query():
        if task.type_ not in ('estimation', 'invoice', 'cancelinvoice'):
            continue
        group = TaskLineGroup(task_id=task.id)

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


def downgrade():
    pass
