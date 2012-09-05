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
            """)


def downgrade():
    pass
