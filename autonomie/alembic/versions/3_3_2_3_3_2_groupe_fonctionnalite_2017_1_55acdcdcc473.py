"""3.3.2 : 3.3.2 groupe fonctionnalite 2017 1

Revision ID: 55acdcdcc473
Revises: 11219b4e619b
Create Date: 2017-06-20 13:21:41.795144

"""

# revision identifiers, used by Alembic.
revision = '55acdcdcc473'
down_revision = '11219b4e619b'

from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import rename_column


def update_database_structure():
    op.add_column(
        'customer',
        sa.Column('civilite', sa.String(10), default=''),
    )
    op.add_column(
        'customer',
        sa.Column('mobile', sa.String(20), default=''),
    )
    op.add_column(
        'customer',
        sa.Column('type_', sa.String(10), default='company'),
    )
    rename_column(
        "customer",
        'contactLastName',
        'lastname',
        sa.String(255)
    )
    rename_column(
        "customer",
        'contactFirstName',
        'firstname',
        sa.String(255)
    )
    rename_column(
        "customer",
        'intraTVA',
        'tva_intracomm',
        sa.String(50)
    )
    rename_column(
        'task',
        'CAEStatus',
        'status',
        sa.String(10),
    )

    op.add_column(
        'estimation',
        sa.Column('estimation_status', sa.String(10), default='waiting'),
    )
    op.add_column(
        'estimation',
        sa.Column('geninv', sa.Boolean(), default=False),
    )
    op.add_column(
        'invoice',
        sa.Column('paid_status', sa.String(10), default='waiting'),
    )
    op.add_column(
        'payment',
        sa.Column("user_id", sa.Integer, sa.ForeignKey('accounts.id'))
    )

    op.add_column(
        'expense_sheet',
        sa.Column('paid_status', sa.String(10), default='waiting'),
    )
    op.add_column(
        'expense_sheet',
        sa.Column('justified', sa.Boolean(), default=False),
    )
    op.add_column(
        "expense_payment",
        sa.Column("user_id", sa.Integer, sa.ForeignKey('accounts.id'))
    )


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from autonomie.models.customer import Customer
    for cust in Customer.query():
        cust.type_ = 'company'
        session.merge(cust)

    from autonomie.models.task import Invoice, Estimation
    for invoice in Invoice.query():
        if invoice.status in ('paid', 'resulted'):
            invoice.paid_status = invoice.status
            invoice.status = 'valid'
            if invoice.statusPersonAccount is not None:
                for payment in invoice.payments:
                    payment.user_id = invoice.statusPersonAccount.id
                    session.merge(payment)

        elif invoice.status == 'aboinv':
            invoice.status = 'valid'
        session.merge(invoice)

    for estimation in Estimation.query():
        if estimation.status in ('aboest',):
            estimation.estimation_status = 'aborted'
            estimation.status = 'valid'

        elif estimation.status == 'geninv':
            estimation.geninv = True
            estimation.status = 'valid'
        session.merge(estimation)

    from autonomie.models.expense import ExpenseSheet
    for expense in ExpenseSheet.query():
        if expense.status in ('paid', 'resulted'):
            expense.paid_status = expense.status
            if expense.status_user is not None:
                for payment in expense.payments:
                    payment.user_id = expense.status_user.id
                    session.merge(payment)
            expense.status = 'valid'
        session.merge(expense)


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    for col in ('civilite', 'mobile', 'type_'):
        op.drop_column('customer', col)
    rename_column(
        "customer",
        'lastname',
        'contactLastName',
        sa.String(255)
    )
    rename_column(
        "customer",
        'firstname',
        'contactFirstName',
        sa.String(255)
    )
    rename_column(
        "customer",
        'tva_intracomm',
        'intraTVA',
        sa.String(50)
    )
