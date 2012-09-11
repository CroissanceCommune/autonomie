"""1.4 : Renommage des colonnes utilisateurs

Revision ID: 1e7d7781a47b
Revises: 209c0f6d7620
Create Date: 2012-09-05 17:43:57.831725

"""

# revision identifiers, used by Alembic.
revision = '1e7d7781a47b'
down_revision = '209c0f6d7620'

from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import force_rename_table
from autonomie.alembic.utils import rename_column

def upgrade():
    force_rename_table("egw_accounts", "accounts")
    force_rename_table("egw_config", "config")
    force_rename_table("coop_customer", "customer")
    force_rename_table("coop_company", "company")
    force_rename_table("coop_company_employee", "company_employee")
    force_rename_table("coop_project", "project")
    force_rename_table("coop_phase", "phase")
    force_rename_table("coop_tva", "tva")
    force_rename_table("coop_task_status", "task_status")
    force_rename_table("coop_holliday", "holiday")
    force_rename_table("symf_operation_treso", "operation_tresorerie")
    force_rename_table("coop_task", "task")
    force_rename_table("coop_invoice", "invoice")
    force_rename_table("coop_invoice_line", "invoice_line")
    force_rename_table("coop_cancel_invoice", "cancelinvoice")
    force_rename_table("coop_cancel_invoice_line", "cancelinvoice_line")
    force_rename_table("coop_payment", "payment")
    force_rename_table("symf_facture_manuelle", "manualinvoice")
    force_rename_table("coop_estimation", "estimation")
    force_rename_table("coop_estimation_line", "estimation_line")
    force_rename_table("coop_estimation_payment", "estimation_payment")
    op.execute("""
alter table accounts change account_id id int(11) NOT NULL AUTO_INCREMENT;
alter table accounts change account_lid login varchar(64) NOT NULL;
alter table accounts change account_pwd password varchar(100) NOT NULL;
alter table accounts change account_firstname firstname varchar(50) DEFAULT NULL;
alter table accounts change account_lastname lastname varchar(50) DEFAULT NULL;
alter table accounts change account_primary_group primary_group int(11) NOT NULL DEFAULT '0';
alter table accounts change account_status active varchar(1) NOT NULL DEFAULT 'Y';
alter table accounts change account_email email varchar(100) DEFAULT NULL;
""")
    # IDProject
    rename_column("project", "IDProject", "id", autoincrement=True)
    rename_column("invoice", "IDProject", "project_id")
    rename_column("estimation", "IDProject", "project_id")
    rename_column("cancelinvoice", "IDProject", "project_id")
    rename_column("phase", 'IDProject', 'project_id')
    # IDCompany
    rename_column("company", 'IDCompany', 'id', autoincrement=True)
    rename_column("customer", 'IDCompany', 'company_id')
    rename_column("project", 'IDCompany', 'company_id')
    rename_column("company_employee", 'IDCompany', 'company_id')
    # IDTask
    rename_column("task", 'IDTask', 'id', autoincrement=True)
    rename_column("estimation", 'IDTask', 'id', autoincrement=True)
    rename_column("invoice", 'IDTask', 'id', autoincrement=True)
    rename_column("invoice", 'IDEstimation', 'estimation_id', nullable=True)
    rename_column("cancelinvoice", 'IDTask', 'id', autoincrement=True)
    rename_column("cancelinvoice", 'IDInvoice', "invoice_id", nullable=True)

    rename_column("estimation_line", 'IDTask', 'task_id')
    rename_column("estimation_line", 'IDWorkLine', 'id', autoincrement=True)
    rename_column("estimation_payment", 'IDTask', 'task_id')
    rename_column("estimation_payment", 'IDPaymentLine', 'id', autoincrement=True)
    rename_column("invoice_line", 'IDTask', 'task_id')
    rename_column("invoice_line", 'IDInvoiceLine', 'id', autoincrement=True)
    rename_column("payment", 'IDTask', 'task_id')
    rename_column("cancelinvoice_line", 'IDTask', 'task_id')

    rename_column("task_status", 'IDTask', 'task_id')

    # IDPhase
    rename_column("phase", "IDPhase", "id", autoincrement=True)
    rename_column("task", "IDPhase", "phase_id")

    # IDEmployee
    rename_column("company_employee", 'IDEmployee', 'account_id')
    rename_column("task", "IDEmployee", 'owner_id')



def downgrade():
    pass
