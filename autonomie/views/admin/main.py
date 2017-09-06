# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
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
#

"""
    Administration views
    - config table configuration
    - welcome message
    - logo upload
"""
import logging
import functools

from sqlalchemy import desc
from pyramid.httpexceptions import HTTPFound
from autonomie.models.config import (
    Config,
    ConfigFiles,
)
from autonomie.models.activity import (
    ActivityType,
    ActivityMode,
    ActivityAction,
)
from autonomie.models.workshop import WorkshopAction
from autonomie.models.company import (
    CompanyActivity,
)
from autonomie.models.user import (
    ZoneOption,
    ZoneQualificationOption,
    StudyLevelOption,
    SocialStatusOption,
    EmployeeQualityOption,
    ActivityTypeOption,
    PcsOption,
    PrescripteurOption,
    NonAdmissionOption,
    ParcoursStatusOption,
    MotifSortieOption,
    SocialDocTypeOption,
    CaeSituationOption,
    TypeSortieOption,
    AntenneOption,
)
from autonomie.models import files
from autonomie.forms.admin import (
    MainConfig,
    WorkshopConfigSchema,
    ActivityConfigSchema,
    get_config_appstruct,
    get_config_dbdatas,
    merge_config_datas,
)
from autonomie.forms.files import get_template_upload_schema
from js.tinymce import tinymce
from autonomie.views import (
    submit_btn,
    BaseView,
    DisableView,
    DeleteView,
)
from autonomie.views.admin.tools import (
    get_model_admin_view,
    BaseAdminFormView,
    make_enter_point_view,
)
from autonomie.forms import (
    merge_session_with_post,
)
from autonomie.views.files import (
    FileUploadView,
    FileEditView,
    file_dl_view,
)


log = logging.getLogger(__name__)


UPLOAD_OK_MSG = u"Le modèle de document a bien été ajouté"
EDIT_OK_MSG = u"Le modèle de document a bien été modifié"


def index(request):
    """
        Return datas for the index view
    """
    menus = []
    menus.append(
        dict(
            label=u"Configuration générale",
            route_name='admin_main',
            title=u"Message d'accueil, logos, entête et pieds de page des \
devis, factures / avoir)"
        )
    )
    menus.append(
        dict(
            label=u"Configuration du module Ventes",
            route_name="admin_vente",
            title=u"Mentions des devis et factures, unité de prestation ...",
        )
    )
    menus.append(
        dict(
            label=u"Configuration du module Notes de dépense",
            route_name="admin_expense",
            title=u"Configuration des types de dépense, des \
différents comptes analytiques liés au module notes de dépense et à leur export"
        )
    )
    menus.append(
        dict(
            label=u"Configuration du module Accompagnement",
            route_name="admin_accompagnement",
            title=u"Ateliers, Rendez-vous, Compétences"
        )
    )
    menus.append(
        dict(
            label=u"Configuration du module Gestion Sociale",
            route_name='admin_userdatas',
            title=u"Typologie des données, modèles de documents",
        )
    )
    menus.append(
        dict(
            label=u"Configuration des domaines d'activité des entreprises \
de la CAE",
            route_name="admin_company_activity",
        )
    )
    return dict(title=u"Configuration du site", menus=menus)


class AdminMain(BaseAdminFormView):
    """
        Main configuration view
    """
    title = u"Configuration générale"
    validation_msg = u"La configuration a bien été modifiée"
    schema = MainConfig()
    buttons = (submit_btn,)

    def before(self, form):
        """
            Add the appstruct to the form
        """
        config_dict = self.request.config
        logo = ConfigFiles.get('logo.png')
        appstruct = get_config_appstruct(self.request, config_dict, logo)
        form.set_appstruct(appstruct)
        tinymce.need()

    def submit_success(self, appstruct):
        """
            Insert config informations into database
        """
        # la table config étant un stockage clé valeur
        # le merge_session_with_post ne peut être utilisé
        logo = appstruct['site'].pop('logo', None)
        if logo:
            ConfigFiles.set('logo.png', logo)
            self.request.session.pop('substanced.tempstore')
            self.request.session.changed()

        dbdatas = self.dbsession.query(Config).all()
        appstruct = get_config_dbdatas(appstruct)
        dbdatas = merge_config_datas(dbdatas, appstruct)
        for dbdata in dbdatas:
            self.dbsession.merge(dbdata)
        self.dbsession.flush()
        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("admin_main"))


class BaseAdminActivities(BaseAdminFormView):
    """
        Activity types config
    """
    title = u"Configuration du module accompagnement"
    validation_msg = u"Le module a bien été configuré"
    buttons = (submit_btn,)

    def _add_pdf_img_to_appstruct(self, data_type, appstruct):
        for file_type in ("header_img", "footer_img"):
            file_name = "%s_%s.png" % (data_type, file_type)
            file_model = ConfigFiles.get(file_name)
            if file_model is not None:
                appstruct[file_type] = {
                    'uid': file_model.id,
                    'filename': file_model.name,
                    'preview_url': self.request.route_url(
                        'public',
                        name=file_name,
                    )
                }

    def _recursive_action_appstruct(self, actions):
        appstruct = []
        for action in actions:
            action_appstruct = action.appstruct()
            if action.children is not None:
                action_appstruct['children'] = self._recursive_action_appstruct(
                    action.children
                )
            appstruct.append(action_appstruct)
        return appstruct

    def get_edited_elements(self, appstruct, key=None):
        """
        Return a dict id:data for the elements that are edited (with an id)
        """
        if key is not None:
            appstruct = appstruct.get(key, {})
        return dict((data['id'], data) for data in appstruct if 'id' in data)

    def get_submitted_modes(self, appstruct):
        """
        Return the modes that have been submitted
        """
        return [data['label'] for data in appstruct['modes']]

    def disable_types(self, appstruct):
        """
        Disable types that are no longer used
        """
        edited_types = self.get_edited_elements(appstruct, "types")

        for element in ActivityType.query():
            if element.id not in edited_types.keys():
                element.active = False
                self.dbsession.merge(element)

    def recursive_collect_ids(self, appstruct, key=None):
        result = []
        if key is not None:
            appstruct = appstruct.get(key, [])
        for local_appstruct in appstruct:
            if 'children' in local_appstruct.keys():
                children_ids = self.recursive_collect_ids(
                    local_appstruct,
                    'children'
                )
                result.extend(children_ids)
            if 'id' in local_appstruct:
                result.append(local_appstruct['id'])
        return result

    def disable_actions(self, appstruct, factory):
        """
        Disable actions that are not active anymore
        """
        # on récupère les ids des actions encore dans la config
        ids = self.recursive_collect_ids(appstruct, 'actions')
        from sqlalchemy import not_

        for element in factory.query().filter(
            not_(getattr(factory, 'id').in_(ids))
        ):
            element.active = False
            self.dbsession.merge(element)

    def delete_modes(self, appstruct):
        """
        Delete modes that are no longer used

        Return modes that have to be added
        """
        all_modes = self.get_submitted_modes(appstruct)
        for element in ActivityMode.query():
            if element.label not in all_modes:
                self.dbsession.delete(element)
            else:
                # Remove it from the submitted list so we don't insert it again
                all_modes.remove(element.label)
        return all_modes

    def _add_or_edit(self, datas, factory):
        """
        Add or edit an element of the given factory
        """
        if 'id' in datas:
            element = factory.get(datas['id'])
            merge_session_with_post(element, datas)
            element = self.dbsession.merge(element)
        else:
            element = factory()
            merge_session_with_post(element, datas)
            self.dbsession.add(element)
        return element

    def add_types(self, appstruct):
        """
        Add/edit the types
        """
        for data in appstruct["types"]:
            self._add_or_edit(data, ActivityType)

    def add_modes(self, new_modes):
        """
        Add new modes
        modes are not relationships so we don't need to keep them
        """
        for mode in new_modes:
            new_mode_obj = ActivityMode(label=mode)
            self.dbsession.add(new_mode_obj)

    def add_actions(self, appstruct, key, factory):
        """
        Add recursively new actions (with parent-child relationship)
        """
        result = []
        for action_appstruct in appstruct[key]:
            # On remplace les noeuds children par des instances
            if 'children' in action_appstruct:
                action_appstruct['children'] = self.add_actions(
                    action_appstruct,
                    'children',
                    factory
                )
            result.append(self._add_or_edit(action_appstruct, factory))
        return result

    def store_pdf_conf(self, appstruct, data_type):
        """
        Store the pdf configuration for the given type

        :param dict appstruct: The datas in which we will find the pdf
        configuration
        :param str data_type: activity/workshop
        """
        pdf_appstruct = appstruct
        for file_type in ("header_img", "footer_img"):
            file_datas = pdf_appstruct.get(file_type)
            if file_datas:
                file_name = "%s_%s.png" % (data_type, file_type)
                ConfigFiles.set(file_name, file_datas)

        Config.set(
            "%s_footer" % data_type,
            pdf_appstruct.get('footer', '')
        )


class AdminActivities(BaseAdminActivities):
    """
    Activities Admin view
    """
    title = u"Configuration du module de Rendez-vous"
    schema = ActivityConfigSchema(title=u"")
    redirect_route_name = "admin_accompagnement"

    def before(self, form):
        query = ActivityType.query()
        types = query.filter_by(active=True)

        modes = ActivityMode.query()

        query = ActivityAction.query()
        query = query.filter_by(parent_id=None)
        actions = query.filter_by(active=True)

        activity_appstruct = {
            'footer': self.request.config.get("activity_footer", ""),
            'types': [type_.appstruct() for type_ in types],
            'modes': [mode.appstruct() for mode in modes],
            'actions': self._recursive_action_appstruct(actions)
        }
        self._add_pdf_img_to_appstruct('activity', activity_appstruct)
        form.set_appstruct(activity_appstruct)

    def submit_success(self, activity_appstruct):
        """
            Handle successfull activity configuration
        """
        self.store_pdf_conf(activity_appstruct, 'activity')
        # We delete the elements that are no longer in the appstruct
        self.disable_types(activity_appstruct)
        self.disable_actions(activity_appstruct, ActivityAction)
        new_modes = self.delete_modes(activity_appstruct)
        self.dbsession.flush()

        self.add_types(activity_appstruct)
        self.add_actions(activity_appstruct, "actions", ActivityAction)
        self.add_modes(new_modes)

        self.request.session.flash(self.validation_msg)
        return HTTPFound(
            self.request.route_path("admin_accompagnement")
        )


class AdminWorkshop(BaseAdminActivities):
    """
    Workshops administration views
    """
    title = u"Configuration du module Atelier"
    schema = WorkshopConfigSchema(title=u"")
    redirect_route_name = "admin_accompagnement"

    def before(self, form):
        """
            Add appstruct to the current form object
        """
        query = WorkshopAction.query()
        query = query.filter_by(parent_id=None)
        actions = query.filter_by(active=True)

        workshop_appstruct = {
            'footer': self.request.config.get("workshop_footer", ""),
            'actions': self._recursive_action_appstruct(actions)
        }

        form.set_appstruct(workshop_appstruct)

    def submit_success(self, workshop_appstruct):
        """
            Handle successfull workshop configuration
        """

        self.store_pdf_conf(workshop_appstruct, 'workshop')
        # We delete the elements that are no longer in the appstruct
        self.disable_actions(workshop_appstruct, WorkshopAction)
        self.dbsession.flush()

        self.add_actions(workshop_appstruct, "actions", WorkshopAction)

        self.request.session.flash(self.validation_msg)
        return HTTPFound(
            self.request.route_path("admin_accompagnement")
        )


class TemplateUploadView(FileUploadView):
    title = u"Configurer les modèles de documents"
    factory = files.Template
    schema = get_template_upload_schema()
    valid_msg = UPLOAD_OK_MSG
    add_template_vars = ('title', 'menus')

    @property
    def menus(self):
        return [dict(label=u'Retour', route_name='templates',
                     icon="fa fa-step-backward")]

    def before(self, form):
        come_from = self.request.referrer
        log.debug(u"Coming from : %s" % come_from)

        appstruct = {
            'come_from': come_from
        }
        form.set_appstruct(appstruct)


class TemplateEditView(FileEditView):
    valid_msg = u"Le modèle de document a bien été modifié"
    factory = files.Template
    schema = get_template_upload_schema()
    valid_msg = EDIT_OK_MSG
    add_template_vars = ('title', 'menus')

    @property
    def menus(self):
        return [dict(label=u'Retour', route_name='templates',
                     icon="fa fa-step-backward")]

    def before(self, form):
        FileEditView.before(self, form)


class TemplateList(BaseView):
    """
    Listview of templates
    """
    title = u"Modèles de documents"

    def __call__(self):
        menus = [dict(label=u"Retour", route_name="admin_userdatas",
                      icon="fa fa-step-backward")]

        templates = files.Template.query()\
            .order_by(desc(files.Template.active))\
            .all()
        return dict(templates=templates, title=self.title, menus=menus)


def get_all_userdatas_views():
    """
    Return view_class, route_name for all option configuration views in the
    userdatas module
    """
    for model in (
        CaeSituationOption,
        AntenneOption,
        ZoneOption,
        ZoneQualificationOption,
        StudyLevelOption,
        SocialStatusOption,
        EmployeeQualityOption,
        ActivityTypeOption,
        PcsOption,
        PrescripteurOption,
        NonAdmissionOption,
        ParcoursStatusOption,
        MotifSortieOption,
        SocialDocTypeOption,
        TypeSortieOption,
    ):
        yield get_model_admin_view(model)
    yield TemplateList, 'templates', '/admin/templates.mako'


class TemplateDisableView(DisableView):
    enable_msg = u"Le template a bien été activé"
    disable_msg = u"Le template a bien été désactivé"
    redirect_route = "templates"


class TemplateDeleteView(DeleteView):
    delete_msg = u"Le modèle a bien été supprimé"
    redirect_route = "templates"


def console_view(request):
    """
    """
    menus = []
    for label, route in (
        (u"Historique mail salaire", 'mailhistory',),
        (u"Tâches celery", 'jobs',),
    ):
        menus.append(
            dict(label=label, route_name=route, title=label)
        )
    return dict(title=u"Console de supervision", menus=menus)


def admin_accompagnement_index_view(request):
    menus = []
    for label, route, icon in (
        (u"Retour", "admin_index", "fa fa-step-backward"),
        (u"Configuration du module Rendez-vous", "admin_activity", ''),
        (u"Configuration du module Atelier", "admin_workshop", ''),
        (u"Configuration du module Compétences", "admin_competences", ''),
    ):
        menus.append(
            dict(label=label, route_name=route, icon=icon)
        )
    return dict(title=u"Configuration du module accompagnement", menus=menus)


def include_userdatas_views(config):
    """
    Include views related to userdatas configuration
    """
    all_option_views = list(get_all_userdatas_views())
    for view, route_name, tmpl in all_option_views:
        config.add_route(route_name, "admin/" + route_name)
        config.add_admin_view(
            view,
            route_name=route_name,
            renderer=tmpl,
        )

    config.add_admin_view(
        TemplateDisableView,
        route_name='template',
        request_param='action=disable',
    )

    config.add_admin_view(
        TemplateDeleteView,
        route_name='template',
        request_param='action=delete',
    )

    config.add_admin_view(
        file_dl_view,
        route_name='template',
    )

    config.add_admin_view(
        TemplateEditView,
        route_name='template',
        renderer='admin/template_edit.mako',
        request_param='action=edit',
    )

    config.add_admin_view(
        TemplateUploadView,
        route_name='templates',
        renderer='admin/template_add.mako',
        request_param='action=new',
    )

    config.add_admin_view(
        make_enter_point_view(
            'admin_index',
            all_option_views,
            u"Configuration de la gestion sociale"
        ),
        route_name="admin_userdatas",
    )


def include_pyramid_sacrud(config):
    config.include('pyramid_sacrud')
    from autonomie.models import user
    settings = config.registry.settings
    settings['pyramid_sacrud.models'] = (
        (u'Comptes utilisateurs', [user.Group, user.User]),
        (u'Gestion sociale', [user.ZoneOption]),
    )


def includeme(config):
    """
        Add module's views
    """
    # Configuration routes
    config.add_route("admin_index", "/admin")
    config.add_route("admin_main", "/admin/main")
    config.add_route("admin_accompagnement", "admin/accompagnement")
    config.add_route("admin_activity", "admin/activity")
    config.add_route("admin_workshop", "admin/workshop")
    config.add_route("admin_userdatas", "admin/userdatas")
    config.add_route("admin_console", "admin_console/")
    config.add_route(
        'template',
        'admin/templates/{id}',
        traverse="templates/{id}",
    )

    config.add_admin_view = functools.partial(
        config.add_view,
        permission='admin',
        renderer="admin/main.mako",
    )

    config.add_admin_view(
        index,
        route_name='admin_index',
    )

    config.add_admin_view(
        AdminMain,
        route_name="admin_main",
    )

    for model in (CompanyActivity, ):
        view, route_name, tmpl = get_model_admin_view(
            model,
            r_path="admin_index",
        )
        config.add_route(route_name, "admin/" + route_name)
        config.add_admin_view(
            view,
            route_name=route_name,
            renderer=tmpl,
        )

    include_userdatas_views(config)

    config.add_admin_view(
        admin_accompagnement_index_view,
        route_name='admin_accompagnement',
    )

    config.add_admin_view(
        AdminActivities,
        route_name='admin_activity',
    )

    config.add_admin_view(
        AdminWorkshop,
        route_name='admin_workshop',
    )
    # Hidden console view
    config.add_admin_view(
        console_view,
        route_name="admin_console",
    )
