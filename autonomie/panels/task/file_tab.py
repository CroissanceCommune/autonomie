# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

from autonomie.panels.files import stream_actions


def task_file_tab_panel(context, request, title, add_url=None):
    """
    render a bootstrap panel used to display a files attached to a task

    :param obj context: The context for which we display the files
    :param str title: The title to give to this tab
    :param str add_url: The url for adding elements
    :returns: dict
    """
    if add_url is None:
        route_name = "/%ss/{id}/addfile" % context.type_
        add_url = request.route_path(
            route_name,
            id=context.id,
        )

    return dict(
        title=title,
        add_url=add_url,
        files=context.files,
        stream_actions=stream_actions,
    )


def includeme(config):
    config.add_panel(
        task_file_tab_panel,
        'task_file_tab',
        renderer='panels/task/file_tab.mako',
    )
