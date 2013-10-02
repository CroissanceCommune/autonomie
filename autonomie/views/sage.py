# -*- coding: utf-8 -*-
# * File Name : sage.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 24-09-2013
# * Last Modified :
#
# * Project :
#
"""
    Sage export views
    Provide views to manage sage invoice exports

    from date to date
    from number to number (in a given year)
"""
import logging
import datetime
from sqlalchemy import or_, and_

from deform import (
        Button,
        Form,
        )
from deform.exception import ValidationFailure

from autonomie.compute.sage import (
        SageExport as ComputeSageExport,
        MissingData,
        )
from autonomie.export.sage import SageCsvWriter
from autonomie.export.csvtools import write_csv_to_request

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
        )

log = logging.getLogger(__name__)

def get_period_form():
    """
        Return the period search form
    """
    submit_btn = Button(name="submit", type="submit",
            title=u"Exporter")
    schema = periodSchema
    return Form(schema=schema,
            buttons=(submit_btn,),
            formid='period_form')


def get_from_invoice_number_form(counter, request):
    """
        Return the export criteria form used to export from a given invoice
    """
    submit_btn = Button(name="submit", type="submit",
            title=u"Exporter")
    schema = FromInvoiceNumberSchema(
            title=u"Exporter les factures à partir d'un numéro")
    schema = schema.bind(request=request)
    return Form(schema=schema,
            buttons=(submit_btn,),
            formid='from_invoice_number_form',
            counter=counter)



def get_invoice_number_form(counter, request):
    """
        Return the search form used to search invoices by number+year
    """
    submit_btn = Button(name="submit", type="submit",
            title=u"Exporter")
    schema = InvoiceNumberSchema(title=u"Exporter une facture")
    schema = schema.bind(request=request)
    return Form(schema=schema,
            buttons=(submit_btn,),
            formid='invoice_number_form',
            counter=counter)


def get_all_form(counter):
    """
        Return a void form used to export all non-exported invoices
    """
    submit_btn = Button(name="submit", type="submit",
            title=u"Exporter")
    schema = AllSchema(title=u"Exporter les factures non exportées")
    return Form(schema=schema,
            buttons=(submit_btn,),
            formid='all_form',
            counter=counter)


class SageExportPage(BaseView):
    """
        Provide a sage export view compound of :
            * a form for date to date invoice exports
            * a form for number to number invoice export
    """
    title = "Export des factures au format CSV pour Sage"

    @property
    def filename(self):
        today = datetime.date.today()
        return u"export_facture_{:%d%m%Y}.csv".format(today)

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

    def query_invoices(self, query_params_dict):
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


    def check_client(self, client):
        """
            Check the invoice's client is configured for exports
        """
        if not client.compte_cg:
            return False
        if self.request.config.get('sage_rgclient'):
            if not client.compte_tiers:
                return False
        return True

    def check_invoices(self, invoices):
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

        for invoice in invoices:
            officialNumber = invoice.officialNumber
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



            if not self.check_client(invoice.client):
                client_url = self.request.route_path(
                        'client',
                        id=invoice.client.id,
                        _query={'action':'edit'})
                message = u"La facture {0} n'est pas exportable :"
                message += u" Des informations sur le client {1} \
sont manquantes"
                message += u" <a href='{2}'>Voir l'entreprise</a>"
                message = message.format(
                        officialNumber,
                        invoice.client.name,
                        client_url)
                res['errors'].append(message)
                continue


        return res

    def record_invoices_exported(self, invoices):
        for invoice in invoices:
            log.info("The invoice number {1} (id : {0}) has been exported"\
                    .format(invoice.id, invoice.officialNumber))
            invoice.exported = True
            self.request.dbsession.merge(invoice)


    def write_csv(self, invoices):
        """
            Write the exported csv file to the request
        """
        exporter = ComputeSageExport(self.request.config)
        writer = SageCsvWriter(exporter.get_book_entries(invoices))
        write_csv_to_request(self.request, self.filename, writer.render())
        self.record_invoices_exported(invoices)
        return self.request.response

    def __call__(self):
        period_form = get_period_form()
        invoice_number_form = get_invoice_number_form(period_form.counter,
                self.request)
        from_invoice_number_form = get_from_invoice_number_form(
                period_form.counter,
                self.request)
        all_form = get_all_form(period_form.counter)
        check_messages = None

        if 'submit' in self.request.params:
            if "invoice_number_form" in self.request.POST.values():
                try:
                    appstruct = invoice_number_form.validate(
                            self.request.POST.items())
                except ValidationFailure as e:
                    invoice_number_form = e

            elif "from_invoice_number_form" in self.request.POST.values():
                try:
                    appstruct = from_invoice_number_form.validate(
                            self.request.POST.items())
                except ValidationFailure as e:
                    from_invoice_number_form = e


            elif "period_form" in self.request.POST.values():
                try:
                    appstruct = period_form.validate(self.request.POST.items())
                except ValidationFailure as e:
                    period_form = e
            elif "all_form" in self.request.POST.values():
                try:
                    appstruct = all_form.validate(self.request.POST.items())
                except ValidationFailure as e:
                    all_form = e
            invoices = self.query_invoices(appstruct)
            check_messages = self.check_invoices(invoices)
            if check_messages['errors'] == []:
                try:
                    return self.write_csv(invoices)
                except (MissingData, KeyError), e:
                    check_messages['errors'] = [u"Des éléments de \
configuration sont manquants, veuillez configurer \
les informations comptables nécessaires à l'export des documents, \
dans Configuration->Configuration des informations comptables de la CAE"]

        return dict(title=self.title,
                period_form=period_form.render(),
                invoice_number_form=invoice_number_form.render(),
                all_form=all_form.render(),
                from_invoice_number_form=from_invoice_number_form.render(),
                check_messages=check_messages)


def includeme(config):
    config.add_route("sage_export", "/sage_export")
    config.add_view(SageExportPage,
            route_name="sage_export",
            renderer="admin/sage_export.mako",
            permission="admin")
