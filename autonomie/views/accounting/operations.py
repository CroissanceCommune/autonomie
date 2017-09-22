# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Upload and operation vizualisation
"""
import colander
from sqlalchemy.orm import load_only

from autonomie.models.accounting.operations import (
    AccountingOperationUpload,
    AccountingOperation,
)
from autonomie.forms.accounting import get_upload_list_schema

from autonomie.views import (
    BaseListView,
    DeleteView,
)


class UploadListView(BaseListView):
    title = u"Liste des fichiers de trésorerie traités par Autonomie"
    add_template_vars = (
        'stream_actions',
    )
    schema = get_upload_list_schema()
    sort_columns = {
        "date": AccountingOperationUpload.date,
        "filename": AccountingOperationUpload.filename,
        "created_at": AccountingOperationUpload.created_at,
    }
    default_sort = "created_at"
    default_direction = "desc"

    def _has_operations(self, item):
        """
        Return true if the given item has operations attached to it

        :param obj item: a AccountingOperationUpload instance
        """
        return self.request.dbsession.query(AccountingOperation.id).filter_by(
            upload_id=item.id
        ).count() > 0

    def stream_actions(self, item):
        """
        Compile the action description for the given item
        """

        if self._has_operations(item):
            yield (
                self.request.route_path(
                    '/accounting/operation_uploads/{id}',
                    id=item.id,
                ),
                u"Voir le détail",
                u"Voir le détail des écritures importées",
                u"pencil",
                {}
            )
            yield (
                self.request.route_path(
                    '/accounting/operation_uploads/{id}',
                    id=item.id,
                    _query={'action': u"compile"}
                ),
                u"Recalculer les indicateurs",
                u"Recalculer les indicateurs générés depuis ce fichier "
                u"(ex : vous avez changé la configuration des indicateurs)",
                u"fa fa-calculator",
                {}
            )

        yield (
            self.request.route_path(
                '/accounting/operation_uploads/{id}',
                id=item.id,
                _query={'action': 'delete'}
            ),
            u"Supprimer",
            u"Supprimer les écritures téléversées ainsi que les indicateurs "
            u"rattachés",
            "trash",
            {
                "onclick": (
                    u"return window.confirm('Supprimer ce téléversement "
                    u"entraînera la suppression : \n- Des indicateurs générés"
                    u" depuis ce fichier\n"
                    u"- Des écritures enregistrées provenant de ce fichier\n"
                    u"Continuez ?');"
                    )
            }
        )

    def query(self):
        return AccountingOperationUpload.query().options(
            load_only(
                AccountingOperationUpload.id,
                AccountingOperationUpload.created_at,
                AccountingOperationUpload.date,
                AccountingOperationUpload.filename,
            )
        )

    def filter_date(self, query, appstruct):
        """
        Filter by date period
        """
        period_appstruct = appstruct.get('period', {})
        if period_appstruct not in (None, colander.null):
            start_date = appstruct.get('start_date')
            if start_date not in (None, colander.null):
                query = query.filter(
                    AccountingOperationUpload.date >= start_date
                )

            end_date = appstruct.get('end_date')
            if end_date not in (None, colander.null):
                query = query.filter(
                    AccountingOperationUpload.date >= end_date
                )
        return query


class DeleteUploadView(DeleteView):
    """
    AccountingOperationUpload delete view
    """
    delete_msg = u"Les données ont bien été supprimées"
    redirect_route = "/accounting/operation_uploads"


def add_routes(config):
    config.add_route(
        "/accounting/operation_uploads",
        "/accounting/operation_uploads",
    )
    config.add_route(
        "/accounting/operation_uploads/{id}",
        "/accounting/operation_uploads/{id}",
        traverse="/accounting_operation_uploads/{id}",
    )


def add_views(config):
    config.add_view(
        UploadListView,
        route_name='/accounting/operation_uploads',
        renderer="/accounting/operation_uploads.mako",
        permission='admin_accounting',
    )

    config.add_view(
        DeleteUploadView,
        route_name='/accounting/operation_uploads/{id}',
        request_param="action=delete",
        permission="admin_accounting",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
