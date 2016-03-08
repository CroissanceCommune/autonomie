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


def upgrade():
    from autonomie.models.user import User, Group
    from autonomie.models.base import DBSESSION

    session = DBSESSION()
    for group_id, group_name, group_label in GROUPS:
        group = session.query(Group.id).filter(Group.name==group_name).first()
        if group is None:
            group = Group(name=group_name, label=group_label)
            session.add(group)
            session.flush()

        users = session.query(User).filter(User.primary_group==group_id)
        for user in users:
            user._groups.append(group)
            session.merge(user)


def downgrade():
    pass
