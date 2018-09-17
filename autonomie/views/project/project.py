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
    Project views
    Context could be either company:
        add and list view
    or project :
        simple view, add_phase, edit, ...
"""
import logging
from deform import Form

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound

from autonomie.utils.navigation import NavigationHandler
from autonomie.models.project import (
    Project,
)
from autonomie.models.task import (
    Task,
    Estimation,
    Invoice,
    CancelInvoice
)
from autonomie.utils.colors import COLORS_SET
from autonomie.forms.project import (
    get_add_project_schema,
    get_add_step2_project_schema,
    get_edit_project_schema,
    PhaseSchema,
)
from autonomie.views import (
    BaseView,
    BaseAddView,
    BaseEditView,
    submit_btn,
    TreeMixin,
)
from autonomie.views.project.routes import (
    COMPANY_PROJECTS_ROUTE,
    PROJECT_ITEM_ROUTE,
    PROJECT_ITEM_GENERAL_ROUTE,
    PROJECT_ITEM_PHASE_ROUTE,
    PROJECT_ITEM_BUSINESS_ROUTE,
    PROJECT_ITEM_ESTIMATION_ROUTE,
)
from autonomie.views.project.lists import (
    redirect_to_customerslist,
    ProjectListView,
)

log = logger = logging.getLogger(__name__)
ADD_STEP1_FORM_GRID = (
    (
        ('name', 12),
    ),
    (
        ('project_type_id', 12),
    ),
    (
        ('customers', 12),
    ),
)
ADD_STEP2_FORM_GRID = (
    (
        ('description', 4),
        ('', 2),
        ('code', 2),
    ),
    (
        ('starting_date', 4),
        ('ending_date', 4),
    ),
    (
        ('definition', 10),
    ),
    (
        ('business_types', 10),
    )
)
EDIT_FORM_GRID = (
    (
        ('name', 12),
    ),
    (
        ('project_type_id', 10),
    ),
    (
        ('customers', 8),
    ),
    (
        ('description', 4),
        ('', 2),
        ('code', 2),
    ),
    (
        ('starting_date', 4),
        ('ending_date', 4),
    ),
    (
        ('definition', 10),
    ),
    (
        ('business_types', 10),
    )
)


def remember_navigation_history(request, project_id):
    """
    Remember the last page the user has visited inside a project

    :param obj request: The request object
    """
    keyword = "/projects/%s" % project_id
    handler = NavigationHandler(request, keyword)
    handler.remember()


def retrieve_navigation_history(request, project_id):
    """
    Retrieve the last page the user has visited inside a project

    :param obj request: The request object
    """
    keyword = "/projects/%s" % project_id
    handler = NavigationHandler(request, keyword)
    return handler.last()


class ProjectEntryPointView(BaseView, TreeMixin):
    route_name = PROJECT_ITEM_ROUTE

    @property
    def title(self):
        return u"Projet {}".format(self.current().name)

    def current(self):
        if hasattr(self.context, 'project_id'):
            return self.context.project
        else:
            return self.context

    @property
    def tree_url(self):
        return self.request.route_path(self.route_name, id=self.current().id)

    def __call__(self):
        """
        Project entry point view only redirects to the most appropriate page
        """
        last = retrieve_navigation_history(self.request, self.context.id)
        if last is None:
            if self.context.project_type.name == "default":
                last = self.request.route_path(
                    PROJECT_ITEM_PHASE_ROUTE,
                    id=self.context.id
                )
            elif self.context.businesses:
                last = self.request.route_path(
                    PROJECT_ITEM_BUSINESS_ROUTE,
                    id=self.context.id
                )
            else:
                last = self.request.route_path(
                    PROJECT_ITEM_ESTIMATION_ROUTE,
                    id=self.context.id
                )
        return HTTPFound(last)


class ProjectPhaseListView(BaseView, TreeMixin):
    route_name = PROJECT_ITEM_PHASE_ROUTE

    def __init__(self, *args, **kw):
        BaseView.__init__(self, *args, **kw)

    def current_id(self):
        if hasattr(self.context, 'project_id'):
            return self.context.project_id
        else:
            return self.context.id

    @property
    def tree_url(self):
        return self.request.route_path(self.route_name, id=self.current_id())

    @property
    def title(self):
        return u"Projet : {0}".format(self.context.name)

    def _get_phase_add_form(self):
        """
        Return a form object for phase add
        :param obj request: The pyramid request object
        :returns: A form
        :rtype: class:`deform.Form`
        """
        schema = PhaseSchema().bind(request=self.request)
        form = Form(
            schema,
            buttons=(submit_btn,),
            action=self.request.route_path(
                PROJECT_ITEM_ROUTE,
                id=self.context.id,
                _query={'action': 'addphase'}
            ),
        )
        return form

    def _get_latest_phase_id(self, tasks_by_phase):
        """
        Return the phase where we can identify the last modification

        :param list tasks_by_phase: The dict of tasks
        """
        result = 0
        if 'phase' in self.request.GET:
            result = int(self.request.GET['phase'])

        else:
            # We get the latest used task and so we get the latest used phase
            all_tasks = []
            for phase_id, tasks in tasks_by_phase.items():
                all_tasks.extend(tasks['estimations'])
                all_tasks.extend(tasks['invoices'])
            all_tasks.sort(key=lambda task: task.status_date, reverse=True)

            if all_tasks:
                result = all_tasks[0].phase_id

        return result

    def _get_color(self, index):
        """
        return the color for the given index (uses modulo to avoid index errors
        """
        return COLORS_SET[index % len(COLORS_SET)]

    def _set_estimation_colors(self, estimations):
        """
        Set colors on the estimations

        :param list estimations: Estimations
        """
        color_index = 0
        for estimation in estimations:
            estimation.color = self._get_color(color_index)
            color_index += 1

    def _set_invoice_colors(self, invoices):
        """
        Set colors on invoices

        :param list invoices: List of invoices
        """
        color_index = 0
        for invoice in invoices:
            if invoice.estimation and hasattr(invoice.estimation, 'color'):
                invoice.color = invoice.estimation.color
            else:
                invoice.color = self._get_color(color_index)
                color_index += 1

    def _set_cancelinvoice_colors(self, invoices):
        """
        Set colors on cancelinvoices

        :param list invoices: List of cancelinvoices
        """
        color_index = 0
        for invoice in invoices:
            if invoice.invoice and hasattr(invoice.invoice, 'color'):
                invoice.color = invoice.invoice.color
            else:
                invoice.color = self._get_color(color_index)
                color_index += 1

    def _collect_documents_by_phase(self, phases):
        """
        Collect all documents (estimations, invoices, cancelinvoices)
        and store them by phase

        :param phases: All the phases attached to this project
        :returns: A dict {phase_id: {'estimations': [], 'invoices': {}}}
        :rtype: dict
        """
        estimations = self.request.dbsession.query(Estimation).filter_by(
            project_id=self.context.id
        ).order_by(Estimation.date).all()

        query = self.request.dbsession.query(Task)
        query = query.with_polymorphic([Invoice, CancelInvoice])
        query = query.filter(Task.type_.in_(('invoice', 'cancelinvoice')))
        query = query.filter_by(project_id=self.context.id)
        invoices = query.order_by(Task.date).all()

        self._set_estimation_colors(estimations)
        self._set_invoice_colors([i for i in invoices if i.type_ == 'invoice'])
        self._set_cancelinvoice_colors(
            [i for i in invoices if i.type_ == 'cancelinvoice']
        )

        result = {}
        for phase in phases:
            result[phase.id] = {'estimations': [], 'invoices': []}
        for estimation in estimations:
            logger.debug("We've got an estimation : %s" % estimation.phase_id)
            phase_dict = result.setdefault(
                estimation.phase_id, {'estimations': [], 'invoices': []}
            )
            phase_dict['estimations'].append(estimation)

        for invoice in invoices:
            phase_dict = result.setdefault(
                invoice.phase_id, {'estimations': [], 'invoices': []}
            )
            phase_dict['invoices'].append(invoice)
        logger.debug("Returning %s" % result)
        return result

    def __call__(self):
        remember_navigation_history(self.request, self.context.id)
        self.populate_navigation()
        phases = self.context.phases
        tasks_by_phase = self._collect_documents_by_phase(phases)

        return dict(
            project=self.context,
            latest_phase_id=self._get_latest_phase_id(tasks_by_phase),
            phase_form=self._get_phase_add_form(),
            tasks_by_phase=tasks_by_phase,
            tasks_without_phases=tasks_by_phase.pop(None, None),
            phases=phases,
        )


class ProjectGeneralView(BaseView, TreeMixin):
    route_name = PROJECT_ITEM_GENERAL_ROUTE

    @property
    def tree_url(self):
        return self.request.route_path(self.route_name, id=self.context.id)

    @property
    def title(self):
        return u"Projet : {0}".format(self.context.name)

    def __call__(self):
        """
            Return datas for displaying one project
        """
        self.populate_navigation()

        return dict(
            title=self.title,
            project=self.context,
            company=self.context.company,
        )


class ProjectAddView(BaseAddView, TreeMixin):
    title = u"Ajout d'un nouveau projet"
    schema = get_add_project_schema()
    msg = u"Le projet a été ajouté avec succès"
    named_form_grid = ADD_STEP1_FORM_GRID
    factory = Project
    route_name = COMPANY_PROJECTS_ROUTE

    def before(self, form):
        BaseAddView.before(self, form)
        self.populate_navigation()
        # If there's no customer, redirect to customer view
        if len(self.request.context.customers) == 0:
            redirect_to_customerslist(self.request, self.request.context)

    def redirect(self, new_model):
        return HTTPFound(
            self.request.route_path(
                PROJECT_ITEM_ROUTE,
                id=new_model.id,
                _query={'action': 'addstep2'},
            )
        )

    def on_add(self, new_model, appstruct):
        """
        On add, set the project's company
        """
        new_model.company = self.context


class ProjectAddStep2View(BaseEditView, TreeMixin):
    named_form_grid = ADD_STEP2_FORM_GRID
    add_template_vars = ('title', 'project_codes')
    schema = get_add_step2_project_schema()
    route_name = PROJECT_ITEM_ROUTE

    @property
    def project_codes(self):
        return Project.get_code_list_with_labels(self.context.company_id)

    @reify
    def title(self):
        return u"Création du projet : {0}, étape 2".format(self.context.name)

    def redirect(self):
        return HTTPFound(
            self.request.route_path(
                PROJECT_ITEM_ROUTE,
                id=self.context.id,
            )
        )


class ProjectEditView(BaseEditView, TreeMixin):
    add_template_vars = ('project', 'project_codes',)
    named_form_grid = EDIT_FORM_GRID
    schema = get_edit_project_schema()
    route_name = PROJECT_ITEM_ROUTE

    def before(self, form):
        BaseEditView.before(self, form)
        self.populate_navigation()

    @property
    def title(self):
        return u"Modification du projet : {0}".format(self.request.context.name)

    @property
    def project(self):
        return self.context

    @property
    def project_codes(self):
        return Project.get_code_list_with_labels(self.context.company_id)

    def redirect(self):
        return HTTPFound(
            self.request.route_path(
                PROJECT_ITEM_ROUTE,
                id=self.context.id
            )
        )


def project_archive(request):
    """
    Archive the current project
    """
    project = request.context
    if not project.archived:
        project.archived = True
    else:
        project.archived = False
        request.session.flash(
            u"Le projet '{0}' a été désarchivé".format(project.name)
        )
    request.dbsession.merge(project)
    if request.referer is not None:
        return HTTPFound(request.referer)
    else:
        return HTTPFound(
            request.route_path(
                COMPANY_PROJECTS_ROUTE,
                id=request.context.company_id
            )
        )


def project_delete(request):
    """
        Delete the current project
    """
    project = request.context
    cid = project.company_id
    log.info(u"Project {0} deleted".format(project))
    request.dbsession.delete(project)
    request.session.flash(
        u"Le projet '{0}' a bien été supprimé".format(project.name)
    )
    if request.referer is not None:
        return HTTPFound(request.referer)
    else:
        return HTTPFound(
            request.route_path(COMPANY_PROJECTS_ROUTE, id=cid)
        )


def includeme(config):
    config.add_tree_view(
        ProjectEntryPointView,
        parent=ProjectListView,
        permission='view.project',
    )
    config.add_tree_view(
        ProjectPhaseListView,
        parent=ProjectListView,
        renderer='project/phases.mako',
        permission='view_project',
        layout='project',
    )
    config.add_tree_view(
        ProjectGeneralView,
        parent=ProjectListView,
        renderer='project/general.mako',
        permission='view_project',
        layout='project',
    )
    config.add_tree_view(
        ProjectAddView,
        parent=ProjectListView,
        renderer='autonomie:templates/base/formpage.mako',
        request_param='action=add',
        permission='add_project',
        layout='default',
    )
    config.add_tree_view(
        ProjectAddStep2View,
        parent=ProjectListView,
        renderer='project/edit.mako',
        request_param='action=addstep2',
        permission='edit_project',
        layout='default',
    )
    config.add_tree_view(
        ProjectEditView,
        parent=ProjectGeneralView,
        renderer='project/edit.mako',
        request_param='action=edit',
        permission='edit_project',
        layout='project',
    )
    config.add_view(
        project_delete,
        route_name=PROJECT_ITEM_ROUTE,
        request_param="action=delete",
        permission='edit_project',
    )
    config.add_view(
        project_archive,
        route_name=PROJECT_ITEM_ROUTE,
        request_param="action=archive",
        permission='edit_project',
    )
