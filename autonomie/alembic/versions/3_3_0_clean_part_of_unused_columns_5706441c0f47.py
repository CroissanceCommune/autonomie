"""3.3.0 : clean part of unused datas

Revision ID: 5706441c0f47
Revises: 2b6ac7b172d3
Create Date: 2016-09-07 11:47:52.522342

"""

# revision identifiers, used by Alembic.
revision = '5706441c0f47'
down_revision = '2b6ac7b172d3'

from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import (
    column_exists,
    table_exists,
    disable_constraints,
    enable_constraints,
)
from sqlalchemy.dialects import mysql

OLD_TABLES = (
    'operation_tresorerie',
    'estimation_line',
    'cancelinvoice_line',
    'manual_invoice',
    'manualinvoice',
    'manualinv',
    'invoice_line',
)


OLD_COLUMNS = (
    ('task', 'taskDate'),
    ('invoice', 'estimationDate'),
    ('invoice', 'estimationNumber'),
    ('accounts', 'primary_group'),
    ('accounts', 'account_challenge'),
    ('accounts', 'account_type'),
    ('accounts', 'account_lastpwd_change'),
    ('accounts', 'code_compta'),
    ('accounts', 'account_expires'),
    ('accounts', 'account_response'),
    ('accounts', 'person_id'),
    ('accounts', 'account_lastloginfrom'),
    ('accounts', 'account_lastlogin'),
    ('activity', 'subaction_label'),
    ('activity', 'action_label'),
    ('cancelinvoice', 'paymentMode'),
    ('cancelinvoice', 'tva'),
    ('company', 'headerType'),
    ('company', 'logoType'),
    ('company', 'header'),
    ('company', 'IDEGWUser'),
    ('company', 'logo'),
    ('company', 'IDGroup'),
    ('company_employee', 'DateStart'),
    ('company_employee', 'DateEnd'),
    ('customer', 'IDContact'),
    ('estimation', 'discount'),
    ('estimation', 'tva'),
    ('estimation', 'discountHT'),
    ('invoice', 'estimationDate'),
    ('invoice', 'estimationNumber'),
    ('invoice', 'paymentMode'),
    ('invoice', 'discount'),
    ('invoice', 'discountHT'),
    ('invoice', 'tva'),
)


def upgrade():
    disable_constraints()
    for table in OLD_TABLES:
        if table_exists(table):
            op.drop_table(table)

    op.alter_column('accounts', 'active',
               existing_type=mysql.VARCHAR(length=1),
               nullable=False,
               existing_server_default=sa.text(u"'Y'"))
    op.alter_column('accounts', 'email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('accounts', 'firstname',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('accounts', 'lastname',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('company', 'active',
               existing_type=mysql.VARCHAR(length=1),
               nullable=False,
               existing_server_default=sa.text(u"'Y'"))
    op.alter_column('company', 'creationDate',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('company', 'name',
               existing_type=mysql.VARCHAR(length=150),
               nullable=False)
    op.alter_column('company', 'object',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('company', 'phone',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
    op.alter_column('company', 'updateDate',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('company_employee', 'account_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('company_employee', 'company_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('customer', 'address',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('customer', 'city',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('customer', 'company_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('configurable_option', 'label',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('customer', 'contactLastName',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('customer', 'creationDate',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('customer', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('customer', 'updateDate',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('customer', 'zipCode',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
    op.alter_column('estimation', 'deposit',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               existing_server_default=sa.text(u"'0'"))
    # Clean table
    for (table, column) in OLD_COLUMNS:
        if column_exists(table, column):
            op.drop_column(table, column)

    enable_constraints()


def downgrade():
    op.drop_column("date_convention_cape_datas", 'end_date')
    op.execute("alter table customer MODIFY code VARCHAR(4) DEFAULT NULL;")
    op.execute("alter table project MODIFY code VARCHAR(4) DEFAULT NULL;")
