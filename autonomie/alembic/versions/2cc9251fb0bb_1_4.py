"""1.4 : Desactivation des comptes sans entreprises (sauf ceux des admin)

Revision ID: 2cc9251fb0bb
Revises: 1902ba0cc2ac
Create Date: 2012-08-28 23:35:43.815154

"""

# revision identifiers, used by Alembic.
revision = '2cc9251fb0bb'
down_revision = '1902ba0cc2ac'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Disable all accounts with no enterprise
    # Enable all accounts part from the 1 and 2 group (admins)
    op.execute("""
update egw_accounts as egwa left outer join coop_company_employee as cce on egwa.account_id=cce.IDEmployee set account_status='I' where cce.IDEmployee is null;
update egw_accounts set account_status='A' where account_primary_group in (1,2);
update egw_accounts set account_status='Y' WHERE account_status='A';
update egw_accounts set account_status='N' WHERE account_status!='A';
""")


def downgrade():
    pass
