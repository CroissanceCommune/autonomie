# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from transaction import commit
import sqlalchemy

from autonomie_base.models.base import DBSESSION
from autonomie_base.models.base import DBBASE


logger = logging.getLogger(__name__)

GROUPS = (
    ('estimation_validation', u"Peut valider ses propres devis", ),
    ('invoice_validation', u"Peut valider ses propres factures", ),
    (
        "payment_admin",
        u"Peut saisir/modifier/supprimer les paiements de ses factures",
    ),
    ('manager', u"Est membre de l'équipe d'appui", ),
    ('admin', u"Administre l'application", ),
    ('contractor', u'Entrepreneur de la coopérative',),
)


def populate_situation_options(session):
    """
    Populate the CAE situation options
    """
    from autonomie.models.user import CaeSituationOption
    query = session.query(CaeSituationOption)
    if query.filter(CaeSituationOption.is_integration == True).count() == 0:
        session.add(CaeSituationOption(
            label=u"Réunion d'information",
            order=0,
        ))
        session.add(CaeSituationOption(
            label=u"Intégré",
            is_integration=True,
            order=1,
        ))
        session.add(CaeSituationOption(
            label=u"Sortie",
            order=2,
        ))
        session.flush()


def populate_groups(session):
    """
    Populate the groups in the database
    """
    from autonomie.models.user import Group
    for name, label in GROUPS:
        if session.query(Group.id).filter(Group.name == name).count() == 0:
            session.add(Group(name=name, label=label))
    session.flush()


def populate_database():
    """
    Populate the database with default values
    """
    logger.debug("Populating the database")
    session = DBSESSION()
    for func in (populate_situation_options, populate_groups):
        try:
            func(session)
        except sqlalchemy.exc.OperationalError as e:
            print("The seem to be an error in the population process")
            print(e)

    commit()
