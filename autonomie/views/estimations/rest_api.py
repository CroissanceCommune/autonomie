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

from autonomie.utils.rest import Apiv1Resp
from autonomie.models.task import (
    WorkUnit,
    PaymentConditions,
    TaskMention,
    Estimation,
)
from autonomie.events.tasks import StatusChanged
from autonomie.forms.tasks.estimation import validate_estimation
from autonomie.models.tva import Tva
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

    def get_schema(self, submitted, edit):
        if edit:
            excludes = ()
            includes = submitted.keys()
        else:
            excludes = ('status', 'children', 'parent',)
            includes = ()

        logger.debug("Building a schema with :")
        logger.debug("includes :")
        logger.debug(includes)
        logger.debug("excludes : %s")
        logger.debug(excludes)

        schema = SQLAlchemySchemaNode(
            Estimation,
            includes=includes,
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
                'common', 'prestations', 'payment_conditions', 'payments'
            ],
            'tva_options': json_tvas(self.request),
            "workunit_options": json_workunits(self.request),
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


def includeme(config):
    add_routes(config)
    add_views(config)
