# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
View related to admin configuration
"""
import logging
import os

from pyramid.httpexceptions import HTTPFound
from autonomie.models.config import (
    Config,
)
from autonomie.forms.admin.main.contact import ContactConfigSchema
from autonomie.views.admin.tools import (
    BaseAdminFormView,
)
from autonomie.views.admin.main import (
    MainIndexView,
    MAIN_ROUTE,
)

MAIN_CONTACT_ROUTE = os.path.join(MAIN_ROUTE, 'contact')


logger = logging.getLogger(__name__)


class AdminContactView(BaseAdminFormView):
    """
    Admin Autonomie welcome page
    """
    title = u"Adresse e-mail de contact"
    description = u"Configurer l'adresse utilisée par Autonomie pour vous \
envoyer des messages (traitement des fichiers ...)"
    route_name = MAIN_CONTACT_ROUTE
    schema = ContactConfigSchema()
    validation_msg = u"Vos modification ont été enregistrées"

    def before(self, form):
        """
            Add the appstruct to the form
        """
        appstruct = {}
        config_dict = self.request.config
        for key, value in config_dict.items():
            if key in self.schema:
                appstruct[key] = value
        form.set_appstruct(appstruct)

    def submit_success(self, appstruct):
        """
            Insert config informations into database
        """
        for key, value in appstruct.items():
            Config.set(key, value)
        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path(self.route_name))


def includeme(config):
    config.add_route(MAIN_CONTACT_ROUTE, MAIN_CONTACT_ROUTE)
    config.add_admin_view(
        AdminContactView,
        parent=MainIndexView,
    )
