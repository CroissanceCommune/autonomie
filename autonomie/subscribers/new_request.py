# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Log all incoming requests
"""
import logging

from pyramid.events import NewRequest

from autonomie.utils.widgets import ActionMenu
from autonomie.i18n import translate

logger = logging.getLogger(__name__)


def log_request(event):
    """
        Log each request
    """
    logger.info(u"####################  NEW REQUEST COMING #################")
    logger.info(u"  + The request object")
    logger.info(event.request)
    logger.info(u"  + The session object")
    logger.info(event.request.session)
    logger.info(u"################### END REQUEST METADATA LOG #############")


def add_request_attributes(event):
    """
        Add usefull tools to the request object
        that may be used inside the views
    """
    request = event.request
    request.translate = translate
    request.actionmenu = ActionMenu()
    request.popups = {}


def includeme(config):
    config.add_subscriber(log_request, NewRequest)
    config.add_subscriber(add_request_attributes, NewRequest)
