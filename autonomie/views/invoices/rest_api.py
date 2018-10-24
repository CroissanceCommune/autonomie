# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Rest views for invoices and cancelinvoices
"""
import os
import logging
import colander

from autonomie.utils.rest import (
    add_rest_views,
)
from autonomie.models.task import (
    Invoice,
    CancelInvoice,
)
from autonomie.forms.tasks.invoice import (
    validate_invoice,
    validate_cancelinvoice,
    get_add_edit_invoice_schema,
    get_add_edit_cancelinvoice_schema,
)
from autonomie.views.task.rest_api import (
    TaskRestView,
    TaskLineGroupRestView,
    TaskLineRestView,
    DiscountLineRestView,
    TaskFileRequirementRestView,
)
from autonomie.views.task.views import TaskStatusView
from autonomie.views.task.utils import json_payment_conditions


logger = logging.getLogger(__name__)


class InvoiceRestView(TaskRestView):
    factory = Invoice

    def get_schema(self, submitted):
        """
        Return the schema for Invoice add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('status', 'children', 'parent',)
        return get_add_edit_invoice_schema(excludes=excludes)

    def _more_form_sections(self, sections):
        """
        Add invoice specific form sections to the sections returned to the
        end user

        :param dict sections: The sections to return
        :returns: The sections
        """
        sections['discounts'] = {'edit': True}
        sections['payment_conditions'] = {'edit': True}

        if self.request.has_permission('set_treasury.invoice'):
            sections['general']['financial_year'] = True
            sections['tasklines']['product'] = True

        return sections

    def _more_form_options(self, form_options):
        """
        Add invoice specific form options to the options returned to the end
        user

        :param dict form_options: The options returned to the end user
        :returns: The form_options with new elements
        """
        form_options.update({
            "payment_conditions": json_payment_conditions(self.request),
        })
        return form_options

    def _get_other_actions(self):
        """
        Return the description of other available actions :
            signed_status
            duplicate
            ...
        """
        result = []
        result.append(self._get_duplicate_button())
        result.extend(TaskRestView._get_other_actions(self))
        return result

    def _get_duplicate_button(self):
        """
        Return the description for the duplicate link
        """
        url = self.request.route_path(
            "/invoices/{id}/duplicate",
            id=self.context.id,
        )
        return {
            "widget": "anchor",
            "option": {
                "url": url,
                "label": u"Dupliquer",
                "title": u"Créer une nouvelle facture à partir de celle-ci",
                "css": "btn btn-default",
                "icon": "fa fa-copy",
            }
        }


class CancelInvoiceRestView(TaskRestView):
    factory = CancelInvoice

    def get_schema(self, submitted):
        """
        Return the schema for CancelInvoice add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('status', 'children', 'parent',)
        return get_add_edit_cancelinvoice_schema(excludes=excludes)

    def _more_form_sections(self, sections):
        """
        Update form sections to set cancelinvoice specific rights

        :param dict sections: The sections to return
        :returns: The sections
        """
        if self.request.has_permission('set_treasury.invoice'):
            sections['general']['financial_year'] = True
            sections['tasklines']['product'] = True
        return sections


class InvoiceStatusRestView(TaskStatusView):
    def validate(self):
        try:
            validate_invoice(self.context, self.request)
        except colander.Invalid as err:
            logger.exception(
                u"An error occured when validating this Invoice (id:%s)" % (
                    self.request.context.id
                )
            )
            raise err
        return {}


class CancelInvoiceStatusRestView(TaskStatusView):
    def validate(self):
        try:
            validate_cancelinvoice(self.context, self.request)
        except colander.Invalid as err:
            logger.exception(
                u"An error occured when validating this CancelInvoice "
                u"(id:%s)" % (
                    self.request.context.id
                )
            )
            raise err
        return {}

    def post_valid_process(self, status, params):
        TaskStatusView.post_valid_process(self, status, params)
        self.context.invoice.check_resulted(
            user_id=self.request.user.id,
        )


def add_invoice_routes(config):
    """
    Add invoice rest related routes to the current configuration

    :param obj config: Pyramid config object
    """
    COLLECTION_ROUTE = "/api/v1/invoices"
    config.add_route(COLLECTION_ROUTE, COLLECTION_ROUTE)
    ITEM_ROUTE = os.path.join(COLLECTION_ROUTE, "{id}")
    config.add_route(ITEM_ROUTE, ITEM_ROUTE, traverse='/invoices/{id}')
    for collection in (
        'task_line_groups', 'discount_lines', 'file_requirements'
    ):
        route = os.path.join(ITEM_ROUTE, collection)
        config.add_route(route, route, traverse='/invoices/{id}')

    FILE_REQ_ITEM_ROUTE = os.path.join(
        COLLECTION_ROUTE, "{eid}", "file_requirements", "{id}"
    )
    config.add_route(
        FILE_REQ_ITEM_ROUTE,
        FILE_REQ_ITEM_ROUTE,
        traverse="/sale_file_requirements/{id}",
    )

    config.add_route(
        "/api/v1/invoices/{eid}/task_line_groups/{id}",
        "/api/v1/invoices/{eid}/task_line_groups/{id:\d+}",
        traverse='/task_line_groups/{id}',
    )
    config.add_route(
        "/api/v1/invoices/{eid}/task_line_groups/{id}/task_lines",
        "/api/v1/invoices/{eid}/task_line_groups/{id:\d+}/task_lines",
        traverse='/task_line_groups/{id}',
    )
    config.add_route(
        "/api/v1/invoices/{eid}/task_line_groups/{tid}/task_lines/{id}",
        "/api/v1/invoices/{eid}/task_line_groups/{tid}/task_lines/{id:\d+}",
        traverse='/task_lines/{id}',
    )
    config.add_route(
        "/api/v1/invoices/{eid}/discount_lines/{id}",
        "/api/v1/invoices/{eid}/discount_lines/{id:\d+}",
        traverse='/discount_lines/{id}',
    )


def add_cancelinvoice_routes(config):
    """
    Add routes specific to cancelinvoices edition

    :param obj config: Pyramid config object
    """
    COLLECTION_ROUTE = "/api/v1/cancelinvoices"
    config.add_route(COLLECTION_ROUTE, COLLECTION_ROUTE)
    ITEM_ROUTE = os.path.join(COLLECTION_ROUTE, "{id}")
    config.add_route(ITEM_ROUTE, ITEM_ROUTE, traverse='/cancelinvoices/{id}')
    for collection in (
        'task_line_groups', 'discount_lines', 'file_requirements'
    ):
        route = os.path.join(ITEM_ROUTE, collection)
        config.add_route(route, route, traverse='/cancelinvoices/{id}')

    FILE_REQ_ITEM_ROUTE = os.path.join(
        COLLECTION_ROUTE, "{eid}", "file_requirements", "{id}"
    )
    config.add_route(
        FILE_REQ_ITEM_ROUTE,
        FILE_REQ_ITEM_ROUTE,
        traverse="/sale_file_requirements/{id}",
    )

    config.add_route(
        "/api/v1/cancelinvoices/{eid}/task_line_groups/{id}",
        "/api/v1/cancelinvoices/{eid}/task_line_groups/{id:\d+}",
        traverse='/task_line_groups/{id}',
    )
    config.add_route(
        "/api/v1/cancelinvoices/{eid}/task_line_groups/{id}/task_lines",
        "/api/v1/cancelinvoices/{eid}/task_line_groups/{id:\d+}/task_lines",
        traverse='/task_line_groups/{id}',
    )
    config.add_route(
        "/api/v1/cancelinvoices/{eid}/task_line_groups/{tid}/task_lines/{id}",
        "/api/v1/cancelinvoices/{eid}/task_line_groups/"
        "{tid}/task_lines/{id:\d+}",
        traverse='/task_lines/{id}',
    )


def add_invoice_views(config):
    """
    Add Invoice related views to the current configuration
    """
    add_rest_views(
        config,
        factory=InvoiceRestView,
        route_name='/api/v1/invoices/{id}',
        collection_route_name='/api/v1/invoices',
        edit_rights='edit.invoice',
        view_rights='view.invoice',
        delete_rights='delete.invoice',
    )

    # Form configuration view
    config.add_view(
        InvoiceRestView,
        attr='form_config',
        route_name='/api/v1/invoices/{id}',
        renderer='json',
        request_param="form_config",
        permission='edit.invoice',
        xhr=True,
    )

    # Status View
    config.add_view(
        InvoiceStatusRestView,
        route_name="/api/v1/invoices/{id}",
        request_param='action=status',
        permission="edit.invoice",
        request_method='POST',
        renderer="json",
    )

    # Task linegroup views
    add_rest_views(
        config,
        route_name="/api/v1/invoices/{eid}/task_line_groups/{id}",
        collection_route_name="/api/v1/invoices/{id}/task_line_groups",
        factory=TaskLineGroupRestView,
        view_rights="view.invoice",
        add_rights="edit.invoice",
        edit_rights='edit.invoice',
        delete_rights='edit.invoice',
    )
    config.add_view(
        TaskLineGroupRestView,
        route_name="/api/v1/invoices/{id}/task_line_groups",
        attr='post_load_groups_from_catalog_view',
        request_param="action=load_from_catalog",
        request_method='POST',
        renderer='json',
        permission='edit.invoice',
        xhr=True,
    )
    # Task line views
    add_rest_views(
        config,
        route_name="/api/v1/invoices/{eid}/"
        "task_line_groups/{tid}/task_lines/{id}",
        collection_route_name="/api/v1/invoices/{eid}/"
        "task_line_groups/{id}/task_lines",
        factory=TaskLineRestView,
        view_rights="view.invoice",
        add_rights="edit.invoice",
        edit_rights='edit.invoice',
        delete_rights='edit.invoice',
    )
    config.add_view(
        TaskLineRestView,
        route_name="/api/v1/invoices/{eid}/task_line_groups/{id}/task_lines",
        attr='post_load_lines_from_catalog_view',
        request_param="action=load_from_catalog",
        request_method='POST',
        renderer='json',
        permission='edit.invoice',
        xhr=True,
    )
    # Discount line views
    add_rest_views(
        config,
        route_name="/api/v1/invoices/{eid}/discount_lines/{id}",
        collection_route_name="/api/v1/invoices/{id}/discount_lines",
        factory=DiscountLineRestView,
        view_rights="view.invoice",
        add_rights="edit.invoice",
        edit_rights='edit.invoice',
        delete_rights='edit.invoice',
    )
    config.add_view(
        DiscountLineRestView,
        route_name="/api/v1/invoices/{id}/discount_lines",
        attr='post_percent_discount_view',
        request_param="action=insert_percent",
        request_method='POST',
        renderer='json',
        permission='edit.invoice',
        xhr=True,
    )
    # File requirements views
    add_rest_views(
        config,
        route_name="/api/v1/invoices/{eid}/file_requirements/{id}",
        collection_route_name="/api/v1/invoices/{id}/file_requirements",
        factory=TaskFileRequirementRestView,
        collection_view_rights="view.invoice",
        view_rights="view.indicator",
    )
    config.add_view(
        TaskFileRequirementRestView,
        route_name="/api/v1/invoices/{eid}/file_requirements/{id}",
        attr="validation_status",
        permission="valid.indicator",
        request_method="POST",
        request_param="action=validation_status",
        renderer='json',
        xhr=True,
    )


def add_cancelinvoice_views(config):
    """
    Add cancelinvoice related views to the current configuration

    :param obj config: The current Pyramid configuration
    """
    add_rest_views(
        config,
        factory=CancelInvoiceRestView,
        route_name='/api/v1/cancelinvoices/{id}',
        collection_route_name='/api/v1/cancelinvoices',
        edit_rights='edit.cancelinvoice',
        view_rights='view.cancelinvoice',
        delete_rights='delete.cancelinvoice',
    )

    # Form configuration view
    config.add_view(
        CancelInvoiceRestView,
        attr='form_config',
        route_name='/api/v1/cancelinvoices/{id}',
        renderer='json',
        request_param="form_config",
        permission='edit.cancelinvoice',
        xhr=True,
    )

    # Status View
    config.add_view(
        CancelInvoiceStatusRestView,
        route_name="/api/v1/cancelinvoices/{id}",
        request_param='action=status',
        permission="edit.cancelinvoice",
        request_method='POST',
        renderer="json",
    )

    # Task linegroup views
    add_rest_views(
        config,
        route_name="/api/v1/cancelinvoices/{eid}/task_line_groups/{id}",
        collection_route_name="/api/v1/cancelinvoices/{id}/task_line_groups",
        factory=TaskLineGroupRestView,
        view_rights="view.cancelinvoice",
        add_rights="edit.cancelinvoice",
        edit_rights='edit.cancelinvoice',
        delete_rights='edit.cancelinvoice',
    )
    config.add_view(
        TaskLineGroupRestView,
        route_name="/api/v1/cancelinvoices/{id}/task_line_groups",
        attr='post_load_groups_from_catalog_view',
        request_param="action=load_from_catalog",
        request_method='POST',
        renderer='json',
        permission='edit.cancelinvoice',
        xhr=True,
    )
    # Task line views
    add_rest_views(
        config,
        route_name="/api/v1/cancelinvoices/{eid}/"
        "task_line_groups/{tid}/task_lines/{id}",
        collection_route_name="/api/v1/cancelinvoices/{eid}/"
        "task_line_groups/{id}/task_lines",
        factory=TaskLineRestView,
        view_rights="view.cancelinvoice",
        add_rights="edit.cancelinvoice",
        edit_rights='edit.cancelinvoice',
        delete_rights='edit.cancelinvoice',
    )
    config.add_view(
        TaskLineRestView,
        route_name="/api/v1/cancelinvoices/{eid}/task_line_groups/{id}/"
        "task_lines",
        attr='post_load_lines_from_catalog_view',
        request_param="action=load_from_catalog",
        request_method='POST',
        renderer='json',
        permission='edit.cancelinvoice',
        xhr=True,
    )
    # File requirements views
    add_rest_views(
        config,
        route_name="/api/v1/cancelinvoices/{eid}/file_requirements/{id}",
        collection_route_name="/api/v1/cancelinvoices/{id}/file_requirements",
        factory=TaskFileRequirementRestView,
        collection_view_rights="view.cancelinvoice",
        view_rights="view.indicator",
    )
    config.add_view(
        TaskFileRequirementRestView,
        route_name="/api/v1/cancelinvoices/{eid}/file_requirements/{id}",
        attr="validation_status",
        permission="valid.indicator",
        request_method="POST",
        request_param="action=validation_status",
        renderer='json',
        xhr=True,
    )


def includeme(config):
    add_invoice_routes(config)
    add_cancelinvoice_routes(config)
    add_invoice_views(config)
    add_cancelinvoice_views(config)
