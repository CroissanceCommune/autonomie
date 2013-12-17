# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
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
#
"""

    Panels used for task rendering

"""

def task_panel(context, request, task, bulk=False):
    """
        Task panel
    """
    tvas = task.get_tvas()
    # Check if we've got multiple positive tvas in our task
    multiple_tvas = len([val for val in tvas if val > 0]) > 1
    return dict(
            task=task,
            project=task.project,
            company=task.project.company,
            multiple_tvas=multiple_tvas,
            tvas=tvas,
            config=request.config,
            bulk=bulk,
            )


def includeme(config):
    """
        Pyramid's inclusion mechanism
    """
    for document_type in ('estimation', 'invoice', 'cancelinvoice'):
        panel_name = "{0}_html".format(document_type)
        template = "panels/{0}.mako".format(document_type)
        config.add_panel(task_panel, panel_name, renderer=template)
