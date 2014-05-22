"""1.9.1 : Add a configurable activity fse type

Revision ID: 1b3d5402f3e4
Revises: 1ca3a6ef9c9d
Create Date: 2014-05-19 15:21:02.209831

"""

# revision identifiers, used by Alembic.
revision = '1b3d5402f3e4'
down_revision = '1ca3a6ef9c9d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from autonomie.models import DBSESSION
    session = DBSESSION()
    from autonomie.models.activity import ActivityAction
    from alembic.context import get_bind
    for name in "subaction_id", "action_id":
        col = sa.Column(name, sa.Integer, sa.ForeignKey("activity_action.id"))
        op.add_column("activity", col)

    label_request = "select id, action_label, subaction_label from activity"

    conn = get_bind()
    result = conn.execute(label_request)

    already_added = {}

    for id, action_label, subaction_label in result:
        if (action_label, subaction_label) not in already_added.keys():
            found = False
            for key, value in already_added.items():
                if action_label == key[0]:
                    action_id = value[0]
                    found = True
            if not found:
                action = ActivityAction(label=action_label)
                session.add(action)
                session.flush()
                action_id = action.id
            subaction = ActivityAction(label=subaction_label, parent_id=action_id)
            session.add(subaction)
            session.flush()
            subaction_id = subaction.id
            already_added[(action_label, subaction_label)] = (action_id, subaction_id)
        else:
            action_id, subaction_id = already_added[(action_label, subaction_label)]

        op.execute("update activity set action_id={0}, subaction_id={1} \
where id={2}".format(action_id, subaction_id, id))


def downgrade():
    op.drop_column("activity", "action_id")
    op.drop_column("activity", "subaction_id")
    op.drop_table('activity_action')
