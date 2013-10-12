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
from colorsys import hsv_to_rgb
from random import uniform

from sqlalchemy import or_
from webhelpers.html.builder import HTML
from deform import Form

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from autonomie.models.project import (
        Project,
        Phase,
        )
from autonomie.models.customer import Customer
from autonomie.utils.widgets import (
        ViewLink,
        ToggleLink,
        ItemActionLink,
        StaticWidget,
        PopUp,
        SearchForm,
        )
from autonomie.utils.views import submit_btn
from autonomie.views.forms import (
        merge_session_with_post,
        BaseFormView,
        )
from autonomie.views.forms.project import (
        ProjectsListSchema,
        ProjectSchema,
        )
from .base import BaseListView

log = logging.getLogger(__name__)


def rgb_to_hex(rgb):
    """
        return an hexadecimal version of the rgb tuple
        for css rendering
    """
    return '#%02x%02x%02x' % rgb


def get_color():
    """
        return a random color
    """
    h = uniform(0.1, 0.8)
    s = uniform(0.8, 1)
    v = uniform(0.8, 1)
    return rgb_to_hex(tuple(255 * c for c in hsv_to_rgb(h, s, v)))


def get_project_form(request):
    """
        Returns the project add/edit form
    """
    schema = ProjectSchema().bind(request=request)
    form = Form(schema, buttons=(submit_btn,))
    return form


def redirect_to_customerslist(request, company):
    """
        Force project page to be redirected to customer page
    """
    request.session.flash(u"Vous avez été redirigé vers la liste \
des clients")
    request.session.flash(u"Vous devez créer des clients afin \
de créer de nouveaux projets")
    raise HTTPFound(request.route_path("company_customers",
                                                id=company.id))


class ProjectsList(BaseListView):
    """
        The project list view is compound of :
            * the list of projects with action buttons (view, delete ...)
            * an action menu with:
                * links
                * an add projectform popup
                * a searchform
    """
    add_template_vars = ('title', 'item_actions',)
    title = u"Liste des projets"
    schema = ProjectsListSchema()
    default_sort = "name"
    sort_columns = {'name':Project.name,
                    "code":Project.code,
                    }

    def query(self):
        company = self.request.context
        # We can't have projects without having customers
        if not company.customers:
            redirect_to_customerslist(self.request, company)
        return Project.query().outerjoin(Project.customers).filter(
                            Project.company_id == company.id)

    def filter_archived(self, query, appstruct):
        archived = appstruct['archived']
        return query.filter(Project.archived == archived)

    def filter_name_or_customer(self, query, appstruct):
        search = appstruct['search']
        if search:
            query = query.filter(
                or_(Project.name.like("%" + search + "%"),
                    Project.customers.any(Customer.name.like("%" + search + "%"))))
        return query

    def populate_actionmenu(self, appstruct):
        populate_actionmenu(self.request)
        if has_permission('add', self.request.context, self.request):
            form = get_project_form(self.request)
            popup = PopUp('add', u"Ajouter un projet", form.render())
            self.request.popups = {popup.name: popup}
            self.request.actionmenu.add(popup.open_btn())
        self.request.actionmenu.add(self._get_archived_btn(appstruct))
        searchform = SearchForm(u"Projet ou nom du client")
        searchform.set_defaults(appstruct)
        self.request.actionmenu.add(searchform)

    def _get_archived_btn(self, appstruct):
        """
            return the show archived button
        """
        archived = appstruct['archived']
        if archived == '0':
            url = self.request.current_route_path(_query=dict(archived="1"))
            link = HTML.a(u"Afficher les projets archivés",  href=url)
        else:
            url = self.request.current_route_path(_query=dict(archived="0"))
            link = HTML.a(u"Afficher les projets actifs", href=url)
        return StaticWidget(link)

    @property
    def item_actions(self):
        """
            return action buttons builder
        """
        return self._get_actions()

    def _get_actions(self):
        """
            Return action buttons with permission handling
        """
        btns = []
        btns.append(ItemActionLink(u"Voir", "view", css='btn',
                path="project", icon="icon-search"))
        btns.append(ItemActionLink(u"Devis", "edit", css="btn",
            title=u"Nouveau devis",
            path="project_estimations", icon=("icon-file", )))
        btns.append(ItemActionLink(u"Facture", "edit", css="btn",
            title=u"Nouvelle facture",
            path="project_invoices", icon=("icon-file", )))
        if self.request.params.get('archived', '0') == '0':
            btns.append(ItemActionLink(u"Archiver", "edit", css="btn",
                   confirm=u'Êtes-vous sûr de vouloir archiver ce projet ?',
                                path="project",
                                title=u"Archiver le projet",
                                _query=dict(action="archive"),
                                icon="icon-book"))
        else:
            del_link = ItemActionLink(u"Supprimer", "edit", css="btn",
                   confirm=u'Êtes-vous sûr de vouloir supprimer ce projet ?',
                                      path="project",
                                      title=u"Supprimer le projet",
                                      _query=dict(action="delete"),
                                      icon="icon-trash")

            def is_deletable_perm(context, req):
                """
                    Return True if the current item (context) is deletable
                """
                return context.is_deletable()
            del_link.set_special_perm_func(is_deletable_perm)
            btns.append(del_link)
        return btns


def project_addphase(request):
    """
        Add a phase to the current project
    """
    #TODO : utiliser deform pour manager l'ajout de phase (pour le principe)
    # This one should be a Form View
    project = request.context
    if not request.params.get('phase'):
        request.session.flash(u"Le nom de la phase est obligatoire",
                                                            queue='error')
        anchor = "showphase"
    else:
        phasename = request.params.get('phase')
        phase = Phase()
        phase.name = phasename
        phase.project_id = project.id
        request.dbsession.add(phase)
        request.session.flash(u"La phase {0} a bien été \
rajoutée".format(phasename))
        anchor = ""
    return HTTPFound(request.route_path('project', id=project.id,
                                                    _anchor=anchor))


def project_archive(request):
    """
        Archive the current project
    """
    project = request.context
    project.archived = 1
    request.dbsession.merge(project)
    request.session.flash(u"Le projet '{0}' a été archivé"\
            .format(project.name))
    return HTTPFound(request.referer)

def project_delete(request):
    """
        Delete the current project
    """
    project = request.context
    request.dbsession.delete(project)
    request.session.flash(u"Le projet '{0}' a bien été supprimé".format(
                                                            project.name))
    return HTTPFound(request.referer)

def project_view(request):
    """
        Return datas for displaying one project
    """
    populate_actionmenu(request, request.context)
    phases = request.context.phases
    for phase in phases:
        for estimation in phase.estimations:
            estimation.color = get_color()
    for phase in phases:
        for invoice in phase.invoices:
            if invoice.estimation:
                invoice.color = invoice.estimation.color
            else:
                invoice.color = get_color()
    for phase in phases:
        for cancelinvoice in phase.cancelinvoices:
            if cancelinvoice.invoice:
                cancelinvoice.color = cancelinvoice.invoice.color
            else:
                cancelinvoice.color = get_color()
    title = u"Projet : {0} ({1})".format(request.context.name,
            ", ".join((customer.name for customer in request.context.customers)))
    return dict(title=title,
                project=request.context,
                company=request.context.company)


class ProjectAdd(BaseFormView):
    add_template_vars = ('title',)
    title = u"Ajout d'un nouveau projet"
    schema = ProjectSchema()
    buttons = (submit_btn,)

    def before(self, form):
        populate_actionmenu(self.request)
        # If there's no customer, redirect to customer view
        if len(self.request.context.customers) == 0:
            redirect_to_customerslist(self.request, self.request.context)

    def submit_success(self, appstruct):
        """
            Add a project with a default phase in the database
        """
        project = Project()
        project.company_id = self.request.context.id
        customer_ids = appstruct.pop("customers", [])
        project = merge_session_with_post(project, appstruct)
        for customer_id in customer_ids:
            customer = Customer.get(customer_id)
            if customer:
                project.customers.append(customer)
        self.dbsession.add(project)
        self.dbsession.flush()
        # Add a default phase to the project
        default_phase = Phase()
        default_phase.project = project
        self.dbsession.add(default_phase)
        message = u"Le projet <b>{0}</b> a été ajouté avec succès".format(
                                                                project.name)
        self.request.session.flash(message)
        return HTTPFound(self.request.route_path('project', id=project.id))


class ProjectEdit(BaseFormView):
    add_template_vars = ('title', 'project',)
    schema = ProjectSchema()
    buttons = (submit_btn,)

    def before(self, form):
        """
            populate the form with the current datas
        """
        appstruct = self.request.context.appstruct()
        appstruct['customers'] = [c.id for c in self.request.context.customers]
        form.set_appstruct(appstruct)
        populate_actionmenu(self.request, self.request.context)

    def submit_success(self, appstruct):
        """
            Flush project edition to the database
        """
        customer_ids = appstruct.pop("customers", [])
        project = merge_session_with_post(self.request.context, appstruct)
        project.customers = []
        for customer_id in customer_ids:
            customer = Customer.get(customer_id)
            if customer is not None:
                project.customers.append(customer)
        self.dbsession.merge(project)
        self.dbsession.flush()
        message = u"Le projet <b>{0}</b> a été édité avec succès".format(
                                                                  project.name)
        self.request.session.flash(message)
        return HTTPFound(self.request.route_path('project', id=project.id))

    @reify
    def title(self):
        return u"Édition du projet : {0}".format(self.request.context.name)

    @reify
    def project(self):
        return self.request.context


def populate_actionmenu(request, project=None):
    """
        add items to the "actionmenu"
    """
    company_id = request.context.get_company_id()
    request.actionmenu.add(get_list_view_btn(company_id))
    if project is not None:
        request.actionmenu.add(get_view_btn(project.id))
        if has_permission("edit", project, request):
            request.actionmenu.add(get_edit_btn(project.id))
            request.actionmenu.add(get_detail_btn())
            request.actionmenu.add(get_phase_btn())

def get_list_view_btn(cid):
    return ViewLink(u"Liste des projets", "edit",
                         path="company_projects",
                                          id=cid)

def get_view_btn(id_):
    return ViewLink(u"Voir", path="project", id=id_)

def get_edit_btn(id_):
    return ViewLink(u"Éditer",  path="project", id=id_,
                                    _query=dict(action="edit"))

def get_detail_btn():
    return ToggleLink(u"Afficher les détails", target="project-description")

def get_phase_btn():
    return ToggleLink(u"Ajouter une phase", target="project-addphase",
                                                       css="addphase")

def includeme(config):
    config.add_route('company_projects',
                     '/company/{id:\d+}/projects',
                     traverse='/companies/{id}')
    config.add_route('project',
                     '/projects/{id:\d+}',
                     traverse='/projects/{id}')
    config.add_view(ProjectAdd,
                    route_name='company_projects',
                    renderer='project.mako',
                    request_method='POST',
                    permission='edit')
    config.add_view(ProjectAdd,
                    route_name='company_projects',
                    renderer='project.mako',
                    request_param='action=add',
                    permission='edit')
    config.add_view(ProjectEdit,
                    route_name='project',
                    renderer='project.mako',
                    request_param='action=edit',
                    permission='edit')
    config.add_view(project_view,
                    route_name='project',
                    renderer='project_view.mako',
                    permission='view')
    config.add_view(project_delete,
                    route_name="project",
                    request_param="action=delete",
                    permission='edit')
    config.add_view(project_archive,
                    route_name="project",
                    request_param="action=archive",
                    permission='edit')
    config.add_view(project_addphase,
                    route_name="project",
                    request_param="action=addphase",
                    permission='edit')
    config.add_view(ProjectsList,
                    route_name='company_projects',
                    renderer='company_projects.mako',
                    request_method='GET',
                    permission='edit')
