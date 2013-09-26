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

from deform import (
        Button,
        Form,
        )
from deform.exception import ValidationFailure

from autonomie.compute.sage import SageExport as ComputeSageExport
from autonomie.export.sage import SageCsvWriter
from autonomie.export.csvtools import write_csv_to_request

from autonomie.models.task import Invoice
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


    def query_invoices(self, query_params_dict):
        """
            Retrieve the exports we want to export
        """
        query = Invoice.query().filter(Invoice.CAEStatus\
                .in_(Invoice.valid_states))

        if 'start_date' in query_params_dict:
            start_date = query_params_dict['start_date']
            end_date = query_params_dict['end_date']
            query = query.filter(Invoice.taskDate.between(start_date, end_date))
        elif 'officialNumber' in query_params_dict:
            officialNumber = query_params_dict['officialNumber']
            query = query.filter(Invoice.officialNumber == officialNumber)
            financial_year = query_params_dict['financial_year']
            query = query.filter(Invoice.financial_year == financial_year)
        elif 'start_officialNumber' in query_params_dict:
            officialNumber = query_params_dict['start_officialNumber']
            query = query.filter(Invoice.officialNumber >= officialNumber)
            financial_year = query_params_dict['financial_year']
            query = query.filter(Invoice.financial_year == financial_year)
        if not 'exported' in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter(Invoice.exported == False)
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
        for module in ('sage_contribution', 'sage_assurance', 'sage_cgscop',
                'sage_rginterne'):
            if self.request.config.get('module'):
                if not company.compte_cg_banque:
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

    def write_csv(self, invoices):
        """
            Write the exported csv file to the request
        """
        exporter = ComputeSageExport(self.request.config)
        writer = SageCsvWriter(exporter.get_book_entries(invoices))
        write_csv_to_request(self.request, self.filename, writer.render())
        return self.request.response

    def __call__(self):
        period_form = get_period_form()
        invoice_number_form = get_invoice_number_form(period_form.counter,
                self.request)
        from_invoice_number_form = get_from_invoice_number_form(
                period_form.counter,
                self.request)
        all_form = get_all_form(period_form.counter)
        log.debug("Here we are")
        log.debug(self.request.params)
        check_messages = None

        if 'submit' in self.request.params:
            log.debug(u"A form has been submitted")
            if "invoice_number_form" in self.request.POST.values():
                log.debug(u"It's the invoice_number_form")
                try:
                    appstruct = invoice_number_form.validate(
                            self.request.POST.items())
                except ValidationFailure as e:
                    invoice_number_form = e

            elif "from_invoice_number_form" in self.request.POST.values():
                log.debug(u"It's the from_invoice_number_form")
                try:
                    appstruct = from_invoice_number_form.validate(
                            self.request.POST.items())
                except ValidationFailure as e:
                    from_invoice_number_form = e


            elif "period_form" in self.request.POST.values():
                log.debug(u"It's the period form")
                try:
                    appstruct = period_form.validate(self.request.POST.items())
                except ValidationFailure as e:
                    period_form = e
            elif "all_form" in self.request.POST.values():
                log.debug(u"Ask for all non-validate invoices")
                try:
                    appstruct = all_form.validate(self.request.POST.items())
                except ValidationFailure as e:
                    all_form = e
            invoices = self.query_invoices(appstruct)
            log.debug(u"We want to export some invoices : '{0}' invoices"\
                    .format(len(invoices.all())))
            check_messages = self.check_invoices(invoices)
            if check_messages['errors'] == []:
                return self.write_csv(invoices)

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
