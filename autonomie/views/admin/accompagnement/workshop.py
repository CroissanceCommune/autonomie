# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
from pyramid.httpexceptions import HTTPFound
from autonomie.forms.admin import (
    WorkshopConfigSchema,
)
from autonomie.models.workshop import WorkshopAction
from autonomie.views.admin.accompagnement import (
    BaseAdminAccompagnement,
    AccompagnementIndexView,
    ACCOMPAGNEMENT_URL,
)


WORKSHOP_URL = os.path.join(ACCOMPAGNEMENT_URL, 'workshop')


class AdminWorkshopView(BaseAdminAccompagnement):
    """
    Workshops administration views
    """
    title = u"Configuration du module Atelier"
    schema = WorkshopConfigSchema(title=u"")
    route_name = WORKSHOP_URL

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
            self.request.route_path(self.parent_view.route_name)
        )


def includeme(config):
    config.add_route(WORKSHOP_URL, WORKSHOP_URL)
    config.add_admin_view(AdminWorkshopView, parent=AccompagnementIndexView)
