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


def restrict_user_id(form, kw):
    """
    Restrict the user selection to the current user
    """
    if not kw['request'].has_permission('admin_competence'):
        current_user = kw['request'].user
        form['contractor_id'].validator = colander.OneOf((current_user.id,))


@colander.deferred
def deferred_deadline_id_validator(node, kw):
    return colander.OneOf(
        [c[0] for c in CompetenceDeadline.query('id').all()]
    )


class _CompetenceGridQuerySchema(colander.Schema):
    contractor_id = user_node(roles=['contractor'])
    deadline = colander.SchemaNode(
        colander.Integer(),
        validator=deferred_deadline_id_validator,
        missing=colander.drop,
    )


CompetenceGridQuerySchema = _CompetenceGridQuerySchema(
    after_bind=restrict_user_id
)
