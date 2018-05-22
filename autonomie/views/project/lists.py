# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
from pyramid.httpexceptions import HTTPFound
from sqlalchemy import (
    or_,
    distinct,
)

from autonomie_base.models.base import DBSESSION

from autonomie.models.customer import Customer
from autonomie.models.project.project import Project
from autonomie.forms.project import (
    get_list_schema,
)
from autonomie.views import (
    BaseListView,
    TreeMixin,
)
from autonomie.views.project.routes import (
    COMPANY_PROJECTS_ROUTE,
    PROJECT_ITEM_ROUTE,
    PROJECT_ITEM_ESTIMATION_ROUTE,
    PROJECT_ITEM_INVOICE_ROUTE,
)


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


class ProjectListView(BaseListView, TreeMixin):
    """
    The project list view is compound of :
        * the list of projects with action buttons (view, delete ...)
        * an action menu with:
            * links
            * an add projectform popup
            * a searchform
    """
    add_template_vars = ('title', 'stream_actions', 'add_url')
    title = u"Liste des projets"
    schema = get_list_schema()
    default_sort = "created_at"
    default_direction = "desc"
    sort_columns = {
        'name': Project.name,
        "code": Project.code,
        "created_at": Project.created_at,
    }
    route_name = COMPANY_PROJECTS_ROUTE
    item_route_name = PROJECT_ITEM_ROUTE

    @property
    def url(self):
        if isinstance(self.context, Project):
            cid = self.context.company_id
        else:
            cid = self.context.id
        return self.request.route_path(self.route_name, id=cid)

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

    def stream_actions(self, project):
        """
        Stream actions available for the given project

        :param obj project: A Project instance
        :rtype: generator
        """
        yield (
            self._get_item_url(project),
            u"Voir/Modifier",
            u"Voir/Modifier",
            u"pencil",
            {}
        )
        if self.request.has_permission('add_estimation', project):
            yield (
                self.request.route_path(
                    PROJECT_ITEM_ESTIMATION_ROUTE,
                    id=project.id,
                    _query={'action': 'add'},
                ),
                u"Nouveau devis",
                u"Créer un devis",
                u"file",
                {}
            )
        if self.request.has_permission('add_invoice', project):
            yield (
                self.request.route_path(
                    PROJECT_ITEM_INVOICE_ROUTE,
                    id=project.id,
                    _query={'action': 'add'},
                ),
                u"Nouvelle facture",
                u"Créer une facture",
                u"file",
                {}
            )
        if self.request.has_permission('edit_project', project):
            if project.archived:
                yield (
                    self._get_item_url(project, action='archive'),
                    u"Désarchiver le projet",
                    u"Désarchiver le projet",
                    u"book",
                    {}
                )
            else:
                yield (
                    self._get_item_url(project, action='archive'),
                    u"Archiver le projet",
                    u"Archiver le projet",
                    u"book",
                    {}
                )
        if self.request.has_permission('delete_project', project):
            yield (
                self._get_item_url(project, action='delete'),
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

    @property
    def add_url(self):
        return self.request.route_path(
            COMPANY_PROJECTS_ROUTE,
            id=self.context.id,
            _query={'action': 'add'}
        )


def includeme(config):
    config.add_tree_view(
        ProjectListView,
        renderer='project/list.mako',
        request_method='GET',
        permission='list_projects',
    )
