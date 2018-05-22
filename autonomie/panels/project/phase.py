# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.utils.widgets import Link

from autonomie.views.project.routes import (
    PROJECT_ITEM_INVOICE_ROUTE,
    PROJECT_ITEM_ESTIMATION_ROUTE,
)


def _stream_actions(request, item):
    """
    Return actions that will be rendered in a dropdown
    """
    yield Link(
        request.route_path("/%ss/{id}" % item.type_, id=item.id),
        u"Voir / Modifier",
        icon="fa fa-pencil"
    )
    yield Link(
        request.route_path("/%ss/{id}.pdf" % item.type_, id=item.id),
        u"PDF",
        title=u"Enregistrer le PDF",
        icon="fa fa-file-pdf-o"
    )
    if request.has_permission('duplicate.%s' % item.type_, item):
        yield Link(
            request.route_path("/%ss/{id}/duplicate" % item.type_, id=item.id),
            u"Dupliquer",
            icon="fa fa-copy"
        )

    if request.has_permission('delete.%s' % item.type_, item):
        yield Link(
            request.route_path("/%ss/{id}/delete" % item.type_, id=item.id),
            u"Supprimer",
            confirm=u"Êtes-vous sûr de vouloir supprimer ce document ?",
            icon="fa fa-trash"
        )

    for phase in request.context.phases:
        if phase.id != item.phase_id:
            yield Link(
                request.route_path(
                    "/%ss/{id}/move" % item.type_, id=item.id,
                    _query={'phase': phase.id}
                ),
                u"Déplacer vers le dossier %s" % phase.name,
                icon="fa fa-arrows-alt",
            )


def phase_estimations_panel(context, request, phase, estimations):
    """
    Phase estimation list panel
    """
    _query = {'action': 'add'}
    if phase is not None:
        _query['phase'] = phase.id

    add_url = request.route_path(
        PROJECT_ITEM_ESTIMATION_ROUTE,
        id=context.id,
        _query=_query
    )

    return dict(
        add_url=add_url,
        estimations=estimations,
        stream_actions=_stream_actions,
    )


def phase_invoices_panel(context, request, phase, invoices):
    """
    Phase invoice list panel
    """
    _query = {'action': 'add'}
    if phase is not None:
        _query['phase'] = phase.id

    add_url = request.route_path(
        PROJECT_ITEM_INVOICE_ROUTE,
        id=context.id,
        _query=_query
    )

    return dict(
        add_url=add_url,
        invoices=invoices,
        stream_actions=_stream_actions,
    )


def includeme(config):
    config.add_panel(
        phase_estimations_panel,
        'phase_estimations',
        renderer="autonomie:templates/panels/project/phase_estimations.mako"
    )
    config.add_panel(
        phase_invoices_panel,
        'phase_invoices',
        renderer="autonomie:templates/panels/project/phase_invoices.mako"
    )
