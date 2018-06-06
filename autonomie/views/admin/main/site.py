# -*- coding: utf-8 -*-
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
#
import logging
import os

from pyramid.httpexceptions import HTTPFound
from autonomie.models.config import (
    Config,
    ConfigFiles,
)
from autonomie.forms import public_file_appstruct
from autonomie.forms.admin.main.site import SiteConfigSchema
from autonomie.views.admin.tools import (
    BaseAdminFormView,
)
from autonomie.views.admin.main import (
    MainIndexView,
    MAIN_ROUTE,
)

MAIN_SITE_ROUTE = os.path.join(MAIN_ROUTE, 'site')


logger = logging.getLogger(__name__)


class AdminSiteView(BaseAdminFormView):
    """
    Admin Autonomie welcome page
    """
    title = u"Logo et page d'accueil"
    description = u"Configurer le message d'accueil et le logo utilisé sur la \
page de connexion"
    route_name = MAIN_SITE_ROUTE
    schema = SiteConfigSchema()
    validation_msg = u"Vos modification ont été enregistrées"

    def before(self, form):
        """
            Add the appstruct to the form
        """
        config_dict = self.request.config
        logo = ConfigFiles.get('logo.png')
        appstruct = {}
        if logo is not None:
            appstruct["logo"] = public_file_appstruct(
                self.request, 'logo.png', logo
            )
        appstruct['welcome'] = config_dict.get('welcome', '')
        form.set_appstruct(appstruct)

    def submit_success(self, appstruct):
        """
            Insert config informations into database
        """
        # la table config étant un stockage clé valeur
        # le merge_session_with_post ne peut être utilisé
        logo = appstruct.pop('logo', None)
        if logo:
            ConfigFiles.set('logo.png', logo)
            self.request.session.pop('substanced.tempstore')
            self.request.session.changed()

        for key, value in appstruct.items():
            Config.set(key, value)
        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path(self.route_name))

#
# class AdminMainView(BaseAdminFormView):
#     """
#         Main configuration view
#     """
#     title = u"Configuration générale"
#     route_name = MAIN_ROUTE
#     description = u"Message d'accueil, logos, entête et pieds de page des \
# devis, factures / avoir)"
#
#     validation_msg = u"La configuration a bien été modifiée"
#     schema = MainConfig()
#     buttons = (submit_btn,)
#
#     def before(self, form):
#         """
#             Add the appstruct to the form
#         """
#         config_dict = self.request.config
#         logo = ConfigFiles.get('logo.png')
#         appstruct = get_config_appstruct(self.request, config_dict, logo)
#         form.set_appstruct(appstruct)
#
#     def submit_success(self, appstruct):
#         """
#             Insert config informations into database
#         """
#         # la table config étant un stockage clé valeur
#         # le merge_session_with_post ne peut être utilisé
#         logo = appstruct['site'].pop('logo', None)
#         if logo:
#             ConfigFiles.set('logo.png', logo)
#             self.request.session.pop('substanced.tempstore')
#             self.request.session.changed()
#
#         dbdatas = self.dbsession.query(Config).all()
#         appstruct = get_config_dbdatas(appstruct)
#         dbdatas = merge_config_datas(dbdatas, appstruct)
#         for dbdata in dbdatas:
#             self.dbsession.merge(dbdata)
#         self.dbsession.flush()
#         self.request.session.flash(self.validation_msg)
#         return HTTPFound(self.request.route_path(self.route_name))


def includeme(config):
    config.add_route(MAIN_SITE_ROUTE, MAIN_SITE_ROUTE)
    config.add_admin_view(
        AdminSiteView,
        parent=MainIndexView,
    )
