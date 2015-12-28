"""3.2 : ajout_quantity_product

Revision ID: 39c70a8da291
Revises: 480d66cbb4c4
Create Date: 2015-10-01 12:18:41.393913

"""

# revision identifiers, used by Alembic.
revision = '39c70a8da291'
down_revision = '480d66cbb4c4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "product_product_group_rel",
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

    for table in ("product_product_group_rel", "task_line_group"):
        op.execute("update %s set quantity=1" % table)

    # On ajoute une primary_key sur cette table (elle passe maintenant par
    # l'orm)
    op.execute("SET FOREIGN_KEY_CHECKS=0;\
ALTER TABLE product_product_group_rel ADD PRIMARY KEY \
(`sale_product_group_id`, `sale_product_id`);\
SET FOREIGN_KEY_CHECKS=1")

    op.execute("update task_line set group_quantity=0")
    from autonomie.models.base import DBSESSION
    from zope.sqlalchemy import mark_changed
    mark_changed(DBSESSION())


def downgrade():
    op.drop_column("product_product_group_rel", "quantity")
    op.drop_column("task_line_group", "quantity")
    op.drop_column("task_line_group", "display_details")
    op.drop_column("task_line", "group_quantity")
