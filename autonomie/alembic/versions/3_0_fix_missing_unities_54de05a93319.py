"""3.0 : fix missing unities

Revision ID: 54de05a93319
Revises: 2192101f133b
Create Date: 2015-08-27 11:44:47.281384

"""

# revision identifiers, used by Alembic.
revision = '54de05a93319'
down_revision = '2192101f133b'

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
    from autonomie_base.models.base import (
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
        try:
            task_lines = task.default_line_group.lines
        except:
            continue
        for index, line in enumerate(task.lines):
            try:
                task_line = task_lines[index]
                task_line.unity = line.unity
                session.merge(task_line)

            except:
                pass

        index += 1
        if index % 100 == 0:
            session.flush()

def downgrade():
    pass
