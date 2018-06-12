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

STAGE_TYPE_OPTIONS = (
    ('', 'Autre',),
    ('entry', u'Entrée CAE',),
    ('contract', u'Contrat de travail',),
    ('amendment', u'Avenant contrat de travail',),
    ('exit', u'Sortie CAE',),
)

CAREER_STAGE_GRID = (
    (('active',12),),
    (('name',12),),
    (('cae_situation_id',12),),
    (('stage_type',12),)
)

class CareerStage(DBBASE):
    """
    Different career stages
    """
    __colanderalchemy_config__ = {
        'validation_msg': u"Les étapes de parcours ont bien été configurées",
        'widget': deform_extensions.GridFormWidget(named_grid=CAREER_STAGE_GRID)
    }
    __tablename__ = 'career_stage'
    __table_args__ = default_table_args
    id = Column(
        'id',
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': {'widget': deform.widget.HiddenWidget()}
        },
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
        String(100),
        nullable=False,
        info={
            'colanderalchemy': {'title': u"Libellé de l'étape"}
        },
    )
    cae_situation_id = Column(
        ForeignKey("cae_situation_option.id"),
        info={
            'colanderalchemy': {
                'title': u"Nouvelle situation dans la CAE",
                'description': u"Lorsque cette étape sera affectée à un \
porteur de projet cette situation lui sera automatiquement attribuée"
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
    stage_type = Column(
        String(15),
        info={
            'colanderalchemy': {'title': u"Type d'étape"},
            'export': {
                'formatter': lambda val: dict(STAGE_TYPE_OPTIONS).get(val),
                'stats': {'options': STAGE_TYPE_OPTIONS},
            }
        }
    )

    @classmethod
    def query(cls, include_inactive=False):
        q = super(CareerStage, cls).query()
        if not include_inactive:
            q = q.filter(CareerStage.active == True)
        return q.order_by('name')
