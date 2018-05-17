# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * MICHEAU Paul <paul@kilya.biz>
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
    Model for career stages
"""
import colander
import deform
import deform_extensions
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Text,
    not_,
)
from sqlalchemy.orm import relationship
from autonomie.models.tools import get_excluded_colanderalchemy
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)

CAREER_STAGE_GRID = (
    (('active', 6,),),
    (('name', 12),),
    (('cae_situation_id', 12),),
    (('is_entree_cae', 4), ('is_contrat', 4), ('is_sortie', 4)),
)

class CareerStage(DBBASE):
    """
    Different career stages
    """
    __colanderalchemy_config__ = {
        'title': u"Etapes de parcours",
        'help_msg': u"Configurez les étapes de parcours qui pourront être ajoutées \
        aux dossiers des porteurs de projet.<br /><br /> \
        <b>Note :</b> La nouvelle situation dans la CAE correspond au statut du porteur \
        après l'affectation de l'étape.",
        'validation_msg': u"Les étapes de parcours ont bien été configurés",
        'widget': deform_extensions.GridFormWidget(named_grid=CAREER_STAGE_GRID)
    }
    __tablename__ = 'career_stage'
    __table_args__ = default_table_args
    id = Column(
        'id',
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}},
    )
    active = Column(
        Boolean(),
        default=True,
        info={
            'colanderalchemy': {'exclude': True}
        },
    )
    name = Column(
        "name",
        String(15),
        nullable=False,
        info={
            'colanderalchemy': {
                'title': u'Libellé de l\'étape',
                }
        },
    )
    cae_situation_id = Column(
        ForeignKey("cae_situation_option.id"),
        info={
            'colanderalchemy':
            {
                'title': u"Nouvelle situation dans la CAE",
                'description': u"Lorsque cette étape sera affectée à un \
porteur cette nouvelle situation sera proposée par défaut"
            }
        }
    )
    cae_situation = relationship(
        "CaeSituationOption",
        primaryjoin='CaeSituationOption.id==CareerStage.cae_situation_id',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u'Situation dans la CAE'
            ),
            'export': {'related_key': 'label'},
        },
    )
    is_entree_cae = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': '',
                'label': u'Correspond à une entrée dans la coopérative'
            }
        },
    )
    is_contrat = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': '',
                'label': u'Correspond à un contrat de travail'
            }
        },
    )
    is_sortie = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': '',
                'label': u'Correspond à une sortie de la coopérative'
            }
        },
    )

    @classmethod
    def query(cls, include_inactive=False):
        q = super(CareerStage, cls).query()
        if not include_inactive:
            q = q.filter(CareerStage.active == True)
        return q.order_by('name')
