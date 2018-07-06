# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from transaction import commit
import sqlalchemy

from autonomie_base.models.base import DBSESSION


logger = logging.getLogger(__name__)

GROUPS = (
    {
        'name': 'manager',
        'label': u"Est membre de l'équipe d'appui",
        'primary': True,
    },
    {
        'name': 'admin',
        'label': u"Administre l'application",
        "primary": True,
    },
    {
        'name': 'contractor',
        'label': u'Entrepreneur de la coopérative',
        'primary': True
    },
    {
        'name': 'estimation_validation',
        'label': u"Peut valider ses propres devis",
    },
    {
        'name': 'invoice_validation',
        'label': u"Peut valider ses propres factures",
    },
    {
        'name': 'estimation_only',
        'label': u"Ne peut pas créer de factures sans devis",
    },
    {
        'name': "payment_admin",
        'label': u"Peut saisir/modifier/supprimer les paiements \
de ses factures",
    },
    {
        'name': 'trainer',
        'label': u"Formateur",
    },
    {
        'name': 'constructor',
        'label': u"Peut initier des chantiers",
    },
)


def populate_cae_situations_and_career_stages(session):
    """
    Populate the database with default CAE situation options and career stages
    """
    # Populate CAE situations
    from autonomie.models.user.userdatas import CaeSituationOption
    query = session.query(CaeSituationOption)
    if query.count() == 0:
        situation_cand = CaeSituationOption(label=u"Candidat", order=0)
        situation_conv = CaeSituationOption(label=u"En convention", is_integration=True, order=1)
        situation_es = CaeSituationOption(label=u"Entrepreneur salarié", is_integration=True, order=2)
        situation_out = CaeSituationOption(label=u"Sortie", order=3)
        session.add(situation_cand)
        session.add(situation_conv)
        session.add(situation_es)
        session.add(situation_out)
        session.flush()
    # Populate Career Stages
    from autonomie.models.career_stage import CareerStage
    if CareerStage.query().count() == 0:
        for active, name, cae_situation_id, stage_type in (
            (True, "Diagnostic", None, None),
            (True, "Contrat CAPE", situation_conv.id, "entry"),
            (True, "Contrat CESA", situation_es.id, "contract"),
            (True, "Avenant contrat", None, "amendment"),
            (True, "Sortie", situation_out.id, "exit"),
        ):
            session.add(
                CareerStage(
                    active=active, 
                    name=name, 
                    cae_situation_id=cae_situation_id, 
                    stage_type=stage_type, 
                )
            )
        session.flush()


def populate_groups(session):
    """
    Populate the groups in the database
    """
    from autonomie.models.user.group import Group
    for group in GROUPS:
        if session.query(Group.id).filter(
            Group.name == group['name']
        ).count() == 0:
            session.add(Group(**group))
    session.flush()


def populate_accounting_treasury_measure_types(session):
    """
    Populate the database with treasury measure types
    """
    from autonomie.models.config import Config
    from autonomie.models.accounting.treasury_measures import (
        TreasuryMeasureType,
    )
    if TreasuryMeasureType.query().count() == 0:
        for internal_id, start, label in (
            (1, '5', u"Trésorerie du jour",),
            (2, "42,-421,-425,43,44", u"Impôts, taxes et cotisations dues",),
            (3, "40", u"Fournisseurs à payer",),
            (5, "421", u"Salaires à payer",),
            (6, "41", u"Clients à encaisser"),
            (7, '425', u"Notes de dépenses à payer"),
            (9, "1,2,3", u"Comptes bilan non pris en compte"),
        ):
            session.add(
                TreasuryMeasureType(
                    internal_id=internal_id, account_prefix=start, label=label
                )
            )
        Config.set("treasury_measure_ui", "1")
        session.flush()


def populate_accounting_income_statement_measure_types(session):
    """
    Populate the database with treasury measure types
    """
    from autonomie.models.accounting.income_statement_measures import (
        IncomeStatementMeasureTypeCategory,
    )
    if IncomeStatementMeasureTypeCategory.query().count() == 0:
        for order, category in enumerate((
            u"Produits",
            u"Achats",
            u"Charges",
            u"Salaires et Cotisations"
        )):
            session.add(
                IncomeStatementMeasureTypeCategory(label=category, order=order)
            )
        session.flush()


def populate_bookentry_config(session):
    from autonomie.models.config import Config
    initial_values = [
        (
            'bookentry_facturation_label_template',
            '{invoice.customer.label} {company.name}'
        ),
        (
            'bookentry_contribution_label_template',
            "{invoice.customer.label} {company.name}"
        ),
        (
            'bookentry_rg_interne_label_template',
            "RG COOP {invoice.customer.label} {company.name}"
        ),
        (
            'bookentry_rg_client_label_template',
            "RG {invoice.customer.label} {company.name}"
        ),
        (
            'bookentry_expense_label_template',
            "{beneficiaire}/frais {expense_date:%-m %Y}"
        ),
        (
            'bookentry_payment_label_template',
            "{company.name} / Rgt {invoice.customer.label}"
        ),
        (
            'bookentry_expense_payment_main_label_template',
            "{beneficiaire_LASTNAME} / REMB FRAIS {expense_date:%B/%Y}"
        ),
        (
            'bookentry_expense_payment_waiver_label_template',
            "Abandon de créance {beneficiaire_LASTNAME} {expense_date:%B/%Y}"
        ),

    ]

    for key, val in initial_values:
        Config.set(key, val)


def populate_project_types(session):
    from autonomie.models.project.types import (
        ProjectType,
        BusinessType,
    )
    for name, label, subtype_label, private, default in (
        ("default", u"Projet classique", "Affaire simple", False, True,),
        ("training", u"Convention de formation", "Formation", True, False),
        ("construction", u"Chantiers", u"Chantier", True, False),
    ):
        ptype = ProjectType.query().filter_by(name=name).first()
        if ptype is None:
            ptype = ProjectType(
                name=name,
                label=label,
                editable=False,
                private=private,
                default=default,
            )
            session.add(ptype)
            session.flush()
            if name is not 'default':
                default_btype = BusinessType.query().filter_by(
                    name='default').first()
                default_btype.other_project_types.append(ptype)
                session.merge(default_btype)
                session.flush()
        if BusinessType.query().filter_by(name=name).count() == 0:
            session.add(
                BusinessType(
                    name=name,
                    label=subtype_label,
                    editable=False,
                    private=private,
                    project_type_id=ptype.id,
                )
            )
    session.flush()


def populate_contract_types(session):
    """
    Populate the database with default contract types
    """
    from autonomie.models.career_path import TypeContratOption
    if session.query(TypeContratOption).filter("label"=="CDD").count() == 0:
        session.add(TypeContratOption(label=u"CDD", order=0))
    if session.query(TypeContratOption).filter("label"=="CDI").count() == 0:
        session.add(TypeContratOption(label=u"CDI", order=0))
    if session.query(TypeContratOption).filter("label"=="CESA").count() == 0:
        session.add(TypeContratOption(label=u"CESA", order=0))
    session.flush()

def populate_invoice_number_template(session):
    from autonomie.models.config import Config
    if not Config.get_value("invoice_number_template"):
        Config.set("invoice_number_template", "{SEQGLOBAL}")
    session.flush()


def populate_database():
    """
    Populate the database with default values
    """
    logger.debug("Populating the database")
    session = DBSESSION()
    for func in (
        populate_cae_situations_and_career_stages,
        populate_groups,
        populate_accounting_treasury_measure_types,
        populate_accounting_income_statement_measure_types,
        populate_bookentry_config,
        populate_project_types,
        populate_contract_types,
        populate_invoice_number_template,
    ):
        try:
            func(session)
        except sqlalchemy.exc.OperationalError as e:
            print("There is an error in the population process :")
            print(e)
    commit()
