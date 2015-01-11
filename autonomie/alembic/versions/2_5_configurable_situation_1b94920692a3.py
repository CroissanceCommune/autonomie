#-*-coding:utf-8-*-
"""2.5 : refactor userdatas situations and roles

Revision ID: 1b94920692a3
Revises: 46beb4c6f140
Create Date: 2014-12-28 14:56:11.070890

"""

# revision identifiers, used by Alembic.
revision = '1b94920692a3'
down_revision = '46beb4c6f140'

from alembic import op
import sqlalchemy as sa

SITUATION_OPTIONS = (
    ('reu_info', u"Réunion d'information",),
    ("entretien", u"Entretien",),
    ("integre", u"Intégré",),
    ("sortie", u"Sortie",),
    ("refus", u"Refus",),
)


def upgrade():
    from alembic.context import get_bind
    op.add_column(
        "user_datas",
        sa.Column(
            "situation_situation_id",
            sa.Integer,
            sa.ForeignKey("cae_situation_option.id"),
        )
    )
    op.add_column(
        "configurable_option",
        sa.Column(
            "order",
            sa.Integer,
            default=0
        )
    )

    from autonomie.models.user import (
        CaeSituationOption,
    )
    from autonomie.models.base import DBSESSION
    temp_dict = {}
    for key, value in SITUATION_OPTIONS:
        if key == "integre":
            option = CaeSituationOption(label=value, is_integration=True)
        else:
            option = CaeSituationOption(label=value)
        DBSESSION().add(option)
        DBSESSION().flush()
        temp_dict[key] = option.id

    conn = get_bind()
    query = "select id, situation_situation from user_datas"
    result = conn.execute(query)

    for id, situation in result:
        option_id = temp_dict.get(situation)
        if option_id is None:
            continue
        query = "update user_datas set situation_situation_id='{0}' \
where id='{1}'".format(option_id, id)
        op.execute(query)


def downgrade():
    op.drop_column("user_datas", "situation_situation_id")
    op.execute("delete from cae_situation_option")
