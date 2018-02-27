# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import datetime
import colander
import traceback

from sqlalchemy import (
    or_,
)
from pyramid.httpexceptions import (
    HTTPForbidden,
)

from autonomie.models.expense.sheet import (
    ExpenseSheet,
    ExpenseLine,
    ExpenseKmLine,
    Communication,
)
from autonomie.models.expense.types import (
    ExpenseType,
    ExpenseKmType,
)
from autonomie.utils import strings
from autonomie.utils.rest import (
    add_rest_views,
    RestError,
    Apiv1Resp,
)
from autonomie.forms.expense import (
    BookMarkSchema,
    get_add_edit_sheet_schema,
    get_add_edit_line_schema,
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
        Return the schema for ExpenseSheet add

        :param dict submitted: The submitted datas
        :returns: A colander.Schema
        """
        return get_add_edit_sheet_schema()

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
            duplicate
            ...
        """
        result = []

        if self.request.has_permission('add_payment.expensesheet'):
            url = self.request.route_path(
                "/expenses/{id}/addpayment",
                id=self.context.id,
            )
            result.append({
                'widget': 'anchor',
                'option': {
                    "url": url,
                    "label": u"Enregistrer un paiement",
                    "title": u"Enregistrer un paiement pour cette note "
                    u"de dépenses",
                    "css": "btn btn-default",
                    "icon": "fa fa-bank",
                }
            })

        if self.request.has_permission('delete.expensesheet'):
            result.append(self._delete_btn())

        if self.request.has_permission('add.file'):
            result.append(self._add_file_btn())

        if self.request.has_permission('view.expensesheet'):
            result.append(self._duplicate_btn())

        if self.request.has_permission('set_justified.expensesheet'):
            result.append(self._get_justified_toggle())

        return result

    def _delete_btn(self):
        """
        Return a deletion btn description

        :rtype: dict
        """
        url = self.request.route_path(
            "/expenses/{id}/delete",
            id=self.context.id
        )
        return {
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
        }

    def _add_file_btn(self):
        """
        Return an add file description button

        :rtype: dict
        """
        url = self.request.route_path(
            "/expenses/{id}/addfile",
            id=self.context.id
        )
        return {
            'widget': 'anchor',
            'option': {
                "url": url,
                "label": u"Attacher un fichier",
                "title": u"Attacher un fichier à ce document",
                "css": "btn btn-default",
                "icon": "fa fa-files-o",
                "attrs": "target=_blank",
            }
        }

    def _duplicate_btn(self):
        """
        Return a duplicate btn description

        :rtype: dict
        """
        url = self.request.route_path(
            "/expenses/{id}/duplicate",
            id=self.context.id
        )
        return {
            'widget': 'anchor',
            'option': {
                "url": url,
                "label": u"Dupliquer",
                "title": u"Créer une nouvelle note de dépenses à partir "
                u"de celle-ci",
                "css": "btn btn-default",
                "icon": "fa fa-copy",
            }
        }

    def _get_justified_toggle(self):
        """
        Return a justification toggle button description

        :rtype: dict
        """
        url = self.request.route_path(
            "/api/v1/expenses/{id}",
            id=self.context.id,
            _query={'action': 'justified_status'}
        )
        actions = self.context.justified_state_manager.get_allowed_actions(
            self.request
        )

        return {
            "widget": "toggle",
            'options': {
                "url": url,
                "name": "justified",
                "current_value": self.context.justified,
                "label": u"Justificatifs",
                "buttons": actions,
                "css": "btn btn-default",
            }
        }
        return

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

        options['edit'] = bool(self.request.has_permission('edit.expensesheet'))
        form_config['options'] = options
        return form_config

    def _get_expense_types_options(self, type_label, include_ids):
        """
        Return ExpenseType defs or ExpenseTelType available for the end user

        :param str type_label: 'expense' or 'expensetel'
        :param list include_ids: The ids of already used types
        :returns: The list of available options
        :rtype: list
        """
        query = ExpenseType.query().filter_by(type=type_label).filter(
            or_(
                ExpenseType.id.in_(include_ids),
                ExpenseType.active == True
            )
        )
        return query.all()

    def _get_kmtype_ids(self):
        """
        Return the kmtype ids that should be presented to the end user
        Filter the given query with the user's configured vehicle
        """
        query = self.request.dbsession.query(ExpenseKmType.id)
        query = query.filter_by(active=True)
        query = query.filter_by(year=self.context.year)

        if self.context.user.vehicle and '-' in self.context.user.vehicle:
            label, code = self.context.user.vehicle.split('-')
            query = query.filter_by(label=label).filter_by(code=code)

        return [i[0] for i in query]

    def _get_expense_km_types_options(self, include_ids):
        """
        Return ExpenseKm defs available for the end user

        :param list include_ids: The ids of already used types
        :returns: The list of available options
        :rtype: list
        """
        available_ids = self._get_kmtype_ids()
        query = ExpenseKmType.query().filter(
            or_(
                ExpenseKmType.id.in_(include_ids),
                ExpenseKmType.id.in_(available_ids),
            )
        )
        return query.all()

    def _get_type_options(self):
        # Load types already used in this expense
        current_expenses_used_type_ids = self._load_used_type_ids()

        options = {
            "expense_types": self._get_expense_types_options(
                'expense',
                current_expenses_used_type_ids
            ),
            "expensetel_types": self._get_expense_types_options(
                'expensetel',
                current_expenses_used_type_ids,
            ),
            "expensekm_types": self._get_expense_km_types_options(
                current_expenses_used_type_ids,
            )
        }
        return options

    def _get_existing_expenses_options(self):
        """
        Return other existing expenses available for expense line duplication
        """
        result = [{
            "label": u"{month_label} / {year} (feuille courante)".format(
                month_label=strings.month_name(self.context.month),
                year=self.context.year,
            ),
            "id": self.context.id,
        }]
        all_expenses = ExpenseSheet.query().filter_by(
            user_id=self.context.user_id
        )
        all_expenses = all_expenses.filter_by(
            company_id=self.context.company_id
        )
        all_expenses = all_expenses.filter(ExpenseSheet.id != self.context.id)
        all_expenses = all_expenses.filter(
            ExpenseSheet.status.in_(['draft', 'invalid'])
        )
        all_expenses = all_expenses.order_by(
            ExpenseSheet.year.desc()
        ).order_by(
            ExpenseSheet.month.desc()
        )
        result.extend([
            {
                "label": u"{month_label} / {year}".format(
                    month_label=strings.month_name(e.month),
                    year=e.year
                ),
                "id": e.id
            } for e in all_expenses
        ])
        return result


class RestExpenseLineView(BaseRestView):
    """
    Base rest view for expense line handling
    """
    def get_schema(self, submitted):
        return get_add_edit_line_schema(ExpenseLine)

    def collection_get(self):
        return self.context.lines

    def post_format(self, entry, edit, attributes):
        """
        Associate a newly created element to the parent task
        """
        if not edit:
            entry.sheet = self.context
        return entry

    def duplicate(self):
        """
        Duplicate an expense line to an existing ExpenseSheet
        """
        logger.info(u"Duplicate ExpenseLine")
        sheet_id = self.request.json_body.get('sheet_id')
        sheet = ExpenseSheet.get(sheet_id)

        if sheet is None:
            return RestError(["Wrong sheet_id"])

        if not self.request.has_permission('edit.expensesheet'):
            logger.error(u"Unauthorized action : possible break in attempt")
            raise HTTPForbidden()

        new_line = self.context.duplicate(sheet=sheet)
        new_line.sheet_id = sheet.id
        self.request.dbsession.add(new_line)
        self.request.dbsession.flush()
        return new_line


class RestExpenseKmLineView(BaseRestView):
    """
    Base rest view for expense line handling
    """
    def get_schema(self, submitted):
        schema = get_add_edit_line_schema(ExpenseKmLine)
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

    def duplicate(self):
        """
        Duplicate an expense line to an existing ExpenseSheet
        """
        logger.info(u"Duplicate ExpenseKmLine")
        sheet_id = self.request.json_body.get('sheet_id')
        sheet = ExpenseSheet.get(sheet_id)

        if sheet is None:
            return RestError(["Wrong sheet_id"])

        if not self.request.has_permission('edit.expensesheet'):
            logger.error(u"Unauthorized action : possible break in attempt")
            raise HTTPForbidden()

        new_line = self.context.duplicate(sheet=sheet)
        if new_line.type_object is None:
            return RestError([
                u"Aucun type de frais kilométriques correspondant n'a pu être "
                u"retrouvé sur l'année {0}".format(sheet.year)
            ], code=403)

        new_line.sheet_id = sheet.id
        self.request.dbsession.add(new_line)
        self.request.dbsession.flush()
        return new_line


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

    def redirect(self):
        loc = self.request.route_path("/expenses/{id}", id=self.context.id)
        return dict(redirect=loc)

    def check_allowed(self, status, params):
        self.request.context.check_status_allowed(status, self.request)

    def pre_status_process(self, status, params):
        if 'comment' in params:
            self.context.communications.append(
                Communication(
                    content=params.get('comment'),
                    user_id=self.request.user.id,
                )
            )

        return StatusView.pre_status_process(self, status, params)


class RestExpenseSheetJustifiedStatusView(StatusView):

    def check_allowed(self, status, params):
        self.request.context.check_justified_status_allowed(
            status,
            self.request
        )

    def notify(self, status):
        if status is True:
            self.request.registry.notify(
                ExpenseStatusChanged(self.request, self.context, 'justified')
            )

    def redirect(self):
        return Apiv1Resp(
            self.request, {'justified': self.context.justified}
        )

    def _get_status(self, params):
        status = params['submit']

        if status in ('True', 'true'):
            status = True
        elif status in ('False', 'false'):
            status = False
        return status

    def pre_status_process(self, status, params):
        logger.debug("In pre_status_process : %s %s" % (status, type(status)))
        if 'comment' in params:
            self.context.communications.append(
                Communication(
                    content=params.get('comment'),
                    user_id=self.request.user.id,
                )
            )

        return StatusView.pre_status_process(self, status, params)

    def status_process(self, status, params):
        return self.context.set_justified_status(
            status,
            self.request,
            **params
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
        traverse="/expenselines/{lid}",
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
        permission="view.expensesheet",
        request_method='POST',
        renderer="json",
    )

    # Status view
    config.add_view(
        RestExpenseSheetJustifiedStatusView,
        route_name='/api/v1/expenses/{id}',
        request_param='action=justified_status',
        permission="view.expensesheet",
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
        add_rights="edit.expensesheet",
        edit_rights="edit.expensesheet",
        delete_rights="edit.expensesheet",
    )
    config.add_view(
        RestExpenseLineView,
        attr='duplicate',
        route_name="/api/v1/expenses/{id}/lines/{lid}",
        request_param='action=duplicate',
        permission="edit.expensesheet",
        request_method='POST',
        renderer="json",
    )

    # Km Line views
    add_rest_views(
        config,
        factory=RestExpenseKmLineView,
        route_name="/api/v1/expenses/{id}/kmlines/{lid}",
        collection_route_name="/api/v1/expenses/{id}/kmlines",
        view_rights="view.expensesheet",
        add_rights="edit.expensesheet",
        edit_rights="edit.expensesheet",
        delete_rights="edit.expensesheet",
    )
    config.add_view(
        RestExpenseKmLineView,
        attr='duplicate',
        route_name="/api/v1/expenses/{id}/kmlines/{lid}",
        request_param='action=duplicate',
        permission="edit.expensesheet",
        request_method='POST',
        renderer="json",
    )
    # BookMarks
    add_rest_views(
        config,
        factory=RestBookMarkView,
        route_name="/api/v1/bookmarks/{id}",
        collection_route_name="/api/v1/bookmarks",
        view_rights="view",
        add_rights="view",
        edit_rights='view',
        delete_rights="view",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
