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
        if context.type_ in ('estimation', 'invoice', 'cancelinvoice'):
            route_name = "/%ss/{id}/addfile" % context.type_
            query = {}
        else:
            route_name = context.type_
            query = {'action': 'attach_file'}
        add_url = request.route_path(
            route_name,
            id=context.id,
            _query=query,
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
