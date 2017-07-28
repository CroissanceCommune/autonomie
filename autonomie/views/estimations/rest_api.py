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
from autonomie.compute.math_utils import percentage
from autonomie.models.task import (
    WorkUnit,
    PaymentConditions,
    TaskMention,
    Estimation,
    TaskStatus,
    TaskLineGroup,
    TaskLine,
    DiscountLine,
    PaymentLine,
)
from autonomie.events.tasks import StatusChanged
from autonomie.forms.tasks.estimation import validate_estimation
from autonomie.models.tva import (
    Tva,
    Product,
)
from autonomie.models.sale_product import (
    SaleProductGroup,
    SaleProduct,
)
from autonomie.views import BaseRestView
from autonomie.views.status import (
    TaskStatusView,
    StatusView,
)

logger = logging.getLogger(__name__)


def json_mentions(request):
    """
    Return the taskmentions available for the task related forms

    :param obj request: The current request object
    :returns: List of TaskMenion in their json repr
    """
    query = TaskMention.query()
    query = query.filter_by(active=True)
    query = query.order_by(TaskMention.order)
    return [item.__json__(request) for item in query]


def json_tvas(request):
    """
    Return the tva objects available for this form

    :param obj request: The current request object
    :returns: List of Tva objects in their json repr
    """
    query = Tva.query()
    return [item.__json__(request) for item in query]


def json_products(request):
    """
    Return the product objects available for this form

    :param obj request: The current request object
    :returns: List of Product objects in their json repr
    """
    query = Product.query()
    return [item.__json__(request) for item in query]


def json_workunits(request):
    """
    Return the workunit objects available for the given form

    :param obj request: The current request object
    :returns: List of Workunits in their json repr
    """
    query = WorkUnit.query()
    return [item.__json__(request) for item in query]


def json_payment_conditions(request):
    """
    Return The PaymentConditions objects available for the given form

    :param obj request: The current request object
    :returns: List of PaymentConditions in their json repr
    """
    query = PaymentConditions.query()
    return [item.__json__(request) for item in query]


class RestEstimation(BaseRestView):

    def get_schema(self, submitted):
        """
        Return the schema for TaskLineGroup add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('status', 'children', 'parent',)
        schema = SQLAlchemySchemaNode(
            Estimation,
            excludes=excludes
        )
        schema = schema.bind(request=self.request)
        return schema

    def form_options(self):
        """
        Return datas used to display an estimation form
        """
        return {
            "sections": [
                'common',
                'tasklines',
                'discounts',
                'payment_conditions',
                'payments'
            ],
            'tva_options': json_tvas(self.request),
            "workunit_options": json_workunits(self.request),
            "product_options": json_products(self.request),
            "mention_options": json_mentions(self.request),
            "payment_conditions": json_payment_conditions(self.request),
            "actions": {
                'status': self._get_status_actions(),
                'others': self._get_other_actions(),
            }
        }

    def _format_status_action(self, action_dict):
        """
        Alter the status description regarding the current context

        Hack to allow better label handling
        """
        if action_dict['status'] == 'draft' and self.context.status == 'wait':
            action_dict['label'] = u"Repasser en brouillon"
            action_dict['title'] = u"Repasser ce document en brouillon"
        return action_dict

    def _get_status_actions(self):
        """
        Returned datas describing available actions on the current item
        """
        actions = []
        url = self.request.current_route_path(_query={'action': 'status'})
        for action in self.context.state_manager.get_allowed_actions(
            self.request
        ):
            json_resp = action.__json__(self.request)
            json_resp['url'] = url
            self._format_status_action(json_resp)
            actions.append(json_resp)
        return actions

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
                "label": u"Dupliquer ce document",
                "title": u"Créer un nouveau document à partir de celui-ci",
                "css": "btn btn-default",
                "icon": "fa fa-copy",
            }
        }

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


class TaskLineGroupRestView(BaseRestView):
    """
    Rest views handling the task line groups
    """
    def get_schema(self, submitted):
        """
        Return the schema for TaskLineGroup add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('task_id',)
        schema = SQLAlchemySchemaNode(TaskLineGroup, excludes=excludes)
        return schema.bind(request=self.request)

    def collection_get(self):
        """
        View returning the task line groups attached to this estimation
        """
        return self.context.line_groups

    def post_format(self, entry, edit):
        """
        Associate a newly created element to the parent task
        """
        if not edit:
            entry.task = self.context
        return entry

    def post_load_groups_from_catalog_view(self):
        """
        View handling product group loading

        expects sale_product_group_ids: [id1, id2] as json POST params
        """
        logger.debug("post_load_from_catalog_view")
        sale_product_group_ids = self.request.json_body.get(
            'sale_product_group_ids', []
        )
        logger.debug("sale_product_ids : %s", sale_product_group_ids)

        groups = []
        for id_ in sale_product_group_ids:
            sale_product_group = SaleProductGroup.get(id_)
            group = TaskLineGroup.from_sale_product_group(sale_product_group)
            self.context.line_groups.append(group)
            groups.append(group)
        self.request.dbsession.merge(self.context)
        return groups


class TaskLineRestView(BaseRestView):
    """
    Rest views used to handle the task lines
    """
    def get_schema(self, submitted):
        """
        Return the schema for TaskLine add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('group_id',)
        schema = SQLAlchemySchemaNode(TaskLine, excludes=excludes)
        return schema.bind(request=self.request)

    def collection_get(self):
        return self.context.lines

    def post_format(self, entry, edit):
        """
        Associate a newly created element to the parent group
        """
        if not edit:
            entry.group = self.context
        return entry

    def post_load_lines_from_catalog_view(self):
        """
        View handling product to line loading

        expects sale_product_ids: [id1, id2] as POST params
        """
        logger.debug("post_load_from_catalog_view")
        sale_product_ids = self.request.json_body.get('sale_product_ids', [])
        logger.debug("sale_product_ids : %s", sale_product_ids)

        lines = []
        for id_ in sale_product_ids:
            sale_product = SaleProduct.get(id_)
            line = TaskLine.from_sale_product(sale_product)
            self.context.lines.append(line)
            lines.append(line)
        self.request.dbsession.merge(self.context)
        return lines


class DiscountLineRestView(BaseRestView):
    """
    Rest views used to handle the task lines
    """
    def get_schema(self, submitted):
        """
        Return the schema for DiscountLine add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('task_id',)
        schema = SQLAlchemySchemaNode(DiscountLine, excludes=excludes)
        return schema.bind(request=self.request)

    def collection_get(self):
        """
        View returning the task line groups attached to this estimation
        """
        return self.context.discounts

    def post_format(self, entry, edit):
        """
        Associate a newly created element to the parent task
        """
        if not edit:
            entry.task = self.context
        return entry

    def post_percent_discount_view(self):
        """
        View handling percent discount configuration

        Generates discounts for each tva used in this document

        current context : Invoice/Estimation/CancelInvoice
        """
        percent = self.request.json_body.get('percentage')
        description = self.request.json_body.get('description')
        lines = []
        if percent is not None and description is not None:
            tva_parts = self.context.tva_ht_parts()
            print(tva_parts)
            for tva, ht in tva_parts.items():
                amount = percentage(ht, percent)
                line = DiscountLine(
                    description=description,
                    amount=amount,
                    tva=tva
                )
                lines.append(line)
                self.context.discounts.append(line)
            self.request.dbsession.merge(self.context)
        return lines


class PaymentLineRestView(BaseRestView):
    """
    Rest views used to handle the task lines
    """
    def get_schema(self, submitted):
        """
        Return the schema for PaymentLine add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('task_id',)
        schema = SQLAlchemySchemaNode(PaymentLine, excludes=excludes)
        return schema.bind(request=self.request)

    def post_format(self, entry, edit):
        """
        Associate a newly created element to the parent task
        """
        if not edit:
            entry.task = self.context
        return entry


class EstimationStatusView(TaskStatusView):
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


class EstimationSignedStatusView(StatusView):
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
    config.add_view(
        RestEstimation,
        attr='get',
        route_name='/api/v1/estimations/{id}',
        renderer='json',
        permission='view.estimation',
        xhr=True,
    )
    config.add_view(
        RestEstimation,
        attr='put',
        request_method='PUT',
        route_name='/api/v1/estimations/{id}',
        renderer='json',
        permission='edit.estimation',
        xhr=True,
    )
    config.add_view(
        RestEstimation,
        attr='put',
        request_method='PATCH',
        route_name='/api/v1/estimations/{id}',
        renderer='json',
        permission='edit.estimation',
        xhr=True,
    )
    config.add_view(
        RestEstimation,
        attr='form_options',
        route_name='/api/v1/estimations/{id}',
        renderer='json',
        request_param="form_options",
        permission='edit.estimation',
        xhr=True,
    )
    config.add_view(
        EstimationStatusView,
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


def includeme(config):
    add_routes(config)
    add_views(config)
