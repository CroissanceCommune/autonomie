# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
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
    Sage export views
    Provide views to manage sage invoice exports

    from date to date
    from number to number (in a given year)
"""
import logging
import datetime
from sqlalchemy import or_

from deform import (
    Button,
    Form,
)
from deform.exception import ValidationFailure

from autonomie.compute.sage import (
    ExpensePaymentExport,
    MissingData,
)
from autonomie.export.sage import (
    SageExpensePaymentCsvWriter
)
from autonomie.export.utils import write_file_to_request
from autonomie.models.expense import (
    ExpenseSheet,
    ExpenseType,
    ExpensePayment,
)
from autonomie.models.task import (
    Task,
    Invoice,
    CancelInvoice,
    Payment,
)
from autonomie.forms.sage import (
    periodSchema,
    InvoiceNumberSchema,
    FromInvoiceNumberSchema,
    AllSchema,
    ExpenseSchema,
    ExpenseIdSchema,
)
from autonomie.views import BaseView
from autonomie.views.render_api import format_account

log = logging.getLogger(__name__)


EXPENSE_CONFIG_ERROR_MSG = u"Veuillez vous assurer que tous les éléments de \
configuration nécessaire à l'export des notes de dépense ont \
bien été fournis : <br /><a href='{0}' target='_blank'>Configuration des \
notes de dépense</a> <br/><a href='{1}' target='_blank'>Configuration \
comptables du module vente</a>"

EXPORT_BTN = Button(name="submit", type="submit", title=u"Exporter")


def get_filename(root_name, extension):
    """
    Return a filename with a date
    """
    today = datetime.date.today()
    return u"{0}_{1}.{2}".format(
        root_name,
        today.strftime("%d%m%Y"),
        extension,
    )


def get_period_form(title=u"Exporter les factures sur une période donnée"):
    """
        Return the period search form
    """
    schema = periodSchema
    schema.title = title
    return Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid='period_form',
    )


def get_all_form(counter, title=u"Exporter les factures non exportées"):
    """
    Return a void form used to export all non-exported documents
    """
    schema = AllSchema(title=title)
    return Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid='all_form',
        counter=counter,
    )


def get_from_invoice_number_form(counter, request):
    """
        Return the export criteria form used to export from a given invoice
    """
    schema = FromInvoiceNumberSchema(
        title=u"Exporter les factures à partir d'un numéro")
    schema = schema.bind(request=request)
    return Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid='from_invoice_number_form',
        counter=counter,
    )


def get_invoice_number_form(counter, request, title=u"Exporter une facture"):
    """
        Return the search form used to search invoices by number+year
    """
    schema = InvoiceNumberSchema(title=title)
    schema = schema.bind(request=request)
    return Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid='invoice_number_form',
        counter=counter,
    )


def get_expense_form(request):
    """
    Return a form for expense export
    """
    schema = ExpenseSchema(title=u"Exporter les notes de dépense")
    schema = schema.bind(request=request)
    return Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid="expense_form",
    )


def get_expense_id_form(counter, title=None):
    """
    Return a form for expense export by id
    :param counter: the iterator used to insert various forms in the same page
    """
    title = title or u"Exporter une notes de dépense depuis un identifiant"
    schema = ExpenseIdSchema(title=title)
    return Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid="expense_id_form",
        counter=counter,
    )


_HELPMSG_CONFIG = u"""Des éléments de configuration sont manquants, veuillez
configurer les informations comptables nécessaires à l'export des documents,
<a href="{0}" target='_blank'>Ici</a>"""


class SageInvoiceExportPage(BaseView):
    """
        Provide a sage export view compound of :
            * a form for date to date invoice exports
            * a form for number to number invoice export
    """
    title = u"Export des factures au format CSV pour Sage"

    def _filter_date(self, query, start_date, end_date):
        return query.filter(Task.date.between(start_date, end_date))

    def _filter_number(self, query, number, year, strict=False):
        prefix = self.request.config.get('invoiceprefix', '')

        if prefix and number.startswith(prefix):
            number = number[len(prefix):]

        if strict:
            query = query.filter(
                or_(Invoice.official_number == number,
                    CancelInvoice.official_number == number))
        else:
            query = query.filter(
                or_(Invoice.official_number >= number,
                    CancelInvoice.official_number >= number))

        return query.filter(
            or_(
                Invoice.financial_year == year,
                CancelInvoice.financial_year == year
            )
        )

    def query(self, query_params_dict):
        """
            Retrieve the exports we want to export
        """
        query = Task.get_valid_tasks()

        if 'start_date' in query_params_dict:
            start_date = query_params_dict['start_date']
            end_date = query_params_dict['end_date']
            query = self._filter_date(query, start_date, end_date)

        elif 'official_number' in query_params_dict:
            official_number = query_params_dict['official_number']
            financial_year = query_params_dict['financial_year']
            query = self._filter_number(
                query, official_number, financial_year, strict=True,
            )

        elif 'start_official_number' in query_params_dict:
            official_number = query_params_dict['start_official_number']
            financial_year = query_params_dict['financial_year']
            query = self._filter_number(
                query, official_number, financial_year, strict=False
            )

        if 'exported' not in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter(
                or_(
                    Invoice.exported == False,
                    CancelInvoice.exported == False,
                )
            )
        return query

    def check_invoice_line(self, line):
        """
            Check the invoice line is ok for export
        """
        return line.product is not None

    def check_company(self, company):
        """
            Check the invoice's company is configured for exports
        """
        if not company.code_compta:
            return False
        return True

    def check_customer(self, customer):
        """
            Check the invoice's customer is configured for exports

        """
        if not customer.compte_cg:
            return False
        if self.request.config.get('sage_rgcustomer'):
            if not customer.compte_tiers:
                return False
        return True

    def check(self, invoices):
        """
            Check that the given invoices are 'exportable'
        """
        count = invoices.count()
        if count == 0:
            title = u"Il n'y a aucune facture à exporter"
            res = {
                'title': title,
                'errors': [""],
            }
            return res
        title = u"Vous vous apprêtez à exporter {0} factures".format(
                count)
        res = {'title': title, 'errors': []}

        prefix = self.request.config.get('invoiceprefix', '')
        for invoice in invoices:
            official_number = "%s%s" % (prefix, invoice.official_number)
            for line in invoice.all_lines:
                if not self.check_invoice_line(line):
                    invoice_url = self.request.route_path(
                        'invoice',
                        id=invoice.id
                    )
                    message = u"""La facture {0} n'est pas exportable :
 des comptes produits sont manquants <a href='{1}' target='_blank'>
 Voir le document</a>"""
                    message = message.format(official_number, invoice_url)
                    res['errors'].append(message)
                    break

            if not self.check_company(invoice.company):
                company_url = self.request.route_path(
                    'company',
                    id=invoice.company.id,
                    _query={'action': 'edit'}
                )
                message = u"""La facture {0} n'est pas exportable :
Des informations sur l'entreprise {1} sont manquantes <a href='{2}'
target='_blank'>Voir l'entreprise</a>"""
                message = message.format(
                    official_number,
                    invoice.company.name,
                    company_url)
                res['errors'].append(message)
                continue

            if not self.check_customer(invoice.customer):
                customer_url = self.request.route_path(
                    'customer',
                    id=invoice.customer.id,
                    _query={'action': 'edit'})
                message = u"""La facture {0} n'est pas exportable :
 Des informations sur le client {1} sont manquantes <a href='{2}'
 target='_blank'>Voir l'entreprise</a>"""
                message = message.format(
                    official_number,
                    invoice.customer.name,
                    customer_url)
                res['errors'].append(message)
                continue

        return res

    def record_exported(self, invoices):
        for invoice in invoices:
            log.info(
                "The invoice number {1} (id : {0}) has been exported"
                .format(invoice.id, invoice.official_number)
            )
            invoice.exported = True
            self.request.dbsession.merge(invoice)

    def write_csv(self, invoices):
        """
            Write the exported csv file to the request
        """
        from autonomie.interfaces import ITreasuryInvoiceProducer
        exporter = self.request.find_service(ITreasuryInvoiceProducer)
        from autonomie.interfaces import ITreasuryInvoiceWriter
        writer = self.request.find_service(ITreasuryInvoiceWriter)

        writer.set_datas(exporter.get_book_entries(invoices))
        write_file_to_request(
            self.request,
            get_filename(u"export_facture", writer.extension),
            writer.render(),
            headers="application/csv")
        self.record_exported(invoices)
        return self.request.response

    def _forms_dict(self):
        """
            Return the different invoice search forms
        """
        _period_form = get_period_form()
        return {
            'all_form': get_all_form(_period_form.counter),
            'from_invoice_number_form': get_from_invoice_number_form(
                _period_form.counter, self.request),

            'period_form': _period_form,
            }

    def __call__(self):
        """
        Render data into 1) initial forms or 2) annotated forms or 3) form
        result

        :rtype: rendering datas (dict) or response object (csv file)
        """
        check_messages = appstruct = None
        forms = self._forms_dict()

        if 'submit' in self.request.params:
            post_values = self.request.POST.values()
            post_items = self.request.POST.items()

            for form_name, form in forms.iteritems():
                if form_name in post_values:
                    log.debug("Form %s was submitted", form_name)
                    try:
                        appstruct = form.validate(post_items)
                    except ValidationFailure as validation_error:
                        log.exception(u"There was an error on form validation")
                        log.exception(post_items)
                        # Replace the form, it now contains errors
                        # - will be displayed again
                        forms[form_name] = validation_error
                    break

            if appstruct is not None:
                invoices = self.query(appstruct)
                check_messages = self.check(invoices)

                if not check_messages.get('errors'):
                    try:
                        # Let's process and return successfully the csvfile
                        return self.write_csv(invoices)
                    except (MissingData, KeyError), validation_error:
                        log.exception("Exception occured while writing CSV \
file")
                        config_help_msg = _HELPMSG_CONFIG.format(
                            self.request.route_url("admin_vente")
                        )
                        check_messages['errors'] = [config_help_msg]

        # We are either
        # * reporting an error
        # * or doing the initial display of forms.

        # rendered forms
        rendered_forms = [form.render() for form in forms.values()]

        return {
            'title': self.title,
            'check_messages': check_messages,
            'forms': rendered_forms,
        }


class SageExpenseExportPage(BaseView):
    """
    Sage Expense export views
    """
    title = u"Export des notes de dépense au format CSV pour Sage"
    config_keys = ('compte_cg_ndf', 'code_journal_ndf',)
    contribution_config_keys = (
        'compte_cg_contribution', 'contribution_cae', 'numero_analytique',
    )

    def query(self, query_params_dict):
        """
        Base Query for expenses
        :param query_params_dict: params passed in the query for expense export
        """
        query = ExpenseSheet.query()
        query = query.filter(
            ExpenseSheet.status.in_(ExpenseSheet.valid_states)
        )

        if query_params_dict.get("sheet_id", 0) != 0:
            sheet_id = query_params_dict['sheet_id']
            query = query.filter(ExpenseSheet.id == sheet_id)

        else:
            if "year" in query_params_dict:
                year = query_params_dict['year']
                query = query.filter(ExpenseSheet.year == year)

                month = query_params_dict['month']
                query = query.filter(ExpenseSheet.month == month)
            if query_params_dict.get('user_id', 0) != 0:
                user_id = query_params_dict['user_id']
                query = query.filter(ExpenseSheet.user_id == user_id)

        if 'exported' not in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter(ExpenseSheet.exported == False)

        return query

    def check_config(self, config):
        """
        Check all configuration values are set for export

        :param config: The application configuration dict
        """
        contribution_is_active = False
        for type_ in ExpenseType.query().filter(ExpenseType.active == True):
            if not type_.code:  # or not type_.compte_tva or not type_.code_tva:
                return False
            if type_.contribution:
                contribution_is_active = True

        for key in self.config_keys:
            if not config.get(key):
                return False
            if contribution_is_active:
                for key in self.contribution_config_keys:
                    if not config.get(key):
                        return False
        return True

    def check_company(self, company):
        """
        Check if the company is fully configured

        :param company: The company we are exporting expenses from
        """
        if not company.code_compta:
            company_url = self.request.route_path(
                'company',
                id=company.id,
                _query={'action': 'edit'},
            )
            message = u""" Des informations sur l'entreprise {0}
sont manquantes <a href='{1}' target='_blank'>Voir l'entreprise</a>"""
            message = message.format(
                company.name,
                company_url)
            return message
        return None

    def check(self, expenses):
        """
        Check if we can export the expenses

        :param expenses: the expenses to export
        """
        count = expenses.count()
        if count == 0:
            title = u"Il n'y a aucune note de dépense à exporter"
            res = {
                'title': title,
                'errors': [""]
            }
            return res

        title = u"Vous vous apprêtez à exporter {0} notes de dépense".format(
                count)

        errors = []

        if not self.check_config(self.request.config):
            url1 = self.request.route_path('admin_expense')
            url2 = self.request.route_path('admin_vente')
            errors.append(EXPENSE_CONFIG_ERROR_MSG.format(url1, url2))

        for expense in expenses:
            company = expense.company
            error = self.check_company(company)
            if error is not None:
                errors.append(u"La note de dépense de {0} n'est pas exportable\
<br />{1}".format(format_account(expense.user), error))

        res = {'title': title, 'errors': errors}
        return res

    def record_exported(self, expenses):
        """
        Tag the exported expenses

        :param expenses: The expenses we are exporting
        """
        for expense in expenses:
            log.info(u"The expense with id {0} has been exported".format(
                expense.id))
            expense.exported = True
            self.request.dbsession.merge(expense)

    def write_csv(self, expenses):
        """
        Write the exported csv file to the request
        """
        from autonomie.interfaces import ITreasuryExpenseProducer
        exporter = self.request.find_service(ITreasuryExpenseProducer)

        from autonomie.interfaces import ITreasuryExpenseWriter
        writer = self.request.find_service(ITreasuryExpenseWriter)

        writer.set_datas(exporter.get_book_entries(expenses))
        write_file_to_request(
            self.request,
            get_filename(u"export_ndf", writer.extension),
            writer.render(),
            headers="application/csv")
        self.record_exported(expenses)
        return self.request.response

    def _forms_dict(self):
        """
        Return a dict with all form used in the export page
        """
        expense_form = get_expense_form(self.request)
        return {
            'expense_form': expense_form,
            'expense_id_form': get_expense_id_form(
                expense_form.counter
            ),
            'all_form': get_all_form(
                expense_form.counter,
                title=u"Exporter les notes de dépense non exportées",
            )
        }

    def __call__(self):
        """
        Render data into 1) initial forms or 2) annotated forms or 3) form
        result

        :rtype: rendering datas (dict) or response object (csv file)
        """
        check_messages = appstruct = None
        forms = self._forms_dict()

        if 'submit' in self.request.params:
            post_values = self.request.POST.values()
            post_items = self.request.POST.items()

            for form_name, form in forms.iteritems():
                if form_name in post_values:
                    log.debug("Form %s was submitted", form_name)
                    try:
                        appstruct = form.validate(post_items)
                    except ValidationFailure as validation_error:
                        log.exception(u"There was an error on form validation")
                        log.exception(post_items)
                        # Replace the form, it now contains errors
                        # - will be displayed again
                        forms[form_name] = validation_error
                    break

            if appstruct is not None:
                expenses = self.query(appstruct)
                check_messages = self.check(expenses)

                if not check_messages.get('errors'):
                    try:
                        # Let's process and return successfully the csvfile
                        return self.write_csv(expenses)
                    except (MissingData, KeyError), validation_error:
                        log.exception("Exception occured while writing CSV \
file")
                        config_help_msg = _HELPMSG_CONFIG.format(
                            self.request.route_url("admin_expense")
                        )
                        check_messages['errors'] = [config_help_msg]

        # We are either
        # * reporting an error
        # * or doing the initial display of forms.

        # rendered forms
        rendered_forms = [form.render() for form in forms.values()]

        return {
            'title': self.title,
            'check_messages': check_messages,
            'forms': rendered_forms,
        }


class SagePaymentExportPage(BaseView):
    """
    Provide a sage export view compound of multiple forms for payment exports
    """
    title = u"Export des encaissements au format CSV pour Sage"

    def _filter_date(self, query, start_date, end_date):
        return query.filter(
            Payment.date.between(start_date, end_date)
        )

    def _filter_number(self, query, number, year):
        prefix = self.request.config.get('invoiceprefix', '')
        if prefix and number.startswith(prefix):
            number = number[len(prefix):]

        inv_query = self.request.dbsession.query(Invoice.id)
        inv_query = inv_query.filter(Invoice.official_number == number)
        inv_query = inv_query.filter(Invoice.financial_year == year)

        task_id = inv_query.first()
        if task_id is None:
            task_id = -1
        else:
            task_id = task_id[0]
        return query.filter(Payment.task_id == task_id)

    def query(self, query_params_dict):
        """
            Retrieve the exports we want to export
        """
        query = Payment.query()

        if 'start_date' in query_params_dict:
            start_date = query_params_dict['start_date']
            end_date = query_params_dict['end_date']
            query = self._filter_date(query, start_date, end_date)

        elif 'official_number' in query_params_dict:
            official_number = query_params_dict['official_number']
            financial_year = query_params_dict['financial_year']
            query = self._filter_number(
                query, official_number, financial_year,
            )

        if 'exported' not in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter(Payment.exported == False)

        return query

    def check_customer(self, customer):
        """
            Check the invoice's customer is configured for exports
        """
        if not customer.compte_cg:
            return False
        if not customer.compte_tiers:
            return False
        return True

    def check_bank(self, payment):
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
            title = u"Il n'y a aucun encaissement à exporter"
            res = {
                'title': title,
                'errors': [""],
            }
            return res
        title = u"Vous vous apprêtez à exporter {0} encaissements".format(
                count)
        res = {'title': title, 'errors': []}
        for payment in payments:
            invoice = payment.invoice
            if not self.check_customer(invoice.customer):
                customer_url = self.request.route_path(
                    'customer',
                    id=invoice.customer.id,
                    _query={'action': 'edit'})
                message = u"""Un encaissement de la facture {0} n'est pas
exportable : Des informations sur le client {1} sont manquantes
 <a href='{2}' target='_blank'>Voir le client</a>"""
                message = message.format(
                    invoice.official_number,
                    invoice.customer.name,
                    customer_url)
                res['errors'].append(message)
                continue

            if not self.check_bank(payment):
                payment_url = self.request.route_path(
                    'payment',
                    id=payment.id,
                    _query={'action': 'edit'})
                message = u"""Un encaissement de la facture {0} n'est pas \
exportable : L'encaissement n'est associé à aucune banque <a href='{1}'
target='_blank'>Voir l'encaissement</a>"""
                message = message.format(
                    invoice.official_number,
                    payment_url)
                res['errors'].append(message)
                continue

        return res

    def record_exported(self, payments):
        for payment in payments:
            log.info(
                u"The payment id : {0} (invoice {1} id:{2}) has been exported"
                .format(
                    payment.id,
                    payment.invoice.official_number,
                    payment.invoice.id,
                )
            )
            payment.exported = True
            self.request.dbsession.merge(payment)

    def write_csv(self, payments):
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
            get_filename(u"export_encaissement", writer.extension),
            writer.render(),
            headers="application/csv")
        self.record_exported(payments)
        return self.request.response

    def _forms_dict(self):
        """
        Return the different payment search forms
        """
        _period_form = get_period_form(
            title=u"Exporter les encaissements saisis sur la période donnée"
        )
        return {
            'all_form': get_all_form(
                _period_form.counter,
                title=u"Exporter les encaissements non exportés",
            ),
            'invoice_number_form': get_invoice_number_form(
                _period_form.counter, self.request,
                title=u"Exporter les encaissements correspondant à une facture",
            ),
            'period_form': _period_form,
            }

    def __call__(self):
        """
        Render data into 1) initial forms or 2) annotated forms or 3) form
        result

        :rtype: rendering datas (dict) or response object (csv file)
        """
        check_messages = appstruct = None
        forms = self._forms_dict()

        if 'submit' in self.request.params:
            post_values = self.request.POST.values()
            post_items = self.request.POST.items()

            for form_name, form in forms.iteritems():
                if form_name in post_values:
                    log.debug("Form %s was submitted", form_name)
                    try:
                        appstruct = form.validate(post_items)
                    except ValidationFailure as validation_error:
                        log.exception(u"There was an error on form validation")
                        log.exception(post_items)
                        # Replace the form, it now contains errors
                        # - will be displayed again
                        forms[form_name] = validation_error
                    break

            if appstruct is not None:
                payments = self.query(appstruct)
                print(payments)
                check_messages = self.check(payments)

                if not check_messages.get('errors'):
                    try:
                        # Let's process and return successfully the csvfile
                        return self.write_csv(payments)
                    except (MissingData, KeyError), validation_error:
                        log.exception("Exception occured while writing CSV \
file")
                        config_help_msg = _HELPMSG_CONFIG.format(
                            self.request.route_url("admin_receipts")
                        )
                        check_messages['errors'] = [config_help_msg]

        # We are either
        # * reporting an error
        # * or doing the initial display of forms.

        # rendered forms
        rendered_forms = [form.render() for form in forms.values()]

        return {
            'title': self.title,
            'check_messages': check_messages,
            'forms': rendered_forms,
        }


ERR_COMPANY_CONFIG = u"""Un paiement de la feuille de notes de dépense {0}
n'est pas exportable : Des informations sur l'entreprise sont manquantes : {1}
<a href='{2}' target='_blank'>Voir l'entreprise</a>"""
ERR_USER_CONFIG = u"""Un paiement de la feuille de notes de dépense {0}
n'est pas exportable : Des informations sur l'entrepreneur sont manquantes : {1}
<a href='{2}' target='_blank'>Voir l'entrepreneur</a>"""
ERR_BANK_CONFIG = u"""Un paiement de la feuille de notes de dépense {0}
n'est pas exportable : Le paiement n'est associé à aucune banque
<a href='{1}' target='_blank'>Voir le paiement</a>"""
ERR_WAIVER_CONFIG = u"""Le compte pour les abandons de créances n'a pas
été configuré, vous pouvez le configurer <a href='{0}' target='_blank'>Ici</a>
"""


class SageExpensePaymentExportPage(BaseView):
    """
    Provide an expense payment export page
    """
    title = u"Export des règlements de notes de frais au format CSV pour Sage"

    def _filter_date(self, query, start_date, end_date):
        return query.filter(
            ExpensePayment.created_at.between(start_date, end_date)
        )

    def _filter_number(self, query, expense_id):
        return query.filter(ExpensePayment.expense_id == expense_id)

    def query(self, query_params_dict):
        """
            Retrieve the exports we want to export
        """
        query = ExpensePayment.query()

        if 'start_date' in query_params_dict:
            start_date = query_params_dict['start_date']
            end_date = query_params_dict['end_date']
            query = self._filter_date(query, start_date, end_date)

        elif 'expense_id' in query_params_dict:
            expense_id = query_params_dict['expense_id']
            query = self._filter_number(
                query,
                expense_id,
            )

        if 'exported' not in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter(ExpensePayment.exported == False)

        return query

    def check_bank(self, payment):
        if not payment.bank and not payment.waiver:
            return False
        return True

    def check_company(self, company):
        if not company.code_compta:
            return False
        return True

    def check_user(self, user):
        if not user.compte_tiers:
            return False
        return True

    def check_waiver(self, payment):
        """
        Check that the wayver cg account has been configured
        """
        if not self.request.config.get('compte_cg_waiver_ndf'):
            return False
        return True

    def check(self, payments):
        """
        Check that the given expense_payments can be exported

        :param obj payments: A SQLA query of ExpensePayment objects
        """
        count = payments.count()
        if count == 0:
            title = u"Il n'y a aucun paiement à exporter"
            res = {
                'title': title,
                'errors': [''],
            }
            return res

        title = u"Vous vous apprêtez à exporter {0} paiements".format(
                count)
        res = {'title': title, 'errors': []}

        for payment in payments:
            expense = payment.expense
            company = expense.company
            if not self.check_company(company):
                company_url = self.request.route_path(
                    "company",
                    id=company.id,
                    _query={'action': 'edit'},
                )
                message = ERR_COMPANY_CONFIG.format(
                    expense.id,
                    company.name,
                    company_url,
                )
                res['errors'].append(message)
                continue

            user = expense.user
            if not self.check_user(user):
                user_url = self.request.route_path(
                    "user",
                    id=user.id,
                    _query={'action': 'edit'},
                )
                message = ERR_USER_CONFIG.format(
                    expense.id,
                    format_account(user),
                    user_url,
                )
                res['errors'].append(message)
                continue

            if not self.check_bank(payment):
                payment_url = self.request.route_path(
                    'expensepayment',
                    id=payment.id,
                    _query={'action': 'edit'}
                )
                message = ERR_BANK_CONFIG.format(
                    expense.id,
                    payment_url)
                res['errors'].append(message)
                continue

            if payment.waiver and not self.check_waiver(payment):
                admin_url = self.request.route_path(
                    'admin_expense_treasury'
                )
                message = ERR_WAIVER_CONFIG.format(admin_url)
                res['errors'].append(message)
                continue

        return res

    def record_exported(self, payments):
        """
        Record that those payments have already been exported
        """
        for payment in payments:
            log.info(
                u"The payment id : {0} (expense {1}) has been exported"
                .format(
                    payment.id,
                    payment.expense.id,
                )
            )
            payment.exported = True
            self.request.dbsession.merge(payment)

    def write_csv(self, payments):
        """
        Write the exported csv file to the request
        """
        exporter = ExpensePaymentExport(self.context, self.request)
        writer = SageExpensePaymentCsvWriter()
        writer.set_datas(exporter.get_book_entries(payments))
        write_file_to_request(
            self.request,
            get_filename(u"export_paiement_ndf", writer.extension),
            writer.render(),
            headers="application/csv")
        self.record_exported(payments)
        return self.request.response

    def _forms_dict(self):
        """
        Return the different payment search forms
        """
        period_form = get_period_form(
            title=u"Exporter les paiements saisis sur la période donnée"
        )
        return {
            'all_form': get_all_form(
                period_form.counter,
                title=u"Exporter les paiements non exportés",
            ),
            'expense_id_form': get_expense_id_form(
                period_form.counter,
                title=u"Exporter les paiements correspondant à une feuille \
de notes de dépense",
            ),
            'period_form': period_form,
        }

    def __call__(self):
        """
        Render data into 1) initial forms or 2) annotated forms or 3) form
        result

        :rtype: rendering datas (dict) or response object (csv file)
        """
        check_messages = appstruct = None
        forms = self._forms_dict()

        if 'submit' in self.request.params:
            post_values = self.request.POST.values()
            post_items = self.request.POST.items()

            for form_name, form in forms.iteritems():
                if form_name in post_values:
                    log.debug("Form %s was submitted", form_name)
                    try:
                        appstruct = form.validate(post_items)
                    except ValidationFailure as validation_error:
                        log.exception(u"There was an error on form validation")
                        log.exception(post_items)
                        # Replace the form, it now contains errors
                        # - will be displayed again
                        forms[form_name] = validation_error
                    break

            if appstruct is not None:
                payments = self.query(appstruct)
                check_messages = self.check(payments)

                if not check_messages.get('errors'):
                    try:
                        # Let's process and return successfully the csvfile
                        return self.write_csv(payments)
                    except (MissingData, KeyError), validation_error:
                        log.exception("Exception occured while writing CSV \
file")
                        config_help_msg = _HELPMSG_CONFIG.format(
                            self.request.route_url("admin_expense_treasury")
                        )
                        check_messages['errors'] = [config_help_msg]

        # We are either
        # * reporting an error
        # * or doing the initial display of forms.

        # rendered forms
        rendered_forms = [form.render() for form in forms.values()]

        return {
            'title': self.title,
            'check_messages': check_messages,
            'forms': rendered_forms,
        }


def includeme(config):
    """
    Add routes and views for this module
    """
    for name, page_obj in (
        ('invoice', SageInvoiceExportPage),
        ('expense', SageExpenseExportPage),
        ('payment', SagePaymentExportPage),
        ('expense_payment', SageExpensePaymentExportPage),
    ):
        route = "sage_{0}_export".format(name)
        config.add_route(route, "/" + route)

        config.add_view(
            page_obj,
            route_name=route,
            renderer="admin/sage_export.mako",
            permission="admin_treasury"
        )
