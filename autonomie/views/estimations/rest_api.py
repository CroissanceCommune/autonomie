# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Estimation rest views :

    1- Edit estimation
    2- Return form options for estimation build
"""
import logging
import colander
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.utils.rest import (
    Apiv1Resp,
    add_rest_views,
)
from autonomie.compute.math_utils import (
    convert_to_int,
)
from autonomie.models.task import (
    Estimation,
    TaskStatus,
    PaymentLine,
)
from autonomie.events.tasks import StatusChanged
from autonomie.forms.tasks.estimation import validate_estimation
from autonomie.views import BaseRestView
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


PAYMENT_DISPLAY_OPTIONS = (
    {
        'value': 'NONE',
        'label': u"Les paiments ne sont pas affichés dans le PDF",
    },
    {
        'value': 'SUMMARY',
        'label': u"Le résumé des paiements apparaît dans le PDF",
    },
    {
        'value': 'ALL',
        'label': u"Le détail des paiements apparaît dans le PDF",
    },
    {
        'value': 'ALL_NO_DATE',
        'label': (u"Le détail des paiements, "
                  u"sans les dates, apparaît dans le PDF",)
    },
)


DEPOSIT_OPTIONS = (
    {'value': 0, 'label':  'Aucun', 'default': True},
    {'value': 5, 'label':  '5%'},
    {'value': 10, 'label':  '10 %'},
    {'value': 20, 'label':  '20 %'},
    {'value': 30, 'label':  '30 %'},
    {'value': 40, 'label':  '40 %'},
    {'value': 50, 'label':  '50 %'},
    {'value': 60, 'label':  '60 %'},
    {'value': 70, 'label':  '70 %'},
    {'value': 80, 'label':  '80 %'},
    {'value': 90, 'label':  '90 %'},
    {'value': 100, 'label':  '100 %'},
)


PAYMENT_TIMES_OPTIONS = (
    {'value': -1, 'label':  u'Configuration manuelle'},
    {'value': 1, 'label':  '1 fois', 'default': True},
    {'value': 2, 'label':  '2 fois'},
    {'value': 3, 'label':  '3 fois'},
    {'value': 4, 'label':  '4 fois'},
    {'value': 5, 'label':  '5 fois'},
    {'value': 6, 'label':  '6 fois'},
    {'value': 7, 'label':  '7 fois'},
    {'value': 8, 'label':  '8 fois'},
    {'value': 9, 'label':  '9 fois'},
    {'value': 10, 'label':  '10 fois'},
    {'value': 11, 'label':  '11 fois'},
    {'value': 12, 'label':  '12 fois'},
)


class EstimationRestView(TaskRestView):
    factory = Estimation

    def pre_format(self, appstruct):
        """
        Pre format the posted appstruct to handle Estimation specific mechanisms
        """
        payment_times = appstruct.pop('payment_times')
        if payment_times is not None:
            if convert_to_int(payment_times, 1) == -1:
                appstruct['manualDeliverables'] = 1
            else:
                appstruct['manualDeliverables'] = 0

        return appstruct

    def is_estimation(self):
        return True

    def _more_form_sections(self, sections):
        """
        Add estimation specific form sections to the sections returned to the
        end user

        :param list sections: The sections to return
        :returns: The sections
        """
        sections.extend([
            'discounts',
            'payment_conditions',
            'payments',
        ])
        return sections

    def _more_form_options(self, form_options):
        """
        Add estimation specific form options to the options returned to the end
        user

        :param dict form_options: The options returned to the end user
        :returns: The form_options with new elements
        """
        form_options.update({
            "payment_conditions": json_payment_conditions(self.request),
            'deposits': DEPOSIT_OPTIONS,
            "payment_times": PAYMENT_TIMES_OPTIONS,
            "payment_displays": PAYMENT_DISPLAY_OPTIONS,
        })
        return form_options

    def _get_signed_status_button(self):
        """
        Return a signed_status toggle button
        """
        url = self.request.current_route_path(
            _query={'action': 'signed_status'}
        )
        widget = {
            'widget': 'toggle',
            "options": {
                "url": url,
                "values": [],
                "name": "signed_status",
                "title": u"Validation par le client",
            }
        }
        for action in self.context.signed_state_manager.get_allowed_actions(
            self.request
        ):
            widget['options']['values'].append(action.__json__(self.request))

        return widget

    def _get_other_actions(self):
        """
        Return the description of other available actions :
            signed_status
            duplicate
            ...
        """
        result = []
        result.append(self._get_duplicate_button())
        if self.request.has_permission('set_signed_status.estimation'):
            result.append(self._get_signed_status_button())
        return result

    def _get_duplicate_button(self):
        """
        Return the description for the duplicate link
        """
        url = self.request.route_path(
            "/estimations/{id}/duplicate",
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


class PaymentLineRestView(BaseRestView):
    """
    Rest views used to handle the estimation payment lines

    context is en Estimation (collection level) or PaymentLine (item level)

    Collection views

        GET

            Return all the items belonging to the parent task

        POST

            Add a new item

    Item views

        GET

            Return the Item

        PUT/PATCH

            Edit the item

        DELETE

            Delete the item
    """
    def get_schema(self, submitted):
        """
        Return the schema for PaymentLine add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('task_id',)
        schema = SQLAlchemySchemaNode(PaymentLine, excludes=excludes)
        return schema

    def collection_get(self):
        """
        View returning the task line groups attached to this estimation
        """
        return self.context.payment_lines

    def post_format(self, entry, edit, attributes):
        """
        Associate a newly created element to the parent task
        """
        if not edit:
            entry.task = self.context
        return entry


class EstimationStatusRestView(TaskStatusView):
    def validate(self):
        try:
            validate_estimation(self.context, self.request)
        except colander.Invalid as err:
            logger.exception(
                u"An error occured when validating this Estimation (id:%s)" % (
                    self.request.context.id
                )
            )
            raise err
        return {}


class EstimationSignedStatusRestView(StatusView):
    def check_allowed(self, status, params):
        self.request.context.check_signed_status_allowed(status, self.request)

    def notify(self, status):
        self.request.registry.notify(
            StatusChanged(
                self.request,
                self.context,
                status,
            )
        )

    def status_process(self, status, params):
        return self.context.set_signed_status(
            status,
            self.request,
            **params
        )

    def post_status_process(self, status, params):
        status_record = TaskStatus(
            task_id=self.context.id,
            status_code=status,
            status_person_id=self.request.user.id,
            status_comment="",
        )
        self.request.dbsession.add(status_record)
        StatusView.post_status_process(self, status, params)

    def redirect(self):
        return Apiv1Resp(
            self.request, {'signed_status': self.context.signed_status}
        )


def add_routes(config):
    """
    Add routes to the current configuration

    :param obj config: Pyramid config object
    """
    config.add_route(
        "/api/v1/estimations",
        "/api/v1/estimations",
    )
    config.add_route(
        "/api/v1/estimations/{id}",
        "/api/v1/estimations/{id:\d+}",
        traverse='/estimations/{id}'
    )
    config.add_route(
        "/api/v1/estimations/{id}/task_line_groups",
        "/api/v1/estimations/{id}/task_line_groups",
        traverse='/estimations/{id}'
    )
    config.add_route(
        "/api/v1/estimations/{id}/discount_lines",
        "/api/v1/estimations/{id}/discount_lines",
        traverse='/estimations/{id}'
    )
    config.add_route(
        "/api/v1/estimations/{id}/payment_lines",
        "/api/v1/estimations/{id}/payment_lines",
        traverse='/estimations/{id}'
    )
    config.add_route(
        "/api/v1/estimations/{eid}/task_line_groups/{id}",
        "/api/v1/estimations/{eid}/task_line_groups/{id:\d+}",
        traverse='/task_line_groups/{id}',
    )
    config.add_route(
        "/api/v1/estimations/{eid}/task_line_groups/{id}/task_lines",
        "/api/v1/estimations/{eid}/task_line_groups/{id:\d+}/task_lines",
        traverse='/task_line_groups/{id}',
    )
    config.add_route(
        "/api/v1/estimations/{eid}/task_line_groups/{tid}/task_lines/{id}",
        "/api/v1/estimations/{eid}/task_line_groups/{tid}/task_lines/{id:\d+}",
        traverse='/task_lines/{id}',
    )
    config.add_route(
        "/api/v1/estimations/{eid}/discount_lines/{id}",
        "/api/v1/estimations/{eid}/discount_lines/{id:\d+}",
        traverse='/discount_lines/{id}',
    )
    config.add_route(
        "/api/v1/estimations/{eid}/payment_lines/{id}",
        "/api/v1/estimations/{eid}/payment_lines/{id:\d+}",
        traverse='/payment_lines/{id}',
    )


def add_views(config):
    """
    Add views to the current configuration
    """
    add_rest_views(
        config,
        factory=EstimationRestView,
        route_name='/api/v1/estimations/{id}',
        collection_route_name='/api/v1/estimations',
        edit_rights='edit.estimation',
        view_rights='view.estimation',
        delete_rights='delete.estimation',
    )

    # Form configuration view
    config.add_view(
        EstimationRestView,
        attr='form_config',
        route_name='/api/v1/estimations/{id}',
        renderer='json',
        request_param="form_config",
        permission='edit.estimation',
        xhr=True,
    )

    # Status View
    config.add_view(
        EstimationStatusRestView,
        route_name="/api/v1/estimations/{id}",
        request_param='action=status',
        permission="edit.estimation",
        request_method='POST',
        renderer="json",
    )

    # Task linegroup views
    add_rest_views(
        config,
        route_name="/api/v1/estimations/{eid}/task_line_groups/{id}",
        collection_route_name="/api/v1/estimations/{id}/task_line_groups",
        factory=TaskLineGroupRestView,
        view_rights="view.estimation",
        add_rights="edit.estimation",
        edit_rights='edit.estimation',
        delete_rights='edit.estimation',
    )
    config.add_view(
        TaskLineGroupRestView,
        route_name="/api/v1/estimations/{id}/task_line_groups",
        attr='post_load_groups_from_catalog_view',
        request_param="action=load_from_catalog",
        request_method='POST',
        renderer='json',
        permission='edit.estimation',
        xhr=True,
    )
    # Task line views
    add_rest_views(
        config,
        route_name="/api/v1/estimations/{eid}/"
        "task_line_groups/{tid}/task_lines/{id}",
        collection_route_name="/api/v1/estimations/{eid}/"
        "task_line_groups/{id}/task_lines",
        factory=TaskLineRestView,
        view_rights="view.estimation",
        add_rights="edit.estimation",
        edit_rights='edit.estimation',
        delete_rights='edit.estimation',
    )
    config.add_view(
        TaskLineRestView,
        route_name="/api/v1/estimations/{eid}/task_line_groups/{id}/task_lines",
        attr='post_load_lines_from_catalog_view',
        request_param="action=load_from_catalog",
        request_method='POST',
        renderer='json',
        permission='edit.estimation',
        xhr=True,
    )
    # Discount line views
    add_rest_views(
        config,
        route_name="/api/v1/estimations/{eid}/discount_lines/{id}",
        collection_route_name="/api/v1/estimations/{id}/discount_lines",
        factory=DiscountLineRestView,
        view_rights="view.estimation",
        add_rights="edit.estimation",
        edit_rights='edit.estimation',
        delete_rights='edit.estimation',
    )
    config.add_view(
        DiscountLineRestView,
        route_name="/api/v1/estimations/{id}/discount_lines",
        attr='post_percent_discount_view',
        request_param="action=insert_percent",
        request_method='POST',
        renderer='json',
        permission='edit.estimation',
        xhr=True,
    )
    # Payment lines views
    add_rest_views(
        config,
        route_name="/api/v1/estimations/{eid}/payment_lines/{id}",
        collection_route_name="/api/v1/estimations/{id}/payment_lines",
        factory=PaymentLineRestView,
        view_rights="view.estimation",
        add_rights="edit.estimation",
        edit_rights='edit.estimation',
        delete_rights='edit.estimation',
    )


def includeme(config):
    add_routes(config)
    add_views(config)
