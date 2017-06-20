"""3.3.2 : Postgresql migration

Revision ID: 113f744a4fed
Revises: 11219b4e619b
Create Date: 2017-05-12 11:44:56.564392

"""

# revision identifiers, used by Alembic.
revision = '113f744a4fed'
down_revision = '11219b4e619b'

from alembic import op
import sqlalchemy as sa


# Lines generated thanks to pgdiff : https://github.com/joncrlsn/pgdiff
ALTER_LINES = """
alter table baseexpense_line Alter column category TYPE category using category::category;
ALTER TABLE competence_grid_sub_item ALTER COLUMN evaluation TYPE double precision;
ALTER TABLE competence_option ALTER COLUMN requirement TYPE double precision;
ALTER TABLE competence_requirement ALTER COLUMN requirement TYPE double precision;
ALTER TABLE competence_scale ALTER COLUMN value TYPE double precision;
ALTER TABLE custom_invoice_book_entry_module ALTER COLUMN percentage TYPE double precision;
ALTER TABLE external_activity_datas ALTER COLUMN brut_salary TYPE double precision;
ALTER TABLE external_activity_datas ALTER COLUMN hours TYPE double precision;
ALTER TABLE sale_product ALTER COLUMN value TYPE double precision;
ALTER TABLE task_line ALTER COLUMN quantity TYPE double precision;
ALTER TABLE user_datas ALTER COLUMN parcours_num_hours TYPE double precision;
ALTER TABLE user_datas ALTER COLUMN parcours_salary TYPE double precision;
ALTER TABLE user_datas ALTER COLUMN parcours_taux_horaire TYPE double precision;"""

def change_bool_column(tablename, column, default=None):
    if default is not None:
        op.execute(
            "ALTER TABLE {0} ALTER COLUMN \"{1}\" DROP DEFAULT".format(
                tablename, column
            )
        )

    op.execute(
        "ALTER TABLE {0} ALTER \"{1}\" TYPE boolean USING CASE WHEN \"{1}\"=0 THEN FALSE ELSE TRUE END;".format(
            tablename, column
        )
    )
    if default is not None:
        op.execute("ALTER TABLE {0} ALTER COLUMN \"{1}\" SET DEFAULT {2}".format(
            tablename, column, str(default).upper()
        ))

def update_database_structure():
    for table, col, default in (
        ('workshop_action', 'active', True),
        ('tva', 'active', True),
        ('tva', 'default', False),
        ('product', 'active', True),
        ('project', 'archived', False),
        ('templates', 'active', True),
        ('statistic_sheet', 'active', True),
        ('cae_situation_option', 'is_integration', False),
        ('userdatas_socialdocs', 'status', False),
        ('external_activity_datas', 'employer_visited', False),
        ('task', 'round_floor', False),
        ('payment_conditions', 'default', False),
        ('invoice', 'exported', False),
        ('cancelinvoice', 'exported', False),
        ('payment', 'exported', False),
        ('bank_account', 'default', False),
        ('activity_type', 'active', True),
        ('activity_action', 'active', True),
        ('configurable_option', 'active', True),
        ('custom_invoice_book_entry_module', 'active', True),
        ('custom_invoice_book_entry_module', 'enabled', True),
        ('customer', 'archived', False),
        ('expense_type', 'active', True),
        ('expense_type', 'contribution', False),
        ('expensetel_type', 'initialize', False),
        ('expense_sheet', 'exported', False),
        ('baseexpense_line', 'valid', False),
        ('expense_payment', 'waiver', False),
        ('expense_payment', 'exported', False),
    ):
        print("Converting the %s.%s to boolean" % (table, col))
        change_bool_column(table, col, default)

    for line in ALTER_LINES.splitlines():
        line = line.strip()
        if line:
            op.execute(line)

    from zope.sqlalchemy import mark_changed
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    mark_changed(session)

def upgrade():
    update_database_structure()


def downgrade():
    pass
