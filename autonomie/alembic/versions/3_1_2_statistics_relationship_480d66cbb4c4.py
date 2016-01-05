"""3.1.2 : statistics relationship

Revision ID: 480d66cbb4c4
Revises: 4cb8e3e01f36
Create Date: 2015-12-19 10:56:38.895757

"""

# revision identifiers, used by Alembic.
revision = '480d66cbb4c4'
down_revision = '4cb8e3e01f36'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "base_statistic_criterion",
        sa.Column(
            'parent_id',
            sa.Integer,
            sa.ForeignKey("base_statistic_criterion.id"),
        )
    )
    op.add_column(
        "task",
        sa.Column(
            "prefix",
            sa.String(15),
            default="",
        )
    )

    from autonomie.models.config import get_config
    prefix = get_config().get('invoiceprefix', '')
    if prefix:
        op.execute("Update task set prefix='%s'" % (prefix,))


def downgrade():
    pass
