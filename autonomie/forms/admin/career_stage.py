# -*- coding: utf-8 -*-
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

import functools
from colanderalchemy import SQLAlchemySchemaNode
from autonomie.models.career_stage import CareerStage
from autonomie.models.user.userdatas import CaeSituationOption
from autonomie.forms import (
    customize_field,
    get_deferred_select,
)


def customize_schema(schema):
    """
    Customize the form schema
    :param obj schema: A CareerStage schema
    """
    customize = functools.partial(customize_field, schema)
    customize(
        'cae_situation_id',
        get_deferred_select(CaeSituationOption)
    )


def get_career_stage_schema():
    schema = SQLAlchemySchemaNode(
        CareerStage,
        includes=(
            "name", 
            "cae_situation_id",
            "is_entree_cae",
            "is_contrat",
            "is_sortie",
        )
    )
    customize_schema(schema)
    return schema
