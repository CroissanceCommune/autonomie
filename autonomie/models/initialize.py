# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    Initialization function
"""
import sqlalchemy

from autonomie.models.base import DBSESSION
from autonomie.models.base import DBBASE
from autonomie.scripts.migrate import fetch_head


GROUPS = (
    ('estimation_validation', u"Peut valider ses propres devis", ),
    ('invoice_validation', u"Peut valider ses propres factures", ),
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
    if query.filter(CaeSituationOption.is_integration==True).count() == 0:
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
    if Group.query().count() == 0:
        for name, label in GROUPS:
            session.add(Group(name=name, label=label))
        session.flush()


def populate_config(session):
    """
    Initialize required configuration elements
    """
    for func in (populate_situation_options, populate_groups):
        try:
            func(session)
        except sqlalchemy.exc.OperationalError as e:
            print("The seem to be an error in the population process")
            print(e)

    from transaction import commit
    commit()


def initialize_sql(engine):
    """
        Initialize the database engine
    """
    DBSESSION.configure(bind=engine)
    DBBASE.metadata.bind = engine
    if not engine.table_names():
        fetch_head()

    import logging
    logger = logging.getLogger(__name__)
    logger.debug("Setting the metadatas")
    DBBASE.metadata.create_all(engine)
    from transaction import commit
    commit()

    logger.debug("Populating the config")
    populate_config(DBSESSION())
    return DBSESSION
