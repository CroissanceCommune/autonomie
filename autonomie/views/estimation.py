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

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_path

from autonomie.models.model import Estimation
from autonomie.models.model import Invoice
from autonomie.models.model import InvoiceLine
from autonomie.models.model import EstimationLine
from autonomie.models.model import PaymentLine
from autonomie.views.forms.estimation import EstimationSchema
from autonomie.views.forms.estimation import get_estimation_appstruct
from autonomie.views.forms.estimation import get_estimation_dbdatas
from autonomie.views.forms.estimation import TaskComputing
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.pdf import render_html
from autonomie.utils.pdf import write_pdf
from autonomie.utils.config import load_config
from autonomie.utils.exception import Forbidden

from .base import TaskView

log = logging.getLogger(__name__)
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


    @view_config(route_name="estimations", renderer='tasks/form.mako')
    @view_config(route_name='estimation', renderer='tasks/form.mako')
    def form(self):
        """
            Return the estimation edit view
        """
        log.debug("#  Estimation Form #")
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
        appstruct = get_estimation_appstruct(dbdatas)

        schema = self.schema.bind(
                                phases=self.get_phases_choice(),
                                tvas=self.get_tvas()
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
                try:
                    dbdatas = get_estimation_dbdatas(appstruct)
                    merge_session_with_post(self.task, dbdatas['estimation'])

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
                    return self.project_view_redirect()
                except Forbidden, e:
                    self.request.session.flash(e.message, queue='error')
                    html_form = form.render(appstruct)
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
        estimation = Estimation()
        estimation.CAEStatus = 'draft'
        phaseid = self.request.params.get('phase')
        estimation.IDPhase = phaseid
        estimation.IDEmployee = self.user.id
        return estimation

    def _html(self):
        """
            Returns an html version of the current estimation
        """
        estimationcompute = TaskComputing(self.task)
        template = "tasks/estimation.mako"
        config = load_config(self.dbsession)
        datas = dict(
                    company=self.company,
                    project=self.project,
                    task=estimationcompute,
                    config=config
                    )
        return render_html(self.request, template, datas)

    @view_config(route_name='estimation',
                renderer='tasks/estimation_html.mako',
                request_param='view=html')
    def html(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        title = u"Devis numéro : {0}".format(self.task.number)
        return dict(
                    title=title,
                    task=self.task,
                    company=self.company,
                    html_datas=self._html()
                    )

    @view_config(route_name='estimation',
                request_param='view=pdf')
    def pdf(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        filename = "{0}.pdf".format(self.task.number)
        write_pdf(self.request, filename, self._html())
        return self.request.response

    @view_config(route_name='estimation', request_param='action=duplicate')
    def duplicate(self):
        """
            Duplicates current estimation
        """
        newone = self.task.duplicate()
        newone.CAEStatus = "draft"
        newone.statusPerson = self.user.id
        newone.name = self.get_taskname()
        newone.sequenceNumber = self.get_sequencenumber()
        newone.number = self.get_tasknumber(newone.taskDate)

        for line in self.task_lines:
            newline = line.duplicate()
            newone.lines.append(newline)

        for line in self.task.payment_lines:
            newline = line.duplicate()
            newone.payment_lines.append(newline)

        newone.project = self.project
        self.dbsession.merge(newone)
        self.dbsession.flush()
        taskid = newone.IDTask
        self.request.session.flash(u"Le devis {0} a bien été dupliqué".format(
            self.task.number
            ), queue='main')
        return HTTPFound(route_path(
                    'estimation',
                    self.request,
                    taskid=taskid))

    @view_config(route_name='estimation', request_param='action=delete')
    def delete(self):
        """
            Delete an estimation
        """
        if self.task.is_deletable():
            self.dbsession.delete(self.task)
            message = u"Le devis {0} a bien été supprimé.".format(
                                                            self.task.number)
        else:
            message = u"Vous n'êtes pas autorisé à supprimer ce devis."
        self.request.session.flash(message, queue='error')
        return self.project_view_redirect()

    @view_config(route_name='estimation', request_param='action=geninv')
    def gen_invoices(self):
        """
            Called when an estimation status is changed
            ( when no form is displayed : the estimation itself is not
            editable anymore )
        """
        log.debug("We change the estimation status")
        newstatus = "geninv"
        self.task.CAEStatus = newstatus

        #recovering common datas needed to generate the invoices
        computer = TaskComputing(self.task)
        count = 1
        taskDate = datetime.date.today()
        invoice_args_common = dict(
            IDProject = self.project.id,
            IDPhase = self.task.IDPhase,
            taskDate=taskDate,
            CAEStatus = 'draft',
            statusPerson = self.user.id,
            IDEmployee = self.user.id,
            tva = self.task.tva,
            IDEstimation=self.task.IDTask,
            paymentConditions=self.task.paymentConditions,
            description=self.task.description,
            course=self.task.course,
            )

        pcode = self.project.code
        ccode = self.project.client.id
        shortdate = "{0}{1}".format(
                taskDate.month,
                str(taskDate.year)[2:])
        already_paid_lines = []

        #generating deposit invoice
        if self.task.deposit > 0:
            invoice_args = invoice_args_common.copy()
            invoice_args.update(
                dict(
                    sequenceNumber=len(self.project.invoices) + count,
                    name = u"Facture d'acompte {0}".format(count),
                    number = "{0}_{1}_FA{2}_{3}".format(pcode,
                                                        ccode,
                                                        count,
                                                        shortdate),
                    displayedUnits=0,
                    ))
            invoice = Invoice(**invoice_args)
            amount = computer.compute_deposit()
            line = InvoiceLine(rowIndex=count,
                               description=u"Facture d'acompte",
                               cost=amount)
            invoice.lines.append(line)
            self.dbsession.merge(invoice)
            count += 1
            #we keep the information to display it in the last invoice
            remember = line.duplicate()
            # setting negative cost
            remember.cost = -1 * remember.cost
            remember.rowIndex = count
            already_paid_lines.append(remember)
        # generating the different payment lines' invoices (not the last one)
        for paymentline in self.payment_lines[:-1]:
            invoice_args = invoice_args_common.copy()
            invoice_args.update(
                    dict(
                        sequenceNumber=len(self.project.invoices) + count,
                        name = u"Facture d'acompte {0}".format(count),
                        number = "{0}_{1}_FA{2}_{3}".format(pcode,
                                                            ccode,
                                                            count,
                                                            shortdate),
                        displayedUnits=0,
                        ))
            invoice = Invoice(**invoice_args)

            # if payment amounts have been set manually or not
            if self.task.manualDeliverables == 0:
                amount = computer.compute_line_amount()
            else:
                amount = paymentline.amount
            line = InvoiceLine(rowIndex=1,
                               description=paymentline.description,
                               cost=amount)

            invoice.lines.append(line)
            self.dbsession.merge(invoice)
            count += 1
            #we keep the information to display it in the last invoice
            remember = line.duplicate()
            # setting negative cost
            remember.cost = -1 * remember.cost
            remember.rowIndex = count
            already_paid_lines.append(remember)

        # generating the sold invoice
        paymentline = self.payment_lines[-1]
        invoice_args = invoice_args_common.copy()
        invoice_args.update(
            dict(sequenceNumber=len(self.project.invoices) + count,
                name=u"Facture de solde {0}".format(count),
                number="{0}_{1}_F{2}_{3}".format(pcode,ccode,count,shortdate),
                displayedUnits=0))
        invoice = Invoice(**invoice_args)
        line = InvoiceLine(rowIndex=1,
                            description=paymentline.description,
                            cost=computer.compute_totalht())
        invoice.lines.append(line)
        for i in already_paid_lines:
            invoice.lines.append(i.duplicate())
        self.dbsession.merge(invoice)
        self.request.session.flash(u"Vos factures ont bien été générées",
                                queue='main')
        return self.project_view_redirect()

    @view_config(route_name='estimation', request_param='action=aboest')
    def abort(self):
        """
            Abort current estimation
        """
        self.task.CAEStatus = "aboest"
        self.request.session.flash(u"Le devis {0} a été annulé \
(indiqué sans suite).".format(self.task.number))
        return self.project_view_redirect()
