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
"""
Competence evaluation module

1- Choose a deadline (if manager choose also a contractor)
2- Fill the displayed grid
3- Display a printable version
"""
from pyramid.httpexceptions import HTTPFound

from autonomie.models.competence import (
    CompetenceDeadline,
    CompetenceScale,
    CompetenceOption,
    CompetenceGrid,
    CompetenceGridItem,
    CompetenceGridSubItem,
)
from autonomie.forms.competence import CompetenceGridQuerySchema
from autonomie.views import BaseFormView


def get_competence_grid(request, contractor_id, deadline_id):
    """
    Return a competence grid record for the given user and deadline
    """
    query = CompetenceGrid.query()
    query = query.filter_by(
        contractor_id=contractor_id,
        deadline_id=deadline_id,
    )
    grid = query.first()
    if grid is None:
        grid = CompetenceGrid(
            contractor_id=contractor_id,
            deadline_id=deadline_id,
        )
        options = CompetenceOption.query(
            True,
            "id"
        ).filter_by(parent_id=None)
        request.dbsession().add(grid)

    # We ensure there is an record instance for each competence option
    for option in options:
        grid_item = grid.get_item(option.id)
        for child in option.children:
            grid_item.get_subitem(child.id)

    return grid


class CompetencesIndexView(BaseFormView):
    """
    Index view used to switch from one competence to another
    """
    title = u"Évaluation des compétences"
    schema = CompetenceGridQuerySchema

    def submit_success(self, appstruct):
        deadline_id = appstruct['deadline_id']
        contractor_id = appstruct['contractor_id']

        grid = get_competence_grid(self.request, contractor_id, deadline_id)

        url = self.request.route_path("competence_grid", id=grid.id)
        return HTTPFound(url)


def competence_grid_view(context, request):
    """
    The competence grid base view
    """
    # loadurl : The url to load the options
    # context_url : The url to load datas about the context in json format
    return dict(
        title=u"Évaluation des compétences de {0} pour la période {1}".format(
            context.contractor.label, context.deadline.label
        )
    )


def includeme(config):
    """
    Pyramid's inclusion mechanism
    """
    config.add_route('competences', '/competences')
    config.add_route(
        'competence_grid',
        '/competences/{id}',
        traverse='/competences/{id}',
    )

    config.add_view(
        CompetencesIndexView,
        route_name='competences',
        renderer='/accompagnement/competences.mako',
        permission='edit',
    )
    config.add_view(
        competence_grid_view,
        route_name='competence_grid',
        renderer='/accompagnement/competence.mako',
        permission='edit',
    )
