# -*- coding: utf-8 -*-
# * File Name : taskaction.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 23-12-2012
# * Last Modified :
#
# * Project :
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

from autonomie.views.mail import StatusChanged
from autonomie.exception import Forbidden
from autonomie.utils.widgets import Submit
from autonomie.utils.widgets import ViewLink
from autonomie.utils.widgets import PopUp
from autonomie.models.client import Client
from autonomie.models.project import Project
from autonomie.models.project import Phase
from autonomie.views.forms.duplicate import DuplicateSchema
from autonomie.views.forms.task import PaymentSchema
from autonomie.views.forms.utils import BaseFormView
from autonomie.utils.pdf import write_pdf
from autonomie.utils.pdf import render_html

DOCUMENT_TYPES = ('estimation', 'invoice', 'cancelinvoice')

log = logging.getLogger(__name__)


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
    request.js_require.add('duplicate')
    schema = DuplicateSchema().bind(request=request)
    action = request.route_path(request.context.__name__,
                                id=request.context.id,
                                _query=dict(action='duplicate'))
    valid_btn = Button(name='submit', value="duplicate", type='submit',
                                                    title=u"Valider")
    form = Form(schema=schema, buttons=(valid_btn,), action=action,
            formid="duplicate_form", counter=counter)
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

    def get_clients(self):
        """
            Return the clients of the current company
        """
        return self.company.clients

    def _valid_btn(self):
        """
            Return the button for document validation
        """
        yield Submit(u"Valider le document",
                    value="valid",
                    request=self.request)

    def _invalid_btn(self):
        """
            Return the button for document invalidation
        """
        yield Submit(u"Document invalide",
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
        yield Submit(u"Enregistrer comme brouillon",
                            value="draft",
                            request=self.request)

    def _wait_btn(self):
        """
            Return the btn for asking document validation
        """
        yield Submit(u"Enregistrer et demander la validation",
                       value="wait",
                       request=self.request)

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
        log.debug(u"   + Available actions :")
        for action in actions:
            log.debug(u"    * {0}".format(action.name))
            if action.allowed(self.context, self.request):
                log.debug(u"     -> is allowed for the current user")
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
        yield Submit(u"Générer les factures",
                  title=u"Générer les factures correspondantes au devis",
                  value="geninv",
                  request=self.request)

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
        yield Submit(u"Annuler cette facture",
                 value="aboinv",
                 request=self.request,
                 confirm=u"Êtes-vous sûr de vouloir annuler cette facture ?")

    def _gencinv_btn(self):
        """
            Return a button for generating a cancelinvoice
        """
        yield Submit(u"Générer un avoir",
                     value="gencinv",
                     request=self.request)


class StatusView(object):
    """
        View for task status handling, allows to easily process states
        on documents
        See the call method for the workflow and the params
        passed to the methods
    """
    valid_msg = u"Le statut a bien été modifié"

    def __init__(self, request):
        self.request = request
        self.session = self.request.session

    def get_task_status(self):
        """
            Get the task status that has been asked
        """
        return self.request.params['submit']

    def get_request_params(self):
        """
            return the request params as a dict (a non locked one)
        """
        return dict(self.request.params.items())

    def pre_duplicate_process(self, task, status, params):
        """
            Common pre process method for document duplication
        """
        form = get_duplicate_form(self.request)
        # if an error is raised here, it will be cached a level higher
        appstruct = form.validate(params.items())
        log.debug(u" * Form has been validated")
        client_id = appstruct.get('client')
        client = Client.get(client_id)
        project_id = appstruct.get('project')
        project = Project.get(project_id)
        phase_id = appstruct.get('phase')
        phase = Phase.get(phase_id)
        log.debug(u" * Phase : %s" % phase)
        log.debug(u" * Project : %s" % project)
        appstruct['phase'] = phase
        appstruct['project'] = project
        appstruct['client'] = client
        appstruct['user'] = self.request.user
        log.debug(u"Appstruct : %s" % appstruct)
        return appstruct

    def pre_status_process(self, task, status, params):
        if hasattr(self, "pre_%s_process" % status):
            func = getattr(self, "pre_%s_process" % status)
            return func(task, status, params)
        return params

    def status_process(self, params, status):
        return self.request.context.set_status(status,
                                        self.request,
                                        self.request.user.id,
                                        **params)

    def post_status_process(self, task, status, params):
        if hasattr(self, "post_%s_process" % status):
            func = getattr(self, "post_%s_process" % status)
            func(task, status, params)

    def set_status(self, task, status):
        pre_params = self.get_request_params()
        params = self.pre_status_process(task, status, pre_params)
        post_params = self.status_process(params, status)
        self.post_status_process(task, status, post_params)
        return task, status

    def merge(self):
        return self.request.dbsession.merge(self.request.context)

    def notify(self, task):
        self.request.registry.notify(StatusChanged(self.request, task))

    def redirect(self):
        return HTTPNotFound()

    def __call__(self):
        task = self.request.context
        if "submit" in self.request.params:
            try:
                status = self.get_task_status()
                task, status = self.set_status(task, status)
                task = self.request.dbsession.merge(task)
                self.notify(task)
                self.session.flash(self.valid_msg)
                log.debug(u" + The status has been set to {0}".format(status))
            except Forbidden, e:
                log.exception(u" !! Unauthorized action by : {0}"\
                        .format(self.request.user.login))
                self.session.pop_flash("")
                self.session.flash(e.message, queue='error')
        return self.redirect()


class TaskFormView(BaseFormView):
    model = None
    def __init__(self, request):
        super(TaskFormView, self).__init__(request)
        self.buttonmaker = TaskFormActions(request, model=self.model)
        self.context = self.request.context


    def before(self, form):
        form.buttons = self.buttonmaker.get_buttons(counter=form.counter)
        # Ici on spécifie un template qui permet de rendre nos boutons de
        # formulaires
        form.widget.template = "autonomie:deform_templates/form.pt"


def html(request, template):
    """
        return the html output of a given task
    """
    task = request.context
    tvas = task.get_tvas()
    if len([value for value in tvas.keys() if value >=0]) > 1:
        multiple_tvas = True
    else:
        multiple_tvas = False
    datas = dict(company=task.project.company,
                 project=task.project,
                 task=task,
                 config=request.config,
                 multiple_tvas=multiple_tvas,
                 tvas=tvas)
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


def make_html_view(model, template):
    """
        Return an html view function
        :model: model class
        :template: model rendering template
    """
    def html_view(request):
        """
            Returns a page displaying an html rendering of the given task
        """
        if context_is_editable(request, request.context):
            return HTTPFound(request.route_path(request.context.__name__,
                                                id=request.context.id))
        title = u"Facture numéro : {0}".format(request.context.number)
        populate_actionmenu(request)
        html_datas = html(request, template)
        button_handler = TaskFormActions(request, model)
        submit_buttons = button_handler.get_buttons()
        return dict(title=title,
                task=request.context,
                html_datas=html_datas,
                submit_buttons=submit_buttons,)
    return html_view


def make_pdf_view(template):
    def pdf(request):
        """
            Returns a page displaying an html rendering of the given task
        """
        log.debug(u"# Generating the pdf file #")
        filename = u"{0}.pdf".format(request.context.number)
        write_pdf(request, filename, html(request, template))
        return request.response
    return pdf


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
        log.info(u"# {user.login} deletes {s.__name__} {s.number}".format(
                    user=user, s=task))
        try:
            task.set_status("delete", request, request.user.id)
        except Forbidden, err:
            log.exception(u"Forbidden operation")
            request.session.flash(err.message, queue="error")
        except:
            log.exception(u"Unknown error")
            request.session.flash(u"Une erreur inconnue s'est produite",
                    queue="error")
        else:
            request.dbsession.delete(task)
            message = valid_msg.format(task=task)
            request.session.flash(message)
        return HTTPFound(request.route_path('project', id=project.id))
    return delete
