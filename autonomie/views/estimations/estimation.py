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
    Estimation views


Estimation datas edition :
    date
    address
    customer
    object
    note
    mentions
    ....

Estimation line edition :
    description
    quantity
    cost
    unity
    tva
    ...

Estimation line group edition :
    title
    description

Estimation discount edition

Estimation payment edition

"""
import logging

from pyramid.httpexceptions import HTTPFound

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.task import (
    Estimation,
)
from autonomie.models.customer import Customer
from autonomie.models.project import (
    Phase,
    Project,
)
from autonomie.forms.task import (
    get_new_task_schema,
    get_duplicate_schema,
)
from autonomie.resources import duplicate_js
from autonomie.views import (
    submit_btn,
    BaseEditView,
    BaseFormView,
    BaseView,
)
from autonomie.views.files import FileUploadView
from autonomie.views.taskaction import (
    populate_actionmenu,
    task_pdf_view,
    get_task_html_view,
    make_task_delete_view,
)

log = logger = logging.getLogger(__name__)


class EstimationAdd(BaseFormView):
    """
    Estimation add view
    context is a project
    """
    title = "Nouveau devis"
    schema = get_new_task_schema()
    buttons = (submit_btn,)

    def before(self, form):
        super(EstimationAdd, self).before(form)
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        log.debug("# Adding a new estimation")
        name = appstruct['name']
        phase_id = appstruct['phase_id']
        phase = Phase.get(phase_id)
        project_id = appstruct['project_id']
        project = Project.get(project_id)
        customer_id = appstruct['customer_id']
        customer = Customer.get(customer_id)

        estimation = Estimation(
            self.context.company,
            customer,
            project,
            phase,
            self.request.user,
        )
        estimation.name = name
        estimation.address = customer.full_address
        estimation.course = appstruct['course']
        self.dbsession.add(estimation)
        self.dbsession.flush()
        logger.debug(
            "  + Estimation successfully added : {0}".format(estimation.id)
        )
        return HTTPFound(
            self.request.route_path(
                "/estimations/{id}",
                id=estimation.id
            )
        )


class EstimationEditView(BaseView):

    @property
    def title(self):
        return u"Édition du devis {task.name}".format(task=self.context)

    def __call__(self):
        populate_actionmenu(self.request)
        return dict(context=self.context, title=self.title)


class AdminEstimation(BaseEditView):
    factory = Estimation
    schema = SQLAlchemySchemaNode(Estimation)


class TaskDuplicate(BaseFormView):
    """
    Task duplication view
    """
    form_options = (('formid', 'duplicate_form'),)
    schema = get_duplicate_schema()

    @property
    def title(self):
        if self.context.type_ == 'estimation':
            label = u'le devis'
        elif self.context.type_ == 'invoice':
            label = u'la facture'
        return u"Dupliquer {0} {1}".format(label, self.context.name)

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
        return HTTPFound(
            self.request.route_path(
                '/%ss/{id}' % self.context.type_,
                id=task.id
            )
        )


def add_routes(config):
    """
    Add module's specific routes
    """
    config.add_route(
        'project_estimations',
        '/projects/{id:\d+}/estimations',
        traverse='/projects/{id}',
    )

    config.add_route(
        '/estimations/{id}',
        '/estimations/{id:\d+}',
        traverse='/estimations/{id}'
    )
    for extension in ('html', 'pdf'):
        config.add_route(
            '/estimations/{id}.%s' % extension,
            '/estimations/{id:\d+}.%s' % extension,
            traverse='/estimations/{id}'
        )
    for action in ('addfile', 'delete', 'duplicate', 'admin'):
        config.add_route(
            '/estimations/{id}/%s' % action,
            '/estimations/{id:\d+}/%s' % action,
            traverse='/estimations/{id}'
        )


def includeme(config):
    add_routes(config)

    config.add_view(
        EstimationAdd,
        route_name="project_estimations",
        renderer='base/formpage.mako',
        permission='add_estimation',
    )
    # Estimation related views
    config.add_view(
        AdminEstimation,
        route_name='/estimations/{id}/admin',
        renderer="base/formpage.mako",
        permission="admin",
    )

    delete_msg = u"Le devis {task.name} a bien été supprimé."
    config.add_view(
        make_task_delete_view(delete_msg),
        route_name='/estimations/{id}/delete',
        permission='delete.estimation',
    )

    config.add_view(
        TaskDuplicate,
        route_name="/estimations/{id}/duplicate",
        permission="view.estimation",
        renderer='base/formpage.mako',
    )
    config.add_view(
        get_task_html_view(),
        route_name="/estimations/{id}.html",
        renderer='tasks/view_only.mako',
        permission='view.estimation',
    )

    config.add_view(
        task_pdf_view,
        route_name='/estimations/{id}.pdf',
        permission='view.estimation',
    )

    config.add_view(
        FileUploadView,
        route_name="/estimations/{id}/addfile",
        renderer='base/formpage.mako',
        permission='add.file',
    )

    config.add_view(
        EstimationEditView,
        route_name='/estimations/{id}',
        renderer='tasks/form.mako',
        permission='edit.estimation',
        layout='opa',
    )
