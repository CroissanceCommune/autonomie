# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Accounting rest api

Used to populate the accounting database from desktop tools

"""
import os

from pyramid.security import NO_PERMISSION_REQUIRED

from autonomie.models.company import Company
from autonomie.models.accounting.operations import AccountingOperation
from autonomie.forms.accounting import get_add_edit_accounting_operation_schema
from autonomie.views import BaseRestView

API_ROOT = "/api/v1"
ACCOUNTING_OPERATION_ROUTE = os.path.join(API_ROOT, "accounting", "operations")
ACCOUNTING_OPERATION_ITEM_ROUTE = os.path.join(
    ACCOUNTING_OPERATION_ROUTE, "{id}"
)


class AccountingOperationRestView(BaseRestView):
    schema = get_add_edit_accounting_operation_schema()

    def collection_get(self):
        return AccountingOperation.query().all()

    def bulk_post(self):
        """
        Handle bulk insertion of AccountingOperation entries

        expect json body with {'datas': [list of AccountingOperation]}

        :returns: The inserted entries
        """
        self.logger.info("POST request (Bulk)")
        result = []
        submitted = self.request.json_body['datas']

        for entry in submitted:
            result.append(self._submit_datas(entry))

        self.logger.debug(
            u"{0} entrie(s) is/are currently added in the database".format(
                len(result)
            )
        )
        return result

    def post_format(self, entry, edit, attributes):
        """
        Set company id if possible after datas validation and model creation

        :param obj entry: The newly created model
        :param bool edit: Is it edition ?
        :param dict attributes: The validated form attributes
        :returns: The entry
        """
        if 'analytical_account' in attributes:
            entry.company_id = Company.get_id_by_analytical_account(
                entry.analytical_account
            )
        return entry


def includeme(config):
    config.add_route(ACCOUNTING_OPERATION_ROUTE, ACCOUNTING_OPERATION_ROUTE)
    config.add_view(
        AccountingOperationRestView,
        route_name=ACCOUNTING_OPERATION_ROUTE,
        attr='collection_get',
        request_method='GET',
        renderer='json',
        xhr=True,
        permission=NO_PERMISSION_REQUIRED,
    )
    config.add_view(
        AccountingOperationRestView,
        route_name=ACCOUNTING_OPERATION_ROUTE,
        attr='bulk_post',
        request_method='POST',
        renderer='json',
        xhr=True,
        permission=NO_PERMISSION_REQUIRED,
    )
