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
from autonomie.forms.admin import (
    MainConfig,
    get_config_appstruct,
    get_config_dbdatas,
    merge_config_datas,
)
from autonomie.views import (
    submit_btn,
)
from autonomie.views.admin import (
    AdminIndexView,
    BASE_URL,
)
from autonomie.views.admin.tools import (
    BaseAdminFormView,
)

MAIN_URL = os.path.join(BASE_URL, 'main')


logger = logging.getLogger(__name__)


class AdminMainView(BaseAdminFormView):
    """
        Main configuration view
    """
    title = u"Configuration générale"
    route_name = MAIN_URL
    description = u"Message d'accueil, logos, entête et pieds de page des \
devis, factures / avoir)"

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
        return HTTPFound(self.request.route_path(self.route_name))


def includeme(config):
    config.add_route(MAIN_URL, MAIN_URL)
    config.add_admin_view(
        AdminMainView,
        parent=AdminIndexView,
    )
