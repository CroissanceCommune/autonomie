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
(
    req_admin_class,
    COMPETENCE_REQ_ROUTE,
    COMPETENCE_REQ_TMPL,
) = get_model_admin_view(
    CompetenceRequirement,
    r_path='admin_competences',
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


class AdminCompetenceOption(main_admin_class):
    """
    competence and subcompetence configuration
    """
    redirect_path = "admin_competences"
    _schema = get_sequence_model_admin(
        CompetenceOption,
        excludes=('requirements',),
    )


class AdminCompetenceRequirement(req_admin_class):
    """
    Requirements configuration
    """
    redirect_path = "admin_competences"
    _schema = get_requirement_admin_schema()

    def before(self, form):
        if CompetenceScale.query().count() == 0:
            self.session.flash(
                u"Les barêmes doivent être configurer avant \
la grille de compétences."
            )
            raise HTTPFound(self.request.route_path("admin_competence_scale"))
        if CompetenceOption.query().count() == 0:
            self.session.flash(
                u"La grille de compétence doit être configurée avant les \
barêmes"
            )
            raise HTTPFound(self.request.route_path("admin_competence_option"))
        req_admin_class.before(self, form)

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


class AdminCompetencePrintOutput(BaseAdminFormView):
    title = u"Configuration de la sortie imprimable"
    validation_msg = u"Vos données ont bien été enregistrées"
    schema = CompetencePrintConfigSchema(title=u"")
    redirect_path = "admin_competences"

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


def admin_competence_index_view(request):
    menus = []
    for label, route, icon in (
        (u"Retour", "admin_accompagnement", "fa fa-step-backward"),
        (u"Configuration des barêmes", "admin_competence_scale", ""),
        (u"Configuration des échéances", "admin_competence_deadline", ""),
        (
            u"Configuration de la grille de compétences",
            "admin_competence_option", ""
        ),
        (
            u"Configuration des niveux de référence de la grille de compétences",
            "admin_competence_requirement", ""
        ),
        (
            u"Configuration de la sortie imprimable",
            'admin_competence_print', ""
        )
    ):
        menus.append(dict(label=label, path=route, icon=icon))
    return dict(title=u"Configuration du module Compétences", menus=menus)


def includeme(config):
    """
    Include views and routes
    """
    config.add_route("admin_competences", "admin/competences")
    config.add_route("admin_competence_print", "admin/competences/print")
    config.add_view(
        admin_competence_index_view,
        route_name="admin_competences",
        renderer="admin/index.mako",
        permission="admin",
    )
    config.add_view(
        AdminCompetencePrintOutput,
        route_name="admin_competence_print",
        renderer="admin/main.mako",
        permission='admin',
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

    config.add_route(
        COMPETENCE_REQ_ROUTE,
        "admin/competences/" + COMPETENCE_REQ_ROUTE,
    )
    config.add_view(
        AdminCompetenceRequirement,
        route_name=COMPETENCE_REQ_ROUTE,
        renderer=COMPETENCE_REQ_TMPL,
        permission='admin',
    )

#    config.add_route("admin_competence_grid", "admin/competences/grid")
#    config.add_view(
#        AdminCompetences,
#        route_name="admin_competence_grid",
#        renderer="admin/main.mako",
#        permission="admin",
#    )
