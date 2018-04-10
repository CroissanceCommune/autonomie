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
import os

from pyramid.httpexceptions import HTTPFound
from autonomie.models.competence import (
    CompetenceScale,
    CompetenceDeadline,
    CompetenceOption,
    CompetenceRequirement,
)
from autonomie.models.config import ConfigFiles
from autonomie.forms.admin import (
    CompetencePrintConfigSchema,
    get_sequence_model_admin,
)
from autonomie.views.admin.tools import (
    get_model_admin_view,
    BaseAdminFormView,
    BaseAdminIndexView,
)
from autonomie.views.admin.accompagnement import (
    ACCOMPAGNEMENT_URL,
    AccompagnementIndexView,
)


COMPETENCE_URL = os.path.join(ACCOMPAGNEMENT_URL, 'competences')
COMPETENCE_PRINT_URL = os.path.join(COMPETENCE_URL, "print")


logger = logging.getLogger(__name__)


BaseCompetenceOptionView = get_model_admin_view(
    CompetenceOption,
    r_path=COMPETENCE_URL,
)
BaseCompetenceRequirementView = get_model_admin_view(
    CompetenceRequirement,
    r_path=COMPETENCE_URL,
)
CompetenceScaleView = get_model_admin_view(
    CompetenceScale,
    r_path=COMPETENCE_URL
)
CompetenceDeadlineView = get_model_admin_view(
    CompetenceDeadline,
    r_path=COMPETENCE_URL
)


def get_requirement_admin_schema():
    schema = get_sequence_model_admin(
        CompetenceOption,
        excludes=('children',),
    )
    import colander
    from deform_extensions import DisabledInput
    schema['datas']['data']['requirements']['requirements'].add_before(
        'requirement',
        colander.SchemaNode(
            colander.String(),
            widget=DisabledInput(),
            name='deadline_label',
            title=u"Échéance",
        )
    )
    return schema


class CompetenceOptionView(BaseCompetenceOptionView):
    """
    competence and subcompetence configuration
    """
    _schema = get_sequence_model_admin(
        CompetenceOption,
        excludes=('requirements',),
    )


class CompetenceRequirementView(BaseCompetenceRequirementView):
    """
    Requirements configuration
    """
    _schema = get_requirement_admin_schema()

    def before(self, form):
        if CompetenceScale.query().count() == 0:
            self.session.flash(
                u"Les barêmes doivent être configurés avant \
la grille de compétences."
            )
            raise HTTPFound(
                self.request.route_path(
                    os.path.join(COMPETENCE_URL, "competence_scale")
                )
            )
        if CompetenceOption.query().count() == 0:
            self.session.flash(
                u"La grille de compétence doit être configurée avant les \
barêmes"
            )
            raise HTTPFound(self.request.route_path("admin_competence_option"))
        BaseCompetenceRequirementView.before(self, form)

    def get_appstruct(self):
        """
        Return the appstruct for competence requirements configuration
        """
        options = CompetenceOption.query().all()
        appstruct = []
        for option in options:
            opt_appstruct = {
                "id": option.id,
                "label": option.label,
                "requirements": []
            }
            for deadline in CompetenceDeadline.query():
                opt_appstruct['requirements'].append(
                    {
                        'deadline_id': deadline.id,
                        "deadline_label": deadline.label,
                        'requirement': option.get_requirement(deadline.id)
                    }
                )
            appstruct.append(opt_appstruct)
        return {'datas': appstruct}

    def _disable_or_remove_elements(self, appstruct):
        pass

    def _add_or_edit(self, index, datas):
        comp_id = datas['id']

        for req in datas['requirements']:
            comp_req = CompetenceRequirement(
                competence_id=comp_id,
                requirement=req['requirement'],
                deadline_id=req['deadline_id'],
            )
            self.dbsession.merge(comp_req)


class CompetencePrintOutputView(BaseAdminFormView):
    title = u"Configuration de la sortie imprimable"
    route_name = COMPETENCE_PRINT_URL
    validation_msg = u"Vos données ont bien été enregistrées"
    schema = CompetencePrintConfigSchema(title=u"")

    def before(self, form):
        appstruct = {}

        file_name = u"competence_header.png"
        file_model = ConfigFiles.get(file_name)
        if file_model is not None:
            appstruct['header_img'] = {
                'uid': file_model.id,
                'filename': file_model.name,
                'preview_url': self.request.route_url(
                    'public',
                    name=file_name,
                )
            }
        form.set_appstruct(appstruct)

    def submit_success(self, appstruct):
        file_datas = appstruct.get('header_img')

        if file_datas:
            file_name = "competence_header.png"
            ConfigFiles.set(file_name, file_datas)


class CompetenceIndexView(BaseAdminIndexView):
    title = u"Configuration du module Compétences"
    route_name = COMPETENCE_URL


def includeme(config):
    """
    Include views and routes
    """
    config.add_route(COMPETENCE_URL, COMPETENCE_URL)
    config.add_admin_view(CompetenceIndexView, parent=AccompagnementIndexView)

    for view in (
        CompetenceRequirementView,
        CompetenceDeadlineView,
        CompetenceOptionView,
        CompetenceScaleView,
        CompetencePrintOutputView,
    ):
        config.add_route(
            view.route_name, view.route_name
        )
        config.add_admin_view(view, parent=CompetenceIndexView)
