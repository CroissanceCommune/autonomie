# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

import logging
from autonomie.models.project.project import Project
from autonomie.utils.menu import (
    MenuItem,
    Menu,
)
from autonomie.default_layouts import DefaultLayout
from autonomie.views.project.routes import (
    PROJECT_ITEM_ROUTE,
    PROJECT_ITEM_ESTIMATION_ROUTE,
    PROJECT_ITEM_INVOICE_ROUTE,
    PROJECT_ITEM_PHASE_ROUTE,
    PROJECT_ITEM_GENERAL_ROUTE,
    PROJECT_ITEM_BUSINESS_ROUTE,
    PROJECT_ITEM_FILE_ROUTE,
)


logger = logging.getLogger(__name__)


ProjectMenu = Menu(name="projectmenu")


def deferred_business_list_show_perms(item, kw):
    proj = kw['current_project']
    request = kw['request']
    return proj.project_type.name != 'default' and \
        request.has_permission('list.businesses')


def deferred_phase_show_perms(item, kw):
    """
    Check if the phase menu should be shown
    """
    proj = kw['current_project']
    request = kw['request']
    if proj.project_type.name in ('training', 'construction'):
        return False
    else:
        return True and request.has_permission('view.project')


ProjectMenu.add(
    MenuItem(
        name="project_businesses",
        label=u"Liste des affaires",
        route_name=PROJECT_ITEM_BUSINESS_ROUTE,
        icon=u'fa fa-folder-open',
        perm=deferred_business_list_show_perms,
    )
)
ProjectMenu.add(
    MenuItem(
        name="project_phases",
        label=u"Document rangés par dossiers",
        route_name=PROJECT_ITEM_PHASE_ROUTE,
        icon=u'fa fa-folder-open',
        perm=deferred_phase_show_perms,
    )
)
ProjectMenu.add(
    MenuItem(
        name="project_estimations",
        label=u'Tous les devis',
        route_name=PROJECT_ITEM_ESTIMATION_ROUTE,
        icon=u'fa fa-files-o',
        perm='list.estimations',
    )
)
ProjectMenu.add(
    MenuItem(
        name="project_invoices",
        label=u'Toutes les factures',
        route_name=PROJECT_ITEM_INVOICE_ROUTE,
        icon=u'fa fa-files-o',
        perm='list.invoices',
    )
)
ProjectMenu.add(
    MenuItem(
        name="project_files",
        label=u'Fichiers rattachés',
        route_name=PROJECT_ITEM_FILE_ROUTE,
        icon=u"fa fa-briefcase",
        perm='list.files',
    )
)


class ProjectLayout(DefaultLayout):
    """
    Layout for project related pages

    Provide the main page structure for project view
    """

    def __init__(self, context, request):
        DefaultLayout.__init__(self, context, request)
        if isinstance(context, Project):
            self.current_project_object = context
        elif hasattr(context, 'project'):
            self.current_project_object = context.project
        else:
            raise KeyError(u"Can't retrieve the associated project object, \
                           current context : %s" % context)

    @property
    def edit_url(self):
        return self.request.route_path(
            PROJECT_ITEM_ROUTE,
            id=self.current_project_object.id,
            _query={'action': 'edit'}
        )

    @property
    def details_url(self):
        return self.request.route_path(
            PROJECT_ITEM_GENERAL_ROUTE,
            id=self.current_project_object.id,
        )

    @property
    def customer_labels(self):
        return (customer.label
                for customer in self.current_project_object.customers)

    @property
    def projectmenu(self):
        ProjectMenu.set_current(self.current_project_object)
        ProjectMenu.bind(current_project=self.current_project_object)
        return ProjectMenu


def includeme(config):
    config.add_layout(
        ProjectLayout,
        template='autonomie:templates/project/layout.mako',
        name='project'
    )
