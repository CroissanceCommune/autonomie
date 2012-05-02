# -*- coding: utf-8 -*-
# * File Name : estimation.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 24-04-2012
# * Last Modified :
#
# * Project :
#
"""
    Estimation views
"""
import logging
import datetime
from deform import ValidationFailure
from deform import Form
from deform import Button

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_path

from autonomie.models import DBSESSION
from autonomie.models.model import Tva
from autonomie.models.model import Estimation
from autonomie.models.model import Invoice
from autonomie.models.model import Phase
from autonomie.models.model import EstimationLine
from autonomie.models.model import InvoiceLine
from autonomie.models.model import PaymentLine
from autonomie.views.forms.estimation import EstimationSchema
from autonomie.views.forms.estimation import InvoiceSchema
from autonomie.views.forms.estimation import get_estimation_appstruct
from autonomie.views.forms.estimation import get_estimation_dbdatas
from autonomie.views.forms.estimation import get_invoice_appstruct
from autonomie.views.forms.estimation import get_invoice_dbdatas
from autonomie.views.forms.estimation import EstimationComputingModel
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.pdf import render_html
from autonomie.utils.pdf import write_pdf
from autonomie.utils.config import load_config

from .base import BaseView

log = logging.getLogger(__name__)
def get_tvas():
    """
        return all configured tva amounts
    """
    tvas = DBSESSION().query(Tva).all()
    return [(tva.value, tva.name)for tva in tvas]

def get_buttons():
    """
        returns submit buttons for estimation form
    """
    draft = Button(name='submit',
                   title=u"Enregistrer en tant que brouillon",
                   type='submit',
                   value="draft")
    askvalidation = Button(name='submit',
                           title=u"Demander à la CAE de valider ce document",
                           type='submit',
                           value="wait")
    cancel = Button(name='cancel',
                    title=u"Annuler",
                    type='reset',
                    value=u"Annuler")
    return (draft, askvalidation, cancel,)

class TaskView(BaseView):
    """
        BaseTask related view
        Base object for estimation and invoice views
    """
    schema = None
    add_title = u""
    edit_title = u""
    taskname_tmpl = u""
    tasknumber_tmpl = u""
    route = u""

    def __init__(self, request):
        BaseView.__init__(self, request)
        self.company = self.get_current_company()
        self.project = self.get_current_project(self.company)
        self.taskid = self.request.matchdict.get('taskid')
        self.task = self.get_task()
        self.set_lines()

    def set_lines(self):
        raise Exception("Not implemented yet")

    def redirect_to_view_only(self):
        """
            redirect the user to the view only url
        """
        return HTTPFound(route_path(
                            self.route,
                            self.request,
                            cid=self.company.id,
                            id=self.project.id,
                            taskid=self.taskid,
                            _query=dict(view='html')
                            ))

    def get_current_project(self, company):
        """
            Returns the current project
        """
        project_id = self.request.matchdict.get('id')
        return company.get_project(project_id)

    def add_default_phase(self):
        """
            Adds a default phase to an existing project
        """
        default_phase = Phase(name=u"Phase par défaut")
        default_phase.id_project = self.project.id
        default_phase = self.dbsession.merge(default_phase)
        self.dbsession.flush()
        return default_phase

    def get_phases_choice(self):
        """
            returns the options for phase select
        """
        phase_choices = ((phase.id, phase.name) \
                        for phase in self.project.phases)
        if not self.project.phases: # On a pas de phase dans le projet
            default_phase = self.add_default_phase()
            phase_choices = ((default_phase.id, default_phase.name),)
        return phase_choices

    def set_sequencenumber(self):
        """
            set the sequence number
            don't know really if this column matters
        """
        num = len(self.project.estimations) + 1
        self.task.sequenceNumber = num

    def set_taskname(self):
        """
            set the current taskname
        """
        self.task.name = self.taskname_tmpl.format(
                                      self.task.sequenceNumber
                                                  )

    def set_tasknumber(self):
        """
            return the task number
        """
        date = "{0}{1}".format(
                               self.task.taskDate.month,
                               str(self.task.taskDate.year)[2:])
        pcode = self.project.code
        ccode = self.project.client.id
        log.debug(self.task.sequenceNumber)
        self.task.number = self.tasknumber_tmpl.format(pcode,
                                  ccode,
                                  self.task.sequenceNumber,
                                  date)
    def set_taskstatus(self):
        """
            Set all status related attributes
        """
        caestatus = self.request.params['submit']
        self.task.statusPerson = self.user.id
        self.task.project = self.project
        if caestatus in ('draft', 'wait'):
            self.task.CAEStatus = caestatus
        else:
            self.task.CAEStatus = 'draft'

class EstimationView(TaskView):
    """
        All estimation related views
        form
        pdf
        html
    """
    schema = EstimationSchema()
    add_title = u"Nouveau devis"
    edit_title = u"Édition du devis {task.number}"
    taskname_tmpl = u"Devis {0}"
    tasknumber_tmpl = "{0}_{1}_D{2}_{3}"
    route = "estimation"


    def set_lines(self):
        """
            set the lines attributes
        """
        self.task_lines = self.task.lines
        self.payment_lines = self.task.payment_lines

    def get_dbdatas_as_dict(self):
        """
            Returns dbdatas as a dict of dict
        """
        return {'estimation':self.task.appstruct(),
                'lines':[line.appstruct()
                                       for line in self.task_lines],
                'payment_lines':[line.appstruct()
                                        for line in self.payment_lines]}


    @view_config(route_name="estimations", renderer='estimation.mako')
    @view_config(route_name='estimation', renderer='estimation.mako')
    def estimation_form(self):
        """
            Return the estimation edit view
        """
        log.debug("#  Estimation Form #")
        if not self.task.is_editable():
            return self.redirect_to_view_only()
        if self.taskid:
            title = self.edit_title.format(self.task)
            #u"Édition du devis"
        else:
            title = self.add_title

        dbdatas = self.get_dbdatas_as_dict()
        # Get colander's schema compatible datas
        appstruct = get_estimation_appstruct(dbdatas)

        schema = self.schema.bind(
                                phases=self.get_phases_choice(),
                                tvas=get_tvas()
                            )
        form = Form(schema, buttons=get_buttons())

        if 'submit' in self.request.params:
            log.debug("   + Values have been submitted")
            datas = self.request.params.items()
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, e:
                html_form = e.render()
            else:
                dbdatas = get_estimation_dbdatas(appstruct)
                merge_session_with_post(self.task, dbdatas['estimation'])

                self.set_sequencenumber()
                self.set_taskname()
                self.set_tasknumber()
                log.debug(self.task.sequenceNumber)
                self.set_taskstatus()
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
    def remove_lines_from_session(self):
        """
            Remove estimation lines and payment lines from the current session
        """
        # if edition we remove all estimation and payment lines
        for line in self.task.lines:
            self.dbsession.delete(line)
        for line in self.task.payment_lines:
            self.dbsession.delete(line)

    def add_lines_to_task(self, dbdatas):
        """
            Add the lines to the current estimation
        """
        for line in dbdatas['payment_lines']:
            pline = PaymentLine()
            merge_session_with_post(pline, line)
            self.task.payment_lines.append(pline)
        for line in dbdatas['lines']:
            eline = EstimationLine()
            merge_session_with_post(eline, line)
            self.task.lines.append(eline)

    def get_task(self):
        """
            return the current estimation or a new one
        """
        if self.taskid:
            return self.project.get_estimation(self.taskid)
        else:
            estimation = Estimation()
            estimation.CAEStatus = 'draft'
            phaseid = self.request.params.get('phase')
            estimation.IDPhase = phaseid
            estimation.IDEmployee = self.user.id
            return estimation

    def html(self):
        """
            Returns an html version of the current estimation
        """
        estimationcompute = EstimationComputingModel(self.task)
        template = "estimation_html.mako"
        config = load_config(self.dbsession)
        datas = dict(
                    company=self.company,
                    project=self.project,
                    estimation=estimationcompute,
                    config=config
                    )
        return render_html(self.request, template, datas)

    @view_config(route_name='estimation',
                renderer='html_view.mako',
                request_param='view=html')
    def html_estimation(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        title = u"Devis numéro : {0}".format(self.task.number)
        return dict(
                    title=title,
                    task=self.task,
                    company=self.company,
                    html_datas=self.html()
                    )

    @view_config(route_name='estimation',
                renderer='html_view.mako',
                request_param='view=pdf')
    def estimation_pdf(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        filename = "{0}.pdf".format(self.task.number)
        write_pdf(self.request, filename, self.html())
        return self.request.response

class InvoiceView(TaskView):
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

    @view_config(route_name="invoices", renderer='estimation.mako')
    @view_config(route_name='invoice', renderer='estimation.mako')
    def invoice_form(self):
        """
            Return the invoice edit view
        """
        log.debug("#  Invoice Form #")
        if not self.task.is_editable():
            return self.redirect_to_view_only()
        if self.taskid:
            title = self.edit_title.format(self.task)
            #u"Édition du devis"
        else:
            title = self.add_title

        dbdatas = self.get_dbdatas_as_dict()
        # Get colander's schema compatible datas
        appstruct = get_invoice_appstruct(dbdatas)

        schema = self.schema.bind(
                                phases=self.get_phases_choice(),
                                tvas=get_tvas(),
                                tasktype='invoice'
                            )
        form = Form(schema, buttons=get_buttons())

        if 'submit' in self.request.params:
            #TODO
            log.debug("   + Values have been submitted")
            datas = self.request.params.items()
            log.debug(datas)
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, e:
                html_form = e.render()
            else:
                dbdatas = get_invoice_dbdatas(appstruct)
                log.debug(dbdatas)
                merge_session_with_post(self.task, dbdatas['invoice'])

                self.set_sequencenumber()
                self.set_taskname()
                self.set_tasknumber()
                self.set_taskstatus()
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

    def set_sequencenumber(self):
        """
            set the sequence number
            don't know really if this column matters
        """
        num = len(self.project.invoices) + 1
        self.task.sequenceNumber = num

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
        #TODO
        invoicecompute = EstimationComputingModel(self.task)
        template = "invoice_html.mako"
        config = load_config(self.dbsession)
        datas = dict(
                    company=self.company,
                    project=self.project,
                    invoice=invoicecompute,
                    config=config
                    )
        return render_html(self.request, template, datas)

    @view_config(route_name='invoice',
                renderer='html_view.mako',
                request_param='view=html')
    def html_invoice(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        #TODO
        title = u"Facture numéro : {0}".format(self.task.number)
        return dict(
                    title=title,
                    task=self.task,
                    company=self.company,
                    html_datas=self.html()
                    )

    @view_config(route_name='invoice',
                renderer='html_view.mako',
                request_param='view=pdf')
    def invoice_pdf(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        #TODO
        filename = "{0}.pdf".format(self.task.number)
        write_pdf(self.request, filename, self.html())
        return self.request.response

