"""3.4 : add expense specific exported flag

Revision ID: 4299e583631c
Revises: 6a8b2495102
Create Date: 2017-09-08 10:23:41.244459

"""

# revision identifiers, used by Alembic.
revision = '4299e583631c'
down_revision = '6a8b2495102'

from alembic import op
import sqlalchemy as sa


sheet_helper = sa.Table(
    'expense_sheet',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column("purchase_exported", sa.Boolean()),
    sa.Column("expense_exported", sa.Boolean()),
    sa.Column("exported", sa.Boolean()),
)



def update_database_structure():
    op.add_column(
        "expense_sheet",
        sa.Column(
            "purchase_exported",
            sa.Boolean(),
            default=False,
        )
    )
    op.add_column(
        "expense_sheet",
        sa.Column(
            "expense_exported",
            sa.Boolean(),
            default=False,
        )
    )

def migrate_datas():
    connection = op.get_bind()

    for sheet in connection.execute(sheet_helper.select()):
        if sheet.exported:
            connection.execute(
                sheet_helper.update().where(
                    sheet_helper.c.id == sheet.id
                ).values(
                    purchase_exported=True,
                    expense_exported=True,
                )
            )

    op.drop_column("expense_sheet", "exported")


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.drop_column("expense_sheet", "purchase_exported")
    op.drop_column("expense_sheet", "expense_exported")
    op.add_column(
        "expense_sheet",
        sa.Column(
            "exported",
            sa.Boolean(),
            default=False,
        )
    )
