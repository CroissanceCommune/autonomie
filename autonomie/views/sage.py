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
import itertools
import logging
import datetime
from sqlalchemy import or_, and_

from deform import (
        Button,
        Form,
        )
from deform.exception import ValidationFailure

from autonomie.compute.sage import (
        InvoiceExport,
        MissingData,
        ExpenseExport,
        )
from autonomie.export.sage import (
        SageInvoiceCsvWriter,
        SageExpenseCsvWriter,
        )
from autonomie.export.utils import write_file_to_request

from autonomie.models.task import (
        Task,
        Invoice,
        CancelInvoice,)
from autonomie.views.base import BaseView
from autonomie.views.forms.sage import (
        periodSchema,
        InvoiceNumberSchema,
        FromInvoiceNumberSchema,
        AllSchema,
        ExpenseSchema,
        ExpenseIdSchema,
        )
from autonomie.views.render_api import format_account
from autonomie.models.treasury import (
        ExpenseSheet,
        ExpenseType,
        )

log = logging.getLogger(__name__)


EXPENSE_CONFIG_ERROR_MSG = u"Veuillez vous assurer que tous les éléments de \
configuration nécessaire à l'export des notes de frais ont \
bien été fournis : <br /><a href='{0}'>Configuration des notes de frais</a> \
<br/><a href='{1}'>Configuration des informations comptables de la CAE</a>"

EXPORT_BTN = Button(name="submit", type="submit", title=u"Exporter")

def get_period_form():
    """
        Return the period search form
    """
    schema = periodSchema
    return Form(schema=schema,
            buttons=(EXPORT_BTN,),
            formid='period_form')


def get_from_invoice_number_form(counter, request):
    """
        Return the export criteria form used to export from a given invoice
    """
    schema = FromInvoiceNumberSchema(
            title=u"Exporter les factures à partir d'un numéro")
    schema = schema.bind(request=request)
    return Form(schema=schema,
            buttons=(EXPORT_BTN,),
            formid='from_invoice_number_form',
            counter=counter)



def get_invoice_number_form(counter, request):
    """
        Return the search form used to search invoices by number+year
    """
    schema = InvoiceNumberSchema(title=u"Exporter une facture")
    schema = schema.bind(request=request)
    return Form(schema=schema,
            buttons=(EXPORT_BTN,),
            formid='invoice_number_form',
            counter=counter)


def get_all_form(counter):
    """
    Return a void form used to export all non-exported documents
    """
    schema = AllSchema(title=u"Exporter les documents non exportées")
    return Form(schema=schema,
            buttons=(EXPORT_BTN,),
            formid='all_form',
            counter=counter)

def get_expense_form(request):
    """
    Return a form for expense export
    """
    schema = ExpenseSchema(title=u"Exporter les notes de frais")
    schema = schema.bind(request=request)
    return Form(schema=schema,
            buttons=(EXPORT_BTN,),
            formid="expense_form")

def get_expense_id_form(counter):
    """
    Return a form for expense export by id
    :param counter: the iterator used to insert various forms in the same page
    """
    schema = ExpenseIdSchema(title=u"Exporter une notes de frais depuis \
un identifiant")
    return Form(schema=schema,
            buttons=(EXPORT_BTN,),
            formid="expense_id_form",
            counter=counter)


_HELPMSG_CONFIG = u"""Des éléments de configuration sont manquants, veuillez
configurer les informations comptables nécessaires à l'export des documents,
dans Configuration->Configuration des informations comptables de la CAE"""


class SageInvoiceExportPage(BaseView):
    """
        Provide a sage export view compound of :
            * a form for date to date invoice exports
            * a form for number to number invoice export
    """
    title = u"Export des factures au format CSV pour Sage"

    @property
    def filename(self):
        today = datetime.date.today()
        return u"export_facture_{0}.txt".format(today.strftime("%d%m%Y"))

    def _filter_valid(self, query):
        inv_validated = Invoice.valid_states
        cinv_valid = CancelInvoice.valid_states
        return query.filter(or_(and_(Task.CAEStatus.in_(inv_validated),
            Task.type_=='invoice'),
            and_(Task.CAEStatus.in_(cinv_valid),
                Task.type_=='cancelinvoice')))

    def _filter_date(self, query, start_date, end_date):
        return query.filter(Task.taskDate.between(start_date, end_date))

    def _filter_number(self, query, number, year, strict=False):
        prefix = self.request.config.get('invoiceprefix', '')
        number = number.strip(prefix)
        if strict:
            query = query.filter(
                or_(Invoice.officialNumber == number,
                    CancelInvoice.officialNumber  == number))
        else:
            query = query.filter(
                or_(Invoice.officialNumber >= number,
                    CancelInvoice.officialNumber  >= number))

        return query.filter(
                or_(Invoice.financial_year == year,
                    CancelInvoice.financial_year == year))

    def query(self, query_params_dict):
        """
            Retrieve the exports we want to export
        """
        query = Task.query().with_polymorphic([Invoice, CancelInvoice])
        query = self._filter_valid(query)


        if 'start_date' in query_params_dict:
            start_date = query_params_dict['start_date']
            end_date = query_params_dict['end_date']
            query = self._filter_date(query, start_date, end_date)
        elif 'officialNumber' in query_params_dict:
            officialNumber = query_params_dict['officialNumber']
            financial_year = query_params_dict['financial_year']
            query = self._filter_number(query, officialNumber, financial_year,
                    strict=True)
        elif 'start_officialNumber' in query_params_dict:
            officialNumber = query_params_dict['start_officialNumber']
            financial_year = query_params_dict['financial_year']
            query = self._filter_number(query, officialNumber, financial_year,
                    strict=False)
        if not 'exported' in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter(or_(Invoice.exported == False,
                                     CancelInvoice.exported == False))
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
            res = {'title': title,
                    'errors': [""]}
            return res
        title = u"Vous vous apprêtez à exporter {0} factures".format(
                count)
        res = {'title': title, 'errors':[]}

        prefix = self.request.config.get('invoiceprefix', '')
        for invoice in invoices:
            officialNumber = "%s%s" % (prefix, invoice.officialNumber)
            for line in invoice.lines:
                if not self.check_invoice_line(line):
                    invoice_url = self.request.route_path('invoice',
                            id=invoice.id)
                    message = u"La facture {0} n'est pas exportable :"
                    message += u" des comptes produits sont manquants"
                    message += u" <a href='{1}'>Voir le document</a>"
                    message = message.format(officialNumber, invoice_url)
                    res['errors'].append(message)
                    break


            if not self.check_company(invoice.company):
                company_url = self.request.route_path(
                        'company',
                        id=invoice.company.id,
                        _query={'action':'edit'})
                message = u"La facture {0} n'est pas exportable :"
                message += u" Des informations sur l'entreprise {1} \
sont manquantes"
                message += u" <a href='{2}'>Voir l'entreprise</a>"
                message = message.format(
                        officialNumber,
                        invoice.company.name,
                        company_url)
                res['errors'].append(message)
                continue



            if not self.check_customer(invoice.customer):
                customer_url = self.request.route_path(
                        'customer',
                        id=invoice.customer.id,
                        _query={'action':'edit'})
                message = u"La facture {0} n'est pas exportable :"
                message += u" Des informations sur le client {1} \
sont manquantes"
                message += u" <a href='{2}'>Voir l'entreprise</a>"
                message = message.format(
                        officialNumber,
                        invoice.customer.name,
                        customer_url)
                res['errors'].append(message)
                continue


        return res

    def record_exported(self, invoices):
        for invoice in invoices:
            log.info("The invoice number {1} (id : {0}) has been exported"\
                    .format(invoice.id, invoice.officialNumber))
            invoice.exported = True
            self.request.dbsession.merge(invoice)


    def write_csv(self, invoices):
        """
            Write the exported csv file to the request
        """
        exporter = InvoiceExport(self.request.config)
        writer = SageInvoiceCsvWriter()
        writer.set_prefix(self.request.config.get('invoice_prefix', ''))
        writer.set_datas(exporter.get_book_entries(invoices))
        write_file_to_request(
                self.request,
                self.filename,
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
            'invoice_number_form': get_invoice_number_form(_period_form.counter,
                self.request),
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
                        check_messages['errors'] = [_HELPMSG_CONFIG]

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
    title = u"Export des notes de frais au format CSV pour Sage"
    config_keys = ('compte_cg_ndf', 'code_journal_ndf',)
    contribution_config_keys = ('compte_cg_contribution',
            'contribution_cae', 'numero_analytique')

    @property
    def filename(self):
        today = datetime.date.today()
        return u"export_ndf_{0}.txt".format(today.strftime("%d%m%Y"))

    def query(self, query_params_dict):
        """
        Base Query for expenses
        :param query_params_dict: params passed in the query for expense export
        """
        query = ExpenseSheet.query()
        query = query.filter(ExpenseSheet.status.in_(['valid', 'resulted']))

        if query_params_dict.get("sheet_id", 0) != 0:
            sheet_id = query_params_dict['sheet_id']
            query = query.filter(ExpenseSheet.id==sheet_id)

        else:
            if "year" in query_params_dict:
                year = query_params_dict['year']
                query = query.filter(ExpenseSheet.year==year)

                month = query_params_dict['month']
                query = query.filter(ExpenseSheet.month==month)
            if query_params_dict.get('user_id', 0) != 0:
                user_id = query_params_dict['user_id']
                query = query.filter(ExpenseSheet.user_id==user_id)

        if not 'exported' in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter(ExpenseSheet.exported == False)

        return query

    def check_config(self, config):
        """
        Check all configuration values are set for export

        :param config: The application configuration dict
        """
        contribution_is_active = False
        for type_ in ExpenseType.query().filter(ExpenseType.active==True):
            if not type_.code: # or not type_.compte_tva or not type_.code_tva:
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
        if not company.code_compta or not company.compte_tiers:
            company_url = self.request.route_path(
                    'company',
                    id=company.id,
                    _query={'action':'edit'},
                    )
            message = u" Des informations sur l'entreprise {0} \
sont manquantes"
            message += u" <a href='{1}'>Voir l'entreprise</a>"
            message = message.format(
                    company.name,
                    company_url)
            return message
        return None

    def check(self, expenses) :
        """
        Check if we can export the expenses

        :param expenses: the expenses to export
        """
        count = expenses.count()
        if count == 0:
            title = u"Il n'y a aucune note de frais à exporter"
            res = {'title': title,
                    'errors': [""]}
            return res

        title = u"Vous vous apprêtez à exporter {0} notes de frais".format(
                count)

        errors = []

        if not self.check_config(self.request.config):
            url1 = self.request.route_path('admin_expense')
            url2 = self.request.route_path('admin_cae')
            errors.append(EXPENSE_CONFIG_ERROR_MSG.format(url1, url2))

        for expense in expenses:
            company = expense.company
            error = self.check_company(company)
            if error is not None:
                errors.append(u"La note de frais de {0} n'est pas exportable\
<br />{1}".format(format_account(expense.user), error))

        res = {'title': title, 'errors':errors}
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
        exporter = ExpenseExport(self.request.config)
        writer = SageExpenseCsvWriter()
        writer.set_datas(exporter.get_book_entries(expenses))
        write_file_to_request(
                self.request,
                self.filename,
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
                'expense_id_form': get_expense_id_form(expense_form.counter),
                'all_form': get_all_form(expense_form.counter)
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
                        check_messages['errors'] = [_HELPMSG_CONFIG]

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
    for name, page_obj in (('invoice', SageInvoiceExportPage),
            ('expense', SageExpenseExportPage)):
        route = "sage_{0}_export".format(name)
        config.add_route(route, "/" + route)

        config.add_view(page_obj,
            route_name=route,
            renderer="admin/sage_export.mako",
            permission="admin")
