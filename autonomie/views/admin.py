# -*- coding: utf-8 -*-
# * File Name : admin.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Administration views
    - config table configuration
    - welcome message
    - logo upload
"""
import logging

from pyramid.httpexceptions import HTTPFound
from autonomie.models.config import Config
from autonomie.models.tva import Tva
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.views import submit_btn
from autonomie.views.forms import MainConfig
from autonomie.views.forms import TvaConfig
from autonomie.views.forms.admin import get_config_appstruct
from autonomie.views.forms.admin import merge_dbdatas
from autonomie.views.forms import BaseFormView
from autonomie.utils.widgets import ActionMenu
from autonomie.utils.widgets import ViewLink

log = logging.getLogger(__name__)

def index(request):
    """
        Return datas for the index view
    """
    menu = ActionMenu()
    menu.add(ViewLink(u"Configuration générale", path='admin_main',
           title=u"Configuration générale de votre installation d'autonomie"))
    menu.add(ViewLink(u"Configuration des taux de TVA", path='admin_tva',
            title=u"Configuration des taux de TVA proposés dans les devis et \
factures"))
    return dict(title=u"Administration du site", action_menu=menu)


class AdminMain(BaseFormView):
    """
        Main configuration view
    """
    add_template_vars = ('title',)
    title = u"Configuration générale"
    validation_msg = u"La configuration a bien été modifiée"
    schema = MainConfig()
    buttons = (submit_btn,)

    def before(self, form):
        """
            Add the appstruct to the form
        """
        config_dict = self.request.config
        appstruct = get_config_appstruct(config_dict)
        form.appstruct = appstruct

    def submit_success(self, appstruct):
        """
            Insert config informations into database
        """
        # la table config étant un stockage clé valeur
        # le merge_session_with_post ne peut être utilisé
        dbdatas = self.dbsession.query(Config).all()
        dbdatas = merge_dbdatas(dbdatas, appstruct)
        for dbdata in dbdatas:
            self.dbsession.merge(dbdata)
        self.dbsession.flush()
        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("admin_main"))


class AdminTva(BaseFormView):
    """
        Tva administration view
        Set tvas used in invoices, estimations and cancelinvoices
    """
    add_template_vars = ('title',)
    title = u"Configuration des taux de TVA"
    validation_msg = u"Les taux de TVA ont bien été modifiés"
    schema = TvaConfig()
    buttons = (submit_btn,)

    def before(self, form):
        """
            Add appstruct to the current form object
        """
        appstruct = [{'name':tva.name,
                      'value':tva.value,
                      "default":tva.default}for tva in Tva.query().all()]
        form.appstruct = {'tvas':appstruct}

    def submit_success(self, appstruct):
        """
            fired on submit success, set Tvas
        """
        for tva in Tva.query().all():
            self.dbsession.delete(tva)
            self.dbsession.flush()
        for data in appstruct['tvas']:
            tva = Tva()
            merge_session_with_post(tva, data)
            self.dbsession.merge(tva)
        self.dbsession.flush()
        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("admin_tva"))


def includeme(config):
    """
        Add module's views
    """
    # Administration routes
    config.add_route("admin_index",
                     "/admin")
    config.add_route("admin_main",
                    "/admin/main")
    config.add_route("admin_tva",
                    "/admin/tva")
    config.add_view(index, route_name='admin_index',
                 renderer='admin/index.mako',
                 permission='admin')
    config.add_view(AdminMain, route_name="admin_main",
                 renderer="admin/main.mako",
                 permission='admin')
    config.add_view(AdminTva, route_name='admin_tva',
                 renderer="admin/tva.mako",
                 permission='admin')
