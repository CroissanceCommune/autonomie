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
    Career path forms configuration
"""
import deform
import colander
import functools
from colanderalchemy import SQLAlchemySchemaNode
from autonomie.forms import (
    customize_field,
    get_deferred_select,
    get_select,
)
from autonomie.models.career_stage import CareerStage
from autonomie.models.career_path import (
    CareerPath,
    PERIOD_OPTIONS,
)
from autonomie.models.user.userdatas import (
    CaeSituationOption,
    TypeContratOption,
    EmployeeQualityOption,
    TypeSortieOption,
    MotifSortieOption,
)

def customize_schema(schema):
    """
    Customize the form schema
    :param obj schema: A CareerPath schema
    """
    customize = functools.partial(customize_field, schema)
    customize(
        'career_stage_id',
        get_deferred_select(CareerStage, keys=('id', 'name'))
    )
    customize(
        'cae_situation_id',
        get_deferred_select(CaeSituationOption)
    )
    customize(
        'type_contrat_id',
        get_deferred_select(TypeContratOption)
    )
    customize(
        'employee_quality_id',
        get_deferred_select(EmployeeQualityOption)
    )
    customize(
        "taux_horaire",
        deform.widget.MoneyInputWidget()
    )
    customize(
        "num_hours",
        deform.widget.MoneyInputWidget()
    )
    customize(
        "goals_amount",
        deform.widget.MoneyInputWidget()
    )
    customize(
        "goals_period",
        get_select(PERIOD_OPTIONS)
    )
    customize(
        'type_sortie_id',
        get_deferred_select(TypeSortieOption)
    )
    customize(
        'motif_sortie_id',
        get_deferred_select(MotifSortieOption)
    )


def customize_edit_schema(schema):
    """
    Customize the form schema for edition
    :param obj schema: A CareerPath schema
    """
    customize = functools.partial(customize_field, schema)
    customize(
        "career_stage_id",
        deform.widget.HiddenWidget()
    )
    customize(
        "cae_situation_id",
        deform.widget.HiddenWidget()
    )
    customize(
        "is_entree_cae",
        deform.widget.HiddenWidget()
    )
    customize(
        "is_contrat",
        deform.widget.HiddenWidget()
    )
    customize(
        "is_sortie",
        deform.widget.HiddenWidget()
    )


def get_add_stage_schema():
    """
    Return a schema for adding a new career path's stage
    Only display stage's type and dates
    """
    schema = SQLAlchemySchemaNode(
        CareerPath,
        excludes=(
            'userdatas_id',
            'cae_situation_id',
            'is_entree_cae',
            'is_contrat',
            'is_sortie',
            'type_contrat_id',
            'employee_quality_id',
            'taux_horaire',
            'num_hours',
            'goals_amount',
            'goals_period',
            'type_sortie_id',
            'motif_sortie_id',
        )
    )
    customize_schema(schema)
    return schema


def get_edit_stage_schema():
    """
    Return a schema for editing career path's stage
    wich is nor 'contrat' nor 'sortie' type
    """
    schema = SQLAlchemySchemaNode(
        CareerPath,
        excludes=(
            'userdatas_id',
            'type_contrat_id',
            'employee_quality_id',
            'taux_horaire',
            'num_hours',
            'goals_amount',
            'goals_period',
            'type_sortie_id',
            'motif_sortie_id',
        )
    )
    customize_schema(schema)
    customize_edit_schema(schema)
    return schema


def get_edit_contrat_stage_schema():
    """
    Return a schema for editing career path's stage
    wich is 'contrat' type
    """
    schema = SQLAlchemySchemaNode(
        CareerPath,
        excludes=(
            'userdatas_id',
            'type_sortie_id',
            'motif_sortie_id',
        )
    )
    customize_schema(schema)
    customize_edit_schema(schema)
    return schema
    

def get_edit_sortie_stage_schema():
    """
    Return a schema for editing career path's stage
    wich is 'sortie' type
    """
    schema = SQLAlchemySchemaNode(
        CareerPath,
        excludes=(
            'userdatas_id',
            'type_contrat_id',
            'employee_quality_id',
            'taux_horaire',
            'num_hours',
            'goals_amount',
            'goals_period',
        )
    )
    customize_schema(schema)
    customize_edit_schema(schema)
    return schema
