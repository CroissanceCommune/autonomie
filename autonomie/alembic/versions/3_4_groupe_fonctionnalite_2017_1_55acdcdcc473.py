"""3.4 : groupe fonctionnalite 2017 1

Revision ID: 55acdcdcc473
Revises: 11219b4e619b
Create Date: 2017-06-20 13:21:41.795144

"""

# revision identifiers, used by Alembic.
revision = '55acdcdcc473'
down_revision = '11219b4e619b'

import logging
from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import rename_column
import traceback


def change_custom_date_type(table, new_column_name, column_name):
    op.add_column(table, sa.Column(new_column_name, sa.Date()))

    helper = sa.Table(
        table,
        sa.MetaData(),
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(new_column_name, sa.Date()),
        sa.Column(column_name, sa.Integer()),
    )

    import datetime

    connection = op.get_bind()

    for element in connection.execute(helper.select()):
        original_value = getattr(element, column_name)

        try:
            value = datetime.datetime.fromtimestamp(original_value).date()
            connection.execute(
                helper.update().where(
                    helper.c.id == element.id
                ).values(
                    {new_column_name: value}
                )
            )
        except:
            traceback.print_exc()
            import sys
            sys.exit(1)
            print("Error %s %s %s : %s" % (
                table, column_name, new_column_name, original_value
            )
            )
            continue
    op.drop_column(table, column_name)


def update_database_structure():
    logger = logging.getLogger(__name__)
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
    logger.debug("Migrating date columns")
    logger.debug(" + Projects")
    change_custom_date_type('project', 'starting_date', 'startingDate')
    change_custom_date_type('project', 'ending_date', 'endingDate')

    logger.debug(" + Customers")
    change_custom_date_type('customer', 'updated_at', 'updateDate')
    change_custom_date_type('customer', 'created_at', 'creationDate')

    logger.debug(" + Companies")
    change_custom_date_type('company', 'updated_at', 'updateDate')
    change_custom_date_type('company', 'created_at', 'creationDate')

    logger.debug(" + Task and TaskStatus")
    change_custom_date_type("task_status", "status_date", "statusDate")
    change_custom_date_type('task', "status_date", "statusDate")


def _user_exists(session, user_id):
    from autonomie.models.user import User
    query = session.query(User.id).filter_by(id=user_id)
    count_q = query.statement.with_only_columns([sa.func.count()]).order_by(
        None
    ).count()

    count = query.session.execute(count_q).scalar()
    return count


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
            if _user_exists(session, person_id) and status_date:
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


def _upgrade_invoices(connection):
    connection.execute(
        "UPDATE invoice JOIN task ON task.id=invoice.id "
        "SET invoice.paid_status=task.status "
        "WHERE status in ('paid', 'resulted');"
    )
    connection.execute(
        "UPDATE invoice JOIN task ON task.id=invoice.id "
        "SET invoice.paid_status='waiting' "
        "WHERE status NOT in ('paid', 'resulted');"
    )
    connection.execute(
        "UPDATE payment inner join ("
        "select task_id, status_person_id, status_date from task_status "
        "inner join accounts on accounts.id=task_status.status_person_id where task_status.status_code IN ('paid', 'resulted') "
        ") as s on payment.task_id=s.task_id AND DATE(payment.created_at)=status_date "
        "SET payment.user_id=status_person_id where payment.user_id is NULL;"
    )



def _upgrade_estimations(connection):
    for cmd in (
        "update estimation join task on task.id=estimation.id set estimation.signed_status='aborted' where task.status='aboest';",
        "update estimation join task on task.id=estimation.id set estimation.signed_status='waiting' where task.status!='aboest';",
        "update estimation join task on task.id=estimation.id set estimation.geninv=1 where task.status='geninv';",
        "update estimation join task on task.id=estimation.id set estimation.geninv=0 where task.status!='geninv';",
    ):
        connection.execute(cmd)


def _upgrade_expenses(connection):
    for cmd in (
        "update expense_sheet set paid_status=status where status in ('paid', 'resulted')",
        "update expense_payment inner join (select e.id, e.status_user_id from expense_sheet as e inner join accounts as a on e.status_user_id=a.id) as sheet on sheet.id=expense_payment.expense_sheet_id set expense_payment.user_id=sheet.status_user_id;",
        "update expense_sheet set paid_status='waiting' where status not in ('paid', 'resulted')",
        "update expense_sheet set status='valid' where status in ('paid', 'resulted')",
        "update expense_sheet set justified=0;",
    ):
        connection.execute(cmd)


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
    connection = op.get_bind()
    connection.execute("update customer set type_='company';")

    connection.execute(
        "UPDATE task INNER JOIN ( "
        "SELECT task_id, status_person_id, status_date from task_status inner join "
        "accounts on accounts.id=task_status.status_person_id where task_status.status_code='valid' "
        "ORDER BY status_date DESC LIMIT 1 "
        ") as s on s.task_id=task.id "
        "SET task.status_person_id=s.status_person_id, task.status_date=s.status_date "
        "where task.status IN ('paid', 'resulted', 'aboinv', 'geninv', 'aboest');"
    )
    _upgrade_invoices(connection)
    _upgrade_estimations(connection)
    _upgrade_expenses(connection)
    _upgrade_estimation_payment_dates(session)
    session.flush()
    drop_old_columns()
    connection.execute(
        "UPDATE task "
        "SET status='valid' "
        "WHERE status IN ('paid', 'resulted', 'aboinv', 'geninv', 'aboest')"
    )


def upgrade():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    update_database_structure()
    migrate_datas(session)


def downgrade():
    print("No downgrade supported for this upgrade")
