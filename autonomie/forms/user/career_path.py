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
from autonomie.models.user.userdatas import CaeSituationOption
from autonomie.models.career_stage import CareerStage
from autonomie.models.career_path import (
    CareerPath,
    PERIOD_OPTIONS,
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


def get_add_stage_schema():
    """
    Return a schema for adding a new career path's stage
    Only display stage's type and dates
    """
    schema = SQLAlchemySchemaNode(
        CareerPath,
        (
            'start_date',
            'end_date',
            'career_stage_id',
        )
    )
    customize_schema(schema)
    return schema


def get_edit_stage_schema(stage_type):
    """
    Return a schema for editing career path's stage
    related to the stage's type
    """
    fields = [
        'id',
        'start_date',
        'end_date',
    ]
    if stage_type == "contract":
        fields.extend([
            'type_contrat_id',
            'employee_quality_id',
            'taux_horaire',
            'num_hours',
            'goals_amount',
            'goals_period',
        ])
    elif stage_type == "amendment":
        fields.extend([
            'type_contrat_id',
            'employee_quality_id',
            'taux_horaire',
            'num_hours',
            'goals_amount',
            'goals_period',
            'amendment_number',
        ])
    elif stage_type == "exit":
        fields.extend([
            'type_sortie_id',
            'motif_sortie_id',
        ])
    schema = SQLAlchemySchemaNode(CareerPath, fields)
    customize_schema(schema)
    return schema
