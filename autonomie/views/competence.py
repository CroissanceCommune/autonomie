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
import logging
import colander
import functools
from pyramid.httpexceptions import HTTPFound
from sqlalchemy import func

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.utils import rest, widgets
from autonomie.models.user import (
    get_users_options,
)
from autonomie.models.competence import (
    CompetenceDeadline,
    CompetenceScale,
    CompetenceOption,
    CompetenceGrid,
    CompetenceGridItem,
    CompetenceGridSubItem,
)
from autonomie.resources import (
    competence_js,
    competence_radar_js,
)
from autonomie.forms.competence import CompetenceGridQuerySchema
from autonomie.views import (
    BaseView,
)


logger = logging.getLogger(__name__)


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
    options = CompetenceOption.query()

    if grid is None:
        grid = CompetenceGrid(
            contractor_id=contractor_id,
            deadline_id=deadline_id,
        )

        request.dbsession.add(grid)

    for option in options:
        grid.ensure_item(option)

    return grid


def competence_index_view(request):
    """
    Index view to go to a competence grid
    """
    competence_js.need()
    user_options = get_users_options(roles=['contractor'])
    deadlines = CompetenceDeadline.query().all()
    if 'deadline' in request.POST or 'sheet' in request.POST:
        logger.debug(request.POST)
        schema = CompetenceGridQuerySchema.bind(request=request)
        try:
            appstruct = schema.deserialize(request.POST)
        except colander.Invalid:
            logger.exception(u"Erreur dans le routage de la page de \
compétences : POSSIBLE BREAK IN ATTEMPT")
        else:
            # On récupère l'id du user pour l'évaluation
            contractor_id = appstruct['contractor_id']
            # L'id de la période d'évaluation
            deadline_id = appstruct['deadline']

            # On redirige vers la page appropriée
            grid = get_competence_grid(
                request,
                contractor_id,
                deadline_id
            )
            url = request.route_path("competence_grid", id=grid.id)
            return HTTPFound(url)

    return {
        'title': u'Évaluation des compétences',
        'user_options': user_options,
        'deadlines': deadlines,
    }


def competence_grid_view(context, request):
    """
    The competence grid base view
    """
    request.actionmenu.add(
        widgets.ViewLink(
            u"Page précédente",
            "view",
            path="competences",
        )
    )
    competence_js.need()
    # loadurl : The url to load the options
    loadurl = request.route_path(
        'competence_grid',
        id=context.id,
        _query=dict(action='options'),
    )
    # contexturl : The url to load datas about the context in json format
    contexturl = request.current_route_path()

    title = u"Évaluation des compétences de {0} pour la période \"{1}\"".format(
        context.contractor.label, context.deadline.label
    )

    return {
        'title': title,
        "loadurl": loadurl,
        "contexturl": contexturl
    }


def competence_form_options(context, request):
    """
    Returns datas used to build the competence form page
    """
    return dict(
        grid=context,
        grid_edit_url=request.route_path(
            'competence_grid',
            id=context.id,
            _query=dict(action='edit')
        ),
        item_root_url=request.route_path(
            'competence_grid_items',
            id=context.id,
        ),
        deadlines=CompetenceDeadline.query().all(),
        scales=CompetenceScale.query().all(),
    )


def competence_radar_chart_view(context, request):
    """
    Competence radar chart view

    :param obj context: a user model
    """
    competence_radar_js.need()
    loadurl = request.route_path(
        'competence_grid',
        id=context.id,
        _query=dict(action='radar'),
    )
    title = u"Profil des compétences entrepreneuriale  \
{0}".format(context.deadline.label)

    grids = []
    # On récupère les grilles de compétences précédent la courant
    deadlines = CompetenceDeadline.query()
    deadlines = deadlines.filter(
        CompetenceDeadline.order <= context.deadline.order
    ).all()
    scales = CompetenceScale.query().all()
    for deadline in deadlines:
        grid = get_competence_grid(request, context.contractor_id, deadline.id)
        grids.append(grid)

    return dict(
        title=title,
        loadurl=loadurl,
        grids=grids,
        deadlines=deadlines,
        scales=scales,
    )


def competence_radar_chart_datas(context, request):
    """
    Return the datas used to show a radar / spider chart of a user's
    competences
    context : CompetenceGrid
    """
    datas = []
    legend = []

    deadlines = CompetenceDeadline.query()
    deadlines = deadlines.filter(
        CompetenceDeadline.order <= context.deadline.order
    )
    for deadline in deadlines:
        grid = get_competence_grid(request, context.contractor_id, deadline.id)
        datas.append(grid.__radar_datas__())
        legend.append(u"Profil {0}".format(deadline.label))

    datas.append(CompetenceOption.__radar_datas__())
    legend.append(u"Profil référence")

    config = {}
    config['levels'] = CompetenceScale.query().count()
    max_value = request.dbsession.query(
        func.max(CompetenceScale.value)
    ).all()[0][0]

    config['maxValue'] = max_value

    return {'datas': datas, 'legend': legend, "config": config}


class RestCompetenceGrid(BaseView):
    """
    Json api for competence grid handling
    """

    def get(self):
        return {
            'grid': self.context,
            'items': self.context.items,
        }


class RestCompetenceGridItem(BaseView):
    """
    Rest view for Item handling

    Provides :

        * get collection
        * edit element
    """
    @property
    def schema(self):
        return SQLAlchemySchemaNode(
            CompetenceGridItem,
            includes=('progress', 'id')
        )

    def collection_get(self):
        """
        Return list of items for a given grid
        context is a grid
        """
        return self.context.items

    def put(self):
        submitted = self.request.json_body
        logger.debug(u"Submitting %s" % submitted)
        schema = self.schema

        try:
            attributes = schema.deserialize(submitted)
        except colander.Invalid, err:
            logger.exception("  - Erreur")
            logger.exception(submitted)
            raise rest.RestError(err.asdict(), 400)

        logger.debug(attributes)

        item = schema.objectify(attributes, self.context)
        item = self.request.dbsession.merge(item)
        return item


class RestCompetenceGridSubItem(BaseView):
    """
    Rest view for Sub item handling:

    Provides:

        * get collection
        * edit element
    """
    @property
    def schema(self):
        return SQLAlchemySchemaNode(
            CompetenceGridSubItem,
            includes=('evaluation', 'id', 'comments',)
        )

    def collection_get(self):
        """
        Return list of subitems for a given item
        context is an item
        """
        return self.context.subitems

    def put(self):
        submitted = self.request.json_body
        logger.debug(u"Submitting %s" % submitted)
        schema = self.schema

        try:
            attributes = schema.deserialize(submitted)
        except colander.Invalid, err:
            logger.exception("  - Erreur")
            logger.exception(submitted)
            raise rest.RestError(err.asdict(), 400)

        logger.debug(attributes)

        subitem = schema.objectify(attributes, self.context)
        subitem = self.request.dbsession.merge(subitem)
        return subitem


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

    config.add_route(
        'competence_grid_items',
        '/competences/{id}/items',
        traverse='/competences/{id}',
    )

    config.add_route(
        'competence_grid_item',
        '/competences/{id}/items/{iid:\d+}',
        traverse='/competence_items/{iid}',
    )

    config.add_route(
        'competence_grid_subitems',
        '/competences/{id}/items/{iid:\d+}/subitems',
        traverse='/competence_items/{iid}',
    )

    config.add_route(
        'competence_grid_subitem',
        '/competences/{id}/items/{iid:\d+}/subitems/{sid:\d+}',
        traverse='/competence_subitems/{sid}',
    )

    config.add_view(
        competence_index_view,
        route_name='competences',
        renderer='/accompagnement/competences.mako',
        permission='view',
    )

    config.add_view(
        competence_grid_view,
        route_name='competence_grid',
        renderer='/accompagnement/competence.mako',
        permission="edit",
    )
    config.add_view(
        competence_radar_chart_view,
        route_name='competence_grid',
        renderer='/accompagnement/competence_resume.mako',
        permission="edit",
        request_param="action=radar",
    )

    add_json_view = functools.partial(
        config.add_view,
        renderer='json',
        permission='edit',
        xhr=True,
    )
    add_json_view(
        RestCompetenceGrid,
        attr="get",
        route_name='competence_grid',
        request_method="GET",
    )

    add_json_view(
        RestCompetenceGridItem,
        attr="collection_get",
        route_name='competence_grid_items',
        request_method="GET",
    )

    add_json_view(
        RestCompetenceGridSubItem,
        attr="collection_get",
        route_name='competence_grid_subitems',
        request_method="GET",
    )

    add_json_view(
        RestCompetenceGridItem,
        attr="put",
        route_name='competence_grid_item',
        request_method="PUT",
    )

    add_json_view(
        RestCompetenceGridSubItem,
        attr="put",
        route_name='competence_grid_subitem',
        request_method="PUT",
    )

    add_json_view(
        competence_form_options,
        route_name='competence_grid',
        request_method='GET',
        request_param="action=options",
    )
    add_json_view(
        competence_radar_chart_datas,
        route_name='competence_grid',
        request_param="action=radar",
    )
