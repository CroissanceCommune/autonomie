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

from autonomie_base.utils.ascii import force_filename
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
from autonomie.views.files import get_add_file_link

DOCUMENT_TYPES = ('estimation', 'invoice', 'cancelinvoice')

logger = logging.getLogger(__name__)


def get_duplicate_form(request, counter=None):
    """
        Return the form for task duplication
    """
    duplicate_js.need()
    schema = DuplicateSchema().bind(request=request)
    action = request.route_path(
        "/%ss/{id}/duplicate" % request.context.type_,
        id=request.context.id,
    )
    valid_btn = Button(
        name='submit',
        value="duplicate",
        type='submit',
        title=u"Valider",
    )
    form = Form(
        schema=schema,
        buttons=(valid_btn,),
        action=action,
        formid="duplicate_form",
        counter=counter,
    )
    return form


def get_edit_metadata_form(request, counter=None):
    """
        Return the used to move a task from one phase to another
    """
    schema = EDIT_METADATASCHEMA.bind(request=request)
    action = request.route_path(
        "/%ss/{id}/metadata" % request.context.type_,
        id=request.context.id,
        _query=dict(action='status'),
    )
    valid_btn = Button(
        name='submit',
        value="edit_metadata",
        type='submit',
        title=u"Valider",
    )
    form = Form(
        schema=schema,
        buttons=(valid_btn,),
        action=action,
        formid="edit_metadata",
        counter=counter,
    )
    return form


def context_is_task(context):
    """
        Return True if given context is a task
    """
    return context.type_ in DOCUMENT_TYPES


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
        yield Submit(
            u"Enregistrer et valider",
            value="valid",
            request=self.request,
        )

    def _invalid_btn(self):
        """
            Return the button for document invalidation
        """
        yield Submit(
            u"Enregistrer et invalider le document",
            value="invalid",
            request=self.request,
        )

    def _cancel_btn(self):
        """
            Return a cancel btn returning the user to the project view
        """
        project = self.get_project()
        yield ViewLink(
            u"Revenir en arrière",
            path="project",
            css="btn btn-primary",
            request=self.request,
            id=project.id,
        )

    def _pdf_btn(self):
        """
            Return a PDF view btn only if the context is a document
        """
        if context_is_task(self.request.context):
            yield ViewLink(u"Voir le PDF",
                           "view_%s" % (self.request.context.__name__),
                           path="/%ss/{id}.pdf" % self.request.context.type_,
                           css="btn btn-primary",
                           request=self.request,
                           id=self.request.context.id,
                           )

    def _draft_btn(self):
        """
            Return the save to draft button
        """
        label = u"Enregistrer comme brouillon"
        if context_is_task(self.context):
            if self.context.status == 'wait':
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
            if self.context.status == 'wait':
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
        Return the button for moving the current task
        to another phase
        """
        if context_is_task(self.context):
            title = u"Modifier ce document"
            form = self._edit_metadata_form()
            form.appstruct = self.context.appstruct()
            popup = PopUp("edit_metadata_form_container", title, form.render())
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
        logger.debug(self)
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


class TaskStatusView(StatusView):
    """
        View for task status handling, allows to easily process states
        on documents
    """

    def pre_duplicate_process(self, status, params):
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

    def pre_edit_metadata_process(self, status, params):
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
    form_actions_factory = TaskFormActions

    def __init__(self, request):
        task.need()
        super(TaskFormView, self).__init__(request)
        self.buttonmaker = self.form_actions_factory(request, model=self.model)
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
        self.request.registry.notify(
            StatusChanged(
                self.request,
                task,
                status,
            )
        )
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

    if tasks is None:
        tasks = [request.context]

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
    return ViewLink(
        u"Revenir au projet",
        path="project",
        id=id_
    )


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
        edit_perm = "edit.%s" % request.context.__name__
        request.actionmenu.add(
            get_add_file_link(request, perm=edit_perm)
        )


def get_task_html_view(form_actions_factory=TaskFormActions):
    """
    Returns a view for the html display of a task

    :param obj form_actions_factory: The form actions class used for the
    expected type of task
    """
    def task_html_view(request):
        """
        The task html view
        """
        from autonomie.resources import task_html_pdf_css
        task_html_pdf_css.need()
        # If the task is editable, we go the edit page
        if request.has_permission('edit.%s' % request.context.__name__):
            return HTTPFound(
                request.route_path(
                    request.context.__name__,
                    id=request.context.id
                )
            )

        # Get the label for the given task
        if request.context.__name__ == 'invoice':
            label = u"Facture"
        elif request.context.__name__ == 'estimation':
            label = u"Devis"
        elif request.context.__name__ == 'cancelinvoice':
            label = u"Avoir"
        else:
            label = u"Objet"

        title = u"{0} numéro : {1}".format(label, request.context.internal_number)
        populate_actionmenu(request)

        # We use the task's class to retrieve the available actions
        model = request.context.__class__
        button_handler = form_actions_factory(request, model)
        submit_buttons = button_handler.get_buttons()

        return dict(
            title=title,
            task=request.context,
            submit_buttons=submit_buttons,
        )
    return task_html_view


def task_pdf_view(request):
    """
        Returns a pdf rendering of the current task
    """
    from autonomie.resources import pdf_css
    pdf_css.need()

    number = request.context.internal_number
    label = force_filename(number)

    filename = u"{0}.pdf".format(label)

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
        logger.info(u"# {user.login} deletes {s.__name__} {s.internal_number}".format(
                    user=user, s=task))
        try:
            task.set_status("delete", request, request.user.id)
        except Forbidden, err:
            logger.exception(u"Forbidden operation")
            request.session.flash(err.message, queue="error")
        except:
            logger.exception(u"Unknown error")
            request.session.flash(
                u"Une erreur inconnue s'est produite",
                queue="error",
            )
        else:
            if task.type_ == 'invoice' and task.estimation is not None:
                task.estimation.status = 'valid'
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
    options['tvas'] = dict(
        (tva.value, tva.__json__(request))
        for tva in Tva.query().all()
    )
    return options


def includeme(config):
    """
        Pyramid's inclusion mechanism
    """
    config.add_route("taskoptions.json", "/task/options.json")
    config.add_view(
        task_options_json,
        route_name="taskoptions.json",
        xhr=True,
        renderer="json",
    )
