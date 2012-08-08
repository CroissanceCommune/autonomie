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

from beaker.cache import cache_region
from deform import ValidationFailure
from deform import Form
from pyramid.view import view_config
from pyramid.security import has_permission
from pyramid.httpexceptions import HTTPFound

from autonomie.models.model import Invoice
from autonomie.models.model import CancelInvoice
from autonomie.models.model import Client
from autonomie.models.model import Company
from autonomie.models.model import Project
from autonomie.models.model import ManualInvoice
from autonomie.models.model import InvoiceLine
from autonomie.models.types import format_to_taskdate
from autonomie.models.main import get_next_officialNumber
from autonomie.views.forms.task import get_invoice_schema
from autonomie.views.forms.task import get_invoice_appstruct
from autonomie.views.forms.task import get_invoice_dbdatas
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.pdf import render_html
from autonomie.utils.exception import Forbidden
from autonomie.views.mail import StatusChanged

from .base import TaskView
from .base import ListView

log = logging.getLogger(__name__)

class CompanyInvoicesView(ListView):
    """
        Treasury and invoice view
    """
    columns = dict(taskDate=("taskDate",),
                   number=("number",),
                   client=("project", "client", "name",),
                   company=("project", "company", "name",),
                   officialNumber=("officialNumber",)
                   )
    default_sort = "officialNumber"
    default_direction = 'desc'

    @view_config(route_name='company_invoices',
                 renderer='company_invoices.mako',
                 permission='view')
    def company_invoices(self):
        """
            List invoices for the given company
        """
        company = self.request.context
        current_year = datetime.date.today().year
        log.debug("Getting invoices")
        search, sort, direction, current_page, items_per_page = \
                    self._get_pagination_args()
        client = self.request.params.get('client')
        if client == '-1':
            client = None
        paid = self.request.params.get('paid', 'both')
        year = self.request.params.get('year', current_year)

        invoices = self.get_invoices(company.id, search, client,
                                        year, paid,sort, direction)
        records = self._get_pagination(invoices, current_page, items_per_page)
        return dict(title=u"Factures",
                    company=company,
                    invoices=records,
                    current_client=client,
                    current_year=year,
                    current_paid=paid,
                    years=self._get_years())

    def _get_taskdates(self):
        """
            Return all taskdates
        """
        @cache_region("long_term", "taskdates")
        def taskdates():
            """
                Cached version
            """
            return self.dbsession.query(Invoice.taskDate), \
                self.dbsession.query(ManualInvoice.taskDate)
        return taskdates()

    def _get_years(self):
        """
            We consider that all documents should be dated after 2000
        """
        inv, man_inv = self._get_taskdates()
        @cache_region("long_term", "taskyears")
        def years():
            """
                cached version
            """
            return sorted(
                    set([i.taskDate.year for i in inv.all()
                            ]).union(
                     set([i.taskDate.year for i in man_inv.all()
                         ]))
                )
        return years()

    @view_config(route_name="invoices",
                renderer="invoices.mako",
                permission="manage")
    def invoices(self):
        """
            Return all invoices
        """
        current_year = datetime.date.today().year
        log.debug("# Getting invoices #")
        search, sort, direction, current_page, items_per_page = \
                    self._get_pagination_args()
        client = self.request.params.get('client')
        if client == '-1':
            client = None
        paid = self.request.params.get('paid', 'both')
        year = self.request.params.get('year', current_year)

        company_id = self.request.params.get('company')
        if company_id == '-1':
            company_id = None

        invoices = self.get_invoices(company_id, search, client,
                    year, paid,sort, direction)
        records = self._get_pagination(invoices, current_page, items_per_page)

        return dict(title=u"Factures",
                    invoices=records,
                    current_client=client,
                    current_year=year,
                    current_paid=paid,
                    years=self._get_years(),
                    current_company=company_id,
                    companies=Company.query(self.dbsession).all())

    def get_invoices(self, company_id=None, search=None, client=None,
                           year=None, paid=None, sort=None, direction="asc"):
        """
            Return the invoices
        """
        cancel_inv, inv, man_inv = self._get_invoices()
        if company_id:
            cancel_inv, inv, man_inv = self._filter_by_company(cancel_inv, inv, man_inv, company_id)
        if search:
            cancel_inv, inv, man_inv = self._filter_by_number(cancel_inv, inv, man_inv, search)
        #If we search an invoice number, we don't need more filter
        else:
            if client:
                cancel_inv, inv, man_inv = self._filter_by_client(cancel_inv, inv, man_inv, client)
            cancel_inv, inv, man_inv = self._filter_by_status(cancel_inv, inv, man_inv, paid)
            if year:
                cancel_inv, inv, man_inv = self._filter_by_date(cancel_inv, inv, man_inv, year)

#        if sort:
#            inv = self._sort(inv, sort, direction)
#            if sort == Invoice.officialNumber:
#                csort = CancelInvoice.officialNumber
#            elif sort == Invoice.taskDate:
#                csort = CancelInvoice.taskDate
#            elif sort == Invoice.number:
#                csort = CancelInvoice.number
#
#            cancel_inv = self._sort(cancel_inv, csort, direction)
#            if sort == Invoice.officialNumber:
#                sort = ManualInvoice.officialNumber
#            elif sort == Invoice.taskDate:
#                sort = ManualInvoice.taskDate
#            elif sort == Invoice.number:
#                sort = ManualInvoice.officialNumber
#            man_inv = self._sort(man_inv, sort, direction)
        all_inv = inv.all()
        all_inv.extend(cancel_inv)
        all_inv.extend(man_inv)
        if direction == 'asc':
            reverse = False
        else:
            reverse = True

        def sort_key(a):
            res = a
            for e in sort:
                res = getattr(res, e)
            return res


        inv = inv.all()
        inv.extend(cancel_inv.all())
        inv.extend(man_inv.all())
        invoices = sorted(inv, key=sort_key, reverse=reverse)
        return invoices

    def _get_invoices(self):
        """
            request filter invoices by clients
        """
        join_args = ("project", "client", "company",)
        cancel_inv = self.dbsession.query(CancelInvoice).join(*join_args)
        inv = self.dbsession.query(Invoice).join(*join_args)
        man_inv = self.dbsession.query(ManualInvoice).join(
                                 ManualInvoice.client).join(Client.company)
        return cancel_inv, inv, man_inv

    @staticmethod
    def _filter_by_company(cancel_inv, inv, man_inv, company_id):
        """
            add a filter on the company id
        """
        inv = inv.filter(Project.id_company==company_id )
        cancel_inv = cancel_inv.filter(Project.id_company==company_id )
        man_inv = man_inv.filter(ManualInvoice.company_id==company_id)
        return cancel_inv, inv, man_inv

    @staticmethod
    def _filter_by_number(cancel_inv, inv, man_inv, number):
        """
            add a filter on the numbers to invoices sqla queries
        """
        inv = inv.filter(Invoice.officialNumber == number)
        cancel_inv = cancel_inv.filter(CancelInvoice.officialNumber == number)
        man_inv = man_inv.filter(
                             ManualInvoice.officialNumber == number)
        return cancel_inv, inv, man_inv

    @staticmethod
    def _filter_by_client(cancel_inv, inv, man_inv, client):
        """
            add a filter on the client to invoices sqla queries
        """
        inv = inv.filter(Project.code_client == client)
        cancel_inv = cancel_inv.filter(Project.code_client == client)
        man_inv = man_inv.filter(
                        ManualInvoice.client_id == client)
        return cancel_inv, inv, man_inv

    @staticmethod
    def _filter_by_status(cancel_inv, inv, man_inv, status):
        """
            add a filter on the status to invoices sqla queries
        """
        if status == "paid":
            inv = inv.filter(Invoice.CAEStatus == 'paid')
            cancel_inv = cancel_inv.filter(CancelInvoice.CAEStatus == 'paid')
            man_inv = man_inv.filter(
                                        ManualInvoice.payment_ok==1)
        elif status == "notpaid":
            inv = inv.filter(Invoice.CAEStatus.in_(
                                        ('sent', 'valid', 'recinv')))
            cancel_inv = cancel_inv.filter(CancelInvoice.CAEStatus.in_(
                                          ('sent','valid','recinv')))
            man_inv = man_inv.filter(ManualInvoice.payment_ok==0)
        else:
            inv = inv.filter(Invoice.CAEStatus.in_(
                                ('paid', 'sent', 'valid','aboinv', 'recinv')))
            cancel_inv = cancel_inv.filter(CancelInvoice.CAEStatus.in_(
                                          ('paid', 'sent', 'valid','recinv')))
        return cancel_inv, inv, man_inv

    @staticmethod
    def _filter_by_date(cancel_inv, inv, man_inv, year):
        """
            add a filter on dates to the invoices sqla queries
        """
        fday = datetime.date(int(year), 1, 1)
        lday = datetime.date(int(year)+1, 1, 1)
        inv = inv.filter(
                        Invoice.taskDate.between(
                                format_to_taskdate(fday),
                                format_to_taskdate(lday))
                        )
        cancel_inv = cancel_inv.filter(CancelInvoice.taskDate.between(
                                format_to_taskdate(fday),
                                format_to_taskdate(lday)))
        man_inv = man_inv.filter(
                        ManualInvoice.taskDate.between(fday, lday))
        return cancel_inv, inv, man_inv

    @view_config(route_name='company_treasury',
                 renderer='company_treasury.mako',
                 permission='view')
    def company_treasury(self):
        """
            View for the treasury view
        """
        company = self.request.context
        today = datetime.date.today()
        current_year = today.year
        year = self.request.params.get('year', current_year)
        log.debug("Getting invoices")
        invoices = self.get_invoices(company_id=company.id,
                                         paid="paid",
                                         year=year,
                                         sort=('taskDate',))
        #inv, man_inv = self._filter_by_status(inv, man_inv, "paid")
        #years = sorted(set([i.taskDate.year for i in inv.all()]))
        #inv, man_inv = self._filter_by_date(inv, man_inv, year)
        #inv = inv.order_by(Invoice.taskDate)
        #man_inv = man_inv.order_by(ManualInvoice.taskDate)
        #invoices = self._wrap_for_computing(inv, man_inv)
        return dict(
                title=u"Trésorerie",
                invoices=invoices,
                company=company,
                years=self._get_years(),
                current_year=year,
                today=today)

class InvoiceView(TaskView):
    """
        All invoice related views
        form
        pdf
        html
    """
    schema = get_invoice_schema()
    add_title = u"Nouvelle facture"
    edit_title = u"Édition de la facture {task.number}"
    taskname_tmpl = u"Facture {0}"
    tasknumber_tmpl = u"{0}_{1}_F{2}_{3:%m%y}"
    route = "invoice"

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

    def is_editable(self):
        """
            Return True if the current task can be edited by the current user
        """
        if self.task.is_editable():
            return True
        if has_permission('manage', self.request.context, self.request):
            if self.task.is_waiting():
                return True
        return False

    @view_config(route_name="project_invoices", renderer='tasks/edit.mako',
            permission='edit')
    @view_config(route_name='invoice', renderer='tasks/edit.mako',
            permission='edit')
    def invoice_form(self):
        """
            Return the invoice edit view
        """
        log.debug("#  Invoice Form #")
        if not self.is_editable():
            return self.redirect_to_view_only()
        if self.taskid:
            title = self.edit_title.format(task=self.task)
            edit = True
            valid_msg = u"La facture a bien été éditée."
        else:
            title = self.add_title
            edit = False
            valid_msg = u"La facture a bien été ajoutée."

        dbdatas = self.get_dbdatas_as_dict()
        # Get colander's schema compatible datas
        appstruct = get_invoice_appstruct(dbdatas)

        schema = self.schema.bind(
                                phases=self.get_phases_choice(),
                                tvas=self.get_tvas(),
                            )
        form = Form(schema, buttons=self.get_buttons())
        form.widget.template = "autonomie:deform_templates/form.pt"

        if 'submit' in self.request.params:
            log.debug(" + Values have been submitted")
            datas = self.request.params.items()
            log.debug(datas)
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, e:
                html_form = e.render()
            else:
                log.debug("  + Values are valid")
                dbdatas = get_invoice_dbdatas(appstruct)
                log.debug(dbdatas)
                merge_session_with_post(self.task, dbdatas['invoice'])
                if not edit:
                    self.task.sequenceNumber = self.get_sequencenumber()
                    self.task.name = self.get_taskname()
                    self.task.number = self.get_tasknumber(self.task.taskDate)
                try:
                    self.request.session.flash(valid_msg, queue="main")
                    self.task.project = self.project
                    self.remove_lines_from_session()
                    self.add_lines_to_task(dbdatas)
                    self._status_process()
                    self._set_modifications()
                    self.request.registry.notify(StatusChanged(self.request,
                                                    self.task))
                except Forbidden, e:
                    self.request.session.pop_flash("main")
                    self.request.session.flash(e.message, queue='error')

                # Redirecting to the project page
                return self.project_view_redirect()
        else:
            html_form = form.render(appstruct)
        return dict(title=title,
                    client=self.project.client,
                    company=self.company,
                    html_form = html_form,
                    action_menu=self.actionmenu
                    )

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
        document = Invoice()
        document.CAEStatus = "draft"
        phaseid = self.request.params.get('phase')
        document.IDPhase = phaseid
        document.IDEmployee = self.user.id
        return document

    def _html(self):
        """
            Returns an html version of the current invoice
        """
        template = "tasks/invoice.mako"
        config = self.request.config
        datas = dict(
                    company=self.company,
                    project=self.project,
                    task=self.task,
                    config=config
                    )
        return render_html(self.request, template, datas)

    @view_config(route_name='invoice',
                renderer='tasks/view_only.mako',
                permission='view',
                request_param='view=html')
    def html(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        if self.is_editable():
            return HTTPFound(self.request.route_path('invoice',
                                                id=self.task.id))
        title = u"Facture numéro : {0}".format(self.task.number)
        return dict(
                    title=title,
                    task=self.task,
                    html_datas=self._html(),
                    action_menu=self.actionmenu,
                    submit_buttons=self.get_buttons(),
                    )

    @view_config(route_name='invoice',
                request_param='view=pdf',
                permission='view')
    def pdf(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        return self._pdf()

    @view_config(route_name="invoice", request_param='action=status',
                permission="edit")
    def status(self):
        """
            Status change view
        """
        return self._status()

    def _post_status_process(self, status):
        """
            Change the current task's status
        """
        if status == "valid":
            officialNumber = get_next_officialNumber(
                                        self.request.dbsession)
            self.task.officialNumber = officialNumber
            self.task.taskDate = datetime.date.today()
            self.request.session.flash(u"La facture porte le numéro \
<b>{0}</b>".format(officialNumber), queue='main')

        elif status == 'paid':
            paymentMode = self.request.params.get('paymentMode')
            self.task.paymentMode = paymentMode

        elif status == 'aboinv':
            log.debug(" + An invoice is aborted -> generating cancel")
            id_ = self._gen_cancel_invoice()
            log.debug(u"   + The cancel id : {0}".format(id_))
            self.request.session.flash(u"La facture a été annulée, \
Un avoir a été généré, vous pouvez l'éditer <a href='{0}'>Ici</a>.".format(
    self.request.route_path("cancelinvoice", id=id_)), queue="main")

    def _can_change_status(self, status):
        """
            Handle the permission on status change depending on
            actual permissions
        """
        if not has_permission('manage', self.request.context, self.request):
            if status in ('invalid', 'valid', 'paid', 'aboinv'):
                return False
        return True

    def _gen_cancel_invoice(self):
        """
            Generates a cancel invoice based on the current invoice
        """
        seq_number = len(self.project.cancelinvoices) + 1
        cancelinvoice = self.task.gen_cancel_invoice()
        today = datetime.date.today()
        cancelinvoice.statusPerson = self.user.id
        cancelinvoice.statusDate = today
        cancelinvoice.owner = self.user
        cancelinvoice.name = u"Avoir {0}".format(seq_number)
        cancelinvoice.number = self.get_tasknumber(today,
                                        tmpl=u"{0}_{1}_A{2}_{3:%m%y}",
                                        seq_number=seq_number)
        for line in self.task.lines:
            cancelinvoice.lines.append(line.gen_cancel_invoice_line())
        cancelinvoice = self.dbsession.merge(cancelinvoice)
        self.dbsession.flush()
        id_ = cancelinvoice.id
        return id_
