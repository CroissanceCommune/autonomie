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
import logging
from pyramid.httpexceptions import HTTPFound
from autonomie.models.competence import (
    CompetenceScale,
    CompetenceDeadline,
    CompetenceOption,
)
from autonomie.utils.widgets import ViewLink
from autonomie.views.admin.tools import (
    get_model_admin_view,
)


logger = logging.getLogger(__name__)


(
    main_admin_class,
    COMPETENCE_OPTION_ROUTE,
    COMPETENCE_OPTION_TMPL,
) = get_model_admin_view(
    CompetenceOption,
    r_path='admin_competences',
)


class AdminCompetenceOption(main_admin_class):
    def before(self, form):
        if CompetenceScale.query().count() == 0:
            self.session.flash(
                u"Les barêmes doivent être configurer avant \
la grille de compétences."
            )
            raise HTTPFound(self.request.route_path("admin_competence_scale"))
        main_admin_class.before(self, form)


def admin_competence_index_view(request):
    for label, route in (
        (u"Retour", "admin_accompagnement",),
        (u"Configuration des barêmes", "admin_competence_scale",),
        (u"Configuration des échéances", "admin_competence_deadline",),
        (
            u"Configuration de la grille de compétences",
            "admin_competence_option",
        ),
    ):
        request.actionmenu.add(
            ViewLink(label, path=route, title=label)
        )
    return dict(title=u"Configuration du module Compétences")


def includeme(config):
    """
    Include views and routes
    """
    config.add_route("admin_competences", "admin/competences")
    config.add_view(
        admin_competence_index_view,
        route_name="admin_competences",
        renderer="admin/index.mako",
        permission="admin",
    )

    for model in (CompetenceScale, CompetenceDeadline):
        view, route_name, tmpl = get_model_admin_view(
            model,
            r_path='admin_competences',
        )
        config.add_route(route_name, "admin/competences/" + route_name)
        config.add_view(
            view,
            route_name=route_name,
            renderer=tmpl,
            permission="admin",
        )

    config.add_route(
        COMPETENCE_OPTION_ROUTE,
        "admin/competences/" + COMPETENCE_OPTION_ROUTE,
    )
    config.add_view(
        AdminCompetenceOption,
        route_name=COMPETENCE_OPTION_ROUTE,
        renderer=COMPETENCE_OPTION_TMPL,
        permission='admin',
    )

#    config.add_route("admin_competence_grid", "admin/competences/grid")
#    config.add_view(
#        AdminCompetences,
#        route_name="admin_competence_grid",
#        renderer="admin/main.mako",
#        permission="admin",
#    )
