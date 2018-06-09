# -*- coding: utf-8 -*-
# * Copyright (C) Coopérer pour entreprendre
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Invoice related exports views
"""
import logging
from collections import OrderedDict

from sqlalchemy import or_

from autonomie.export.utils import write_file_to_request
from autonomie.utils.widgets import ViewLink
from autonomie.utils.files import get_timestamped_filename

from autonomie.models.task import (
    Task,
    Invoice,
    CancelInvoice,
)

from autonomie.views.admin.sale.accounting import (
    ACCOUNTING_URL,
    ACCOUNTING_CONFIG_URL,
)
from autonomie.views.export import BaseExportView
from autonomie.views.export.utils import (
    get_period_form,
    get_all_form,
    get_invoice_number_form,
)


logger = logging.getLogger(__name__)


MISSING_PRODUCT_ERROR_MSG = u"""Le document {0} n'est pas exportable :
 des comptes produits sont manquants
<a onclick="openPopup('{1}');" href='#'>
        Voir le document
</a>"""

COMPANY_ERROR_MSG = u"""Le document {0} n'est pas exportable :
Le code analytique de l'entreprise {1} n'a pas été configuré
<a onclick="openPopup('{2}');" href='#'>
    Voir l'entreprise
</a>"""

CUSTOMER_ERROR_MSG = u"""Le document {0} n'est pas exportable :
Le compte général du client {1} n'a pas été configuré
<a onclick="openPopup('{2}');" href='#'>
    Voir le client
</a>"""


MISSING_RRR_CONFIG_ERROR_MSG = u"""Le document {0} n'est pas exportable :
Il contient des remises et les comptes RRR ne sont pas configurés.
<a onclick="openPopup('{1}');" href='#'>
Configurer les comptes RRR
</a>"""


class SageSingleInvoiceExportPage(BaseExportView):
    """
    Single invoice export page
    """
    admin_route_name = ACCOUNTING_URL

    @property
    def title(self):
        return "Export de la facture {0}{1} au format CSV".format(
            self.context.official_number,
        )

    def populate_action_menu(self):
        """
        Add a back button to the action menu
        """
        self.request.actionmenu.add(
            ViewLink(
                label=u"Retour au document",
                path='/%ss/{id}.html' % self.context.type_,
                id=self.context.id,
                _anchor='treasury'
            )
        )

    def before(self):
        self.populate_action_menu()

    def validate_form(self, forms):
        """
        Return a a void form name and an appstruct so processing goes on
        """
        return "", {}

    def query(self, appstruct, formname):
        force = self.request.params.get('force', False)
        if not force and self.context.exported:
            return []
        else:
            return [self.context]

    def _check_invoice_line(self, line):
        """
        Check the invoice line is ok for export

        :param obj line: A TaskLine instance
        """
        return line.product is not None

    def _check_company(self, company):
        """
            Check the invoice's company is configured for exports
        """
        if not company.code_compta:
            return False
        return True

    def _check_customer(self, customer):
        """
            Check the invoice's customer is configured for exports

        """
        if not customer.compte_cg:
            return False
        if self.request.config.get('sage_rgcustomer'):
            if not customer.compte_tiers:
                return False
        return True

    def check_num_invoices(self, invoices):
        """
        Return the number of invoices to export
        """
        return len(invoices)

    def _check_discount_config(self):
        """
        Check that the rrr accounts are configured
        """
        return self.request.config.get("compte_rrr") and \
            self.request.config.get("compte_cg_tva_rrr")

    def check(self, invoices):
        """
            Check that the given invoices are 'exportable'
        """
        count = self.check_num_invoices(invoices)
        if count == 0:
            title = u"Il n'y a aucune facture à exporter"
            res = {
                'title': title,
                'errors': [],
            }
            return False, res
        title = u"Vous vous apprêtez à exporter {0} factures".format(
                count)
        res = {'title': title, 'errors': []}

        prefix = self.request.config.get('invoiceprefix', '')
        for invoice in invoices:
            official_number = "%s%s" % (prefix, invoice.official_number)
            for line in invoice.all_lines:
                if not self._check_invoice_line(line):
                    invoice_url = self.request.route_path(
                        '/%ss/{id}/set_products' % invoice.type_,
                        id=invoice.id
                    )
                    message = MISSING_PRODUCT_ERROR_MSG.format(
                        official_number, invoice_url
                    )
                    res['errors'].append(message)
                    break

            if invoice.discounts:
                if not self._check_discount_config():
                    admin_url = self.request.route_path(
                        ACCOUNTING_CONFIG_URL,
                    )

                    message = MISSING_RRR_CONFIG_ERROR_MSG.format(
                        official_number,
                        admin_url,
                    )
                    res['errors'].append(message)

            if not self._check_company(invoice.company):
                company_url = self.request.route_path(
                    'company',
                    id=invoice.company.id,
                    _query={'action': 'edit'}
                )
                message = COMPANY_ERROR_MSG.format(
                    official_number,
                    invoice.company.name,
                    company_url)
                res['errors'].append(message)
                continue

            if not self._check_customer(invoice.customer):
                customer_url = self.request.route_path(
                    'customer',
                    id=invoice.customer.id,
                    _query={'action': 'edit'})

                message = CUSTOMER_ERROR_MSG.format(
                    official_number,
                    invoice.customer.name,
                    customer_url)
                res['errors'].append(message)
                continue

        return len(res['errors']) == 0, res

    def record_exported(self, invoices, form_name, appstruct):
        for invoice in invoices:
            logger.info(
                "The {0.type_} number {0.official_number} (id : {0.id})"
                "has been exported".format(invoice)
            )
            invoice.exported = True
            self.request.dbsession.merge(invoice)

    def write_file(self, invoices, form_name, appstruct):
        """
            Write the exported csv file to the request
        """
        from autonomie.interfaces import ITreasuryInvoiceProducer
        exporter = self.request.find_service(ITreasuryInvoiceProducer)
        from autonomie.interfaces import ITreasuryInvoiceWriter
        writer = self.request.find_service(ITreasuryInvoiceWriter)

        logger.debug(writer.headers)
        logger.debug(getattr(writer, 'extra_headers', ()))
        writer.set_datas(exporter.get_book_entries(invoices))
        write_file_to_request(
            self.request,
            get_timestamped_filename(u"export_facture", writer.extension),
            writer.render(),
            headers="application/csv")
        return self.request.response


class SageInvoiceExportPage(SageSingleInvoiceExportPage):
    """
        Provide a sage export view compound of :
            * a form for date to date invoice exports
            * a form for number to number invoice export
    """
    title = u"Export des factures au format CSV pour Sage"

    def populate_action_menu(self):
        self.request.actionmenu.add(
            ViewLink(
                label=u"Liste des factures",
                path='invoices',
            )
        )

    def get_forms(self):
        """
            Return the different invoice search forms
        """
        result = OrderedDict()
        period_form = get_period_form(self.request)
        number_form = get_invoice_number_form(
            self.request,
            period_form.counter,
        )
        all_form = get_all_form(
            self.request,
            period_form.counter
        )
        for form in all_form, number_form, period_form:
            result[form.formid] = {'form': form, 'title': form.schema.title}

        return result

    def _filter_date(self, query, start_date, end_date):
        return query.filter(Task.date.between(start_date, end_date))

    def _filter_number(self, query, start, end, year):
        logger.debug("Filtering numbers : %s %s" % (start, end))
        query = query.filter(Task.official_number >= start)
        query = query.filter(Task.official_number <= end)

        query = query.filter(
            or_(
                Invoice.financial_year == year,
                CancelInvoice.financial_year == year
            )
        )
        return query

    def query(self, query_params_dict, form_name):
        query = Task.get_valid_tasks()

        if form_name == 'period_form':
            start_date = query_params_dict['start_date']
            end_date = query_params_dict['end_date']
            query = self._filter_date(query, start_date, end_date)

        elif form_name == 'invoice_number_form':
            start = query_params_dict['start']
            end = query_params_dict['end']
            financial_year = query_params_dict['financial_year']
            query = self._filter_number(query, start, end, financial_year)

        if 'exported' not in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter(
                or_(
                    Invoice.exported == False,
                    CancelInvoice.exported == False,
                )
            )

        return query

    def check_num_invoices(self, invoices):
        return invoices.count()

    def validate_form(self, forms):
        return BaseExportView.validate_form(self, forms)


def add_routes(config):
    config.add_route(
        '/export/treasury/invoices',
        '/export/treasury/invoices'
    )
    config.add_route(
        '/export/treasury/invoices/{id}',
        '/export/treasury/invoices/{id}',
        traverse="/tasks/{id}"
    )


def add_views(config):
    config.add_view(
        SageSingleInvoiceExportPage,
        route_name='/export/treasury/invoices/{id}',
        renderer='/export/single.mako',
        permission='admin_treasury',
    )

    config.add_view(
        SageInvoiceExportPage,
        route_name='/export/treasury/invoices',
        renderer="/export/main.mako",
        permission='admin_treasury',
    )


def includeme(config):
    add_routes(config)
    add_views(config)
