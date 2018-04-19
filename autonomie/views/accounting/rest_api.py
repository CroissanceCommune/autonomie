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

from autonomie.statistics.query_helper import get_query
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

        Respond to a Http POST request

        E.g:

            Setting:

            autonomie.accounting_api_key=06dda91136f6ad4688cdf6c8fd991696

            in the development.ini



            import request
            import time

            params = {'datas': [{
                    'analytical_account': u"ANALYTICAL",
                    "general_account": "GENERAL",
                    "date": "2018-01-01",
                    'label': u"LABEL",
                    "debit": "15",
                    "credit": "15",
                    "balance": "25"
                }]
            }

            def send_post_request(params, api_key):
                timestamp = str(time.time())
                secret = "%s-%s" % (timestamp, api_key)
                encoded = md5(secret).hexdigest()
                url = "http://127.0.0.1:8080/api/v1/accounting/operations"
                headers = {
                    'X-Requested-With': 'XMLHttpRequest',
                    "Authorization" : "HMAC-MD5 %s" % encoded,
                    "Timestamp": timestamp
                }
                resp = requests.post(url, json=params, headers=headers)

            send_post_request(
                params,
                "06dda91136f6ad4688cdf6c8fd991696"
            )


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

    def collection_delete(self):
        """
        Handle bulk AccountingOperation deletion

        Respond to a Http DELETE request

        expects json body with filters on the AccountingOperation attributes
        Filters follow a format used in statistics

        e.g:

            import requests
            import time
            params = {'filters': [{'key': 'date', 'type': 'date', 'method':
                'dr', 'search1': '2018-01-01', 'search2': '2018-02-01'}]}

            def send_del_request(params, api_key):
                timestamp = str(time.time())
                secret = "%s-%s" % (timestamp, api_key)
                encoded = md5(secret).hexdigest()
                url = "http://127.0.0.1:8080/api/v1/accounting/operations"
                headers = {
                    'X-Requested-With': 'XMLHttpRequest',
                    "Authorization": "HMAC-MD5 %s" % encoded,
                    "Timestamp": timestamp
                }
                resp = requests.delete(url, json=params, headers=headers)

            send_del_request(
                params,
                "06dda91136f6ad4688cdf6c8fd991696"
            )



        """
        self.logger.info(u"Bulk AccountingOperation delete")
        filters = self.request.json_body['filters']
        self.logger.info(u"    Filters : %s" % filters)

        query = get_query(AccountingOperation, filters)
        self.logger.debug(u"Deleting {0} entries".format(query.count()))
        for id_, entry in query.all():
            self.request.dbsession.delete(entry)
        return {}


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
        api_key_authentication="autonomie.accounting_api_key",
    )
    config.add_view(
        AccountingOperationRestView,
        route_name=ACCOUNTING_OPERATION_ROUTE,
        attr='bulk_post',
        request_method='POST',
        renderer='json',
        xhr=True,
        permission=NO_PERMISSION_REQUIRED,
        api_key_authentication="autonomie.accounting_api_key",
    )
    config.add_view(
        AccountingOperationRestView,
        route_name=ACCOUNTING_OPERATION_ROUTE,
        attr='collection_delete',
        request_method='DELETE',
        renderer='json',
        xhr=True,
        permission=NO_PERMISSION_REQUIRED,
        api_key_authentication="autonomie.accounting_api_key",
    )
