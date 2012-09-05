"""Renommage des colonnes utilisateurs

Revision ID: 1e7d7781a47b
Revises: 209c0f6d7620
Create Date: 2012-09-05 17:43:57.831725

"""

# revision identifiers, used by Alembic.
revision = '1e7d7781a47b'
down_revision = '209c0f6d7620'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""
rename table egw_accounts to accounts;
alter table accounts change account_id id int(11) NOT NULL AUTO_INCREMENT;
alter table accounts change account_lid login varchar(64) NOT NULL;
alter table accounts change account_pwd password varchar(100) NOT NULL;
alter table accounts change account_firstname firstname varchar(50) DEFAULT NULL;
alter table accounts change account_lastname lastname varchar(50) DEFAULT NULL;
alter table accounts change account_primary_group primary_group int(11) NOT NULL DEFAULT '0';
alter table accounts change account_status active varchar(1) NOT NULL DEFAULT 'Y';
alter table accounts change account_email email varchar(100) DEFAULT NULL;
rename table egw_config to config;
rename table coop_customer to customer;
rename table coop_company to company;
rename table coop_company_employee to company_employee;
rename table coop_project to project;
alter table project change IDProject id int(11) NOT NULL AUTO_INCREMENT;
alter table coop_invoice change IDProject project_id int(11) NOT NULL;
alter table coop_estimation change IDProject project_id int(11) NOT NULL;
alter table coop_cancel_invoice change IDProject project_id int(11) NOT NULL;
alter table coop_phase change IDProject project_id int(11) NOT NULL;
rename table coop_phase to phase;
rename table coop_tva to tva;
rename table coop_task_status to task_status;
rename table coop_holliday to holiday;
rename table symf_operation_treso to operation_tresorerie;
rename table coop_task to document;
rename table coop_invoice to invoice;
rename table coop_invoice_line to invoice_line;
rename table coop_cancel_invoice to cancelinvoice;
rename table coop_cancel_invoice_line to cancelinvoice_line;
rename table coop_payment to payment;
rename table symf_facture_manuelle to manualinvoice;
rename table coop_estimation to estimation;
rename table coop_estimation_line to estimation_line;
rename table coop_estimation_payment to estimation_payment;
""")


def downgrade():
    pass
