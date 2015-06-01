# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
import colander

from autonomie.models.user import user_node
from autonomie.models.competence import CompetenceDeadline
from autonomie import forms


def remove_manager_fields(schema, kw):
    """
    Remove the manager specific fields if the user is a contractor
    """
    if kw['request'].user.is_contractor():
        del schema['contractor_id']


class _CompetenceGridQuerySchema(colander.Schema):
    contractor_id = user_node(title=u"* L'entrepreneur")
    deadline_id = colander.SchemaNode(
        colander.Integer(),
        title=u"* à l'échéance",
        description=u"L'échéance pour laquelle vous voulez saisir les \
compétences de l'entrepreneur",
        widget=forms.get_deferred_select(CompetenceDeadline)
    )


CompetenceGridQuerySchema = _CompetenceGridQuerySchema(
    after_bind=remove_manager_fields
)
