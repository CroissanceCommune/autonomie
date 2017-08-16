# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import datetime
import colander
import traceback

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.expense import (
    ExpenseSheet,
    ExpenseType,
    ExpenseLine,
    ExpenseKmLine,
)

from autonomie.utils.rest import (
    add_rest_views,
    RestError,
)
from autonomie.forms.expense import (
    BookMarkSchema,
)

from autonomie.events.expense import StatusChanged as ExpenseStatusChanged
from autonomie.views import BaseRestView
from autonomie.views.expenses.bookmarks import (
    get_bookmarks,
    BookMarkHandler,
)
from autonomie.views import (
    BaseView,
)
from autonomie.views.status import StatusView

logger = logging.getLogger(__name__)


class RestExpenseSheetView(BaseRestView):
    factory = ExpenseSheet

    def get_schema(self, submitted):
        """
        Return the schema for TaskLineGroup add/edition

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        if self.factory is None:
            raise Exception("Child class should provide a factory attribute")
        excludes = (
            'status',
            'status_user_id',
            'user',
            'company',
            'children',
            'parent',
            'user_id',
            'company_id',
            "name"
        )
        schema = SQLAlchemySchemaNode(
            self.factory,
            excludes=excludes
        )
        return schema

    def post_format(self, entry, edit, attributes):
        """
        Add the company and user id after sheet add
        """
        if not edit:
            entry.company_id = self.context.id
            entry.user_id = self.request.user.id

        return entry

    def _load_used_type_ids(self):
        """
        Return the ids of expense types used in this expense (if they are
        disabled, we want to display them anyway)
        """
        res = []
        for line in self.context.lines:
            res.append(line.type_id)
        for line in self.context.kmlines:
            res.append(line.type_id)
        return res

    def form_config(self):
        """
        Form display options

        :returns: The sections that the end user can edit, the options available
        for the different select boxes
        """
        result = {
            "actions": {
                'status': self._get_status_actions(),
                'others': self._get_other_actions(),
            }
        }
        result = self._add_form_options(result)
        return result

    def _get_status_actions(self):
        """
        Returned datas describing available actions on the current item
        :returns: List of actions
        :rtype: list of dict
        """
        actions = []
        url = self.request.current_route_path(_query={'action': 'status'})
        for action in self.context.state_manager.get_allowed_actions(
            self.request
        ):
            json_resp = action.__json__(self.request)
            json_resp['url'] = url
            self._format_status_action(json_resp)
            actions.append(json_resp)
        return actions

    def _format_status_action(self, action_dict):
        """
        Alter the status description regarding the current context

        Hack to allow better label handling
        """
        if action_dict['status'] == 'draft' and self.context.status == 'wait':
            action_dict['label'] = u"Repasser en brouillon"
            action_dict['title'] = u"Repasser ce document en brouillon"
            action_dict['icon'] = 'remove'
        return action_dict

    def _get_other_actions(self):
        """
        Return the description of other available actions :
            signed_status
            duplicate
            ...
        """
        result = []
        if self.request.has_permission('delete.expensesheet'):
            url = self.request.route_path(
                "/expenses/{id}/delete",
                id=self.context.id
            )
            result.append({
                'widget': 'anchor',
                'option': {
                    "url": url,
                    "label": u"Supprimer",
                    "title": u"Supprimer définitivement ce document",
                    "css": "btn btn-default",
                    "icon": "fa fa-trash",
                    "onclick": u"return confirm('Êtes-vous sûr de vouloir"
                    u"supprimer cet élément ?');"
                }
            })

        if self.request.has_permission('add.file'):
            url = self.request.route_path(
                "/expenses/{id}/addfile",
                id=self.context.id
            )
            result.append({
                'widget': 'anchor',
                'option': {
                    "url": url,
                    "label": u"Attacher un fichier",
                    "title": u"Attacher un fichier à ce document",
                    "css": "btn btn-default",
                    "icon": "fa fa-files-o",
                    "attrs": "target=_blank",
                }
            })
        return result

    def _add_form_options(self, form_config):
        """
        add form options to the current configuration
        """
        options = self._get_type_options()

        options['categories'] = [
            {
                'value': '1',
                "label": u"Frais",
                'description': u"Frais liés au fonctionnement de l'entreprise"
            },
            {
                'value': '2',
                "label": u"Achats",
                'description': u"Frais concernant directement votre activité \
    auprès de vos clients"
            }]

        options['bookmarks'] = get_bookmarks(self.request)

        options['expenses'] = self._get_existing_expenses_options()

        expense_sheet = self.request.context
        month = expense_sheet.month
        year = expense_sheet.year

        date = datetime.date(year, month, 1)
        options['today'] = date
        form_config['options'] = options
        return form_config

    def _get_type_options(self):
        # Load types already used in this expense
        current_expenses_used_types = self._load_used_type_ids()

        options = {
            "expense_types": [],
            "expensekm_types": [],
            "expensetel_types": [],
        }

        for etype in ExpenseType.query():
            if etype.id in current_expenses_used_types or etype.active:
                key = "%s_types" % etype.type
                options[key].append(etype)
        return options

    def _get_existing_expenses_options(self):
        """
        Return other existing expenses available for expense line duplication
        """
        all_expenses = ExpenseSheet.query().filter_by(user_id=self.context.id)
        all_expenses = all_expenses.filter_by(company_id=self.company_id)
        all_expenses = all_expenses.filter(ExpenseSheet.id != self.context.id)
        return [
            {
                "label": u"{e.month_label} / {e.year}".format(e),
                "id": e.id
            } for e in all_expenses
        ]


class RestExpenseLineView(BaseRestView):
    """
    Base rest view for expense line handling
    """
    def get_schema(self, submitted):
        excludes = ('sheet_id',)
        schema = SQLAlchemySchemaNode(ExpenseLine, excludes=excludes)
        return schema

    def collection_get(self):
        return self.context.lines

    def post_format(self, entry, edit, attributes):
        """
        Associate a newly created element to the parent task
        """
        if not edit:
            entry.sheet = self.context
        return entry


class RestExpenseKmLineView(BaseRestView):
    """
    Base rest view for expense line handling
    """
    def get_schema(self, submitted):
        excludes = ('sheet_id',)
        schema = SQLAlchemySchemaNode(ExpenseKmLine, excludes=excludes)
        return schema

    def collection_get(self):
        return self.context.kmlines

    def post_format(self, entry, edit, attributes):
        """
        Associate a newly created element to the parent task
        """
        if not edit:
            entry.sheet = self.context
        return entry


class RestBookMarkView(BaseView):
    """
        Json rest-api for expense bookmarks handling
    """
    _schema = BookMarkSchema()

    @property
    def schema(self):
        return self._schema.bind(request=self.request)

    def get(self):
        """
            Rest GET Method : get
        """
        return get_bookmarks(self.request)

    def post(self):
        """
            Rest POST method : add
        """
        logger.debug(u"In the bookmark edition")

        appstruct = self.request.json_body
        try:
            bookmark = self.schema.deserialize(appstruct)
        except colander.Invalid, err:
            traceback.print_exc()
            logger.exception("  - Error in posting bookmark")
            logger.exception(appstruct)
            raise RestError(err.asdict(), 400)

        handler = BookMarkHandler(self.request)
        bookmark = handler.store(bookmark)
        return bookmark

    def put(self):
        """
            Rest PUT method : edit
        """
        self.post()

    def delete(self):
        """
            Removes a bookmark
        """
        logger.debug(u"In the bookmark deletion view")

        handler = BookMarkHandler(self.request)

        # Retrieving the id from the request
        id_ = self.request.matchdict.get('id')

        bookmark = handler.delete(id_)

        # if None is returned => there was no bookmark with this id
        if bookmark is None:
            raise RestError({}, 404)
        else:
            return dict(status="success")


class RestExpenseSheetStatusView(StatusView):
    def notify(self, status):
        """
        Notify a status change
        """
        self.request.registry.notify(
            ExpenseStatusChanged(self.request, self.context, status)
        )


def add_routes(config):
    """
    Add module's related routes
    """
    config.add_route("/api/v1/bookmarks/{id}", "/api/v1/bookmarks/{id:\d+}")
    config.add_route("/api/v1/bookmarks", "/api/v1/bookmarks")

    config.add_route(
        "/api/v1/expenses",
        "/api/v1/expenses",
    )

    config.add_route(
        "/api/v1/expenses/{id}",
        "/api/v1/expenses/{id:\d+}",
        traverse="/expenses/{id}"
    )

    config.add_route(
        "/api/v1/expenses/{id}/lines",
        "/api/v1/expenses/{id}/lines",
        traverse="/expenses/{id}"
    )

    config.add_route(
        "/api/v1/expenses/{id}/lines/{lid}",
        "/api/v1/expenses/{id:\d+}/lines/{lid:\d+}",
        traverse="/expenselines/{lid}",
    )

    config.add_route(
        "/api/v1/expenses/{id}/kmlines",
        "/api/v1/expenses/{id:\d+}/kmlines",
        traverse="/expenses/{id}",
    )

    config.add_route(
        "/api/v1/expenses/{id}/kmlines/{lid}",
        "/api/v1/expenses/{id:\d+}/kmlines/{lid:\d+}",
        traverse="/expensekmlines/{lid}",
    )


def add_views(config):
    """
    Add rest api views
    """
    add_rest_views(
        config,
        factory=RestExpenseSheetView,
        route_name="/api/v1/expenses/{id}",
        collection_route_name="/api/v1/expenses",
        view_rights="view.expensesheet",
        add_rights="add.expensesheet",
        edit_rights="edit.expensesheet",
        delete_rights="delete.expensesheet",
    )

    # Form configuration view
    config.add_view(
        RestExpenseSheetView,
        attr='form_config',
        route_name='/api/v1/expenses/{id}',
        renderer='json',
        request_param="form_config",
        permission='view.expensesheet',
        xhr=True,
    )

    # Status view
    config.add_view(
        RestExpenseSheetStatusView,
        route_name='/api/v1/expenses/{id}',
        request_param='action=status',
        permission="edit.expensesheet",
        request_method='POST',
        renderer="json",
    )

    # Line views
    add_rest_views(
        config,
        factory=RestExpenseLineView,
        route_name="/api/v1/expenses/{id}/lines/{lid}",
        collection_route_name="/api/v1/expenses/{id}/lines",
        view_rights="view.expensesheet",
        add_rights="add.expensesheet",
        edit_rights="edit.expensesheet",
        delete_rights="edit.expensesheet",
    )

    # Km Line views
    add_rest_views(
        config,
        factory=RestExpenseKmLineView,
        route_name="/api/v1/expenses/{id}/kmlines/{lid}",
        collection_route_name="/api/v1/expenses/{id}/kmlines",
        view_rights="view.expensesheet",
        add_rights="add.expensesheet",
        edit_rights="edit.expensesheet",
        delete_rights="edit.expensesheet",
    )
    # BookMarks
    add_rest_views(
        config,
        factory=RestBookMarkView,
        route_name="/api/v1/bookmarks/{id}",
        collection_route_name="/api/v1/bookmarks",
        view_rights="edit.expense",
        add_rights="add.expense",
        edit_rights='edit.expense',
    )


def includeme(config):
    add_routes(config)
    add_views(config)
