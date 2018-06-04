# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.utils.widgets import Link


def _stream_actions(request, item):
    """
    Collect actions available for the given item
    """
    if request.has_permission('edit.file', item):
        yield Link(
            request.route_path('file', id=item.id),
            u"Voir le détail / Modifier",
            icon='pencil',
        )
    if request.has_permission('view.file', item):
        yield Link(
            request.route_path(
                'file', id=item.id, _query=dict(action='download')
            ),
            u"Télécharger",
            icon="download",
        )
    if request.has_permission('delete.file', item):
        yield Link(
            request.route_path(
                'file', id=item.id, _query=dict(action='delete')
            ),
            u"Supprimer",
            confirm=u"Êtes-vous sûr de vouloir définitivement supprimer "
            u"ce fichier ?",
            icon="trash",
        )


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


def filetable_panel(
    context, request, add_url, files, add_perm="add.file", help_message=None
):
    """
    render a table listing files

    :param obj context: The context for which we display the files
    :param str add_url: The url for adding elements
    :param list files: A list of :class:`autonomie.models.files.File`
    :param str add_perm: The permission required to add a file
    :param str help_message: An optionnal help message
    :returns: dict
    """
    return dict(
        files=files,
        add_url=add_url,
        stream_actions=_stream_actions,
        add_perm=add_perm,
        help_message=help_message,
    )


def includeme(config):
    config.add_panel(
        filelist_tab_panel,
        'filelist_tab',
        renderer='panels/filelist_tab.mako',
    )
    config.add_panel(
        filetable_panel,
        'filetable',
        renderer='panels/filetable.mako',
    )
