"""4.2.0 : migrate mentions

Revision ID: 2e4c3172fc54
Revises: 11a62732db65
Create Date: 2018-06-08 11:30:11.574174

"""

# revision identifiers, used by Alembic.
revision = '2e4c3172fc54'
down_revision = '11a62732db65'

from alembic import op
import sqlalchemy as sa


def update_database_structure():
    pass

def migrate_datas():
    from autonomie.models.project.types import BusinessType
    from autonomie.models.config import Config
    from autonomie.models.task.mentions import TaskMention
    from autonomie.models.project.mentions import BusinessTypeTaskMention
    from autonomie_base.models.base import DBSESSION
    from alembic.context import get_bind
    session = DBSESSION()
    conn = get_bind()

    # Collect business type ids
    business_type_ids = [b[0] for b in session.query(BusinessType.id)]

    # for each fixed config key we now use mentions
    for doctype, key, label, title in (
        (
            'estimation',
            'coop_estimationfooter',
            u"Informations sur l'acceptation des devis",
            u"Acceptation du devis",
        ),
        (
            "invoice",
            "coop_invoicepayment",
            u"Informations de paiement pour les factures",
            u"Mode de paiement",
        ),
        (
            "invoice",
            "coop_invoicelate",
            u"Informations sur les retards de paiement",
            u"Retard de paiement",
        )
    ):
        # We retrieve the configurated value
        value = Config.get_value(key, "")
        mention = TaskMention(
            label=label,
            title=title,
            full_text=value.replace(
                '%IBAN%', "{IBAN}").replace(
                    '%RIB%', "{RIB}").replace(
                        '%ENTREPRENEUR%', '{name}')
        )
        session.add(mention)
        session.flush()

        for btype_id in business_type_ids:
            rel = BusinessTypeTaskMention(
                task_mention_id=mention.id,
                business_type_id=btype_id,
                doctype=doctype,
                mandatory=True,
            )
            session.add(rel)
            session.flush()

        op.execute(
            u"INSERT INTO mandatory_task_mention_rel (task_id, mention_id) \
    SELECT task.id, {mention_id} from task join node on task.id=node.id where \
    node.type_='{type_}'".format(mention_id=mention.id, type_=doctype)
        )

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    pass
