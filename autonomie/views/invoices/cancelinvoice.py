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
    View for assets
"""
import logging

from pyramid.httpexceptions import HTTPFound
from colanderalchemy import SQLAlchemySchemaNode

from autonomie_base.utils.date import format_date

from autonomie.utils.widgets import ViewLink
from autonomie.models.task import (
    CancelInvoice,
)
from autonomie.resources import (
    task_html_pdf_css,
)
from autonomie.views import (
    BaseEditView,
    add_panel_page_view,
)
from autonomie.views.files import FileUploadView
from autonomie.views.task.views import (
    TaskEditView,
    TaskDeleteView,
    TaskHtmlView,
    TaskPdfView,
    TaskSetMetadatasView,
    TaskSetProductsView,
    TaskSetDraftView,
)


log = logging.getLogger(__name__)


class CancelInvoiceEditView(TaskEditView):
    def title(self):
        customer = self.context.customer
        customer_label = customer.label
        if customer.code is not None:
            customer_label += u" ({0})".format(customer.code)

        return (
            u"Modification de l'avoir {task.name} avec le client "
            u"{customer}".format(
                task=self.context,
                customer=customer_label,
            )
        )


class CancelInvoiceDeleteView(TaskDeleteView):
    pass


class CancelInvoiceHtmlView(TaskHtmlView):
    label = u"Avoir"


class CancelInvoicePdfView(TaskPdfView):
    pass


class CancelInvoiceAdminView(BaseEditView):
    factory = CancelInvoice
    schema = SQLAlchemySchemaNode(
        CancelInvoice,
        title=u"Formulaire d'édition forcée de devis/factures/avoirs",
        help_msg=u"Les montants sont *10^5   10 000==1€",
    )


class CancelInvoiceSetTreasuryiew(BaseEditView):
    """
    View used to set treasury related informations

    context

        An invoice

    perms

        set_treasury.invoice
    """
    factory = CancelInvoice
    schema = SQLAlchemySchemaNode(
        CancelInvoice,
        includes=('prefix', 'financial_year',),
        title=u"Modifier l'année fiscale de référence et le préfixe "
        u"du numéro de facture",
    )

    def redirect(self):
        return HTTPFound(
            self.request.route_path(
                "/invoices/{id}.html",
                id=self.context.id,
                _anchor="treasury"
            )
        )

    def before(self, form):
        BaseEditView.before(self, form)
        self.request.actionmenu.add(
            ViewLink(
                label=u"Revenir à la facture",
                path="/invoices/{id}.html",
                id=self.context.id,
                _anchor="treasury",
            )
        )

    @property
    def title(self):
        return u"Facture numéro {0} en date du {1}".format(
            self.context.official_number,
            format_date(self.context.date),
        )


class CancelInvoiceSetMetadatasView(TaskSetMetadatasView):
    """
    View used for editing invoice metadatas
    """

    @property
    def title(self):
        return u"Modification de l'avoir {task.name}".format(
            task=self.context
        )


class CancelInvoiceSetProductsView(TaskSetProductsView):
    @property
    def title(self):
        return (
            u"Configuration des codes produits pour l'avoir {0.name}".format(
                self.context
            )
        )


def add_routes(config):
    """
    Add module related routes
    """
    config.add_route(
        '/cancelinvoices/{id}',
        '/cancelinvoices/{id:\d+}',
        traverse='/cancelinvoices/{id}'
    )
    for extension in ('html', 'pdf', 'preview'):
        config.add_route(
            '/cancelinvoices/{id}.%s' % extension,
            '/cancelinvoices/{id:\d+}.%s' % extension,
            traverse='/cancelinvoices/{id}'
        )
    for action in (
        'addfile',
        'delete',
        'admin',
        'set_treasury',
        'set_products',
        'set_metadatas',
        'set_draft',
    ):
        config.add_route(
            '/cancelinvoices/{id}/%s' % action,
            '/cancelinvoices/{id:\d+}/%s' % action,
            traverse='/cancelinvoices/{id}'
        )


def includeme(config):
    add_routes(config)

    # Here it's only view.cancelinvoice to allow redirection to the html view
    config.add_view(
        CancelInvoiceEditView,
        route_name='/cancelinvoices/{id}',
        renderer="tasks/form.mako",
        permission='view.cancelinvoice',
    )

    config.add_view(
        CancelInvoiceAdminView,
        route_name='/cancelinvoices/{id}/admin',
        renderer="base/formpage.mako",
        request_param="token=admin",
        permission="admin",
    )

    config.add_view(
        CancelInvoiceDeleteView,
        route_name='/cancelinvoices/{id}/delete',
        permission='delete.cancelinvoice',
    )

    config.add_view(
        CancelInvoicePdfView,
        route_name='/cancelinvoices/{id}.pdf',
        permission='view.cancelinvoice',
    )

    config.add_view(
        CancelInvoiceHtmlView,
        route_name='/cancelinvoices/{id}.html',
        renderer='tasks/cancelinvoice_view_only.mako',
        permission='view.cancelinvoice',
    )

    add_panel_page_view(
        config,
        'cancelinvoice_html',
        js_resources=(task_html_pdf_css,),
        route_name='/cancelinvoices/{id}.preview',
        permission="view.cancelinvoice",
    )

    config.add_view(
        FileUploadView,
        route_name='/cancelinvoices/{id}/addfile',
        renderer='base/formpage.mako',
        permission='edit.cancelinvoice',
    )

    config.add_view(
        CancelInvoiceSetTreasuryiew,
        route_name="/cancelinvoices/{id}/set_treasury",
        renderer='base/formpage.mako',
        permission="set_treasury.cancelinvoice",
    )
    config.add_view(
        CancelInvoiceSetMetadatasView,
        route_name="/cancelinvoices/{id}/set_metadatas",
        renderer='tasks/add.mako',
        permission="view.cancelinvoice",
    )
    config.add_view(
        TaskSetDraftView,
        route_name="/cancelinvoices/{id}/set_draft",
        permission="draft.cancelinvoice",
    )
    config.add_view(
        CancelInvoiceSetProductsView,
        route_name="/cancelinvoices/{id}/set_products",
        permission="set_treasury.cancelinvoice",
        renderer='base/formpage.mako',
    )
