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
    Model for career path
"""
import logging
import deform
import deform_extensions
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    Date,
)
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship
from autonomie.models.tools import get_excluded_colanderalchemy
from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie.models.career_stage import STAGE_TYPE_OPTIONS

logger = logging.getLogger(__name__)

PERIOD_OPTIONS = (
    ('', '',),
    ('month', u'par mois',),
    ('quarter', u'par trimestre',),
    ('semester', u'par semestre',),
    ('year', u'par an',),
)

CAREER_PATH_GRID = (
    (('career_stage_id', 12), ),
    (('start_date', 6), ('end_date', 6)),
    (('cae_situation_id', 12), ),
    (('stage_type', 6), ),
    (('type_contrat_id', 6), ('employee_quality_id', 6)),
    (('taux_horaire', 6), ('num_hours', 6)),
    (('goals_amount', 6), ('goals_period', 6)),
    (('amendment_number', 6), ),
    (('type_sortie_id', 6), ('motif_sortie_id', 6)),
)


# CONFIGURABLE OPTIONS
###############################################################################
class TypeContratOption(ConfigurableOption):
    """
    Possible values for contract type
    """
    __colanderalchemy_config__ = {
        'title': u"Type de contrat",
        'validation_msg': u"Les types de contrat ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class EmployeeQualityOption(ConfigurableOption):
    """
    Different values for employee quality
    """
    __colanderalchemy_config__ = {
        'title': u"Qualité du salarié",
        'validation_msg': u"Les qualité du salarié ont bien été configurées",
        "help_msg": u"Configurer les options possibles pour définir la qualité\
 d'un salarié (cadre, employé ...)",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class TypeSortieOption(ConfigurableOption):
    """
    Possible values for exit type
    """
    __colanderalchemy_config__ = {
        'title': u"Type de sortie",
        'validation_msg': u"Les types de sortie ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class MotifSortieOption(ConfigurableOption):
    """
    Possible values for exit motivation
    """
    __colanderalchemy_config__ = {
        'title': u"Motif de sortie",
        'validation_msg': u"Les motifs de sortie ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


# CAREER PATH CLASS
###############################################################################
class CareerPath(DBBASE):
    """
    Different career path stages
    """
    __colanderalchemy_config__ = {
        'title': u"Etape de parcours",
        'help_msg': u"",
        'validation_msg': u"L'étape de parcours a bien été enregistrée",
        'widget': deform_extensions.GridFormWidget(named_grid=CAREER_PATH_GRID)
    }
    __tablename__ = 'career_path'
    __table_args__ = default_table_args
    id = Column(
        'id',
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}},
    )
    userdatas_id = Column(
        ForeignKey('user_datas.id', ondelete="CASCADE"),
        info={
            'colanderalchemy': {'exclude': True},
            'export': {
                'label': u"Identifiant Autonomie",
                'stats': {'exclude': True},
            }
        },
    )
    userdatas = relationship(
        'UserDatas',
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        },
        back_populates="career_paths",
    )
    start_date = Column(
        Date(),
        nullable=False,
        info={'colanderalchemy': {'title': u"Date d'effet"}}
    )
    end_date = Column(
        Date(),
        info={'colanderalchemy': {'title': u"Date d'échéance"}}
    )
    career_stage_id = Column(
        ForeignKey('career_stage.id'),
        info={'colanderalchemy': {'title': u"Type d'étape"}}
    )
    career_stage = relationship(
        'CareerStage',
        primaryjoin='CareerStage.id==CareerPath.career_stage_id',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u'Etape de parcours'
            ),
            'export': {'related_key': 'label'},
        },
    )
    cae_situation_id = Column(
        ForeignKey('cae_situation_option.id'),
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
        'CaeSituationOption',
        primaryjoin='CaeSituationOption.id==CareerPath.cae_situation_id',
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
    type_contrat_id = Column(
        ForeignKey('type_contrat_option.id'),
        info={'colanderalchemy': {'title': u"Type de contrat"}}
    )
    type_contrat = relationship(
        'TypeContratOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u'Type de contrat'
            ),
            'export': {'related_key': 'label'},
        },
    )
    employee_quality_id = Column(
        ForeignKey('employee_quality_option.id'),
        info={'colanderalchemy': {'title': u"Qualité du salarié"}}
    )
    employee_quality = relationship(
        'EmployeeQualityOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u"Qualité du salarié"
            ),
            'export': {'related_key': 'label'},
        }
    )
    taux_horaire = Column(
        Float(),
        info={'colanderalchemy': {'title': u"Taux horaire"}}
    )
    num_hours = Column(
        Float(),
        info={'colanderalchemy': {'title': u"Nombre d'heures"}}
    )
    goals_amount = Column(
        Float(),
        info={'colanderalchemy': {'title': u"Objectif de CA / d'activité"}}
    )
    goals_period = Column(
        String(15),
        info={
            'colanderalchemy':
            {
                'title': u"Période de l'objectif"
            },
            'export': {
                'formatter': lambda val: dict(PERIOD_OPTIONS).get(val),
                'stats': {'options': PERIOD_OPTIONS},
            }
        }
    )
    amendment_number = Column(
        Integer(),
        info={'colanderalchemy': {'title': u"Numéro de l'avenant"}}
    )
    type_sortie_id = Column(
        ForeignKey('type_sortie_option.id'),
        info={'colanderalchemy': {'title': u"Type de sortie"}}
    )
    type_sortie = relationship(
        'TypeSortieOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u"Type de sortie"),
            'export': {'related_key': 'label'},
        },
    )
    motif_sortie_id = Column(
        ForeignKey('motif_sortie_option.id'),
        info={'colanderalchemy': {'title': u"Motif de sortie"}}
    )
    motif_sortie = relationship(
        'MotifSortieOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u"Motif de sortie"),
            'export': {'related_key': 'label'},
        },
    )

    @classmethod
    def query(cls, user):
        q = super(CareerPath, cls).query()
        q = q.filter(CareerPath.userdatas_id == user)
        return q.order_by(CareerPath.start_date.desc())


def update_user_situation_cae(mapper, connection, target):
    """
    Update - if needed - the CAE situation of the user
    when it's career path change
    """
    if target.cae_situation_id is not None:
        from autonomie.models.user.userdatas import UserDatas
        user = UserDatas.query().filter(
            UserDatas.id == target.userdatas_id
        ).first()
        situation = user.get_cae_situation_from_career_path(None)
        if situation:
            if user.situation_situation_id != situation.id:
                logger.debug(
                    u"Update CAE situation for user %s to '%s'" % (
                        target.userdatas_id, situation.label
                    )
                )
                connection.execute(
                    "UPDATE user_datas SET situation_situation_id=%s \
                    WHERE id=%s" % (situation.id, user.id))


listen(CareerPath, "after_insert", update_user_situation_cae)
listen(CareerPath, "after_update", update_user_situation_cae)
listen(CareerPath, "after_delete", update_user_situation_cae)
