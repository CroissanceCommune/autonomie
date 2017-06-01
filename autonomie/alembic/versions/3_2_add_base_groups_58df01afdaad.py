# -*- coding: utf-8 -*-
"""3.2 : add_base_groups

Revision ID: 58df01afdaad
Revises: 480d66cbb4c4
Create Date: 2016-03-03 20:05:57.369844

"""

# revision identifiers, used by Alembic.
revision = '58df01afdaad'
down_revision = '480d66cbb4c4'

from alembic import op
import sqlalchemy as sa

GROUPS = (
    (3, 'contractor', u"Porteur de projet", ),
    (2, 'manager', u"Est membre de l'équipe d'appui", ),
    (1, 'admin', u"Administre l'application", ),
)

def disable_listeners():
    from autonomie.models.task.task import Task, cache_amounts
    sa.event.remove(Task, "before_insert", cache_amounts)
    sa.event.remove(Task, "before_update", cache_amounts)


def upgrade():
    disable_listeners()
    op.add_column('task', sa.Column('date', sa.Date()))
    from autonomie.models.task import Task
    from autonomie_base.models.base import DBSESSION

    session = DBSESSION()
    for task in Task.query().filter(Task.type_!='manualinvoice'):
        task.date = task.taskDate
        session.merge(task)
    session.flush()

    op.execute("alter table groups modify label VARCHAR(255);")
    op.execute("alter table payment modify remittance_amount VARCHAR(255);")
    from autonomie.models.user import User, Group
    for group_id, group_name, group_label in GROUPS:
        group = session.query(Group).filter(Group.name==group_name).first()
        if group is None:
            group = Group(name=group_name, label=group_label)
            session.add(group)
            session.flush()

        users = session.query(User).filter(User.primary_group==group_id)
        for user in users:
            user._groups.append(group)
            session.merge(user)

    label = u"Peut saisir/modifier/supprimer les paiements de ses factures"
    group_name = "payment_admin"
    group = Group.query().filter(Group.name==group_name).first()
    if group is not None:
        group.label = label
        session.merge(group)


def downgrade():
    pass
