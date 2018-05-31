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
from autonomie.forms.tasks.estimation import InvoiceAttachSchema
from autonomie.models.task import (
    Estimation,
    PaymentLine,
    Invoice,
)
from autonomie.utils.widgets import ViewLink
from autonomie.resources import (
    estimation_signed_status_js,
    task_html_pdf_css,
)
from autonomie.forms.tasks.estimation import get_add_edit_estimation_schema
from autonomie.views import (
    BaseEditView,
    BaseFormView,
    submit_btn,
    cancel_btn,
    add_panel_page_view,
)
from autonomie.views.files import FileUploadView
from autonomie.views.project.routes import PROJECT_ITEM_ESTIMATION_ROUTE
from autonomie.views.task.views import (
    TaskAddView,
    TaskEditView,
    TaskDeleteView,
    TaskHtmlView,
    TaskPdfView,
    TaskDuplicateView,
    TaskSetMetadatasView,
    TaskSetDraftView,
    TaskMoveToPhaseView,
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
        customer = self.context.customer
        customer_label = customer.label
        if customer.code is not None:
            customer_label += u" ({0})".format(customer.code)
        return (
            u"Modification du devis {task.name} avec le client "
            u"{customer}".format(
                task=self.context,
                customer=customer_label,
            )
        )

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
    schema = get_add_edit_estimation_schema(isadmin=True)


class EstimationHtmlView(TaskHtmlView):
    label = u"Devis"

    def actions(self):
        estimation_signed_status_js.need()
        actions = []
        for action in self.context.signed_state_manager.get_allowed_actions(
            self.request
        ):
            actions.append(action)
        return actions


class EstimationPdfView(TaskPdfView):
    pass


class EstimationDuplicateView(TaskDuplicateView):
    label = u"le devis"


class EstimationSetMetadatasView(TaskSetMetadatasView):
    @property
    def title(self):
        return u"Modification du devis {task.name}".format(
            task=self.context
        )


class EstimationAttachInvoiceView(BaseFormView):
    schema = InvoiceAttachSchema()
    buttons = (submit_btn, cancel_btn,)

    def before(self, form):
        self.request.actionmenu.add(
            ViewLink(
                label=u"Revenir au devis",
                path="/estimations/{id}.html",
                id=self.context.id,
            )
        )
        form.set_appstruct(
            {
                'invoice_ids': [
                    str(invoice.id) for invoice in self.context.invoices
                ]
            }
        )

    def redirect(self):
        return HTTPFound(
            self.request.route_path(
                '/estimations/{id}.html',
                id=self.context.id,
            )
        )

    def submit_success(self, appstruct):
        invoice_ids = appstruct.get('invoice_ids')
        for invoice_id in invoice_ids:
            invoice = Invoice.get(invoice_id)
            invoice.estimation_id = self.context.id
            self.request.dbsession.merge(invoice)

        self.context.geninv = True
        self.request.dbsession.merge(self.context)
        return self.redirect()

    def cancel_success(self, appstruct):
        return self.redirect()

    cancel_failure = cancel_success


def estimation_geninv_view(context, request):
    """
    Invoice generation view : used in shorthanded workflow

    :param obj context: The current context (estimation)
    """
    business = context.gen_business()
    request.dbsession.add(business)
    request.dbsession.flush()

    invoices = context.gen_invoices(request.user)
    for invoice in invoices:
        invoice.business = business
        request.dbsession.add(invoice)

    context.geninv = True

    if len(invoices) > 1:
        msg = u"{0} factures ont été générées".format(len(invoices))
    else:
        msg = u"Une facture a été générée"
    request.session.flash(msg)
    request.dbsession.flush()
    return HTTPFound(
        request.route_path('/invoices/{id}', id=invoices[0].id)
    )


def estimation_genbusiness_view(context, request):
    """
    Business generation view : used in long handed workflows

    :param obj context: The current estimation
    """
    business = context.gen_business()
    request.dbsession.add(business)
    request.dbsession.flush()
    return HTTPFound(request.route_path("/businesses/{id}", id=business.id))


def add_routes(config):
    """
    Add module's specific routes
    """
    config.add_route(
        '/estimations/{id}',
        '/estimations/{id:\d+}',
        traverse='/estimations/{id}'
    )
    for extension in ('html', 'pdf', 'preview'):
        config.add_route(
            '/estimations/{id}.%s' % extension,
            '/estimations/{id:\d+}.%s' % extension,
            traverse='/estimations/{id}'
        )
    for action in (
        'addfile',
        'delete',
        'duplicate',
        'admin',
        'geninv',
        'genbusiness',
        'set_metadatas',
        'attach_invoices',
        'set_draft',
        'move',
    ):
        config.add_route(
            '/estimations/{id}/%s' % action,
            '/estimations/{id:\d+}/%s' % action,
            traverse='/estimations/{id}'
        )


def includeme(config):
    add_routes(config)

    config.add_view(
        EstimationAddView,
        route_name=PROJECT_ITEM_ESTIMATION_ROUTE,
        renderer='tasks/add.mako',
        permission='add_estimation',
        request_param="action=add",
        layout="default"
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
        permission="duplicate.estimation",
        renderer='tasks/add.mako',
    )
    config.add_view(
        EstimationHtmlView,
        route_name="/estimations/{id}.html",
        renderer='tasks/estimation_view_only.mako',
        permission='view.estimation',
    )
    add_panel_page_view(
        config,
        'estimation_html',
        js_resources=(task_html_pdf_css,),
        route_name="/estimations/{id}.preview",
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

    config.add_view(
        estimation_geninv_view,
        route_name="/estimations/{id}/geninv",
        permission='geninv.estimation',
    )

    config.add_view(
        estimation_genbusiness_view,
        route_name="/estimations/{id}/genbusiness",
        permission='genbusiness.estimation',
    )

    config.add_view(
        EstimationSetMetadatasView,
        route_name="/estimations/{id}/set_metadatas",
        permission='view.estimation',
        renderer='tasks/add.mako',
    )
    config.add_view(
        TaskMoveToPhaseView,
        route_name="/estimations/{id}/move",
        permission='view.estimation',
    )
    config.add_view(
        TaskSetDraftView,
        route_name="/estimations/{id}/set_draft",
        permission="draft.estimation",
    )

    config.add_view(
        EstimationAttachInvoiceView,
        route_name="/estimations/{id}/attach_invoices",
        permission='view.estimation',
        renderer="/base/formpage.mako",
    )
