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
    Action on document/task handling
    Handles the buttons available for the different actions possible on the
    documents regarding the current request, the state ...
"""
import logging

from pyramid.security import has_permission
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPFound

from deform import Button
from deform import Form

from autonomie.events.tasks import StatusChanged
from autonomie.exception import Forbidden
from autonomie.utils.pdf import (
    write_pdf,
    render_html,
)
from autonomie.resources import (
    task,
    duplicate as duplicate_js,
)
from autonomie.utils.widgets import (
    Submit,
    ViewLink,
    PopUp,
)
from autonomie.models.customer import Customer
from autonomie.models.project import (
    Project,
    Phase,
)
from autonomie.models.tva import Tva
from autonomie.views import (
    BaseView,
    BaseFormView,
)
from autonomie.forms.duplicate import (
    DuplicateSchema,
    EDIT_METADATASCHEMA,
)
from autonomie.forms.task import (
    FinancialYearSchema,
    PaymentSchema,
    SetProductsSchema,
)
from autonomie.views.files import get_add_file_link

DOCUMENT_TYPES = ('estimation', 'invoice', 'cancelinvoice')

logger = logging.getLogger(__name__)


def get_set_products_form(request, counter=None):
    """
        Return a form used to set products reference to :
            * invoice lines
            * cancelinvoice lines
    """
    schema = SetProductsSchema().bind(request=request)
    action = request.route_path(
        request.context.__name__,
        id=request.context.id,
        _query=dict(action='set_products')
    )
    valid_btn = Button(
        name='submit',
        value="set_products",
        type='submit',
        title=u"Valider"
    )
    form = Form(schema=schema, buttons=(valid_btn,), action=action,
                counter=counter)
    return form


def get_paid_form(request, counter=None):
    """
        Return a payment form
    """
    valid_btn = Button(name='submit', value="paid", type='submit',
                        title=u"Valider")
    schema = PaymentSchema().bind(request=request)
    action = request.route_path("invoice",
            id=request.context.id,
            _query=dict(action='payment'))
    form = Form(schema=schema, buttons=(valid_btn,), action=action,
                counter=counter)
    return form


def get_duplicate_form(request, counter=None):
    """
        Return the form for task duplication
    """
    duplicate_js.need()
    schema = DuplicateSchema().bind(request=request)
    action = request.route_path(request.context.__name__,
                                id=request.context.id,
                                _query=dict(action='duplicate'))
    valid_btn = Button(name='submit', value="duplicate", type='submit',
                                                    title=u"Valider")
    form = Form(schema=schema, buttons=(valid_btn,), action=action,
            formid="duplicate_form", counter=counter)
    return form


def get_edit_metadata_form(request, counter=None):
    """
        Return the used to move a task from one phase to another
    """
    schema = EDIT_METADATASCHEMA.bind(request=request)
    action = request.route_path(request.context.__name__,
            id=request.context.id,
            _query=dict(action='status'))
    valid_btn = Button(name='submit', value="edit_metadata", type='submit',
            title=u"Valider")
    form = Form(schema=schema, buttons=(valid_btn,), action=action,
            formid="edit_metadata", counter=counter)
    return form


def get_set_financial_year_form(request, counter=None):
    """
        Return the form to set the financial year of an
        invoice or a cancelinvoice
    """
    schema = FinancialYearSchema().bind(request=request)
    action = request.route_path(request.context.__name__,
            id=request.context.id,
            _query=dict(action='set_financial_year'))
    valid_btn = Button(name='submit', value="set_financial_year", type='submit',
                title=u"Valider")
    form = Form(schema=schema, buttons=(valid_btn,), action=action,
            counter=counter)
    return form


def context_is_task(context):
    """
        Return True if given context is a task
    """
    return context.__name__ in DOCUMENT_TYPES


def context_is_editable(request, context):
    """
       Return True if the current task can be edited by the current user
    """
    if not context_is_task(context):
        return True
    elif context.is_editable():
        return True
    elif has_permission('manage', context, request):
        #MAnager has the right to manage waiting task
        if context.is_waiting():
            return True
    return False


class TaskFormActions(object):
    """
        Tool to build the form action buttons regarding the context and
        its state machine
    """
    def __init__(self, request, model=None):
        self.request = request
        self.context = self.request.context
        self.project = self.get_project()
        self.company = self.get_company()
        self.route = self.request.matched_route
        self.model = model
        self.formcounter = None

    def get_project(self):
        """
            return the current project we're working on
        """
        if context_is_task(self.context):
            return self.request.context.project
        else:
            return self.request.context

    def get_company(self):
        """
            Return the current company we're working on
        """
        return self.project.company

    def get_customers(self):
        """
            Return the customers of the current company
        """
        return self.company.customers

    def _valid_btn(self):
        """
            Return the button for document validation
        """
        yield Submit(u"Enregistrer et valider",
                    value="valid",
                    request=self.request)

    def _invalid_btn(self):
        """
            Return the button for document invalidation
        """
        yield Submit(u"Enregistrer et invalider le document",
                     value="invalid",
                     request=self.request)

    def _cancel_btn(self):
        """
            Return a cancel btn returning the user to the project view
        """
        if self.request.context.__name__ in DOCUMENT_TYPES:
            project_id = self.request.context.project.id
        else:
            project_id = self.request.context.id
        yield ViewLink(u"Revenir en arrière",
                          "view",
                          path="project",
                          css="btn btn-primary",
                          request=self.request,
                          id=project_id)

    def _pdf_btn(self):
        """
            Return a PDF view btn only if the context is a document
        """
        if self.request.context.__name__ in DOCUMENT_TYPES:
            yield ViewLink(u"Voir le PDF",
                           "view",
                           path=self.request.context.__name__,
                           css="btn btn-primary",
                           request=self.request,
                           id=self.request.context.id,
                           _query=dict(view="pdf"))

    def _draft_btn(self):
        """
            Return the save to draft button
        """
        label = u"Enregistrer comme brouillon"
        if context_is_task(self.context):
            if self.context.is_waiting():
                if not self.request.user.is_contractor():
                    return
                label = u"Annuler la mise en validation et repasser en \
brouillon"
        yield Submit(
            label,
            value="draft",
            request=self.request,
        )

    def _wait_btn(self):
        """
            Return the btn for asking document validation
        """
        label = u"Enregistrer et demander la validation"
        if context_is_task(self.context):
            if self.context.is_waiting():
                label = u"Enregistrer et garder en attente"
        yield Submit(label, value="wait", request=self.request)

    def _duplicate_form(self):
        """
            Return the form for task duplication
        """
        form = get_duplicate_form(self.request, self.formcounter)
        self.formcounter = form.counter
        return form

    def _duplicate_btn(self):
        """
            Return the button for asking duplication of the current document
        """
        if context_is_task(self.context):
            title = u"Dupliquer le document"
            form = self._duplicate_form()
            popup = PopUp("duplicate_form_container", title, form.render())
            self.request.popups[popup.name] = popup
            yield popup.open_btn(css='btn btn-primary')

    def _edit_metadata_form(self):
        """
            return the form used to change a task's phase
        """
        form = get_edit_metadata_form(self.request, self.formcounter)
        form.set_appstruct(self.context.appstruct())
        self.formcounter = form.counter
        return form

    def _edit_metadata_btn(self):
        """
            Return the button for moving the current task to another phase
        """
        if self.request.user.is_contractor():
            manage = False
        else:
            manage = True
        if context_is_task(self.context) and not self.context.is_editable(manage):
            title = u"Modifier ce document"
            form = self._edit_metadata_form()
            form.appstruct = self.context.appstruct()
            popup = PopUp("edit_metadata_form_container", title, form.render())
            self.request.popups[popup.name] = popup
            yield popup.open_btn(css='btn btn-primary')

    def _set_financial_year_form(self):
        """
            Return the form for setting the financial year of a document
        """
        form = get_set_financial_year_form(self.request, self.formcounter)
        form.set_appstruct({'financial_year':self.context.financial_year})
        self.formcounter = form.counter
        return form

    def _set_products_form(self):
        """
            Return the form for configuring the products for each lines
        """
        form = get_set_products_form(self.request, self.formcounter)
        form.set_appstruct(
            {
                'lines':[line.appstruct() \
                         for line in self.context.all_lines]
            }
        )
        self.formcounter = form.counter
        return form

    def _set_financial_year_btn(self):
        """
            Return the button for the popup with the financial year set form
            of the current document
        """
        if context_is_task(self.context):
            title = u"Année comptable de référence"
            form = self._set_financial_year_form()
            popup = PopUp("set_financial_year_form_container", title,
                                                        form.render())
            self.request.popups[popup.name] = popup
            yield popup.open_btn(css='btn btn-primary')

    def _set_products_btn(self):
        """
            Popup fire button
        """
        title = u"Configuration des produits"
        form = self._set_products_form()
        popup = PopUp("set_products_form", title, form.render())
        self.request.popups[popup.name] = popup
        yield popup.open_btn(css='btn btn-primary')


    def get_next_actions(self):
        """
            returns the next available actions for the current task
        """
        if context_is_task(self.context):
            return self.request.context.get_next_actions()
        else:
            return self.model.state_machine.get_next_states()

    def get_buttons(self, counter=None):
        """
            returns submit buttons for estimation/invoice form
            :param counter: itertools form counter used by deformto give ids
                            to the forms
        """
        self.formcounter = counter
        btns = []
        actions = self.get_next_actions()
        logger.debug(u"   + Available actions :")
        for action in actions:
            logger.debug(u"    * {0}".format(action.name))
            if action.allowed(self.context, self.request):
                logger.debug(u"     -> is allowed for the current user")
                if hasattr(self, "_%s_btn" % action.name):
                    func = getattr(self, "_%s_btn" % action.name)
                    btns.extend(func())
        btns.extend(self._cancel_btn())
        btns.extend(self._pdf_btn())
        return btns

    def _aboest_btn(self):
        """
            Return a button to abort an estimation
        """
        yield Submit(u"Indiquer sans suite",
                     title=u"Indiquer que le devis n'aura pas de suite",
                     value="aboest",
                     request=self.request)

    def _geninv_btn(self):
        """
            Return a button for invoice generation
        """
        if not self.context.invoices :
            yield Submit(
                u"Générer les factures",
                title=u"Générer les factures correspondantes au devis",
                value="geninv",
                request=self.request,
            )
        else:
            yield Submit(
                u"Re-générer les factures",
                title=u"Re-générer les factures correspondantes au devis",
                value="geninv",
                request=self.request,
                confirm=u"Êtes-vous sûr de vouloir re-générer des factures \
pour ce devis ?"
            )


    def _paid_form(self):
        """
            return the form for payment registration
        """
        form = get_paid_form(self.request, self.formcounter)
        self.formcounter = form.counter
        return form

    def _paid_btn(self):
        """
            Return a button to set a paid btn and a select to choose
            the payment mode
        """

        if has_permission("manage", self.context, self.request):
            form = self._paid_form()
            title = u"Notifier un paiement"
            popup = PopUp("paidform", title, form.render())
            self.request.popups[popup.name] = popup
            yield popup.open_btn(css='btn btn-primary')

    def _aboinv_btn(self):
        """
            Return a button to abort an invoice
        """
        yield Submit(
            u"Annuler cette facture",
            value="aboinv",
            request=self.request,
            confirm=u"Êtes-vous sûr de vouloir annuler cette facture ?"
        )

    def _gencinv_btn(self):
        """
            Return a button for generating a cancelinvoice
        """
        if self.request.context.topay() != 0:
            yield Submit(
                u"Générer un avoir",
                value="gencinv",
                request=self.request,
            )


class StatusView(BaseView):
    """
        View for status handling

        See the call method for the workflow and the params
        passed to the methods
    """
    valid_msg = u"Le statut a bien été modifié"

    def redirect(self):
        """
            Redirect function to be used after status processing
        """
        return HTTPNotFound()

    def _get_status(self):
        """
            Get the status that has been asked for
        """
        return self.request.params['submit']

    def _get_request_params(self):
        """
            return the request params as a dict (a non locked one)
        """
        return dict(self.request.params.items())

    def pre_status_process(self, item, status, params):
        """
            Launch pre process functions
        """
        if hasattr(self, "pre_%s_process" % status):
            func = getattr(self, "pre_%s_process" % status)
            return func(item, status, params)
        return params

    def status_process(self, params, status):
        """
            Definitively Set the status of the element
        """
        return self.request.context.set_status(status,
                                        self.request,
                                        self.request.user.id,
                                        **params)

    def post_status_process(self, item, status, params):
        """
            Launch post status process functions
        """
        if hasattr(self, "post_%s_process" % status):
            func = getattr(self, "post_%s_process" % status)
            func(item, status, params)

    def set_status(self, item, status):
        """
            handle the status pre/set/post workflow
        """
        pre_params = self.request.params
        params = self.pre_status_process(item, status, pre_params)
        post_params = self.status_process(params, status)
        self.post_status_process(item, status, post_params)
        return item, status

    def notify(self, item, status):
        """
            Notify the change to the registry
        """
        self.request.registry.notify(StatusChanged(self.request,
            item,
            status,
            ))

    def __call__(self):
        """
            Main entry for this view object
        """
        item = self.request.context
        if "submit" in self.request.params:
            try:
                status = self._get_status()
                logger.debug(u"New status : %s "%status)
                item, status = self.set_status(item, status)
                item = self.request.dbsession.merge(item)
                self.notify(item, status)
                self.session.flash(self.valid_msg)
                logger.debug(u" + The status has been set to {0}".format(status))
            except Forbidden, e:
                logger.exception(u" !! Unauthorized action by : {0}"\
                        .format(self.request.user.login))
                self.session.pop_flash("")
                self.session.flash(e.message, queue='error')
        return self.redirect()


class TaskStatusView(StatusView):
    """
        View for task status handling, allows to easily process states
        on documents
    """

    def pre_duplicate_process(self, task, status, params):
        """
            Common pre process method for document duplication
        """
        form = get_duplicate_form(self.request)
        # if an error is raised here, it will be cached a level higher
        appstruct = form.validate(params.items())
        logger.debug(u" * Form has been validated")
        customer_id = appstruct.get('customer')
        customer = Customer.get(customer_id)
        project_id = appstruct.get('project')
        project = Project.get(project_id)
        phase_id = appstruct.get('phase')
        phase = Phase.get(phase_id)
        logger.debug(u" * Phase : %s" % phase)
        logger.debug(u" * Project : %s" % project)
        appstruct['phase'] = phase
        appstruct['project'] = project
        appstruct['customer'] = customer
        appstruct['user'] = self.request.user
        return appstruct

    def pre_edit_metadata_process(self, task, status, params):
        """
            pre process method for phase changing
        """
        form = get_edit_metadata_form(self.request)
        appstruct = form.validate(params.items())
        logger.debug(u" * Form has been validated")
        return appstruct

    def post_edit_metadata_process(self, task, status, params):
        task = self.request.dbsession.merge(task)
        msg = u"Le document a bien été modifié"
        self.request.session.flash(msg)


class TaskFormView(BaseFormView):
    model = None
    # Tag to know if it's an edition or an add view
    edit = False
    use_csrf_token = True

    def __init__(self, request):
        task.need()
        super(TaskFormView, self).__init__(request)
        self.buttonmaker = TaskFormActions(request, model=self.model)
        self.context = self.request.context

    def before(self, form):
        form.buttons = self.buttonmaker.get_buttons(counter=form.counter)
        form.set_appstruct({'lines': {'lines': [{'description': ''}]}})

    def set_task_status(self, task):
        # self.request.POST is a locked dict, we need a non locked one
        logger.info(u"Set task status")
        params = dict(self.request.POST)
        status = params['submit']
        task.set_status(status, self.request, self.request.user.id, **params)
        self.request.registry.notify(StatusChanged(
            self.request,
            task,
            status,
            ))
        return task

    @property
    def load_options_url(self):
        return self.request.route_path("taskoptions.json")

    @property
    def load_catalog_url(self):
        return self.request.route_path(
            "sale_categories",
            id=self.buttonmaker.company.id,
            _query=dict(action='jstree')
        )

    @property
    def tvas(self):
        return Tva.query().all()

    def _more_template_vars(self):
        """
        Add template vars to the response dict
        List the attributes configured in the add_template_vars attribute
        and add them
        """
        result = BaseFormView._more_template_vars(self)
        result['title'] = self.title
        result['company'] = self.company
        result['tvas'] = self.tvas
        result['load_options_url'] = self.load_options_url
        result['load_catalog_url'] = self.load_catalog_url
        return result


def html(request, tasks=None, bulk=False):
    """
        return the html output of a given task
    """
    template = "autonomie:templates/tasks/task.mako"

    if tasks == None:
        tasks = [ request.context ]

    datas = dict(
                 tasks=tasks,
                 config=request.config,
                 bulk=bulk,
                 )

    return render_html(request, template, datas)


def get_project_redirect_btn(request, id_):
    """
        Button for "go back to project" link
    """
    return ViewLink(u"Revenir au projet", "edit", path="project", id=id_)


def populate_actionmenu(request):
    """
        Add buttons in the request actionmenu attribute
    """
    if context_is_task(request.context):
        project = request.context.project
    else:
        project = request.context
    request.actionmenu.add(get_project_redirect_btn(request, project.id))
    if context_is_task(request.context):
        request.actionmenu.add(
            get_add_file_link(request)
            )


def task_html_view(request):
    """
        Returns a page displaying an html rendering of a task
    """
    # If the task is editable, we go the edit page
    if context_is_editable(request, request.context):
        return HTTPFound(request.route_path(request.context.__name__,
                                            id=request.context.id))

    # Get the label for the given task
    if request.context.__name__ == 'invoice':
        label = u"Facture"
    elif request.context.__name__ == 'estimation':
        label = u"Estimation"
    elif request.context.__name__ == 'cancelinvoice':
        label = u"Avoir"
    else:
        label = u"Objet"

    title = u"{0} numéro : {1}".format(label, request.context.number)
    populate_actionmenu(request)

    # We use the task's class to retrieve the available actions
    model = request.context.__class__
    button_handler = TaskFormActions(request, model)
    submit_buttons = button_handler.get_buttons()

    return dict(
        title=title,
        task=request.context,
        submit_buttons=submit_buttons,
        )


def task_pdf_view(request):
    """
        Returns a pdf rendering of the current task
    """
    filename = u"{0}.pdf".format(request.context.number)

    html_string = html(request)
    write_pdf(request, filename, html_string)

    return request.response


def make_task_delete_view(valid_msg):
    """
        Return a task deletion view
        :param valid_msg: string called with task object as format argument
    """
    def delete(request):
        """
            delete a task
        """
        task = request.context
        user = request.user
        project = task.project
        logger.info(u"# {user.login} deletes {s.__name__} {s.number}".format(
                    user=user, s=task))
        try:
            task.set_status("delete", request, request.user.id)
        except Forbidden, err:
            logger.exception(u"Forbidden operation")
            request.session.flash(err.message, queue="error")
        except:
            logger.exception(u"Unknown error")
            request.session.flash(u"Une erreur inconnue s'est produite",
                    queue="error")
        else:
            if task.type_ == 'invoice' and task.estimation is not None:
                task.estimation.CAEStatus = 'valid'
                request.dbsession.merge(task.estimation)
            request.dbsession.delete(task)
            message = valid_msg.format(task=task)
            request.session.flash(message)
        return HTTPFound(request.route_path('project', id=project.id))
    return delete


def task_options_json(request):
    """
        Returns the task form options as a dict
    """
    options = dict()
    options['tvas'] = dict((tva.value, tva.__json__(request)) \
            for tva in Tva.query().all())
    return options


def includeme(config):
    """
        Pyramid's inclusion mechanism
    """
    config.add_route("taskoptions.json", "/task/options.json")
    config.add_view(task_options_json,
            route_name="taskoptions.json",
            xhr=True,
            renderer="json")
