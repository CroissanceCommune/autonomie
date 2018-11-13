#-*-coding:utf-8-*-
"""4.2.0 Migrate parcours data

Revision ID: 2a66d798c55d
Revises: 44f964dc36a2
Create Date: 2018-06-20 13:56:49.344898

"""

# revision identifiers, used by Alembic.
revision = '2a66d798c55d'
down_revision = '44f964dc36a2'

from alembic import op
import sqlalchemy as sa
from autonomie_base.models.base import DBSESSION
from autonomie.alembic.utils import (
    disable_constraints,
    enable_constraints,
    column_exists,
)


def populate_default_datas():
    """
    Populate the database with missing default entries if needed
    """
    from autonomie.models.user.userdatas import CaeSituationOption
    from autonomie.models.career_stage import CareerStage
    from autonomie.models.career_path import TypeContratOption
    session = DBSESSION()
    # Populate contract types
    if session.query(TypeContratOption).filter(TypeContratOption.label=="CDD").count() == 0:
        session.add(TypeContratOption(label=u"CDD", order=0))
    if session.query(TypeContratOption).filter(TypeContratOption.label=="CDI").count() == 0:
        session.add(TypeContratOption(label=u"CDI", order=0))
    if session.query(TypeContratOption).filter(TypeContratOption.label=="CESA").count() == 0:
        session.add(TypeContratOption(label=u"CESA", order=0))
    session.flush()
    # Populate CAE situations
    situation_cand = session.query(CaeSituationOption).filter(CaeSituationOption.label=="Candidat").first()
    if situation_cand is None:
        situation_cand = CaeSituationOption(label=u"Candidat", order=0)
        session.add(situation_cand)
    situation_conv = session.query(CaeSituationOption).filter(CaeSituationOption.label=="En convention").first()
    if situation_conv is None:
        situation_conv = CaeSituationOption(label=u"En convention", is_integration=True)
        session.add(situation_conv)
    situation_es = session.query(CaeSituationOption).filter(CaeSituationOption.label=="Entrepreneur salarié").first()
    if situation_es is None:
        situation_es = CaeSituationOption(label=u"Entrepreneur salarié", is_integration=True)
        session.add(situation_es)
    situation_out = session.query(CaeSituationOption).filter(CaeSituationOption.label=="Sortie").first()
    if situation_out is None:
        situation_out = CaeSituationOption(label=u"Sortie")
        session.add(situation_out)
    session.flush()
    # Populate Career Stages
    if CareerStage.query().count() == 0:
        stage_diag = CareerStage(active=True,
                    name="Diagnostic",
                    cae_situation_id=None,
                    stage_type=None,
                )
        stage_cape = CareerStage(active=True,
                    name="Contrat CAPE",
                    cae_situation_id=situation_conv.id,
                    stage_type="entry",
                )
        stage_dpae = CareerStage(active=True,
                    name="Contrat DPAE",
                    cae_situation_id=None,
                    stage_type=None,
                )
        stage_cesa = CareerStage(active=True,
                    name="Contrat CESA",
                    cae_situation_id=situation_es.id,
                    stage_type="contract",
                )
        stage_avct = CareerStage(active=True,
                    name="Avenant contrat",
                    cae_situation_id=None,
                    stage_type="amendment",
                )
        stage_out = CareerStage(active=True,
                    name="Sortie",
                    cae_situation_id=situation_out.id,
                    stage_type="exit",
                )
        session.add(stage_diag)
        session.add(stage_cape)
        session.add(stage_dpae)
        session.add(stage_cesa)
        session.add(stage_avct)
        session.add(stage_out)
        session.flush()
    return (
        situation_conv.id,
        situation_es.id,
        situation_out.id
    ), (
        stage_diag.id,
        stage_cape.id,
        stage_dpae.id,
        stage_cesa.id,
        stage_avct.id,
        stage_out.id,
    )


def migrate_datas(situations_ids, stages_ids):
    """
    Migrate parcours's data from user_datas and related tables to career_path
    """
    from autonomie.models.career_path import CareerPath
    session = DBSESSION()
    cnx = op.get_bind()
    userdatas = cnx.execute("SELECT \
        id,\
        parcours_contract_type,\
        parcours_start_date,\
        parcours_end_date,\
        parcours_last_avenant,\
        parcours_taux_horaire,\
        parcours_taux_horaire_letters,\
        parcours_num_hours,\
        parcours_salary,\
        parcours_salary_letters,\
        parcours_employee_quality_id,\
        sortie_date,\
        sortie_motif_id,\
        sortie_type_id \
        FROM user_datas")
    for u in userdatas:
        # Diagnotic
        diagnotics = cnx.execute("SELECT date FROM date_diagnostic_datas WHERE date>'2000-01-01' AND userdatas_id=%s" % u.id)
        for diagnotic in diagnotics:
            session.add(CareerPath(userdatas_id=u.id, career_stage_id=stages_ids[0], start_date=diagnotic.date))
        # CAPE
        capes = cnx.execute("SELECT date, end_date FROM date_convention_cape_datas WHERE date>'2000-01-01' AND userdatas_id=%s" % u.id)
        for cape in capes:
            session.add(CareerPath(
                userdatas_id=u.id,
                career_stage_id=stages_ids[1],
                start_date=cape.date,
                end_date=cape.end_date,
                cae_situation_id=situations_ids[0],
                stage_type="entry"
            ))
        # DPAE
        dpaes = cnx.execute("SELECT date FROM date_dpae_datas WHERE date>'2000-01-01' AND userdatas_id=%s" % u.id)
        for dpae in dpaes:
            session.add(CareerPath(userdatas_id=u.id, career_stage_id=stages_ids[2], start_date=dpae.date))
        # Contrat
        if u.parcours_start_date and u.parcours_contract_type is not None:
            from autonomie.models.career_path import TypeContratOption
            cdi_type = session.query(TypeContratOption).filter(
                TypeContratOption.label==u.parcours_contract_type.upper()
            ).first()
            if cdi_type:
                cdi_type_id = cdi_type.id
            else:
                cdi_type_id = None
            session.add(CareerPath(
                userdatas_id=u.id,
                career_stage_id=stages_ids[3],
                start_date=u.parcours_start_date,
                end_date=u.parcours_end_date,
                cae_situation_id=situations_ids[1],
                stage_type="contrat",
                type_contrat_id=cdi_type_id,
                employee_quality_id=u.parcours_employee_quality_id,
                taux_horaire=u.parcours_taux_horaire,
                num_hours=u.parcours_num_hours
            ))
        # Avenant contrat
        if u.parcours_last_avenant:
            avenants = cnx.execute("SELECT date, number FROM contract_history WHERE date>'2000-01-01' AND userdatas_id=%s" % u.id)
            for avenant in avenants:
                model_avenant = CareerPath(
                    userdatas_id=u.id,
                    career_stage_id=stages_ids[4],
                    start_date=avenant.date,
                    stage_type="amendment",
                    amendment_number=avenant.number
                )
                if u.parcours_last_avenant==avenant.date:
                    model_avenant.taux_horaire=u.parcours_taux_horaire
                    model_avenant.num_hours=u.parcours_num_hours
                session.add(model_avenant)
        # Sortie
        if u.sortie_date:
            session.add(CareerPath(
                userdatas_id=u.id,
                career_stage_id=stages_ids[5],
                start_date=u.sortie_date,
                cae_situation_id=situations_ids[2],
                stage_type="exit",
                type_sortie_id=u.sortie_type_id,
                motif_sortie_id=u.sortie_motif_id
            ))
        # Historique des situations
        changes = cnx.execute("SELECT date, situation_id FROM cae_situation_change WHERE date>'2000-01-01' AND userdatas_id=%s" % u.id)
        for change in changes:
            session.add(CareerPath(userdatas_id=u.id, start_date=change.date, cae_situation_id=change.situation_id))
        # Sauvegarde du parcours de l'utilisateur
        session.flush()


def clean_database():
    """
    Remove obsolete tables and columns
    """
    disable_constraints()
    op.drop_table('cae_situation_change')
    op.drop_table('contract_history')
    op.drop_table('date_convention_cape_datas')
    op.drop_table('date_diagnostic_datas')
    op.drop_table('date_dpae_datas')
    op.drop_constraint('fk_user_datas_parcours_employee_quality_id', 'user_datas', type_='foreignkey')
    if column_exists('user_datas', 'sortie_motif_id'):
        try:
            op.drop_constraint('fk_user_datas_sortie_motif_id', 'user_datas', type_='foreignkey')
        except:
            pass
        op.drop_column('user_datas', 'sortie_motif_id',)

    if column_exists('user_datas', 'sortie_type_id'):
        try:
            op.drop_constraint('fk_user_datas_sortie_type_id', 'user_datas', type_='foreignkey')
        except:
            pass
        op.drop_column('user_datas', 'sortie_type_id',)

    for column in (
        ('user_datas', 'parcours_contract_type',),
        ('user_datas', 'parcours_start_date',),
        ('user_datas', 'parcours_end_date',),
        ('user_datas', 'parcours_last_avenant',),
        ('user_datas', 'parcours_taux_horaire',),
        ('user_datas', 'parcours_taux_horaire_letters',),
        ('user_datas', 'parcours_num_hours',),
        ('user_datas', 'parcours_salary',),
        ('user_datas', 'parcours_salary_letters',),
        ('user_datas', 'parcours_employee_quality_id',),
        ('user_datas', 'sortie_date',),
        ('user_datas', 'sortie_motif_id',),
    ):
        if column_exists('user_datas', column):
            op.drop_column('user_datas', column)
    enable_constraints()


def upgrade():
    situations_id, stages_id = populate_default_datas()
    migrate_datas(situations_id, stages_id)
    clean_database()


def downgrade():
    pass
