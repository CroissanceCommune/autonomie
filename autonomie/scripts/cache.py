# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2016 Croissance Commune
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
import logging
import datetime

from sqlalchemy import extract

from autonomie.scripts.utils import (
    command,
    get_value,
)
from autonomie.models.task import (
    Task,
)
from autonomie_base.models.base import DBSESSION as db
from autonomie.models.task.task import cache_amounts


def refresh_cache(arguments, env):
    logger = logging.getLogger(__name__)
    if not arguments['refresh']:
        logger.exception(u"Unknown error")

    logger.debug(u"Refreshing cache")
    session = db()
    index = 0
    types = get_value(arguments, '--type')
    if types is None:
        types = ['invoice', 'estimation', 'cancelinvoice']

    this_year = datetime.date.today().year

    for task in Task.query().filter(
        Task.type_.in_(types)
    ).filter(extract('year', Task.date) == this_year):
        try:
            cache_amounts(None, None, task)
            session.merge(task)
            index += 1
            if index % 200 == 0:
                logger.debug('flushing')
                session.flush()
        except:
            logger.exception(u"Error while caching total : {0}".format(task.id))


def cache_cmd():
    """Test migration of costs

    Usage:
        autonomie-cache <config_uri> refresh [--type=<type>]

    o refresh : Ask for a cache refresh

    Options:
        -h --help         Show this screen
        --type=<type>     Only refresh cache for a given type
        (estimation/invoice/cancelinvoice)
    """
    try:
        return command(refresh_cache, cache_cmd.__doc__)
    finally:
        pass
