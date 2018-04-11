# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
from autonomie.models.config import (
    Config,
    ConfigFiles,
)
from autonomie.models.activity import (
    ActivityType,
    ActivityMode,
)
from autonomie.forms import (
    merge_session_with_post,
)
from autonomie.views import submit_btn
from autonomie.views.admin import (
    AdminIndexView,
    BASE_URL,
)
from autonomie.views.admin.tools import (
    BaseAdminFormView,
    BaseAdminIndexView,
)


ACCOMPAGNEMENT_URL = os.path.join(BASE_URL, 'accompagnement')


class AccompagnementIndexView(BaseAdminIndexView):
    route_name = ACCOMPAGNEMENT_URL
    title = u"Module Accompagnement"
    description = u"Ateliers, Rendez-vous, Compétences"


class BaseAdminAccompagnement(BaseAdminFormView):
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


def includeme(config):
    config.add_route(ACCOMPAGNEMENT_URL, ACCOMPAGNEMENT_URL)
    config.add_admin_view(
        AccompagnementIndexView, parent=AdminIndexView
    )
    config.include('.activities')
    config.include('.workshop')
    config.include('.competence')
