# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Base Task views
"""
import datetime
import logging
from pyramid.httpexceptions import HTTPFound
from autonomie_base.utils.ascii import force_filename
from autonomie.utils.widgets import ViewLink
from autonomie.models.customer import Customer
from autonomie.models.project import (
    Phase,
    Project,
)
from autonomie.models.task.task import TaskLine
from autonomie.models.task import TaskStatus
from autonomie.forms.tasks.base import (
    get_duplicate_schema,
    get_new_task_schema,
    get_task_metadatas_edit_schema,
)
from autonomie.forms.tasks.invoice import (
    SetProductsSchema,
)
from autonomie.export.utils import (
    write_file_to_request,
)
from autonomie.utils.pdf import (
    buffer_pdf,
    render_html,
)
from autonomie.resources import (
    task_resources,
    task_html_pdf_css,
    pdf_css,
    task_add_js,
)
from autonomie.views import (
    BaseView,
    BaseFormView,
    submit_btn,
    cancel_btn,
    TreeMixin,
)
from autonomie.views.status import StatusView
from autonomie.views.project.routes import (
    PROJECT_ITEM_PHASE_ROUTE,
    PROJECT_ITEM_ROUTE,
)


logger = logging.getLogger(__name__)


def get_project_redirect_btn(request, id_):
    """
        Button for "go back to project" link
    """
    return ViewLink(
        u"Revenir au projet",
        path=PROJECT_ITEM_ROUTE,
        id=id_
    )


def populate_actionmenu(request):
    """
        Add buttons in the request actionmenu attribute
    """
    if request.context.type_ == 'project':
        project_id = request.context.id
    else:
        if request.context.phase:
            project_id = request.context.phase.project_id
        else:
            project_id = request.context.project_id
    request.actionmenu.add(get_project_redirect_btn(request, project_id))


class TaskAddView(BaseFormView):
    """
    Base task add view

    Handles stuff common to all Tasks
    """
    title = u"Nouveau document"
    schema = get_new_task_schema()
    buttons = (submit_btn,)
    factory = None

    def before(self, form):
        BaseFormView.before(self, form)
        populate_actionmenu(self.request)
        task_add_js.need()

    def submit_success(self, appstruct):
        if self.factory is None:
            raise Exception("Forgot to set the factory attribute")

        project_id = appstruct.pop('project_id')
        appstruct['project'] = Project.get(project_id)

        customer_id = appstruct.pop('customer_id')
        appstruct['customer'] = Customer.get(customer_id)

        new_object = self.factory(
            user=self.request.user,
            company=self.context.company,
            **appstruct
        )

        if hasattr(self, "_more_init_attributes"):
            self._more_init_attributes(new_object, appstruct)

        self.dbsession.add(new_object)
        self.dbsession.flush()

        if hasattr(self, "_after_flush"):
            self._after_flush(new_object)

        url = self.request.route_path(
            "/%ss/{id}" % new_object.type_,
            id=new_object.id
        )
        return HTTPFound(url)


class TaskEditView(BaseView, TreeMixin):

    def title(self):
        return u"Modification du document {task.name}".format(task=self.context)

    def load_catalog_url(self):
        return self.request.route_path(
            "sale_categories",
            id=self.context.company.id,
            _query=dict(action='jstree')
        )

    def context_url(self, _query={}):
        return self.request.route_path(
            '/api/v1/' + self.request.context.type_ + 's/{id}',
            id=self.request.context.id,
            _query=_query,
        )

    def form_config_url(self):
        return self.context_url(_query={'form_config': '1'})

    def __call__(self):
        if not self.request.has_permission('edit.%s' % self.context.type_):
            return HTTPFound(self.request.current_route_path() + '.html')

        if hasattr(self, '_before'):
            self._before()

        self.populate_navigation()

        task_resources.need()
        # populate_actionmenu(self.request)
        return dict(
            context=self.context,
            title=self.title,
            context_url=self.context_url(),
            form_config_url=self.form_config_url(),
            load_catalog_url=self.load_catalog_url(),
        )


class TaskDeleteView(BaseView):
    """
    Base task deletion view
    """
    msg = u"Le document {context.name} a bien été supprimé."

    def __call__(self):
        logger.info(
            u"# {user.login} deletes {task.type_} {task.id}".format(
                user=self.request.user,
                task=self.context,
            )
        )
        project = self.context.project

        if hasattr(self, 'pre_delete'):
            self.pre_delete()

        try:
            self.request.dbsession.delete(self.context)
        except:
            logger.exception(u"Unknown error")
            self.request.session.flash(
                u"Une erreur inconnue s'est produite",
                queue="error",
            )
        else:
            if hasattr(self, 'post_delete'):
                self.post_delete()
            message = self.msg.format(context=self.context)
            self.request.session.flash(message)

        return HTTPFound(
            self.request.route_path(PROJECT_ITEM_ROUTE, id=project.id)
        )


class TaskDuplicateView(BaseFormView):
    """
    Task duplication view
    """
    schema = get_duplicate_schema()

    @property
    def title(self):
        return u"Dupliquer {0} {1}".format(self.label, self.context.name)

    def before(self, form):
        BaseFormView.before(self, form)
        task_add_js.need()

    def submit_success(self, appstruct):
        logger.debug("# Duplicating a document #")

        project_id = appstruct.pop('project_id')
        appstruct['project'] = Project.get(project_id)

        customer_id = appstruct.pop('customer_id')
        appstruct['customer'] = Customer.get(customer_id)

        task = self.context.duplicate(
            user=self.request.user,
            **appstruct
        )
        if hasattr(self, "_after_task_duplicate"):
            self._after_task_duplicate(task, appstruct)

        self.dbsession.add(task)
        self.dbsession.flush()
        logger.debug(
            u"The {t.type_} {t.id} has been duplicated to {new_t.id}".format(
                t=self.context,
                new_t=task
            )
        )
        return HTTPFound(
            self.request.route_path(
                '/%ss/{id}' % self.context.type_,
                id=task.id
            )
        )


class TaskMoveToPhaseView(BaseView):
    """
    View used to move a document to a specific directory/phase

    expects a get arg "phase" containing the destination phase_id
    """
    def __call__(self):
        phase_id = self.request.params.get('phase')
        if phase_id:
            phase = Phase.get(phase_id)
            if phase in self.context.project.phases:
                self.context.phase_id = phase_id
                self.request.dbsession.merge(self.context)

        return HTTPFound(
            self.request.route_path(
                PROJECT_ITEM_PHASE_ROUTE,
                id=self.context.project_id,
                _query={'phase': phase_id}
            )
        )


class TaskHtmlView(BaseView, TreeMixin):
    """
    Base Task html view
    """
    label = u"Objet"

    @property
    def title(self):
        return u"{0} : {1}".format(
            self.label,
            self.context.internal_number
        )

    def actions(self):
        """
        Return the description of the action buttons

        :returns: A list of dict (url, icon, label)
        :rtype: list
        """
        return []

    def _collect_file_indicators(self):
        """
        Collect file requirements attached to the given context
        """
        return self.context.file_requirements

    def __call__(self):
        self.populate_navigation()
        task_html_pdf_css.need()
        # If the task is editable, we go the edit page
        if self.request.has_permission('edit.%s' % self.context.type_):
            return HTTPFound(
                self.request.route_path(
                    "/%ss/{id}" % self.context.type_,
                    id=self.context.id
                )
            )

        return dict(
            title=self.title,
            task=self.context,
            actions=self.actions(),
            indicators=self._collect_file_indicators(),

        )


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


class TaskPdfView(BaseView):
    """
    Return A pdf representation of the current context

    """
    def _cache_pdf(self, filename, pdf_datas):
        if self.context.status == 'valid':
            self.context.persist_pdf(filename, pdf_datas)

    def _get_html_output(self):
        """
        Produce an html output of the current context
        """
        pdf_css.need()
        html_string = html(self.request)
        return html_string

    def _get_filename(self):
        """
        Returns the pdf's filename
        """
        number = self.request.context.internal_number
        label = force_filename(number)
        return u"{0}.pdf".format(label)

    def _get_pdf_buffer(self, filename):
        """
        Collect the pdf representation of the current context
        """
        if self.context.status == 'valid' and self.context.pdf_file is not None:
            result = self.context.pdf_file.data_obj
        else:
            html_string = self._get_html_output()
            result = buffer_pdf(html_string)
            if self.context.status == 'valid':
                self._cache_pdf(filename, result)
        return result

    def __call__(self):
        filename = self._get_filename()
        pdf_datas = self._get_pdf_buffer(filename)

        write_file_to_request(
            self.request,
            filename,
            pdf_datas,
            'application/pdf'
        )
        return self.request.response


class TaskSetMetadatasView(BaseFormView):
    schema = get_task_metadatas_edit_schema()
    buttons = (submit_btn, cancel_btn)

    @property
    def title(self):
        return u"Modification du document {task.name}".format(
            task=self.context
        )

    def before(self, form):
        task_add_js.need()
        self.request.actionmenu.add(
            ViewLink(
                u"Revenir au document",
                path='/%ss/{id}.html' % self.context.type_,
                id=self.context.id,
            ),
        )
        form.set_appstruct(
            {
                "name": self.context.name,
                "customer_id": self.context.customer_id,
                "project_id": self.context.customer_id,
                "phase_id": self.context.customer_id,
            }
        )

    def redirect(self):
        url = self.request.route_path(
            "/%ss/{id}" % self.context.type_,
            id=self.context.id
        )
        return HTTPFound(url)

    def _get_related_elements(self):
        """
        List elements related to the current estimation
        Produce a list of visible elements that will be moved
        and a list of all elements that will be moved

        :returns: a 2-uple (visible elements, list of elements to be moved)
        :rtype: tuple
        """
        all_items = []
        visible_items = []
        business = self.context.business
        if business:
            if business.is_visible():
                visible_items.append(business)
            all_items.append(business)

            all_items.extend(business.invoices)
            visible_items.extend(business.invoices)
            for estimation in business.estimations:
                if estimation != self.context:
                    visible_items.append(estimation)
                    all_items.append(estimation)
        return visible_items, all_items

    def _handle_move_to_project(self, appstruct):
        """
        Handle the specific case where a document is moved to another project

        :param dict appstruct: The appstruct returned after form validation
        """
        visible_items, all_items = self._get_related_elements()
        if visible_items:
            logger.debug(
                u"We want the user to confirm the Move to project action"
            )

        self._apply_modifications(appstruct)
        # We move all elements to the other project
        for element in all_items:
            element.project_id = appstruct['project_id']
            if hasattr(element, 'phase_id') and 'phase_id' in appstruct:
                element.phase_id = appstruct['phase_id']
            self.dbsession.merge(element)

        result = self.redirect()

        return result

    def _apply_modifications(self, appstruct):
        """
        Apply the modification described by appstruct to the current context

        :param dict appstruct: The appstruct returned after form validation
        """
        # On a besoin du customer_id pour que la partie js qui gère le
        # formulaire fonctionne (cf static/js/task_add.js)
        appstruct.pop('customer_id')
        for key, value in appstruct.items():
            setattr(self.context, key, value)
        return self.request.dbsession.merge(self.context)

    def submit_success(self, appstruct):
        """
        Handle successfull modification

        :param dict appstruct: The appstruct returned after form validation
        :rtype: HTTPFound
        """
        logger.debug(
            u"TaskSetMetadatasView.submit_success : %s" % appstruct
        )
        project_id = appstruct.get('project_id')

        if project_id not in (None, self.context.project_id):
            result = self._handle_move_to_project(appstruct)
        else:
            self._apply_modifications(appstruct)
            result = self.redirect()

        return result

    def cancel_success(self, appstruct):
        return self.redirect()

    cancel_failure = cancel_success


class TaskSetProductsView(BaseFormView):
    """
    Base view for setting product codes (on invoices and cancelinvoices)

    context

        invoice or cancelinvoice
    """
    schema = SetProductsSchema()

    def before(self, form):
        form.set_appstruct(
            {
                'lines': [
                    line.appstruct() for line in self.context.all_lines
                ]
            }
        )
        self.request.actionmenu.add(
            ViewLink(
                u"Revenir au document",
                path="/%ss/{id}.html" % self.context.type_,
                id=self.context.id
            )
        )

    def submit_success(self, appstruct):
        for line in appstruct['lines']:
            line_id = line.get('id')
            product_id = line.get('product_id')
            if line_id is not None and product_id is not None:
                taskline = TaskLine.get(line_id)
                if taskline.task == self.context:
                    taskline.product_id = product_id
                    self.request.dbsession.merge(taskline)
                else:
                    logger.error(
                        u"Possible break in attempt: trying to set product id "
                        u"on the wrong task line (not belonging to this task)"
                    )
        return HTTPFound(
            self.request.route_path(
                '/%ss/{id}' % self.context.type_,
                id=self.context.id,
            )
        )


class TaskSetDraftView(BaseView):
    """
    Set the current task status to draft
    """
    def __call__(self):
        self.request.context.status = 'draft'
        return HTTPFound(
            self.request.route_path(
                '/%ss/{id}' % self.context.type_,
                id=self.context.id,
            )
        )


class TaskStatusView(StatusView):
    """
    View handling base status for tasks (estimation/invoice/cancelinvoice)

    Status related views should implement the validate function to ensure data
    integrity
    """

    def validate(self):
        raise NotImplemented()

    def check_allowed(self, status, params):
        self.request.context.check_status_allowed(status, self.request)

    def redirect(self):
        project_id = self.request.context.project.id
        loc = self.request.route_path(PROJECT_ITEM_ROUTE, id=project_id)
        if self.request.is_xhr:
            return dict(redirect=loc)
        else:
            return HTTPFound(loc)

    def pre_status_process(self, status, params):
        if 'comment' in params:
            self.context.status_comment = params.get('comment')
            logger.debug(self.context.status_comment)

        if 'change_date' in params and params['change_date'] in ('1', 1):
            logger.debug("Forcing the document's date !!!")
            self.context.date = datetime.date.today()

        return StatusView.pre_status_process(self, status, params)

    def pre_wait_process(self, status, params):
        """
        Launched before the wait status is set

        :param str status: The new status that should be affected
        :param dict params: The params that were transmitted by the associated
        State's callback
        """
        self.validate()
        return {}

    def pre_valid_process(self, status, params):
        """
        Launched before the valid status is set

        :param str status: The new status that should be affected
        :param dict params: The params that were transmitted by the associated
        State's callback
        """
        self.validate()
        return {}

    def post_valid_process(self, status, params):
        """
        Launched after the status is set to valid

        :param str status: The new status that should be affected
        :param dict params: The params that were transmitted by the associated
        State's callback
        """
        # Generate a cached version of the pdf output
        view = TaskPdfView(self.context, self.request)
        filename = view._get_filename()
        pdf_buffer = view._get_pdf_buffer()
        self.context.persist_pdf(filename, pdf_buffer)

    def post_status_process(self, status, params):
        """
        Launch post status process functions

        :param str status: The new status that should be affected
        :param dict params: The params that were transmitted by the associated
        State's callback
        """
        logger.debug("post_status_process")
        logger.debug(self.context.status_comment)
        # Record a task status change
        self.context.status_date = datetime.date.today()
        status_record = TaskStatus(
            task_id=self.context.id,
            status_code=status,
            status_person_id=self.request.user.id,
            status_comment=self.context.status_comment
        )
        self.context.statuses.append(status_record)
        self.request.dbsession.merge(self.context)
        StatusView.post_status_process(self, status, params)
