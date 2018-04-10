# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
from pyramid.httpexceptions import HTTPFound
from autonomie.forms.admin import (
    ActivityConfigSchema,
)
from autonomie.models.activity import (
    ActivityType,
    ActivityMode,
    ActivityAction,
)
from autonomie.views.admin.accompagnement import (
    BaseAdminAccompagnement,
    AccompagnementIndexView,
    ACCOMPAGNEMENT_URL,
)


ACTIVITY_URL = os.path.join(ACCOMPAGNEMENT_URL, 'activity')


class AdminActivitiesView(BaseAdminAccompagnement):
    """
    Activities Admin view
    """
    title = u"Configuration du module de Rendez-vous"
    schema = ActivityConfigSchema(title=u"")
    route_name = ACTIVITY_URL

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
            self.request.route_path(self.parent_view.route_name)
        )


def includeme(config):
    config.add_route(ACTIVITY_URL, ACTIVITY_URL)
    config.add_admin_view(AdminActivitiesView, parent=AccompagnementIndexView)
