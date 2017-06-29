"""3.3.2 : groupe fonctionnalite 2017 1

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
        sa.String(255),
        nullable=True,
    )
    rename_column(
        "customer",
        'intraTVA',
        'tva_intracomm',
        sa.String(50),
        nullable=True
    )
    rename_column(
        "customer",
        'zipCode',
        'zip_code',
        sa.String(20),
    )
    rename_column(
        'task',
        'CAEStatus',
        'status',
        sa.String(10),
    )

    op.add_column(
        'estimation',
        sa.Column('signed_status', sa.String(10)),
    )
    op.add_column(
        'estimation',
        sa.Column('geninv', sa.Boolean()),
    )
    op.add_column(
        'invoice',
        sa.Column('paid_status', sa.String(10)),
    )
    op.add_column(
        'payment',
        sa.Column("user_id", sa.Integer, sa.ForeignKey('accounts.id'))
    )

    op.add_column(
        'expense_sheet',
        sa.Column('paid_status', sa.String(10)),
    )
    op.add_column(
        'expense_sheet',
        sa.Column('justified', sa.Boolean()),
    )
    op.add_column(
        "expense_payment",
        sa.Column("user_id", sa.Integer, sa.ForeignKey('accounts.id'))
    )


def _user_exists(session, user_id):
    from autonomie.models.user import User
    return session.query(User.id).filter_by(id=user_id).count()


def _find_status(session, task_id, statusnames):
    """
    Return the statusPerson id and the date of the given status
    """
    from autonomie.models.task.task import TaskStatus
    query = session.query(TaskStatus.statusPerson, TaskStatus.statusDate)
    query = query.filter_by(task_id=task_id)
    query = query.filter(TaskStatus.statusCode.in_(statusnames))
    query = query.order_by(sa.desc(TaskStatus.statusDate))
    all_items = query.all()
    result = []
    if all_items:
        for record in all_items:
            person_id, status_date = record
            if _user_exists(session, person_id):
                result.append((person_id, status_date))

    return result


def _update_payments(session, task_id, statuses):
    """
    Update the payments set on task_id
    """
    from autonomie.models.task import Payment
    for person_id, statusdate in statuses:
        payment = session.query(Payment).\
            filter_by(task_id=task_id).\
            filter_by(user_id=None).\
            filter_by(created_at=statusdate).first()
        if payment is not None:
            payment.user_id = person_id
            session.merge(payment)


def _upgrade_invoices(session):
    from autonomie.models.task import Invoice
    for invoice in Invoice.query():
        if invoice.status in ('paid', 'resulted'):
            invoice.paid_status = invoice.status
            invoice.status = 'valid'
            statuses = _find_status(session, invoice.id, ('valid'))
            if statuses:
                invoice.statusPerson = statuses[-1][0]
                invoice.statusDate = statuses[-1][1]

            statuses = _find_status(session, invoice.id, ('paid', 'resulted'))
            if statuses:
                _update_payments(session, invoice.id, statuses)
        else:
            if invoice.status == 'aboinv':
                invoice.status = 'valid'

            invoice.paid_status = 'waiting'

        session.merge(invoice)


def _upgrade_estimations(session):
    from autonomie.models.task import Estimation

    for estimation in Estimation.query():
        if estimation.status in ('aboest',):
            estimation.signed_status = 'aborted'
            estimation.status = 'valid'

            statuses = _find_status(session, estimation.id, ('valid'))
            if statuses:
                estimation.statusPerson = statuses[-1][0]
                estimation.statusDate = statuses[-1][1]

        else:
            if estimation.status == 'geninv':
                estimation.geninv = True
                estimation.status = 'valid'
            else:
                estimation.geninv = False

            estimation.signed_status = 'waiting'

        session.merge(estimation)


def _upgrade_expenses(session):
    from autonomie.models.expense import ExpenseSheet
    for expense in ExpenseSheet.query():
        if expense.status in ('paid', 'resulted'):
            expense.paid_status = expense.status
            if _user_exists(session, expense.status_user_id):
                for payment in expense.payments:
                    payment.user_id = expense.status_user_id
                    session.merge(payment)
            expense.status = 'valid'
        else:
            expense.paid_status = 'waiting'
        expense.justified = False
        session.merge(expense)


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from autonomie.models.customer import Customer
    for cust in Customer.query():
        cust.type_ = 'company'
        session.merge(cust)

    _upgrade_invoices(session)
    session.flush()
    _upgrade_estimations(session)
    session.flush()
    _upgrade_expenses(session)
    session.flush()


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
