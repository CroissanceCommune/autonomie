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
    CompetenceRequirement,
    CompetenceOption,
)
from autonomie.utils.widgets import ViewLink
from autonomie.forms.admin import (
    CompetenceGridSchema,
)
from autonomie.views import (
    submit_btn,
    BaseFormView,
)
from autonomie.views.admin.tools import (
    get_model_admin_view,
)


logger = logging.getLogger(__name__)


class AdminCompetences(BaseFormView):
    title = u"Administration des barêmes"
    validation_msg = u"Les barêmes ont bien été enregistrées"
    schema = CompetenceGridSchema(title=u"")
    buttons = (submit_btn, )

    def before(self, form):
        if CompetenceScale.query().count() == 0 or \
                CompetenceDeadline.query().count() == 0:
            self.session.flash(
                u"Les barêmes et les échéances doivent être configurer avant \
la grille de compétences."
            )
            raise HTTPFound(self.request.route_path("admin_scales"))

        appstruct = {'competences': []}
        for competence in CompetenceOption.query().filter_by(parent_id=None):
            c_appstruct = {
                'label': competence.label,
                'id': competence.id,
                'children': [],
                'requirements': [],
            }

            # On doit peupler l'appstruct avec les deadlines ajoutées entre
            # temps.
            # On utilise un dict pour permettre d'identifier les éléments entre
            # les deux boucles for
            req_appstruct = {}
            for deadline in CompetenceDeadline.query():
                req_appstruct[deadline.id] = {
                    'deadline_id': deadline.id,
                    'deadline_label': deadline.label,
                }

            # On update avec les pré-requis déjà configurés
            for rqt in competence.requirements:
                req_appstruct[rqt._deadline.id] = {
                    'deadline_id': rqt._deadline.id,
                    'deadline_label': rqt._deadline.label,
                    'scale_id': rqt._scale.id
                }
            # Seul les valeurs nous intéresse
            c_appstruct['requirements'] = req_appstruct.values()

            for child in competence.children:
                c_appstruct['children'].append(
                    {
                        'id': child.id,
                        'label': child.label,
                    }
                )
            appstruct['competences'].append(c_appstruct)

        logger.debug(appstruct)

        form.set_appstruct(appstruct)

        self.request.actionmenu.add(
            ViewLink(
                u"Retour",
                path="admin_competences",
                title=u"Retour à la page précédente"
            )
        )

    def get_bind_data(self):
        return {
            'request': self.request,
            'deadlines': CompetenceDeadline.query().all()
        }

    def get_competence(self, appstruct):
        id_ = appstruct.get('id')
        label = appstruct['label']
        if id_ is not None:
            # on stocke l'id des éléments qu'on retrouve
            self.current_ids.append(id_)
            model = CompetenceOption.get(id_)
            model.label = label
        else:
            model = CompetenceOption(label=label)
        return model

    def get_requirement(self, appstruct, competence_id):
        scale_id = appstruct['scale_id']
        deadline_id = appstruct['deadline_id']

        req = CompetenceRequirement.query().filter(
            CompetenceRequirement.deadline_id == deadline_id
        ).filter(
            CompetenceRequirement.competence_id == competence_id
        ).first()

        if req is None:
            req = CompetenceRequirement(
                competence_id=competence_id,
            )
        req.scale_id = scale_id
        req.deadline_id = deadline_id
        return req

    def submit_success(self, appstruct):
        self.current_ids = []
        logger.info("Successfull submission")
        logger.debug(appstruct)

        for competence in appstruct['competences']:
            children = competence.pop('children', [])
            sub_competences = []
            for child in children:
                sub_competences.append(
                    self.get_competence(child)
                )

            instance = self.get_competence(competence)
            instance.children = sub_competences
            for requirement in competence['requirements']:
                instance.requirements.append(
                    self.get_requirement(requirement, instance.id)
                )
            if instance.id is not None:
                instance = self.dbsession.merge(instance)
            else:
                self.dbsession.add(instance)
                self.dbsession.flush()
                # on stocke l'id des éléments qu'on vient d'insérer
                self.current_ids.append(instance.id)

        logger.debug(self.current_ids)

        # On désactive les éléments qui ne servent plus
        for competence in CompetenceOption.query(active=True).filter(
            CompetenceOption.id.notin_(self.current_ids)
        ):
            competence.active = False
            self.dbsession.merge(competence)

        return HTTPFound(
            self.request.route_path(
                "admin_competences"
            )
        )


def admin_competence_index_view(request):
    for label, route in (
        (u"Retour", "admin_accompagnement",),
        (u"Configuration des barêmes", "admin_scale",),
        (u"Configuration des échéances", "admin_deadline",),
        (
            u"Configuration de la grille de compétences",
            "admin_competence_grid",
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

    config.add_route("admin_competence_grid", "admin/competences/grid")
    config.add_view(
        AdminCompetences,
        route_name="admin_competence_grid",
        renderer="admin/main.mako",
        permission="admin",
    )
