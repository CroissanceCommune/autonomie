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
import traceback


def change_custom_date_type(
    session, model, table, new_column_name, column_name
):
    import datetime
    op.add_column(table, sa.Column(new_column_name, sa.Date()))
    session.flush()

    from alembic.context import get_bind
    conn = get_bind()
    request = "select id, %s from %s" % (column_name, table)
    result = conn.execute(request)

    for (id_, original_value,) in result:
        try:
            value = datetime.datetime.fromtimestamp(original_value).date()
            obj = model.get(id_)
            setattr(obj, new_column_name, value)
            session.merge(obj)
        except:
            traceback.print_exc()
            import sys
            sys.exit(1)
            print("Error %s %s %s : %s" % (
                table, column_name, new_column_name, original_value
            )
            )
            continue

    session.flush()
    op.drop_column(table, column_name)


def update_database_structure(session):
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
    op.add_column(
        'estimation_payment',
        sa.Column('date', sa.Date()),
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
    rename_column(
        'task',
        'statusComment',
        'status_comment',
        sa.Text,
    )
    rename_column(
        'task',
        'statusPerson',
        'status_person_id',
        sa.Integer,
    )
    #op.create_foreign_key(
    #    None, 'task', 'accounts', ['status_person_id'], ['id']
    #)
    rename_column(
        'task_status',
        'statusPerson',
        'status_person_id',
        sa.Integer,
    )
    #op.create_foreign_key(
    #    None, 'task_status', 'accounts', ['status_person_id'], ['id']
    #)
    rename_column(
        'task_status',
        'statusCode',
        'status_code',
        sa.String(10),
    )
    rename_column(
        'task_status',
        'statusComment',
        'status_comment',
        sa.Text,
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

    from autonomie.models.project import Project
    change_custom_date_type(
        session,
        Project, 'project', 'starting_date', 'startingDate'
    )
    change_custom_date_type(
        session,
        Project, 'project', 'ending_date', 'endingDate'
    )

    from autonomie.models.customer import Customer
    change_custom_date_type(
        session,
        Customer, 'customer', 'updated_at', 'updateDate'
    )
    change_custom_date_type(
        session,
        Customer, 'customer', 'created_at', 'creationDate'
    )

    from autonomie.models.company import Company
    change_custom_date_type(
        session,
        Company, 'company', 'updated_at', 'updateDate'
    )
    change_custom_date_type(
        session,
        Company, 'company', 'created_at', 'creationDate'
    )

    from autonomie.models.task.task import (TaskStatus, Task)
    change_custom_date_type(
        session,
        TaskStatus, "task_status", "status_date", "statusDate"
    )
    change_custom_date_type(
        session,
        Task, 'task', "status_date", "statusDate"
    )


def _user_exists(session, user_id):
    from autonomie.models.user import User
    return session.query(User.id).filter_by(id=user_id).count()


def _find_status(session, task_id, statusnames):
    """
    Return the status_person_id id and the date of the given status
    """
    from autonomie.models.task.task import TaskStatus
    query = session.query(TaskStatus.status_person_id, TaskStatus.status_date)
    query = query.filter_by(task_id=task_id)
    query = query.filter(TaskStatus.status_code.in_(statusnames))
    query = query.order_by(sa.desc(TaskStatus.status_date))
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
                invoice.status_person_id = statuses[-1][0]
                invoice.status_date = statuses[-1][1]

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
                estimation.status_person_id = statuses[-1][0]
                estimation.status_date = statuses[-1][1]

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


def _upgrade_estimation_payment_dates(session):
    from autonomie.models.task.estimation import PaymentLine
    from autonomie_base.models.utils import format_from_taskdate
    request = "select id, paymentDate from estimation_payment;"
    conn = op.get_bind()
    result = conn.execute(request)
    for (id_, paymentDate) in result:
        p = PaymentLine.get(id_)
        try:
            value = format_from_taskdate(paymentDate)
            p.date = value
        except:
            print("Error paymentDate : %s" % paymentDate)
            continue
        session.merge(p)
    session.flush()
    op.drop_column('estimation_payment', 'paymentDate')


def drop_old_columns():
    try:
        op.drop_column('task', 'creationDate')
    except:
        pass
    try:
        op.drop_column('task', 'updateDate')
    except:
        pass
    try:
        op.drop_column('task', '_number')
    except:
        pass
    try:
        op.drop_column('task', 'documentType')
    except:
        pass
    try:
        op.drop_column('phase', 'creationDate')
    except:
        pass

    try:
        op.drop_column('phase', 'updateDate')
    except:
        pass

    try:
        op.drop_column('estimation_payment', 'creationDate')
    except:
        pass

    try:
        op.drop_column('estimation_payment', 'updateDate')
    except:
        pass


def migrate_datas(session):
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
    _upgrade_estimation_payment_dates(session)
    session.flush()
    drop_old_columns()


def upgrade():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    update_database_structure(session)
    migrate_datas(session)


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
