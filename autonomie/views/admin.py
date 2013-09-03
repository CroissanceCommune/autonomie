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
from autonomie.models.tva import (
        Tva,
        Product)
from autonomie.models.task.invoice import PaymentMode
from autonomie.models.task import WorkUnit
from autonomie.models.treasury import (
        ExpenseType,
        ExpenseKmType,
        ExpenseTelType,
)
from autonomie.models.company import Company

from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.views import submit_btn
from autonomie.views.forms.admin import (
        MainConfig,
        TvaConfig,
        PaymentModeConfig,
        WorkUnitConfig,
        ExpenseTypesConfig,
        CAECONFIG,
        get_config_appstruct,
        get_config_dbdatas,
        merge_config_datas,
        )
from autonomie.views.forms import BaseFormView
from autonomie.utils.widgets import ViewLink
from js.tinymce import tinymce

log = logging.getLogger(__name__)

def index(request):
    """
        Return datas for the index view
    """
    request.actionmenu.add(ViewLink(u"Configuration générale",
        path='admin_main',
        title=u"Configuration générale de votre installation d'autonomie"))
    request.actionmenu.add(ViewLink(u"Configuration des taux de TVA",
        path='admin_tva',
        title=u"Configuration des taux de TVA proposés dans les devis et \
factures"))
    request.actionmenu.add(ViewLink(u"Configuration des modes de paiement",
        path="admin_paymentmode",
        title=u"Configuration des modes de paiement des factures"))
    request.actionmenu.add(ViewLink(u"Configuration des unités de prestation",
        path="admin_workunit",
        title=u"Configuration des unités de prestation proposées \
dans les formulaires"))
    request.actionmenu.add(ViewLink(u"Configuration des notes de frais",
        path="admin_expense",
        title=u"Configuration des types de notes de frais"))
    request.actionmenu.add(ViewLink(u"Configuration des informations comptables\
            de la CAE",
        path="admin_cae",
        title=u"Configuration des différents comptes analytiques de la CAE"))
    return dict(title=u"Administration du site")


def populate_actionmenu(request):
    """
        Add a back to index link
    """
    request.actionmenu.add(ViewLink(u"Revenir à l'index", path="admin_index",
        title=u"Revenir à l'index de l'administration"))


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
        form.set_appstruct(appstruct)
        populate_actionmenu(self.request)
        tinymce.need()

    def submit_success(self, appstruct):
        """
            Insert config informations into database
        """
        # la table config étant un stockage clé valeur
        # le merge_session_with_post ne peut être utilisé
        dbdatas = self.dbsession.query(Config).all()
        appstruct = get_config_dbdatas(appstruct)
        dbdatas = merge_config_datas(dbdatas, appstruct)
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
                      "default":tva.default,
                      "compte_cg":tva.compte_cg,
                      "products":[{"name":product.name,
                                   "compte_cg":product.compte_cg}
                                   for product in tva.products]}
                                   for tva in Tva.query().all()]
        form.set_appstruct({'tvas':appstruct})
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        """
            fired on submit success, set Tvas
        """
        for tva in Tva.query().all():
            self.dbsession.delete(tva)
        for data in appstruct['tvas']:
            products = data.pop('products')
            tva = Tva()
            merge_session_with_post(tva, data)
            self.dbsession.add(tva)
            for product in products:
                product_obj = Product()
                merge_session_with_post(product_obj, product)
                product_obj.tva = tva
                self.dbsession.add(product_obj)
        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("admin_tva"))


class AdminPaymentMode(BaseFormView):
    """
        Payment Mode administration view
        Allows to set different payment mode
    """
    title = u"Configuration des modes de paiement"
    validation_msg = u"Les modes de paiement ont bien été modifiés"
    schema = PaymentModeConfig()
    buttons = (submit_btn,)

    def before(self, form):
        """
            Add appstruct to the current form object
        """
        appstruct = [mode.label for mode in PaymentMode.query()]
        form.set_appstruct({'paymentmodes':appstruct})
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        """
            handle successfull payment mode configuration
        """
        for mode in PaymentMode.query():
            self.dbsession.delete(mode)
        for data in appstruct['paymentmodes']:
            mode = PaymentMode(label=data)
            self.dbsession.add(mode)
        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("admin_paymentmode"))


class AdminWorkUnit(BaseFormView):
    """
        Work Unit administration view
        Allows to configure custom unities
    """
    title = u"Configuration des unités de prestation"
    validation_msg = u"Les unités de prestation ont bien été modifiées"
    schema = WorkUnitConfig()
    buttons = (submit_btn,)

    def before(self, form):
        """
            Add appstruct to the current form object
        """
        appstruct = [mode.label for mode in WorkUnit.query()]
        form.set_appstruct({'workunits':appstruct})
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        """
            Handle successfull work unit configuration
        """
        for unit in WorkUnit.query():
            self.dbsession.delete(unit)
        for data in appstruct['workunits']:
            unit = WorkUnit(label=data)
            self.dbsession.add(unit)
        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("admin_workunit"))


class AdminExpense(BaseFormView):
    """
        Expense administration view
        Allows to configure expense types and codes
    """
    title = u"Configuration des notes de frais"
    validation_msg = u"Les différents paramètres des notes de frais \
ont été configurés"
    schema = ExpenseTypesConfig()
    buttons = (submit_btn,)
    factories = {'expenses':(ExpenseType, 'expense'),
                 'expenseskm':(ExpenseKmType, 'expensekm'),
                 'expensestel':(ExpenseTelType, 'expensetel')}

    def before(self, form):
        """
            Add appstruct to the current form object
        """
        appstruct = {}
        for key, (factory, polytype) in self.factories.items():
            appstruct[key] = [e.appstruct() for e in factory.query()\
                                            .filter(factory.type==polytype)\
                                            .filter(factory.active==True)]
        form.set_appstruct(appstruct)
        populate_actionmenu(self.request)

    def get_all_ids(self, appstruct):
        """
            Return the ids of the options still present in the submitted form
        """
        ids = []
        for key in self.factories:
            ids.extend([data['id'] for data in appstruct[key]])
        return ids

    def submit_success(self, appstruct):
        """
            Handle successfull expense configuration
        """
        all_ids = self.get_all_ids(appstruct)

        # We delete the elements that are no longer in the appstruct
        for (factory, polytype) in self.factories.values():
            for element in factory.query().filter(factory.type==polytype):
                if element.id not in all_ids:
                    element.active = False
                    self.dbsession.merge(element)
        self.dbsession.flush()

        for key, (factory, polytype) in self.factories.items():
            for data in appstruct[key]:
                if data['id'] is not None:
                    type_ = factory.query()\
                            .filter(factory.id==data['id'])\
                            .filter(factory.active==True)\
                            .one()
                    merge_session_with_post(type_, data)
                    self.dbsession.merge(type_)
                else:
                    type_ = factory()
                    merge_session_with_post(type_, data)
                    self.dbsession.add(type_)
        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("admin_expense"))


class AdminCae(BaseFormView):
    """
        Cae information configuration
    """
    title = u"Configuration de la CAE"
    validation_msg = u"Les informations ont bien été enregistrées"
    schema = CAECONFIG
    buttons = (submit_btn, )

    def before(self, form):
        """
            Add the appstruct to the form
        """
        appstruct = self.request.config
        form.set_appstruct(appstruct)
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        """
            Insert config informations into database
        """
        # la table config étant un stockage clé valeur
        # le merge_session_with_post ne peut être utilisé
        dbdatas = self.dbsession.query(Config).all()
        log.debug("appstruct")
        log.debug(appstruct)
        new_dbdatas = merge_config_datas(dbdatas, appstruct)
        log.debug("New config")
        for dbdata in new_dbdatas:
            log.debug(dbdata.name)
            if dbdata in dbdatas:
                self.dbsession.merge(dbdata)
            else:
                self.dbsession.add(dbdata)
            # If we set the contribution_cae value, we want it to be the default
            # for every company that has no contribution value set
            if dbdata.name == 'contribution_cae':
                for comp in Company.query():
                    if comp.contribution is None:
                        comp.contribution = dbdata.value
                        self.dbsession.merge(comp)
        self.dbsession.flush()
        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("admin_cae"))


def includeme(config):
    """
        Add module's views
    """
    # Administration routes
    config.add_route("admin_index", "/admin")
    config.add_route("admin_main", "/admin/main")
    config.add_route("admin_tva", "/admin/tva")
    config.add_route("admin_paymentmode", "admin/paymentmode")
    config.add_route("admin_workunit", "admin/workunit")
    config.add_route("admin_expense", "admin/expense")
    config.add_route("admin_cae", "admin/cae")
    config.add_view(index, route_name='admin_index',
                 renderer='admin/index.mako',
                 permission='admin')
    config.add_view(AdminMain, route_name="admin_main",
                 renderer="admin/main.mako",
                 permission='admin')
    config.add_view(AdminTva, route_name='admin_tva',
                 renderer="admin/main.mako",
                 permission='admin')
    config.add_view(AdminPaymentMode, route_name='admin_paymentmode',
                renderer="admin/main.mako",
                permission='admin')
    config.add_view(AdminWorkUnit, route_name='admin_workunit',
                renderer="admin/main.mako",
                permission='admin')
    config.add_view(AdminExpense, route_name='admin_expense',
                renderer="admin/main.mako",
                permission='admin')
    config.add_view(AdminCae, route_name='admin_cae',
            renderer="admin/main.mako",
            permission="admin")
