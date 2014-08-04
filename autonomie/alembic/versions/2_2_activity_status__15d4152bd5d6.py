"""2.2 : activity status and participants

Revision ID: 15d4152bd5d6
Revises: b04de7c28
Create Date: 2014-06-23 17:55:00.671922

"""

# revision identifiers, used by Alembic.
revision = '15d4152bd5d6'
down_revision = 'b04de7c28'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from autonomie.models.activity import Attendance, Activity
    from autonomie.models import DBSESSION
    from alembic.context import get_bind

    session = DBSESSION()

    # Migrating attendance relationship
    query = "select event.id, event.status, rel.account_id, rel.activity_id from activity_participant rel inner join activity on rel.activity_id=activity.id LEFT JOIN event on event.id=activity.id"
    conn = get_bind()
    result = conn.execute(query)

    for event_id, status, user_id, activity_id in result:
        if status == 'planned':
            user_status = 'registered'

        elif status == 'excused':
            user_status = 'excused'
            status = 'cancelled'

        elif status == 'closed':
            user_status = 'attended'

        elif status == 'absent':
            user_status = 'absent'
            status = 'cancelled'

        # create attendance for each participant
        a = Attendance()
        a.status = user_status
        a.account_id = user_id
        a.event_id = activity_id
        session.add(a)
        session.flush()

        # Update the event's status regarding the new norm
        query = "update event set status='{0}' where id='{1}';".format(
            status, event_id,)
        op.execute(query)

    # Migrating activity to add duration and use datetimes
    op.add_column('activity', sa.Column('duration', sa.Integer, default=0))
    op.alter_column(
        'event',
        'date',
        new_column_name='datetime',
        type_=sa.DateTime()
    )

    query = "select id, conseiller_id from activity;"
    result = conn.execute(query)

    values = []
    for activity_id, conseiller_id in result:
        values.append("(%s, %s)" % (activity_id, conseiller_id))
    if values != []:
        query = "insert into activity_conseiller (`activity_id`, `account_id`) \
VALUES {0}".format(','.join(values))
        op.execute(query)

    op.execute("alter table activity drop foreign key `activity_ibfk_2`;")

    op.drop_column('activity', 'conseiller_id')
    op.drop_table('activity_participant')


def downgrade():
    pass
