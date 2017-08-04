# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.compute.math_utils import (
    percentage,
)
from autonomie.models.task import (
    TaskLine,
    TaskLineGroup,
    DiscountLine,
)
from autonomie.models.sale_product import (
    SaleProductGroup,
    SaleProduct,
)
from autonomie.views import BaseRestView
from autonomie.views.task.utils import (
    json_tvas,
    json_workunits,
    json_products,
    json_mentions,
)


logger = logging.getLogger(__name__)


class TaskRestView(BaseRestView):
    """
    Base class for task rest api

    The views contexts are instances of self.factory

    Collection Views

        POST

            Create a new task

    Item views

        GET

            Returns the context in json format

        GET?form_config

            returns the form configuration

        PUT / PATCH

            Edit the current element

        DELETE

            Delete the current element
    """
    factory = None

    def get_schema(self, submitted):
        """
        Return the schema for TaskLineGroup add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        if self.factory is None:
            raise Exception("Child class should provide a factory attribute")
        excludes = ('status', 'children', 'parent',)
        schema = SQLAlchemySchemaNode(
            self.factory,
            excludes=excludes
        )
        return schema

    def form_config(self):
        """
        Form display options

        :returns: The sections that the end user can edit, the options available
        for the different select boxes
        """
        result = {
            'is_estimation': self.is_estimation(),
            "actions": {
                'status': self._get_status_actions(),
                'others': self._get_other_actions(),
            }
        }
        result = self._add_form_options(result)
        result = self._add_form_sections(result)
        return result

    def is_estimation(self):
        """
        Return True if this is an estimation
        """
        return False

    def _add_form_options(self, form_config):
        """
        Add the main options provided to the end user UI

        :param dict form_config: The current form configuration
        :returns: The dict with a new 'options' key
        """
        options = {
            'tvas': json_tvas(self.request),
            "workunits": json_workunits(self.request),
            "products": json_products(self.request),
            "mentions": json_mentions(self.request),
        }
        if hasattr(self, '_more_form_options'):
            options = self._more_form_options(options)

        form_config['options'] = options
        return form_config

    def _add_form_sections(self, form_config):
        """
        Return the sections that should be displayed to the end user

        :param dict form_config: The current form_config
        """
        sections = [
            'general',
            'common',
            'tasklines',
            'notes',
        ]
        if hasattr(self, '_more_form_sections'):
            sections = self._more_form_sections(sections)

        form_config['sections'] = sections
        return form_config

    def _get_status_actions(self):
        """
        Returned datas describing available actions on the current item
        :returns: List of actions
        :rtype: list of dict
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

    def _format_status_action(self, action_dict):
        """
        Alter the status description regarding the current context

        Hack to allow better label handling
        """
        if action_dict['status'] == 'draft' and self.context.status == 'wait':
            action_dict['label'] = u"Repasser en brouillon"
            action_dict['title'] = u"Repasser ce document en brouillon"
            action_dict['icon'] = 'remove'
        return action_dict

    def _get_other_actions(self):
        """
        Return the description of other available actions :
            signed_status
            duplicate
            ...
        """
        return []


class TaskLineGroupRestView(BaseRestView):
    """
    Rest views handling the task line groups

    Collection views : Context Task

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
        Return the schema for TaskLineGroup add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('task_id',)
        schema = SQLAlchemySchemaNode(TaskLineGroup, excludes=excludes)
        return schema

    def collection_get(self):
        """
        View returning the task line groups attached to this estimation
        """
        return self.context.line_groups

    def post_format(self, entry, edit, attributes):
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

    Collection views : Context Task

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
        Return the schema for TaskLine add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('group_id',)
        schema = SQLAlchemySchemaNode(TaskLine, excludes=excludes)
        return schema

    def collection_get(self):
        return self.context.lines

    def post_format(self, entry, edit, attributes):
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


    Collection views : Context Task

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
        Return the schema for DiscountLine add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        excludes = ('task_id',)
        schema = SQLAlchemySchemaNode(DiscountLine, excludes=excludes)
        return schema

    def collection_get(self):
        """
        View returning the task line groups attached to this estimation
        """
        return self.context.discounts

    def post_format(self, entry, edit, attributes):
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
