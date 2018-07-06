#! -*- coding: utf-8 -*-

"""initialize accounting entries label templates in Config

Revision ID: 18b00b9e3b46
Revises: 3519f2dab802
Create Date: 2018-06-18 19:30:28.605541

"""

# revision identifiers, used by Alembic.
revision = '18b00b9e3b46'
down_revision = '3519f2dab802'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    pass

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    from autonomie.models.config import Config
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()

    initial_values = [
        (
            'bookentry_facturation_label_template',
            '{invoice.customer.label} {company.name}'
        ),
        (
            'bookentry_contribution_label_template',
            "{invoice.customer.label} {company.name}"
        ),
        (
            'bookentry_rg_interne_label_template',
            "RG COOP {invoice.customer.label} {company.name}"
        ),
        (
            'bookentry_rg_client_label_template',
            "RG {invoice.customer.label} {company.name}"
        ),
        (
            'bookentry_expense_label_template',
            "{beneficiaire}/frais {expense_date:%-m %Y}"
        ),
        (
            'bookentry_payment_label_template',
            "{company.name} / Rgt {invoice.customer.label}"
        ),
        (
            'bookentry_expense_payment_main_label_template',
            "{beneficiaire_LASTNAME} / REMB FRAIS {expense_date:%B/%Y}"
        ),
        (
            'bookentry_expense_payment_waiver_label_template',
            "Abandon de créance {beneficiaire_LASTNAME} {expense_date:%B/%Y}"
        ),
    ]

    for key, val in initial_values:
        Config.set(key, val)


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
