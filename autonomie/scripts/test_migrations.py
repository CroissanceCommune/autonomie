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
from autonomie.scripts.utils import (
    command,
    get_value,
)
from autonomie.models.task import (
    Task,
)
from autonomie_base.models.base import DBSESSION as db
from autonomie.models.task.task import cache_amounts


def query_tasks():
    tasks = db().query(Task.id, Task.ht, Task.tva, Task.ttc)
    return tasks


def gen_csv(filename):
    tasks = query_tasks()

    res = "\n".join(
        str(task.id) + "," + str(task.ht) + "," + str(task.tva) + "," + str(task.ttc)
        for task in tasks)

    with open(filename, 'w+') as f_buf:
        f_buf.write(res)


def export_task_totals(arguments, env):
    action = get_value(arguments, 'a')

    if action == "check":
        check_totals(arguments, env)
        return

    print(arguments)
    logger = logging.getLogger(__name__)
    filename = get_value(arguments, 'f')
    if filename:
        print("Generating a csv filename %s" % filename)
        gen_csv(filename)

    if action == 'cache':
        print(u"Caching amounts")
        session = db()
        index = 0
        for task in Task.query().filter(
            Task.type_.in_(['invoice', 'estimation', 'cancelinvoice'])
        ):
            try:
                cache_amounts(None, None, task)
                session.merge(task)
                index += 1
                if index % 50 == 0:
                    print('flushing')
                    session.flush()
            except:
                logger.exception(
                    u"Erreur avec un cache_amount : %s" % task.id
                )


def check_totals(arguments, env):
    print(u"Checking totals")
    f = get_value(arguments, 'f')

    lines = file(f, 'r').read().splitlines()
    query = query_tasks()
    for line in lines:
        id, ht, tva, ttc = line.split(',')
        if 'None' in (id, ht, tva, ttc):
            continue

        vals = int(id), int(ht), int(tva), int(ttc)
        task = query.filter(Task.id == vals[0]).one()
        if not task == vals:
            print(u"Unconform data migration detected")
            print(u"  + Task.id : %s" % task[0])
            print(u"    + Found %s" % str(task))
            print(u"    + Used to be %s" % str(vals))




def export_task_totals_cmd():
    """Test migration of costs

    Usage:
        test-migration <config_uri> test [--f=<filename>] [--a=<action>]

    Options:
        -h --help     Show this screen
    """
    try:
        return command(export_task_totals, export_task_totals_cmd.__doc__)
    finally:
        pass
