# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from autonomie.events.expense import ExpenseMailStatusChangedWrapper
from autonomie.events.tasks import (
    TaskMailStatusChangedWrapper,
    on_status_changed_alert_related_business,
)
from autonomie.events.mail import send_mail_from_event


logger = logging.getLogger(__name__)


class StatusChanged(object):
    """
        Event fired when a document changes its status
    """
    def __init__(self, request, node, status, comment=None):
        self.request = request
        self.node = node
        self.comment = comment
        self.status = status
        self.node_type = node.type_


def mail_on_status_changed(event):
    """
    Dispatch the event, wrap it with a node specific wrapper and the send email
    from it
    """
    logger.info(u"+ StatusChanged : Mail alert")
    if event.node.type_ == 'expensesheet':
        wrapper = ExpenseMailStatusChangedWrapper(event)
    elif event.node_type in ('invoice', 'estimation', 'cancelinvoice'):
        wrapper = TaskMailStatusChangedWrapper(event)
    send_mail_from_event(wrapper)


def alert_related(event):
    """
    Dispatch the event to alert some related objects
    """
    logger.info("+ StatusChanged : dispatching event")
    if event.node_type == 'invoice':
        on_status_changed_alert_related_business(event)


def includeme(config):
    config.add_subscriber(mail_on_status_changed, StatusChanged)
    config.add_subscriber(alert_related, StatusChanged)
