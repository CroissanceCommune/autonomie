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
from autonomie.models.activity import (
        ActivityType,
        ActivityMode,
        )
from autonomie.models.company import Company

from autonomie.utils.views import submit_btn
from autonomie.views.forms.admin import (
        MainConfig,
        TvaConfig,
        PaymentModeConfig,
        WorkUnitConfig,
        ExpenseTypesConfig,
        ActivityTypesConfig,
        CAECONFIG,
        get_config_appstruct,
        get_config_dbdatas,
        merge_config_datas,
        )
from autonomie.views.forms import (
        BaseFormView,
        merge_session_with_post,
        )
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
    request.actionmenu.add(ViewLink(u"Configuration du module accompagnement",
        path="admin_activity",
        title=u"Configuration des types d'activité du module accompagnement"))
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
        appstruct = []
        for tva in Tva.query().all():
            struct = tva.appstruct()
            struct['products'] = [product.appstruct()
                    for product in tva.products]
            appstruct.append(struct)

        form.set_appstruct({'tvas':appstruct})
        populate_actionmenu(self.request)
        log.debug("AdminTva struct: %s", appstruct)

    @staticmethod
    def get_remaining_prod_ids(appstruct):
        """
            return id of products remaining in the submitted config
        """
        ids = []
        for tva in appstruct['tvas']:
            ids.extend([product['id'] for product in tva['products']])
        return ids

    @staticmethod
    def get_remaining_tva_ids(appstruct):
        """
            Return ids of tva remaining in the submitted config
        """
        return [tva['id'] for tva in appstruct['tvas']]

    def disable_elements(self, factory, ids):
        """
            Disable elements of type "factory" that are not in the ids list
        """
        for element in factory.query(include_inactive=True).all():
            if element.id not in ids:
                element.active = False
                self.dbsession.merge(element)

    def submit_success(self, appstruct):
        """
            fired on submit success, set Tvas
        """
        # First we disable the elements that are no longer part of the
        # configuration
        self.disable_elements(Product, self.get_remaining_prod_ids(appstruct))
        self.disable_elements(Tva, self.get_remaining_tva_ids(appstruct))
        self.dbsession.flush()

        for data in appstruct['tvas']:
            products = data.pop('products')
            if data['id'] != 0:
                tva = Tva.get(data['id'])
                merge_session_with_post(tva, data)
                tva = self.dbsession.merge(tva)
            else:
                tva = Tva()
                merge_session_with_post(tva, data)
                self.dbsession.add(tva)

            for prod in products:
                if prod['id'] is not None:
                    product = Product.get(prod['id'])
                    product.tva = tva
                    merge_session_with_post(product, prod)
                    self.dbsession.merge(product)
                else:
                    product = Product()
                    merge_session_with_post(product, prod)
                    product.tva = tva
                    self.dbsession.add(product)
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
        compte_cg = self.request.config.get('compte_cg_ndf', '')

        for key, (factory, polytype) in self.factories.items():
            appstruct[key] = [e.appstruct() for e in factory.query()\
                                            .filter(factory.type==polytype)\
                                            .filter(factory.active==True)]
        appstruct['compte_cg'] = compte_cg
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

    def _get_actual_compte_cg(self):
        """
        Return the actual configured compte_cg object
        """
        return Config.get("compte_cg_ndf")

    def _set_compte_cg(self, appstruct):
        """
        Set the compte cg
        :param appstruct: the form submitted values
        """
        cg_obj = self._get_actual_compte_cg()
        value = appstruct.pop('compte_cg', None)

        if value:
            if cg_obj is None:
                cg_obj = Config(name="compte_cg_ndf", value=value)
                self.dbsession.add(cg_obj)

            else:
                cg_obj.value = value
                self.dbsession.merge(cg_obj)

        log.debug(u"Setting the new compte CG : {0}".format(value))

    def submit_success(self, appstruct):
        """
        Handle successfull expense configuration
        :param appstruct: submitted datas
        """
        all_ids = self.get_all_ids(appstruct)

        # We delete the elements that are no longer in the appstruct
        for (factory, polytype) in self.factories.values():
            for element in factory.query().filter(factory.type==polytype):
                if element.id not in all_ids:
                    element.active = False
                    self.dbsession.merge(element)
        self.dbsession.flush()

        self._set_compte_cg(appstruct)

        for key, (factory, polytype) in self.factories.items():
            for data in appstruct[key]:
                if data['id'] is not None:
                    type_ = factory.get(data['id'])
                    merge_session_with_post(type_, data)
                    self.dbsession.merge(type_)
                else:
                    type_ = factory()
                    merge_session_with_post(type_, data)
                    self.dbsession.add(type_)

        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("admin_expense"))


class AdminActivities(BaseFormView):
    """
        Activity types config
    """
    title = u"Configuration des activités"
    validation_msg = u"Les activités ont bien été configurées"
    schema = ActivityTypesConfig(title=u"")
    buttons = (submit_btn,)

    def before(self, form):
        """
            Add appstruct to the current form object
        """
        query = ActivityType.query()
        types = query.filter(ActivityType.active==True)

        modes = ActivityMode.query()

        appstruct = {
                'types': [type_.appstruct() for type_ in types],
                'modes': [mode.appstruct() for mode in modes],
                }

        form.set_appstruct(appstruct)
        populate_actionmenu(self.request)

    def get_submitted_type_ids(self, appstruct):
        """
            Return the ids of the options still present in the submitted form
        """
        return [data['id'] for data in appstruct["types"]]

    def get_submitted_modes(self, appstruct):
        return [data['label'] for data in appstruct['modes']]

    def submit_success(self, appstruct):
        """
            Handle successfull expense configuration
        """
        all_type_ids = self.get_submitted_type_ids(appstruct)
        all_modes = self.get_submitted_modes(appstruct)

        # We delete the elements that are no longer in the appstruct
        for element in ActivityType.query():
            if element.id not in all_type_ids:
                element.active = False
                self.dbsession.merge(element)
        for element in ActivityMode.query():
            if element.label not in all_modes:
                self.dbsession.delete(element)
            else:
                # Remove it from the submitted list so we don't insert it again
                all_modes.remove(element.label)
        self.dbsession.flush()

        for data in appstruct["types"]:
            if data['id'] is not None:
                type_ = ActivityType.get(data['id'])
                merge_session_with_post(type_, data)
                self.dbsession.merge(type_)
            else:
                type_ = ActivityType()
                merge_session_with_post(type_, data)
                self.dbsession.add(type_)
        for mode in all_modes:
            new_mode = ActivityMode(label=mode)
            self.dbsession.add(new_mode)

        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("admin_activity"))


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
        appstruct = {}
        for key, value in self.request.config.items():
            if key.startswith('sage'):
                appstruct.setdefault('sage_export', {})[key] = value
            else:
                appstruct[key] = value

        form.set_appstruct(appstruct)
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        """
            Insert config informations into database
        """
        # la table config étant un stockage clé valeur
        # le merge_session_with_post ne peut être utilisé
        dbdatas = Config.query().all()

        log.debug(u"Cae configuration submission")
        log.debug(appstruct)

        new_dbdatas = merge_config_datas(dbdatas, appstruct)
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
    config.add_route("admin_activity", "admin/activity")
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
    config.add_view(AdminActivities, route_name='admin_activity',
                renderer="admin/main.mako",
                permission='admin')
    config.add_view(AdminCae, route_name='admin_cae',
            renderer="admin/main.mako",
            permission="admin")
