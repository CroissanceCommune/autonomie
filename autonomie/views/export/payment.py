# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from collections import OrderedDict

from autonomie.export.utils import write_file_to_request
from autonomie.utils.files import get_timestamped_filename

from autonomie.models.task import (
    Payment,
    Invoice,
)
from autonomie.utils.widgets import ViewLink

from autonomie.views.admin.sale.receipts import RECEIPT_URL
from autonomie.views.export.utils import (
    get_period_form,
    get_all_form,
    get_invoice_number_form,
)

from autonomie.views.export import BaseExportView

logger = logging.getLogger(__name__)

PAYMENT_VOID_ERROR_MSG = u"Il n'y a aucun encaissement à exporter"

PAYMENT_CUSTOMER_ERROR_MSG = u"""Un encaissement de la facture {0} n'est pas
exportable : Des informations sur le client {1} (compte général ou compte tiers)
sont manquantes
 <a onclick="window.openPopup('{2}');" href='#'>Voir le client</a>"""

PAYMENT_BANK_ERROR_MSG = u"""Un encaissement de la facture {0}
n'est pas exportable : L'encaissement n'est associé à aucune banque
<a onclick="window.openPopup('{1}');" href='#'>
    Voir l'encaissement
</a>"""


class SagePaymentExportPage(BaseExportView):
    """
    Provide a sage export view compound of multiple forms for payment exports
    """
    title = u"Export des encaissements au format CSV pour Sage"
    admin_route_name = RECEIPT_URL

    def _populate_action_menu(self):
        self.request.actionmenu.add(
            ViewLink(
                label=u"Liste des factures",
                path='invoices',
            )
        )

    def before(self):
        self._populate_action_menu()

    def get_forms(self):
        """
        Return the different payment search forms
        """
        result = OrderedDict()
        period_form = get_period_form(
            self.request,
            title=u"Exporter les encaissements saisis sur la période donnée"
        )

        number_form = get_invoice_number_form(
            self.request,
            period_form.counter,
            title=u"Exporter les encaissements correspondant à une facture",
        )

        all_form = get_all_form(
            self.request,
            period_form.counter,
            title=u"Exporter les encaissements non exportés",
        )

        for form in all_form, number_form, period_form:
            result[form.formid] = {'form': form, 'title': form.schema.title}

        return result

    def _filter_date(self, query, start_date, end_date):
        return query.filter(
            Payment.date.between(start_date, end_date)
        )

    def _filter_number(self, query, start, end, year):
        inv_query = self.request.dbsession.query(Invoice.id)

        inv_query = inv_query.filter(Invoice.official_number >= start)

        if end:
            inv_query.filter(Invoice.official_number <= end)

        inv_query = inv_query.filter(Invoice.financial_year == year)

        task_ids = [item[0] for item in inv_query]

        return query.filter(Payment.task_id.in_(task_ids))

    def query(self, query_params_dict, form_name):
        query = Payment.query()

        if form_name == "period_form":
            start_date = query_params_dict['start_date']
            end_date = query_params_dict['end_date']
            query = self._filter_date(query, start_date, end_date)

        elif form_name == 'invoice_number_form':
            start = query_params_dict['start']
            end = query_params_dict['end']
            financial_year = query_params_dict['financial_year']
            query = self._filter_number(
                query, start, end, financial_year,
            )

        if 'exported' not in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter(Payment.exported == False)

        return query

    def _check_customer(self, customer):
        """
            Check the invoice's customer is configured for exports
        """
        if not customer.compte_cg:
            return False
        if not customer.compte_tiers:
            return False
        return True

    def _check_bank(self, payment):
        if payment.bank is None:
            return False
        return True

    def check(self, payments):
        """
        Check that the given payments are 'exportable'
        :param obj payments: a SQLA query of Payments
        """
        count = payments.count()
        if count == 0:
            res = {
                'title': PAYMENT_VOID_ERROR_MSG,
                'errors': [],
            }
            return False, res

        title = u"Vous vous apprêtez à exporter {0} encaissements".format(
                count)
        res = {'title': title, 'errors': []}
        for payment in payments:
            invoice = payment.invoice
            if not self._check_customer(invoice.customer):
                customer_url = self.request.route_path(
                    'customer',
                    id=invoice.customer.id,
                    _query={'action': 'edit'})
                message = PAYMENT_CUSTOMER_ERROR_MSG.format(
                    invoice.official_number,
                    invoice.customer.name,
                    customer_url)
                res['errors'].append(message)
                continue

            if not self._check_bank(payment):
                payment_url = self.request.route_path(
                    'payment',
                    id=payment.id,
                    _query={'action': 'edit'}
                )
                message = PAYMENT_BANK_ERROR_MSG.format(
                    invoice.official_number,
                    payment_url)
                res['errors'].append(message)
                continue

        return len(res['errors']) == 0, res

    def record_exported(self, payments, form_name, appstruct):
        for payment in payments:
            logger.info(
                u"The payment id : {0} (invoice {1} id:{2}) has been exported"
                .format(
                    payment.id,
                    payment.invoice.official_number,
                    payment.invoice.id,
                )
            )
            payment.exported = True
            self.request.dbsession.merge(payment)

    def write_file(self, payments, form_name, appstruct):
        """
            Write the exported csv file to the request
        """
        from autonomie.interfaces import ITreasuryPaymentProducer
        exporter = self.request.find_service(ITreasuryPaymentProducer)
        from autonomie.interfaces import ITreasuryPaymentWriter
        writer = self.request.find_service(ITreasuryPaymentWriter)

        writer.set_datas(exporter.get_book_entries(payments))
        write_file_to_request(
            self.request,
            get_timestamped_filename(u"export_encaissement", writer.extension),
            writer.render(),
            headers="application/csv")
        return self.request.response


def add_routes(config):
    config.add_route(
        '/export/treasury/payments',
        '/export/treasury/payments'
    )
    config.add_route(
        '/export/treasury/payments/{id}',
        '/export/treasury/payments/{id}'
    )


def add_views(config):
    config.add_view(
        SagePaymentExportPage,
        route_name='/export/treasury/payments',
        renderer='/export/main.mako',
        permission='admin_treasury',
    )


def includeme(config):
    add_routes(config)
    add_views(config)
