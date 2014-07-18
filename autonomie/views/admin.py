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
    ActivityAction,
)
from autonomie.utils.ascii import (
    camel_case_to_name,
)
from autonomie.models.company import Company
from autonomie.models.user import (
    ZoneOption,
    ZoneQualificationOption,
    StudyLevelOption,
    SocialStatusOption,
    ActivityTypeOption,
    PcsOption,
    PrescripteurOption,
    NonAdmissionOption,
    ParcoursStatusOption,
    MotifSortieOption,
    SocialDocTypeOption,
)

from autonomie.views.forms import submit_btn
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
    get_sequence_model_admin,
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
    request.actionmenu.add(
        ViewLink(
            u"Administration de la gestion sociale",
            path='admin_userdatas',
            title=u"Configuration des types pour la gestion sociale",
        )
    )
    return dict(title=u"Administration du site")


def make_enter_point_view(parent_route, views_to_link_to, title=u""):
    """
    Builds a view with links to the views passed as argument

        views_to_link_to

            list of 2-uples (view_obj, route_name) we'd like to link to

        parent_route

            route of the parent page
    """
    def myview(request):
        """
        The dinamycally built view
        """
        request.actionmenu.add(
            ViewLink(
                u"Retour",
                path=parent_route
            )
        )
        for view, route_name in views_to_link_to:
            request.actionmenu.add(
                ViewLink(
                    view.title,
                    path=route_name,
                    title=view.title,
                )
            )
        return dict(title=title)
    return myview


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
                if prod['id'] != 0:
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

    def _get_config_key(self, rel_keyname):
        return rel_keyname + "_ndf"

    def before(self, form):
        """
        Add appstruct to the current form object
        """
        appstruct = {}

        for key in ('code_journal', 'compte_cg'):
            cfg_key = self._get_config_key(key)
            appstruct[key] = self.request.config.get(cfg_key, '')

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

    def _get_actual_config_obj(self, config_key):
        """
        Return the actual configured compte_cg object
        """
        return Config.get(config_key)

    def _set_config_value(self, appstruct, config_key, appstruct_key):
        """
        Set a config value
        :param appstruct: the form submitted values
        :param config_key: The name of the configuration key
        :param appstruct_key: The name of the key in the appstruct
        """
        cfg_obj = self._get_actual_config_obj(config_key)
        value = appstruct.pop(appstruct_key, None)

        if value:
            if cfg_obj is None:
                cfg_obj = Config(name=config_key, value=value)
                self.dbsession.add(cfg_obj)

            else:
                cfg_obj.value = value
                self.dbsession.merge(cfg_obj)

        log.debug(u"Setting the new {0} : {1}".format(config_key, value))

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

        for key in ('code_journal', 'compte_cg'):
            cfg_key = self._get_config_key(key)
            self._set_config_value(appstruct, cfg_key, key)

        for key, (factory, polytype) in self.factories.items():
            for data in appstruct[key]:
                if data['id'] != 0:
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

        query = ActivityAction.query()
        query = query.filter(ActivityAction.parent_id==None)
        actions = query.filter(ActivityAction.active==True)

        appstruct = {
            'types': [type_.appstruct() for type_ in types],
            'modes': [mode.appstruct() for mode in modes],
            'actions': [
                {
                'id': act.id,
                'label': act.label,
                'children': [child.appstruct() for child in act.children],
                }
                for act in actions]
            }

        print appstruct

        form.set_appstruct(appstruct)
        populate_actionmenu(self.request)

    def get_edited_elements(self, appstruct, key):
        """
        Return a dict id:data for the elements that are edited (with an id)
        """
        return dict((data['id'], data) for data in appstruct.get(key, {}) \
            if data.get('id') !=0)

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

    def disable_actions(self, appstruct):
        """
        Disable actions that are not active anymore
        """
        edited_actions = self.get_edited_elements(appstruct, 'actions')

        for element in ActivityAction.query()\
                .filter(ActivityAction.parent_id==None):
            if element.id not in edited_actions.keys():
                element.active = False
                self.dbsession.merge(element)
            # On désactive ensuite les enfants
            datas = edited_actions.get(element.id, {})
            edited_children = self.get_edited_elements(
                datas, "children")
            for child in element.children:
                if child.id in edited_children.keys():
                    child.active = False
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
        if datas['id'] != 0:
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
        """
        for mode in new_modes:
            new_mode_obj = ActivityMode(label=mode)
            self.dbsession.add(new_mode_obj)

    def add_actions(self, appstruct):
        """
        Add new actions
        """
        for data in appstruct["actions"]:
            # First replace children datas by children objects
            children_datas = data.pop('children')
            data['children'] = []
            for child_datas in children_datas:
                child = self._add_or_edit(child_datas, ActivityAction)
                data['children'].append(child)

            self._add_or_edit(data, ActivityAction)

    def submit_success(self, appstruct):
        """
            Handle successfull expense configuration
        """
        # We delete the elements that are no longer in the appstruct
        self.disable_types(appstruct)
        self.disable_actions(appstruct)
        new_modes = self.delete_modes(appstruct)
        self.dbsession.flush()

        self.add_types(appstruct)
        self.add_actions(appstruct)
        self.add_modes(new_modes)

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


class AdminOption(BaseFormView):
    """
    Main view for option configuration
    It allows to configure a set of models

        factory

            The model we are manipulating.

        disable

            If the model has an "active" column, it can be used to
            enable/disable elements

        validation_msg

            The message shown to the end user on successfull validation

        redirect_path

            The route we're redirecting to after successfull validation
    """
    title = u""
    validation_msg = u""
    factory = None
    redirect_path = 'admin_index'
    disable = True
    _schema = None

    @property
    def schema(self):
        if self._schema is None:
            self._schema = get_sequence_model_admin(
                self.factory,
                self.title,
            )
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value

    def before(self, form):
        """
        Populate the form with existing elements
        """
        appstruct = {'datas': [elem.appstruct() \
                               for elem in self.factory.query()]}
        form.set_appstruct(appstruct)
        self.populate_actionmenu()

    def populate_actionmenu(self):
        self.request.actionmenu.add(
            ViewLink(u"Retour", path=self.redirect_path)
        )

    def _get_edited_elements(self, appstruct):
        """
        Return the elements that are edited (already have an id)
        """
        return dict((data['id'], data) \
                    for data in appstruct.get('datas', {}) \
                    if data.get('id') != 0
                   )

    def _disable_or_remove_elements(self, appstruct):
        """
        Disable existing elements that are no more in the results
        """
        edited = self._get_edited_elements(appstruct)

        for element in self.factory.query():
            if element.id not in edited.keys():
                if self.disable:
                    element.active = False
                    self.dbsession.merge(element)
                else:
                    self.dbsession.delete(element)

    def _add_or_edit(self, datas):
        """
        Add or edit an element of the given factory
        """
        node_schema = self.schema.children[0].children[0]
        element = node_schema.objectify(datas)
        if element.id != 0:
            element = self.dbsession.merge(element)
        else:
            self.dbsession.add(element)
        return element

    def submit_success(self, appstruct):
        """
        Handle successfull submission
        """
        self._disable_or_remove_elements(appstruct)

        for datas in appstruct.get('datas', []):
            self._add_or_edit(datas)

        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path(self.redirect_path))


def get_model_view(model):
    infos = model.__colanderalchemy_config__
    view_title = infos.get('title', u'Titre inconnu')
    class MyView(AdminOption):
        title = view_title
        validation_msg = infos.get('validation_msg', u'')
        factory = model
        schema = get_sequence_model_admin(model, u"")
        redirect_path = 'admin_userdatas'
    return (
        MyView,
        camel_case_to_name(model.__name__),
    )


def get_all_option_views():
    """
    Return view_class, route_name for all option configuration views
    """
    for model in (
        ZoneOption,
        ZoneQualificationOption,
        StudyLevelOption,
        SocialStatusOption,
        ActivityTypeOption,
        PcsOption,
        PrescripteurOption,
        NonAdmissionOption,
        ParcoursStatusOption,
        MotifSortieOption,
        SocialDocTypeOption,
    ):
        yield get_model_view(model)


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


    # User Datas view configuration
    config.add_route("admin_userdatas", "admin/userdatas")

    all_option_views = list(get_all_option_views())
    for view, route_name in all_option_views:
        config.add_route(route_name, "admin/" + route_name)
        config.add_view(
            view,
            route_name=route_name,
            renderer="admin/main.mako",
            permission="admin",
        )

    config.add_view(
        make_enter_point_view(
            'admin_index',
            all_option_views,
            u"Administration de la gestion sociale"
        ),
        route_name="admin_userdatas",
        renderer='admin/index.mako',
        permission="admin",
    )


