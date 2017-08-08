# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Base Task views
"""
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
from autonomie.forms.tasks.base import (
    get_duplicate_schema,
    get_new_task_schema,
    get_task_metadatas_edit_schema,
)
from autonomie.forms.tasks.invoice import (
    SetProductsSchema,
)
from autonomie.utils.pdf import (
    write_pdf,
    render_html,
)
from autonomie.resources import (
    duplicate_js,
    task_css,
    jstree_css,
    task_html_pdf_css,
    pdf_css,
    task_add_js,
)
from autonomie.views import (
    BaseView,
    BaseFormView,
    submit_btn,
    cancel_btn,
)


logger = logging.getLogger(__name__)


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
    if request.context.type_ == 'project':
        project = request.context
    else:
        project = request.context.project
    request.actionmenu.add(get_project_redirect_btn(request, project.id))


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

        name = appstruct['name']
        phase_id = appstruct['phase_id']
        phase = Phase.get(phase_id)
        project_id = appstruct['project_id']
        project = Project.get(project_id)
        customer_id = appstruct['customer_id']
        customer = Customer.get(customer_id)

        new_object = self.factory(
            self.context.company,
            customer,
            project,
            phase,
            self.request.user,
        )
        new_object.name = name

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


class TaskEditView(BaseView):

    def title(self):
        return u"Modification du document {task.name}".format(task=self.context)

    def load_catalog_url(self):
        return self.request.route_path(
            "sale_categories",
            id=self.context.company.id,
            _query=dict(action='jstree')
        )

    def context_url(self):
        return self.request.route_path(
            '/api/v1/' + self.request.context.type_ + 's/{id}',
            id=self.request.context.id
        )

    def form_config_url(self):
        return self.request.route_path(
            '/api/v1/' + self.request.context.type_ + 's/{id}',
            id=self.request.context.id,
            _query={'form_config': '1'}
        )

    def __call__(self):
        if not self.request.has_permission('edit.%s' % self.context.type_):
            return HTTPFound(self.request.current_route_path() + '.html')

        if hasattr(self, '_before'):
            self._before()

        task_css.need()
        jstree_css.need()
        populate_actionmenu(self.request)
        return dict(
            context=self.context,
            title=self.title(),
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

        return HTTPFound(self.request.route_path('project', id=project.id))


class TaskDuplicateView(BaseFormView):
    """
    Task duplication view
    """
    form_options = (('formid', 'duplicate_form'),)
    schema = get_duplicate_schema()

    @property
    def title(self):
        return u"Dupliquer {0} {1}".format(self.label, self.context.name)

    def before(self, form):
        BaseFormView.before(self, form)
        duplicate_js.need()

    def submit_success(self, appstruct):
        logger.debug("# Duplicating a document #")

        name = appstruct['name']
        phase_id = appstruct['phase_id']
        phase = Phase.get(phase_id)
        project_id = appstruct['project_id']
        project = Project.get(project_id)
        customer_id = appstruct['customer_id']
        customer = Customer.get(customer_id)

        task = self.context.duplicate(
            self.request.user,
            project,
            phase,
            customer,
        )
        task.name = name
        task.course = appstruct['course']
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


class TaskHtmlView(BaseView):
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

    def __call__(self):
        task_html_pdf_css.need()
        # If the task is editable, we go the edit page
        if self.request.has_permission('edit.%s' % self.context.type_):
            return HTTPFound(
                self.request.route_path(
                    "/%ss/{id}" % self.context.type_,
                    id=self.context.id
                )
            )

        populate_actionmenu(self.request)

        return dict(
            title=self.title,
            task=self.context,
            actions=self.actions(),
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
    def __call__(self):
        pdf_css.need()
        number = self.request.context.internal_number
        label = force_filename(number)
        filename = u"{0}.pdf".format(label)
        html_string = html(self.request)
        write_pdf(self.request, filename, html_string)
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

    def submit_success(self, appstruct):
        appstruct.pop('customer_id')
        for key, value in appstruct.items():
            setattr(self.context, key, value)
        self.request.dbsession.merge(self.context)
        return self.redirect()

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
