# -*- coding: utf-8 -*-
# * File Name : invoice.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-05-2012
# * Last Modified :
#
# * Project :
#
"""
    Invoice views
"""
import logging
import datetime

from deform import ValidationFailure
from deform import Form
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_path

from autonomie.models.model import Invoice
from autonomie.models.model import Project
from autonomie.models.model import ManualInvoice
from autonomie.models.model import InvoiceLine
from autonomie.models.model import format_to_taskdate
from autonomie.views.forms.estimation import InvoiceSchema
from autonomie.views.forms.estimation import get_invoice_appstruct
from autonomie.views.forms.estimation import get_invoice_dbdatas
from autonomie.views.forms.estimation import TaskComputing
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.pdf import render_html
from autonomie.utils.pdf import write_pdf
from autonomie.utils.config import load_config

from .base import TaskView
from .base import ListView

log = logging.getLogger(__file__)

class ManualInvoiceComputing:
    """
        wrap manual invoices to allow computing
    """
    def __init__(self, model):
        self.model = model

    def compute_totalht(self):
        """
            Compute ht total
        """
        return int(self.model.montant_ht * 100)

    def compute_tva(self):
        """
            compute_tva
        """
        if self.model.tva:
            totalht = self.compute_totalht()
            if self.model.tva < 0 :
                return int(float(self.model.tva) * 100)
            else:
                tva = max(int(self.model.tva), 0)
                return int(float(totalht) * (tva / 10000.0))
        else:
            return 0

    def get_client(self):
        """
            returns the associated client
        """
        return self.model.client

class InvoiceView(TaskView, ListView):
    """
        All invoice related views
        form
        pdf
        html
    """
    schema = InvoiceSchema()
    add_title = u"Nouvelle facture"
    edit_title = u"Édition de la facture {task.number}"
    taskname_tmpl = u"Facture {0}"
    tasknumber_tmpl = "{0}_{1}_F{2}_{3}"
    route = "invoice"
    columns = ('coop_invoice_taskDate', 'coop_invoice_number', 'coop_Client_name')
    default_sort = 'coop_task_taskDate'
    default_direction = 'desc'

    def set_lines(self):
        """
            set the lines attributes
        """
        self.task_lines = self.task.lines

    def get_dbdatas_as_dict(self):
        """
            Returns dbdatas as a dict of dict
        """
        return {'invoice':self.task.appstruct(),
                'lines':[line.appstruct()
                                       for line in self.task_lines],
                }

    @view_config(route_name="invoices", renderer='tasks/form.mako')
    @view_config(route_name='invoice', renderer='tasks/form.mako')
    def invoice_form(self):
        """
            Return the invoice edit view
        """
        log.debug("#  Invoice Form #")
        if not self.task.is_editable():
            return self.redirect_to_view_only()
        if self.taskid:
            title = self.edit_title.format(task=self.task)
            edit = True
        else:
            title = self.add_title
            edit = False

        dbdatas = self.get_dbdatas_as_dict()
        # Get colander's schema compatible datas
        appstruct = get_invoice_appstruct(dbdatas)

        schema = self.schema.bind(
                                phases=self.get_phases_choice(),
                                tvas=self.get_tvas(),
                                tasktype='invoice'
                            )
        form = Form(schema, buttons=self.get_buttons())

        if 'submit' in self.request.params:
            log.debug("   + Values have been submitted")
            datas = self.request.params.items()
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, e:
                html_form = e.render()
            else:
                dbdatas = get_invoice_dbdatas(appstruct)
                log.debug(dbdatas)
                merge_session_with_post(self.task, dbdatas['invoice'])

                if not edit:
                    self.task.sequenceNumber = self.get_sequencenumber()
                    self.task.name = self.get_taskname()
                    self.task.number = self.get_tasknumber(self.task.taskDate)
                self.task.statusPerson = self.user.id
                self.task.CAEStatus = self.get_taskstatus()
                self.task.project = self.project
                self.remove_lines_from_session()
                self.add_lines_to_task(dbdatas)

                self.dbsession.merge(self.task)
                self.dbsession.flush()
                # Redirecting to the project page
                return HTTPFound(route_path('company_project',
                              self.request,
                              cid=self.company.id,
                              id=self.project.id)
                              )
        else:
            html_form = form.render(appstruct)
        return dict(title=title,
                    client=self.project.client,
                    company=self.company,
                    html_form = html_form
                    )

    @view_config(route_name='company_invoices',
                renderer='company_invoices.mako')
    def company_invoices(self):
        """
            List invoices for the given company
        """
        current_year = datetime.date.today().year
        log.debug("Getting invoices")
        search, sort, direction, current_page, items_per_page = \
                    self._get_pagination_args()

        client = self.request.params.get('client')
        if client == '-1':
            client = None
        paid = self.request.params.get('paid', 'both')
        year = self.request.params.get('year', current_year)

        invoices = self.dbsession.query(Invoice).join(
                        Invoice.project).join(
                                Project.client).filter(
                                Project.id_company==self.company.id )
        manual_invoices = self.dbsession.query(ManualInvoice).join(
                                ManualInvoice.client).filter(
                             ManualInvoice.company_id==self.company.id)

        years = sorted(
                    set([i.taskDate.year for i in invoices.all()]).union(
                     set([i.taskDate.year for i in manual_invoices.all()]))
                )

        if search:
            invoices = invoices.filter(
                                Invoice.officialNumber == search)
            manual_invoices = manual_invoices.filter(
                                ManualInvoice.officialNumber == search)
        #If we search an invoice number, we don't need more filter
        else:
            if client:
                invoices = invoices.filter(Project.code_client == client)
                manual_invoices = manual_invoices.filter(
                                ManualInvoice.client_id == client)
            if paid == 'paid':
                invoices = invoices.filter(Invoice.CAEStatus == 'paid')
                manual_invoices = manual_invoices.filter(
                                ManualInvoice.payment_ok==1)
            elif paid == 'notpaid':
                invoices = invoices.filter(Invoice.CAEStatus.in_(('sent',
                                                                  'valid',)
                                            ))
                manual_invoices = manual_invoices.filter(
                                ManualInvoice.payment_ok==0)
            else:
                invoices = invoices.filter(Invoice.CAEStatus.in_(('paid',
                                                              'sent',
                                                              'valid',)
                                                            ))
            if year:
                fday = datetime.date(int(year), 1, 1)
                lday = datetime.date(int(year)+1, 1, 1)
                invoices = invoices.filter(
                        Invoice.taskDate.between(
                                format_to_taskdate(fday),
                                format_to_taskdate(lday))
                        )
                manual_invoices = manual_invoices.filter(
                        ManualInvoice.taskDate.between(fday, lday))


        invoices = invoices.order_by(sort + " " + direction).all()
        invoices = [TaskComputing(i) for i in invoices]
        invoices.extend([ManualInvoiceComputing(i)
                                        for i in manual_invoices.all()])
        records = self._get_pagination(invoices, current_page, items_per_page)
        return dict(title=u"Factures",
                    company=self.company,
                    invoices=records,
                    current_client=client,
                    current_year=year,
                    current_paid=paid,
                    manual_invoices=manual_invoices,
                    years=years)

    def get_sequencenumber(self):
        """
            set the sequence number
            don't know really if this column matters
        """
        return len(self.project.invoices) + 1

    def remove_lines_from_session(self):
        """
            Remove invoice lines and payment lines from the current session
        """
        # if edition we remove all invoice lines
        for line in self.task.lines:
            self.dbsession.delete(line)

    def add_lines_to_task(self, dbdatas):
        """
            Add the lines to the current invoice
        """
        for line in dbdatas['lines']:
            eline = InvoiceLine()
            merge_session_with_post(eline, line)
            self.task.lines.append(eline)

    def get_task(self):
        """
            return the current invoice or a new one
        """
        if self.taskid:
            return self.project.get_invoice(self.taskid)
        else:
            invoice = Invoice()
            invoice.CAEStatus = 'draft'
            phaseid = self.request.params.get('phase')
            invoice.IDPhase = phaseid
            invoice.IDEmployee = self.user.id
            return invoice

    def html(self):
        """
            Returns an html version of the current invoice
        """
        invoicecompute = TaskComputing(self.task)
        template = "tasks/invoice.mako"
        config = load_config(self.dbsession)
        datas = dict(
                    company=self.company,
                    project=self.project,
                    task=invoicecompute,
                    config=config
                    )
        return render_html(self.request, template, datas)

    @view_config(route_name='invoice',
                renderer='tasks/invoice_html.mako',
                request_param='view=html')
    def html_invoice(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        title = u"Facture numéro : {0}".format(self.task.number)
        return dict(
                    title=title,
                    task=self.task,
                    company=self.company,
                    html_datas=self.html()
                    )

    @view_config(route_name='invoice',
                renderer='tasks/invoice_html.mako',
                request_param='view=pdf')
    def invoice_pdf(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        filename = "{0}.pdf".format(self.task.number)
        write_pdf(self.request, filename, self.html())
        return self.request.response

    @view_config(route_name='company_treasury',
                 renderer='company_treasury.mako')
    def company_treasury(self):
        """
            View for the treasury view
        """
        current_year = datetime.date.today().year
        year = self.request.params.get('year', current_year)
        today = datetime.date.today()
        log.debug("Getting invoices")
        invoices = self.dbsession.query(Invoice).join(
                        Invoice.project).filter(
                                Project.id_company==self.company.id
                                       ).filter(
                                Invoice.CAEStatus=='paid'
                                       )
        manual_invoices = self.dbsession.query(ManualInvoice).filter(
                                ManualInvoice.company_id==self.company.id
                                        ).filter(
                                    ManualInvoice.payment_ok==1)
        years = sorted(set([i.taskDate.year for i in invoices.all()]))

        fday = datetime.date(int(year), 1, 1)
        lday = datetime.date(int(year) + 1, 1, 1)
        invoices = invoices.filter(
                                Invoice.taskDate.between(
                                        format_to_taskdate(fday),
                                        format_to_taskdate(lday))
                                       ).order_by(Invoice.taskDate)
        manual_invoices = manual_invoices.filter(
                                ManualInvoice.taskDate.between(
                                        format_to_taskdate(fday),
                                        format_to_taskdate(lday))
                                        ).order_by(ManualInvoice.taskDate)
        invoices = [TaskComputing(i) for i in invoices.all()]
        invoices.extend([ManualInvoiceComputing(i)
                            for i in manual_invoices.all()])
        return dict(
                title=u"Trésorerie",
                invoices=invoices,
                company=self.company,
                years=years,
                current_year=year,
                today=datetime.date.today())
