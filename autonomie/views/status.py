# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Status change related views

Common to :
    Estimation
    Invoice
    CancelInvoice
    ExpenseSheet
"""
import logging
import colander
import datetime

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)

from autonomie.exception import (
    Forbidden,
    BadRequest,
)
from autonomie.events.tasks import StatusChanged
from autonomie.utils.rest import RestError
from autonomie.views import BaseView

logger = logging.getLogger(__name__)


class StatusView(BaseView):
    """
    View for status handling

    See the call method for the workflow and the params
    passed to the methods
    """
    valid_msg = u"Le statut a bien été modifié"

    def redirect(self):
        """
        Redirect function to be used after status processing
        """
        return HTTPNotFound()

    def _get_status(self, params):
        """
        Get the status that has been asked for
        """
        return params['submit']

    def _get_request_params(self):
        """
        return the request params as a dict (a non locked one)
        """
        return dict(self.request.params.items())

    def check_allowed(self, status, params):
        """
        Check that the status change is allowed

        :param str status: The new status that should be affected
        :param dict params: Params currently passed
        :rtype: bool
        :raises: Forbidden exception if the action isn't allowed
        """
        return True

    def pre_status_process(self, status, params):
        """
        Launch pre process functions
        """
        self.check_allowed(status, params)

        if hasattr(self, "pre_%s_process" % status):
            func = getattr(self, "pre_%s_process" % status)
            return func(status, params)
        return params

    def status_process(self, status, params):
        """
        Definitively Set the status of the element

        :param str status: The new status that should be affected
        :param dict params: The params that were transmitted by the pre_process
        function
        """
        return self.context.set_status(
            status,
            self.request,
            **params
        )

    def post_status_process(self, status, params):
        """
        Launch post status process functions

        :param str status: The new status that should be affected
        :param dict params: The params that were transmitted by the associated
        State's callback
        """
        if hasattr(self, "post_%s_process" % status):
            func = getattr(self, "post_%s_process" % status)
            func(status, params)

    def set_status(self, status):
        """
        Set the new status to the given item
        handle pre_status and post_status processing

        :param str status: The new status that should be affected
        """
        pre_params = self.request.params
        params = self.pre_status_process(status, pre_params)
        post_params = self.status_process(status, params)
        self.post_status_process(status, post_params)
        return True

    def notify(self, status):
        """
        Notify the change to the registry

        :param str status: The new status that was affected
        """
        raise NotImplemented()

    def __call__(self):
        """
            Main entry for this view object
        """
        logger.debug("# Entering the status view")
        if self.request.is_xhr:
            params = self.request.json_body
        else:
            params = self.request.POST

        if "submit" in params:
            try:
                status = self._get_status(params)
                logger.debug(u"New status : %s " % status)
                self.set_status(status)
                self.context = self.request.dbsession.merge(self.context)
                self.notify(status)
                self.session.flash(self.valid_msg)
                logger.debug(u" + The status has been set to {0}".format(
                    status))

            except Forbidden, e:
                logger.exception(u" !! Unauthorized action by : {0}".format(
                    self.request.user.login
                ))
                if self.request.is_xhr:
                    raise RestError(e.message, code=403)
                else:
                    self.session.pop_flash("")
                    self.session.flash(e.message, queue='error')

            except (colander.Invalid, BadRequest), e:
                if self.request.is_xhr:
                    raise RestError(e.messages())
                else:
                    for message in e.messages():
                        self.session.flash(message, 'error')

            return self.redirect()

        if self.request.is_xhr:
            raise RestError(
                [
                    u'Il manque des arguments pour changer le statut '
                    u'du document'
                ])
        else:
            self.session.flash(
                u"Il manque des arguments pour changer le statut du document",
                "error"
            )
            return self.redirect()


class TaskStatusView(StatusView):
    """
    View handling base status for tasks (estimation/invoice/cancelinvoice)

    Status related views should implement the validate function to ensure data
    integrity
    """

    def validate(self):
        raise NotImplemented()

    def check_allowed(self, status, params):
        self.request.context.check_status_allowed(status, self.request)

    def redirect(self):
        project_id = self.request.context.project.id
        return HTTPFound(self.request.route_path('project', id=project_id))

    def pre_status_process(self, status, params):
        if 'comment' in params:
            self.context.status_comment = params.get('comment')

        if 'change_date' in params and params['change_date'] in ('1', 1):
            logger.debug("Forcing the document's date !!!")
            self.context.date = datetime.date.today()

        return StatusView.pre_status_process(self, status, params)

    def pre_wait_process(self, status, params):
        """
        Launched before the wait status is set
        """
        self.validate()
        return {}

    def pre_valid_process(self, status, params):
        """
        Launched before the wait status is set
        """
        self.validate()
        return {}

    def notify(self, status):
        """
        Notify the change to the registry
        """
        self.request.registry.notify(
            StatusChanged(
                self.request,
                self.context,
                status,
            )
        )
