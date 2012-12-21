# -*- coding: utf-8 -*-
# * File Name : status.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 20-12-2012
# * Last Modified :
#
# * Project :
#
"""
    Base Status modification view
"""
import logging

from pyramid.httpexceptions import HTTPNotFound

from autonomie.views.mail import StatusChanged
from autonomie.exception import Forbidden

log = logging.getLogger(__name__)


class StatusView(object):
    """
        View for task status handling, allows to easily process states
        on documents
        See the call method for the workflow and the params
        passed to the methods
    """
    valid_msg = u"Le statut a bien été modifié"

    def __init__(self, request):
        self.request = request
        self.session = self.request.session

    def get_task_status(self):
        return self.request.context.CAEStatus

    def get_request_params(self):
        return dict(self.request.params.items())

    def pre_status_process(self, task, status, params):
        if hasattr(self, "pre_%s_process" % status):
            func = getattr(self, "pre_%s_process" % status)
            return func(task, status, params)
        return params

    def status_process(self, params, status):
        return self.request.context.set_status(status,
                                        self.request,
                                        self.request.user.id,
                                        **params)

    def post_status_process(self, task, status, params):
        if hasattr(self, "post_%s_process" % status):
            func = getattr(self, "post_%s_process" % status)
            func(task, status, params)

    def merge(self):
        return self.request.dbsession.merge(self.request.context)

    def notify(self):
        task = self.request.context
        self.request.registry.notify(StatusChanged(self.request, task))

    def redirect(self):
        return HTTPNotFound()

    def __call__(self):
        task = self.request.context
        if "submit" in self.request.params:
            try:
                status = self.get_task_status()
                pre_params = self.get_request_params()
                params = self.pre_status_process(task, status, pre_params)
                post_params = self.status_process(params, status)
                self.post_status_process(task, status, post_params)
                task = self.request.dbsession.merge(task)
                self.request.registry.notify(StatusChanged(self.request, task))
                self.session.flash(self.valid_msg, queue="main")
                log.debug(u" + The status has been set to {0}".format(status))
            except Forbidden, e:
                log.exception(u" !! Unauthorized action by : {0}"\
                        .format(self.request.user.login))
                self.session.pop_flash("main")
                self.session.flash(e.message, queue='error')
        return self.redirect()
