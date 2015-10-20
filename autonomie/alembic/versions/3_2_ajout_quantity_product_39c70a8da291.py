"""3.2 : ajout_quantity_product

Revision ID: 39c70a8da291
Revises: bdb7dd32c2c
Create Date: 2015-10-01 12:18:41.393913

"""

# revision identifiers, used by Alembic.
revision = '39c70a8da291'
down_revision = '4cb8e3e01f36'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "sale_product",
        sa.Column('quantity', sa.Float(), default=1)
    )
    op.add_column(
        "task_line_group",
        sa.Column('quantity', sa.Float(), default=1)
    )
    op.add_column(
        "task_line_group",
        sa.Column("display_details", sa.Boolean(), default=True),
    )
    op.add_column(
        "task_line",
        sa.Column('group_quantity', sa.Float(), default=0)
    )

    for table in ("sale_product", "task_line_group"):
        op.execute("update %s set quantity=1" % table)

    op.execute("update task_line set group_quantity=0")


def downgrade():
    op.drop_column("sale_product", "quantity")
    op.drop_column("task_line_group", "quantity")
    op.drop_column("task_line_group", "display_details")
    op.drop_column("task_line", "group_quantity")
