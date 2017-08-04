# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Rest views for invoices and cancelinvoices
"""
import logging
import colander

from autonomie.events.tasks import StatusChanged
from autonomie.utils.rest import (
    add_rest_views,
)
from autonomie.models.task import (
    Invoice,
    TaskStatus,
)
from autonomie.forms.tasks.invoice import validate_invoice
from autonomie.views.task.rest_api import (
    TaskRestView,
    TaskLineGroupRestView,
    TaskLineRestView,
    DiscountLineRestView,
)
from autonomie.views.task.utils import json_payment_conditions

from autonomie.views.status import (
    TaskStatusView,
    StatusView,
)

logger = logging.getLogger(__name__)


class InvoiceRestView(TaskRestView):
    factory = Invoice

    def _more_form_sections(self, sections):
        """
        Add invoice specific form sections to the sections returned to the
        end user

        :param list sections: The sections to return
        :returns: The sections
        """
        sections.extend([
            'discounts',
            'payment_conditions',
        ])
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
                "label": u"Dupliquer ce devis",
                "title": u"Créer un nouveau devis à partir de celui-ci",
                "css": "btn btn-default",
                "icon": "fa fa-copy",
            }
        }


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


def add_routes(config):
    """
    Add routes to the current configuration

    :param obj config: Pyramid config object
    """
    config.add_route(
        "/api/v1/invoices",
        "/api/v1/invoices",
    )
    config.add_route(
        "/api/v1/invoices/{id}",
        "/api/v1/invoices/{id:\d+}",
        traverse='/invoices/{id}'
    )
    config.add_route(
        "/api/v1/invoices/{id}/task_line_groups",
        "/api/v1/invoices/{id}/task_line_groups",
        traverse='/invoices/{id}'
    )
    config.add_route(
        "/api/v1/invoices/{id}/discount_lines",
        "/api/v1/invoices/{id}/discount_lines",
        traverse='/invoices/{id}'
    )
    config.add_route(
        "/api/v1/invoices/{id}/payment_lines",
        "/api/v1/invoices/{id}/payment_lines",
        traverse='/invoices/{id}'
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


def add_views(config):
    """
    Add views to the current configuration
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


def includeme(config):
    add_routes(config)
    add_views(config)
