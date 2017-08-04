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

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.task import (
    Estimation,
    PaymentLine,
)
from autonomie.views import (
    BaseEditView,
)
from autonomie.views.files import FileUploadView
from autonomie.views.task.views import (
    TaskAddView,
    TaskEditView,
    TaskDeleteView,
    TaskHtmlView,
    TaskPdfView,
    TaskDuplicateView,
)

log = logger = logging.getLogger(__name__)


class EstimationAddView(TaskAddView):
    """
    Estimation add view
    context is a project
    """
    title = "Nouveau devis"
    factory = Estimation

    def _more_init_attributes(self, estimation, appstruct):
        """
        Add Estimation's specific attribute while adding this task
        """
        estimation.course = appstruct['course']
        estimation.payment_lines = [PaymentLine(description='Solde', amount=0)]
        return estimation

    def _after_flush(self, estimation):
        """
        Launch after the new estimation has been flushed
        """
        logger.debug(
            "  + Estimation successfully added : {0}".format(estimation.id)
        )


class EstimationEditView(TaskEditView):

    def title(self):
        return u"Modification du devis {task.name}".format(task=self.context)

    def _before(self):
        """
        Ensure some stuff on the current context
        """
        if not self.context.payment_lines:
            self.context.payment_lines = [
                PaymentLine(description='Solde', amount=self.context.ttc)
            ]
            self.request.dbsession.merge(self.context)
            self.request.dbsession.flush()


class EstimationDeleteView(TaskDeleteView):
    msg = u"Le devis {context.name} a bien été supprimé."


class EstimationAdminView(BaseEditView):
    factory = Estimation
    schema = SQLAlchemySchemaNode(Estimation)


class EstimationHtmlView(TaskHtmlView):
    label = u"Devis"


class EstimationPdfView(TaskPdfView):
    pass


class EstimationDuplicateView(TaskDuplicateView):
    label = u"le devis"


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
        EstimationAddView,
        route_name="project_estimations",
        renderer='base/formpage.mako',
        permission='add_estimation',
    )

    config.add_view(
        EstimationEditView,
        route_name='/estimations/{id}',
        renderer='tasks/form.mako',
        permission='view.estimation',
        layout='opa',
    )

    config.add_view(
        EstimationDeleteView,
        route_name='/estimations/{id}/delete',
        permission='delete.estimation',
    )

    config.add_view(
        EstimationAdminView,
        route_name='/estimations/{id}/admin',
        renderer="base/formpage.mako",
        permission="admin",
    )

    config.add_view(
        EstimationDuplicateView,
        route_name="/estimations/{id}/duplicate",
        permission="view.estimation",
        renderer='base/formpage.mako',
    )
    config.add_view(
        EstimationHtmlView,
        route_name="/estimations/{id}.html",
        renderer='tasks/view_only.mako',
        permission='view.estimation',
    )

    config.add_view(
        EstimationPdfView,
        route_name='/estimations/{id}.pdf',
        permission='view.estimation',
    )

    config.add_view(
        FileUploadView,
        route_name="/estimations/{id}/addfile",
        renderer='base/formpage.mako',
        permission='add.file',
    )
