# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def filelist_tab_panel(context, request, title, add_url=None):
    """
    render a bootstrap panel used to display a filelist

    :param obj context: The context for which we display the files
    :param str title: The title to give to this tab
    :param str add_url: The url for adding elements
    :returns: dict
    """
    if add_url is None:
        add_url = request.route_path(
            context.type_,
            id=context.id,
            _query={"action": "attach_file"}
        )
    return dict(
        title=title,
        files=context.children,
        add_url=add_url,
    )


def includeme(config):
    config.add_panel(
        filelist_tab_panel,
        'filelist_tab',
        renderer='panels/filelist_tab.mako',
    )
