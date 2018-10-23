# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Upload and operation vizualisation
"""
import logging
import colander
from sqlalchemy.orm import load_only
from pyramid.httpexceptions import HTTPFound

from autonomie_celery.tasks.utils import check_alive
from autonomie_celery.tasks.accounting_measure_compute import (
    compile_measures_task,
)

from autonomie.models.accounting.operations import (
    AccountingOperationUpload,
    AccountingOperation,
)
from autonomie.forms.accounting import (
    get_upload_list_schema,
    get_operation_list_schema,
)
from autonomie.utils.widgets import (
    ViewLink,
    Link,
)

from autonomie.views import (
    BaseListView,
    DeleteView,
)

logger = logging.getLogger(__name__)


class UploadListView(BaseListView):
    title = u"Liste des fichiers comptables traités par Autonomie"
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
            yield Link(
                self.request.route_path(
                    '/accounting/operation_uploads/{id}',
                    id=item.id,
                ),
                u"Voir le détail",
                title=u"Voir le détail des écritures importées",
                icon=u"pencil",
            )
            yield Link(
                self.request.route_path(
                    '/accounting/operation_uploads/{id}',
                    id=item.id,
                    _query={'action': u"compile"}
                ),
                u"Recalculer les indicateurs",
                title=u"Recalculer les indicateurs générés depuis ce fichier "
                u"(ex : vous avez changé la configuration des indicateurs)",
                icon=u"fa fa-calculator",
            )

        yield Link(
            self.request.route_path(
                '/accounting/operation_uploads/{id}',
                id=item.id,
                _query={'action': 'delete'}
            ),
            u"Supprimer",
            title=u"Supprimer les écritures téléversées ainsi que les "
            u"indicateurs rattachés",
            icon="trash",
            confirm=u"Supprimer ce téléversement "
            u"entraînera la suppression : \n- Des indicateurs générés"
            u" depuis ce fichier\n"
            u"- Des écritures enregistrées provenant de ce fichier\n"
            u"Continuez ?"
        )

    def query(self):
        return AccountingOperationUpload.query().options(
            load_only(
                AccountingOperationUpload.id,
                AccountingOperationUpload.created_at,
                AccountingOperationUpload.date,
                AccountingOperationUpload.filename,
                AccountingOperationUpload.filetype,
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

    def filter_filetype(self, query, appstruct):
        """
        Filter uploads by filetype
        """
        filetype = appstruct.get('filetype', None)
        if filetype not in ('all', None, colander.null):
            query = query.filter(AccountingOperationUpload.filetype == filetype)

        return query


class DeleteUploadView(DeleteView):
    """
    AccountingOperationUpload delete view
    """
    delete_msg = u"Les données ont bien été supprimées"
    redirect_route = "/accounting/operation_uploads"


class OperationListView(BaseListView):
    """
    Return the list of operations of a given upload (the view's context)
    """
    schema = get_operation_list_schema()
    sort_columns = {
        "analytical_account": AccountingOperation.analytical_account,
        "general_account": AccountingOperation.general_account,
    }
    default_sort = "analytical_account"
    default_direction = "asc"

    @property
    def title(self):
        return u"Liste des écritures extraites du fichier {0}".format(
            self.context.filename
        )

    def populate_actionmenu(self, appstruct):
        self.request.actionmenu.add(
            ViewLink(
                u"Liste des fichiers téléversés",
                path="/accounting/operation_uploads",
            )
        )

    def query(self):
        query = AccountingOperation.query().options(
            load_only(
                AccountingOperation.id,
                AccountingOperation.analytical_account,
                AccountingOperation.general_account,
                AccountingOperation.company_id,
                AccountingOperation.label,
                AccountingOperation.debit,
                AccountingOperation.credit,
                AccountingOperation.balance,
            )
        )
        return query.filter_by(upload_id=self.context.id)

    def filter_analytical_account(self, query, appstruct):
        account = appstruct.get('analytical_account')
        if account not in ('', colander.null, None):
            logger.debug("    + Filtering by analytical_account")
            query = query.filter_by(analytical_account=account)
        return query

    def filter_general_account(self, query, appstruct):
        account = appstruct.get('general_account')
        if account not in ('', colander.null, None):
            logger.debug("    + Filtering by general_account")
            query = query.filter_by(general_account=account)
        return query

    def filter_include_associated(self, query, appstruct):
        include = appstruct.get('include_associated')
        if not include:
            query = query.filter_by(company_id=None)
        return query

    def filter_company_id(self, query, appstruct):
        cid = appstruct.get('company_id')
        if cid not in ('', None, colander.null):
            query = query.filter_by(company_id=cid)
        return query


def compile_measures_view(context, request):
    """
    Handle compilation of measures

    :param obj context: The AccountingOperationUpload instance
    :param obj request: The pyramid request object
    """
    service_ok, msg = check_alive()
    if not service_ok:
        request.session.flash(msg, 'error')
        return HTTPFound(request.referrer)
    logger.debug(u"Compiling measures for upload {0}".format(context.id))
    celery_job = compile_measures_task.delay(context.id)

    logger.info(
        u"The Celery Task {0} has been delayed, see celery logs for "
        u"details".format(
            celery_job.id
        )
    )
    request.session.flash(u"Les indicateurs sont en cours de génération")
    return HTTPFound(request.referrer)


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

    config.add_view(
        OperationListView,
        route_name='/accounting/operation_uploads/{id}',
        renderer="/accounting/operations.mako",
        permission='admin_accounting',
    )
    config.add_view(
        compile_measures_view,
        route_name='/accounting/operation_uploads/{id}',
        request_param="action=compile",
        permission="admin_accounting",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
