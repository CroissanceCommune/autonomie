#-*-coding:utf-8-*-
"""2.7.1 : add_columns

Revision ID: 36b1d9c38c43
Revises: 577f50e908d1
Create Date: 2015-04-09 16:52:36.065153

"""

# revision identifiers, used by Alembic.
revision = '36b1d9c38c43'
down_revision = '577f50e908d1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from autonomie_base.models.base import DBSESSION
    from autonomie.models.workshop import WorkshopAction
    from alembic.context import get_bind
    session = DBSESSION()
    conn = get_bind()

    col = sa.Column('activity_id', sa.Integer(), sa.ForeignKey('company_activity.id'))
    op.add_column('company_datas', col)
    col = sa.Column('archived', sa.Boolean(), default=False, server_default="0")
    op.add_column('customer', col)


    # Migration de accompagnement_header.png en activity_header.png
    op.execute('update config_files set config_files.key="activity_header_img.png" where \
config_files.key="accompagnement_header.png";')

    # Le bas de page des pdfs est celui par defaut pour les ateliers et rdv
    from autonomie.models.config import Config
    val = Config.get('coop_pdffootertext').value
    if val:
        for key in ('activity', 'workshop'):
            config_key = '%s_footer' % key
            config = Config.set(config_key, val)

    # Migration de la taille des libelles pour les actions des rendez-vous
    op.execute("alter table activity_action modify label VARCHAR(255)")
    # Migration des intitules des ateliers
    # 1- Ajout des nouvelles foreignkey
    for name in 'info1_id', 'info2_id', 'info3_id':
        col = sa.Column(name, sa.Integer, sa.ForeignKey("workshop_action.id"))
        op.add_column("workshop", col)

    # 2- création des options en fonction des valeurs en durs
    request = "select id, info1, info2, info3 from workshop"
    result = conn.execute(request)

    already_added = {}

    for id, info1, info2, info3 in result:
        info1 = info1.lower()
        info2 = info2.lower()
        info3 = info3.lower()
        info1_id = info2_id = info3_id = None
        if (info1, info2, info3) not in already_added.keys():

            for key, value in already_added.items():
                if key[0] == info1 and info1:
                    info1_id = value[0]
                    if key[1] == info2 and info2:
                        info2_id = value[1]

            if info1_id is None and info1:
                w = WorkshopAction(label=info1)
                session.add(w)
                session.flush()
                info1_id = w.id

            if info2_id is None and info2:
                w = WorkshopAction(label=info2, parent_id=info1_id)
                session.add(w)
                session.flush()
                info2_id = w.id

            if info3:
                w = WorkshopAction(label=info3, parent_id=info2_id)
                session.add(w)
                session.flush()
                info3_id = w.id
            already_added[(info1, info2, info3)] = (info1_id, info2_id, info3_id,)
        else:
            info1_id, info2_id, info3_id = already_added[(info1, info2, info3)]

        request = "update workshop "
        if info1_id:
            request += "set info1_id={0}".format(info1_id)
            if info2_id:
                request += ", info2_id={0}".format(info2_id)
                if info3_id:
                    request += ", info3_id={0}".format(info3_id)
            request +=  " where id={0}".format(id)
            op.execute(request)


def downgrade():
    op.drop_column('customer', 'archived')
    for i in ('info1_id', 'info2_id', 'info3_id',):
        op.drop_column('workshop', i)
