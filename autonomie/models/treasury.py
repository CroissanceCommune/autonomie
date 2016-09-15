# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2016 Croissance Commune
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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

import deform_extensions
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
)
from autonomie.models.base import (
    DBBASE,
    default_table_args,
)


GRID = (
    (('title', 6),),
    (('compte_cg_debit', 6), ('compte_cg_credit', 6),),
    (('label_template', 6), ('percentage', 6),),
    (('enabled', 6),),
)


class CustomInvoiceBookEntryModule(DBBASE):
    """
    An Invoice Export module configuration

    :param compte_cg_credit: The account used for 'credit'
    :param compte_cg_debit: The account used for 'debit'
    :param label_template: The label template used for this module
    :param int percentage: The percentage that should be used in this module
    """
    __colanderalchemy_config__ = {
        "title": u"un module de contribution personnalisé",
        "validation_msg": u"Vos modules de contribution ont bien été \
configurés",
        "help_msg": u"""Configurez des modules de contribution personnalisés.
Ceux-ci viennent apporter de nouvelles lignes de contribution dans les \
exports des factures.
        <h4>Configuration</h4>\
        <ul> \
        <li>Un titre</li>\
        <li>Le compte général auquel la contribution est associé</li>\
        <li>Le compte de contrepartie</li>\
        <li>Un gabarit pour la génération des libellés (voir ci-dessous pour \
les variables associées)</li>\
        <li>Un taux de contribution (pourcentage prélevé sur le <b>HT</b>)</li>\
        </ul>\
        Pour chaque module, 8 lignes seront générées (4 lignes \
analytiques et 4 lignes générales).
        Le montant du débit et du crédit seront calculés selon le pourcentage \
indiqué (taux de contribution).
        <h4>Variable utilisable dans les gabarits de libellés</h4>\
        <ul>\
        <li>client.name</li>\
        <li>entreprise.name</li>\
        <li>numero_facture</li>\
        </ul>
        <h4>Utilisation des variables</h4>\
        Les variables s'utilise au sein des gabarits de libellés en les \
entourant par des accolades {}.
        ex : "Contribution {entreprise.name} {client.name} {numero_facture}"
        """,
        'widget': deform_extensions.GridMappingWidget(named_grid=GRID)
    }
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}}
    )
    title = Column(
        String(100),
        info={
            'colanderalchemy': {
                'title': u"Nom du module",
            }
        }
    )
    active = Column(
        Boolean(),
        default=True,
        info={
            'colanderalchemy': {
                'exclude': True,
                'title': u'Is this module unactivated (deleted)'
            }
        },
    )
    enabled = Column(
        Boolean(),
        default=True,
        info={
            'colanderalchemy': {
                'title': u"Activer le module ?",
                "description": u"Si ce module est actif, les écritures seront \
produites dans les prochains exports de facture."
            }
        },
    )
    compte_cg_credit = Column(
        String(100),
        nullable=False,
        info={
            'colanderalchemy': {
                'title': u"Compte de contrepartie",
                "description": u"Compte utilisé pour les lignes de crédit",
            }
        },
    )
    compte_cg_debit = Column(
        String(100),
        nullable=False,
        info={
            'colanderalchemy': {
                'title': u"Compte de charge",
                "description": u"Compte utilisé pour les lignes de débit",
            }
        },
    )
    label_template = Column(
        String(100),
        nullable=False,
        info={
            'colanderalchemy': {
                'title': u"Gabarit pour les libellés d'écriture",
                'description': u"Les variables disponibles \
pour la génération des écritures sont décrites en haut de page"
            }
        },
    )
    percentage = Column(
        Integer,
        nullable=False,
        info={
            'colanderalchemy': {
                'title': u"Taux de contribution de ce module",
                'description': u"Valeur numérique utilisée pour calculer le \
pourcentage du montant HT prélevé par le biais de ce module"
            }
        },
    )

    @classmethod
    def query(cls, include_inactive=False, *args):
        q = super(CustomInvoiceBookEntryModule, cls).query(*args)
        if not include_inactive:
            q = q.filter(CustomInvoiceBookEntryModule.active == True)
        return q
