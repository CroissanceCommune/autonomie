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
from pyramid.security import has_permission

from autonomie.models.model import Estimation
from autonomie.models.model import Invoice
from autonomie.models.model import InvoiceLine
from autonomie.models.model import EstimationLine
from autonomie.models.model import PaymentLine
from autonomie.views.forms.task import EstimationSchema
from autonomie.views.forms.task import get_estimation_appstruct
from autonomie.views.forms.task import get_estimation_dbdatas
from autonomie.views.forms.task import TaskComputing
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.pdf import render_html
from autonomie.utils.pdf import write_pdf
from autonomie.utils.exception import Forbidden
from autonomie.views.mail import StatusChanged

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
    tasknumber_tmpl = "{0}_{1}_D{2}_{3:%m%y}"
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

    @view_config(route_name="estimations", renderer='tasks/form.mako',
                permission='edit')
    @view_config(route_name='estimation', renderer='tasks/form.mako',
                permission='edit')
    def form(self):
        """
            Return the estimation edit view
        """
        log.debug("#  Estimation Form #")
        if not self.is_editable():
            return self.redirect_to_view_only()
        if self.taskid:
            title = self.edit_title.format(task=self.task)
            edit = True
            valid_msg = u"Le devis a bien été édité."
        else:
            title = self.add_title
            edit = False
            valid_msg = u"Le devis a bien été ajouté."

        dbdatas = self.get_dbdatas_as_dict()
        # Get colander's schema compatible datas
        appstruct = get_estimation_appstruct(dbdatas)

        schema = self.schema.bind(
                                phases=self.get_phases_choice(),
                                tvas=self.get_tvas()
                            )
        form = Form(schema, buttons=self.get_buttons())
        form.widget.template = 'autonomie:deform_templates/form.pt'

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
                dbdatas = get_estimation_dbdatas(appstruct)
                log.debug(dbdatas)
                merge_session_with_post(self.task, dbdatas['estimation'])
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
                    log.debug(" > Estimation has been added/edited succesfully")
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
        config = self.request.config
        datas = dict(
                    company=self.company,
                    project=self.project,
                    task=estimationcompute,
                    config=config
                    )
        return render_html(self.request, template, datas)

    @view_config(route_name='estimation',
                renderer='tasks/estimation_html.mako',
                request_param='view=html',
                permission='view')
    def html(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        if self.is_editable():
            return HTTPFound(self.request.route_path(self.route,
                                                     id=self.task.id))
        title = u"Devis numéro : {0}".format(self.task.number)
        return dict(
                    title=title,
                    task=self.task,
                    html_datas=self._html(),
                    action_menu=self.actionmenu,
                    submit_buttons=self.get_buttons()
                    )

    @view_config(route_name='estimation',
                request_param='view=pdf',
                permission='view')
    def pdf(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        log.debug("# Generating the pdf file #")
        filename = "{0}.pdf".format(self.task.number)
        write_pdf(self.request, filename, self._html())
        return self.request.response

    @view_config(route_name='estimation', request_param='action=duplicate',
            permission='edit')
    def duplicate(self):
        """
            Duplicates current estimation
        """
        log.debug("# Duplicate estimation #")
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
        newone = self.dbsession.merge(newone)
        self.dbsession.flush()
        taskid = newone.IDTask
        self.request.session.flash(u"Le devis {0} a bien été dupliqué".format(
            self.task.number
            ), queue='main')
        return HTTPFound(self.request.route_path(self.route, id=taskid))

    @view_config(route_name='estimation', request_param='action=delete',
            permission='edit')
    def delete(self):
        """
            Delete an estimation
        """
        log.debug("# Deleting an invoice #")
        if self.task.is_deletable():
            self.dbsession.delete(self.task)
            message = u"Le devis {0} a bien été supprimé.".format(
                                                            self.task.number)
            self.request.session.flash(message, queue='main')
        else:
            message = u"Vous n'êtes pas autorisé à supprimer ce devis."
            self.request.session.flash(message, queue='error')
        return self.project_view_redirect()

    def gen_invoices(self):
        """
            Called when an estimation status is changed
            ( when no form is displayed : the estimation itself is not
            editable anymore )
        """
        log.debug("# Invoice Generation #")
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

        already_paid_lines = []

        #generating deposit invoice
        log.debug(" + Generating deposit invoice")
        if self.task.deposit > 0:
            invoice_args = invoice_args_common.copy()
            invoice_args.update(
                dict(
                    sequenceNumber=len(self.project.invoices) + count,
                    name=u"Facture d'acompte {0}".format(count),
                    number=self.get_tasknumber(taskDate,
                                               tmpl="{0}_{1}_FA{2}_{3:%m%y}",
                                               seq_number=count),
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
        log.debug(" + Generating payment invoices")
        for paymentline in self.payment_lines[:-1]:
            invoice_args = invoice_args_common.copy()
            invoice_args.update(
                    dict(
                        sequenceNumber=len(self.project.invoices) + count,
                        name=u"Facture d'acompte {0}".format(count),
                        number=self.get_tasknumber(taskDate,
                                                 tmpl="{0}_{1}_FA{2}_{3:%m%y}",
                                                 seq_number=count),
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
        log.debug(" + Generating the last invoice")
        paymentline = self.payment_lines[-1]
        invoice_args = invoice_args_common.copy()
        invoice_args.update(
            dict(sequenceNumber=len(self.project.invoices) + count,
                name=u"Facture de solde",
                number=self.get_tasknumber(taskDate,
                                           tmpl="{0}_{1}_F{2}_{3:%m%y}",
                                           seq_number=count),
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

    @view_config(route_name="estimation", request_param='action=status',
                 permission="edit")
    def status(self):
        """
            Status change view
        """
        return self._status()

    def _can_change_status(self, status):
        """
            Handle the permission on status change depending on
            actual permissions
        """
        if not has_permission('manage', self.request.context, self.request):
            if status in ('invalid', 'valid', 'aboest'):
                return False
        return True

    def _post_status_process(self, status):
        """
            Handle specific status changes
        """
        if status == "geninv":
            self.gen_invoices()
        elif status == "aboest":
            self.request.session.flash(u"Le devis {0} a été annulé \
(indiqué sans suite).".format(self.task.number))
