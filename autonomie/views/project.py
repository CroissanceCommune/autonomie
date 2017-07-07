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
import colander
from sqlalchemy import (
    or_,
    distinct,
)
from deform import Form

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound

from autonomie_base.models.base import DBSESSION
from autonomie.models.project import (
    Project,
    Phase,
    FORM_GRID,
)
from autonomie.models.customer import Customer
from autonomie.utils.colors import COLORS_SET
from autonomie.utils.widgets import (
    ViewLink,
)
from autonomie.forms.project import (
    get_list_schema,
    get_project_schema,
    PhaseSchema,
)
from autonomie.forms import (
    merge_session_with_post,
)
from deform_extensions import GridFormWidget
from autonomie.views import (
    BaseFormView,
    submit_btn,
    BaseListView,
)
from autonomie.views.files import (
    FileUploadView,
)

log = logger = logging.getLogger(__name__)


class PhaseAddFormView(BaseFormView):
    title = u"Ajouter un dossier au projet"
    schema = PhaseSchema()

    def submit_success(self, appstruct):
        model = Phase()
        model.project_id = self.context.id
        merge_session_with_post(model, appstruct)
        self.dbsession.add(model)
        self.dbsession.flush()
        redirect = self.request.route_path(
            "project",
            id=model.project_id,
            _query={'phase': model.id}
        )
        return HTTPFound(redirect)


class PhaseEditFormView(BaseFormView):
    title = u"Édition du dossier"
    schema = PhaseSchema()

    def before(self, form):
        form.set_appstruct(self.context.appstruct())

    def submit_success(self, appstruct):
        merge_session_with_post(self.context, appstruct)
        self.dbsession.merge(self.context)
        redirect = self.request.route_path(
            "project",
            id=self.context.project_id,
        )
        return HTTPFound(redirect)


def phase_delete_view(context, request):
    """
    Phase deletion view

    Allows to delete phases without documents
    :param obj context: The current phase
    :param obj request: The pyramid request object
    """
    redirect = request.route_path(
        "project",
        id=context.project_id,
    )
    if len(context.tasks) == 0:
        msg = u"Le dossier {0} a été supprimé".format(context.name)
        request.dbsession.delete(context)
        request.session.flash(msg)
    else:
        msg = u"Impossible de supprimer le dossier {0}, il contient \
des documents".format(context.name)
        request.session.flash(msg, 'error')
    return HTTPFound(redirect)


def get_project_form(request):
    """
    Returns the project add/edit form
    """
    schema = get_project_schema().bind(request=request)
    form = Form(schema, buttons=(submit_btn,))
    form.widget = GridFormWidget(named_grid=FORM_GRID)
    return form


def redirect_to_customerslist(request, company):
    """
        Force project page to be redirected to customer page
    """
    request.session.flash(u"Vous avez été redirigé vers la liste \
des clients")
    request.session.flash(u"Vous devez créer des clients afin \
de créer de nouveaux projets")
    raise HTTPFound(
        request.route_path("company_customers", id=company.id)
    )


class ProjectsList(BaseListView):
    """
    The project list view is compound of :
        * the list of projects with action buttons (view, delete ...)
        * an action menu with:
            * links
            * an add projectform popup
            * a searchform
    """
    add_template_vars = ('title', 'stream_actions', 'addform')
    title = u"Liste des projets"
    schema = get_list_schema()
    default_sort = "created_at"
    default_direction = "desc"
    sort_columns = {
        'name': Project.name,
        "code": Project.code,
        "created_at": Project.created_at,
    }

    def query(self):
        company = self.request.context
        # We can't have projects without having customers
        if not company.customers:
            redirect_to_customerslist(self.request, company)
        main_query = DBSESSION().query(distinct(Project.id), Project)
        main_query = main_query.outerjoin(Project.customers)
        return main_query.filter(Project.company_id == company.id)

    def filter_archived(self, query, appstruct):
        archived = appstruct.get('archived', False)
        if archived in (False, colander.null):
            query = query.filter(Project.archived == False)
        return query

    def filter_name_or_customer(self, query, appstruct):
        search = appstruct['search']
        if search:
            query = query.filter(
                or_(
                    Project.name.like("%" + search + "%"),
                    Project.customers.any(
                        Customer.name.like("%" + search + "%")
                    )
                )
            )
        return query

    @property
    def addform(self):
        res = None
        if self.request.has_permission('add_project'):
            form = get_project_form(self.request)
            res = form.render()
        return res

    def stream_actions(self, project):
        """
        Stream actions available for the given project

        :param obj project: A Project instance
        :rtype: generator
        """
        yield (
            self.request.route_path("project", id=project.id),
            u"Voir/Modifier",
            u"Voir/Modifier",
            u"pencil",
            {}
        )
        if self.request.has_permission('add_estimation'):
            yield (
                self.request.route_path("project_estimations", id=project.id),
                u"Nouveau devis",
                u"Créer un devis",
                u"file",
                {}
            )
        if self.request.has_permission('add_invoice'):
            yield (
                self.request.route_path("project_invoices", id=project.id),
                u"Nouvelle facture",
                u"Créer une facture",
                u"file",
                {}
            )
        if self.request.has_permission('edit_project'):
            if project.archived:
                yield (
                    self.request.route_path(
                        "project",
                        id=project.id,
                        _query=dict(action="archive")
                    ),
                    u"Désarchiver le projet",
                    u"Désarchiver le projet",
                    u"book",
                    {}
                )
                if not project.has_tasks():
                    yield (
                        self.request.route_path(
                            "project",
                            id=project.id,
                            _query=dict(action="delete")
                        ),
                        u"Supprimer",
                        u"Supprimer ce projet",
                        u"trash",
                        {
                            "onclick": (
                                u"return confirm('Êtes-vous sûr de "
                                "vouloir supprimer ce projet ?')"
                            )
                        }
                    )
            else:
                yield (
                    self.request.route_path(
                        "project",
                        id=project.id,
                        _query=dict(action="archive")
                    ),
                    u"Archiver le projet",
                    u"Archiver le projet",
                    u"book",
                    {}
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
    return HTTPFound(request.referer)


def project_delete(request):
    """
        Delete the current project
    """
    project = request.context
    log.info(u"Project {0} deleted".format(project))
    request.dbsession.delete(project)
    request.session.flash(
        u"Le projet '{0}' a bien été supprimé".format(project.name)
    )
    return HTTPFound(request.referer)


def get_color(index):
    """
    return the color for the given index (uses modulo to avoid index errors
    """
    return COLORS_SET[index % len(COLORS_SET)]


def get_phase_add_form(request):
    """
    Return a form object for phase add
    :param obj request: The pyramid request object
    :returns: A form
    :rtype: class:`deform.Form`
    """
    schema = PhaseSchema().bind(request=request)
    form = Form(
        schema,
        buttons=(submit_btn,),
        action=request.current_route_path(_query={'action': 'addphase'}),
    )
    return form


def set_task_colors(phases):
    """
    Set colors on the estimation/invoice/cancelinvoice objects so that we can
    visually identify related objects

    :param list phases: The list of phases of this project
    """
    index = 0

    for phase in phases:
        for estimation in phase.estimations:
            estimation.color = get_color(index)
            index += 1

    for phase in phases:
        for invoice in phase.invoices:
            if invoice.estimation:
                invoice.color = invoice.estimation.color
            else:
                invoice.color = get_color(index)
                index += 1

    for phase in phases:
        for cancelinvoice in phase.cancelinvoices:
            if cancelinvoice.invoice:
                cancelinvoice.color = cancelinvoice.invoice.color
            else:
                cancelinvoice.color = get_color(index)
                index += 1


def get_latest_phase(request, phases):
    """
    Return the phase where we can identify the last modification
    :param list phases: The list of phases of the given project
    """
    result = 0
    if 'phase' in request.GET:
        result = Phase.get(request.GET['phase'])

    else:
        # We get the latest used task and so we get the latest used phase
        all_tasks = []
        for phase in phases:
            all_tasks.extend(phase.tasks)
        all_tasks.sort(key=lambda task: task.status_date, reverse=True)

        if all_tasks:
            result = all_tasks[0].phase
    return result


def project_view(request):
    """
        Return datas for displaying one project
    """
    populate_actionmenu(request, request.context)
    phases = request.context.phases

    set_task_colors(phases)

    customer_names = (
        customer.get_label() for customer in request.context.customers
    )
    title = u"Projet : {0} ({1})".format(
        request.context.name,
        ", ".join(customer_names)
    )

    return dict(
        title=title,
        project=request.context,
        company=request.context.company,
        latest_phase=get_latest_phase(request, phases),
        phase_form=get_phase_add_form(request),
    )


class ProjectAdd(BaseFormView):
    add_template_vars = ('title', 'projects', )
    title = u"Ajout d'un nouveau projet"
    schema = get_project_schema()
    buttons = (submit_btn,)
    validation_msg = u"Le projet a été ajouté avec succès"

    @property
    def projects(self):
        return self.context.get_project_codes_and_names()

    def before(self, form):
        populate_actionmenu(self.request)
        form.widget = GridFormWidget(named_grid=FORM_GRID)
        # If there's no customer, redirect to customer view
        if len(self.request.context.customers) == 0:
            redirect_to_customerslist(self.request, self.request.context)

    def submit_success(self, appstruct):
        """
            Add a project with a default phase in the database
        """
        # It's an add form
        model = self.schema.objectify(appstruct)
        model.company = self.context

        # Add a default phase to the project
        default_phase = Phase()
        model.phases.append(default_phase)

        self.dbsession.add(model)

        self.dbsession.flush()

        self.session.flash(self.validation_msg)
        return HTTPFound(
            self.request.route_path(
                'project',
                id=model.id
            )
        )


class ProjectEdit(ProjectAdd):
    add_template_vars = ('title', 'project', 'projects',)
    validation_msg = u"Le projet a été modifié avec succès"

    def appstruct(self):
        """
        Populate the form with the current edited context (customer)
        """
        return self.schema.dictify(self.request.context)

    @reify
    def title(self):
        return u"Modification du projet : {0}".format(self.request.context.name)

    @reify
    def project(self):
        return self.context

    @property
    def projects(self):
        query = self.context.company.get_project_codes_and_names()
        return query.filter(Project.id != self.context.id)

    def submit_success(self, appstruct):
        # It's an edition one
        model = self.schema.objectify(appstruct, self.context)
        model = self.dbsession.merge(model)

        self.dbsession.flush()

        self.session.flash(self.validation_msg)
        return HTTPFound(
            self.request.route_path(
                'project',
                id=model.id
            )
        )


def populate_actionmenu(request, project=None):
    """
        add items to the "actionmenu"
    """
    company_id = request.context.get_company_id()
    request.actionmenu.add(get_list_view_btn(company_id))


def get_list_view_btn(cid):
    """
    Build a button returning the user to the project list

    :param int cid: The company id we're working on
    :returns: A Link object
    """
    return ViewLink(
        u"Liste des projets",
        "list_projects",
        path="company_projects",
        id=cid,
    )


def includeme(config):
    config.add_route(
        'company_projects',
        '/company/{id:\d+}/projects',
        traverse='/companies/{id}',
    )
    config.add_route(
        'project',
        '/projects/{id:\d+}',
        traverse='/projects/{id}',
    )
    config.add_route(
        'phase',
        '/phases/{id:\d+}',
        traverse='/phases/{id}',
    )
    config.add_view(
        ProjectAdd,
        route_name='company_projects',
        renderer='project_edit.mako',
        request_method='POST',
        permission='list_projects',
    )
    config.add_view(
        ProjectAdd,
        route_name='company_projects',
        renderer='project_edit.mako',
        request_param='action=add',
        permission='add_project',
    )
    config.add_view(
        ProjectEdit,
        route_name='project',
        renderer='project_edit.mako',
        request_param='action=edit',
        permission='edit_project',
    )
    config.add_view(
        project_view,
        route_name='project',
        renderer='project.mako',
        permission='view_project',
    )
    config.add_view(
        project_delete,
        route_name="project",
        request_param="action=delete",
        permission='edit_project',
    )
    config.add_view(
        project_archive,
        route_name="project",
        request_param="action=archive",
        permission='edit_project',
    )
    config.add_view(
        PhaseAddFormView,
        route_name="project",
        request_param="action=addphase",
        renderer="base/formpage.mako",
        permission='edit_project',
    )
    config.add_view(
        PhaseEditFormView,
        route_name="phase",
        renderer="base/formpage.mako",
        permission='edit_phase',
    )
    config.add_view(
        phase_delete_view,
        route_name="phase",
        renderer="base/formpage.mako",
        permission='edit_phase',
        request_param="action=delete",
    )
    config.add_view(
        ProjectsList,
        route_name='company_projects',
        renderer='projects.mako',
        request_method='GET',
        permission='list_projects',
    )
    config.add_view(
        FileUploadView,
        route_name="project",
        renderer='base/formpage.mako',
        permission='edit_project',
        request_param='action=attach_file',
    )
