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
from deform import ValidationFailure
from deform import Form

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from autonomie.models.task.estimation import Estimation
from autonomie.models.task.estimation import EstimationLine
from autonomie.models.task.estimation import PaymentLine
from autonomie.models.task.task import DiscountLine
from autonomie.views.forms.task import get_estimation_schema
from autonomie.views.forms.task import get_estimation_appstruct
from autonomie.views.forms.task import get_estimation_dbdatas
from autonomie.utils.forms import merge_session_with_post
from autonomie.exception import Forbidden
from autonomie.views.mail import StatusChanged
from autonomie.views.status import StatusView

from .base import TaskView
from .base import make_pdf_view

log = logging.getLogger(__name__)


class EstimationView(TaskView):
    """
        All estimation related views
        form
        pdf
        html
    """
    model = Estimation
    type_ = "estimation"
    schema = get_estimation_schema()
    add_title = u"Nouveau devis"
    edit_title = u"Édition du devis {task.number}"
    route = "estimation"
    template = "tasks/estimation.mako"

    def get_dbdatas_as_dict(self):
        """
            Returns dbdatas as a dict of dict
        """
        return {'estimation': self.task.appstruct(),
                'lines': [line.appstruct()
                          for line in self.task.lines],
                'discounts': [discount.appstruct()
                              for discount in self.task.discounts],
                'payment_lines': [line.appstruct()
                                  for line in self.task.payment_lines]}

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

    @view_config(route_name="estimations", renderer='tasks/edit.mako',
                permission='edit')
    @view_config(route_name='estimation', renderer='tasks/edit.mako',
                permission='edit')
    def form(self):
        """
            Return the estimation edit view
        """
        if self.taskid:
            if not self.is_editable():
                return self.redirect_to_view_only()
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

        schema = self.schema.bind(request=self.request)
        self.request.js_require.add('address')
        form = Form(schema, buttons=self.get_buttons(),
                                counter=self.formcounter)
        form.widget.template = 'autonomie:deform_templates/form.pt'

        if 'submit' in self.request.params:
            datas = self.request.params.items()
            log.debug(u"Estimation form submission : {0}".format(datas))
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, e:
                log.exception(u" - Values are not valid")
                html_form = e.render()
            else:
                dbdatas = get_estimation_dbdatas(appstruct)
                log.debug(u"Values are valid : {0}".format(dbdatas))
                merge_session_with_post(self.task, dbdatas['estimation'])
                if not edit:
                    self.task.sequenceNumber = self.get_sequencenumber()
                    self.task.name = self.get_taskname()
                    self.task.number = self.get_tasknumber(
                                                        self.task.taskDate)
                try:
                    self.request.session.flash(valid_msg, queue="main")
                    self.task.project = self.project
                    self.remove_lines_from_session()
                    self.add_lines_to_task(dbdatas)
                    self._status_process()
                    self._set_modifications()
                    self.request.registry.notify(StatusChanged(self.request,
                                                    self.task))
                    debug = " > Estimation has been added/edited succesfully"
                    log.debug(debug)

                except Forbidden, e:
                    self.request.session.pop_flash("main")
                    self.request.session.flash(e.message, queue='error')

                # Redirecting to the project page
                return self.project_view_redirect()
        else:
            html_form = form.render(appstruct)
        return dict(title=title,
                    company=self.company,
                    html_form=html_form,
                    action_menu=self.actionmenu,
                    popups=self.popups
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
        for line in self.task.discounts:
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
        for line in dbdatas.get('discounts', []):
            dline = DiscountLine()
            merge_session_with_post(dline, line)
            self.task.discounts.append(dline)

    @view_config(route_name='estimation',
                renderer='tasks/view_only.mako',
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
                    submit_buttons=self.get_buttons(),
                    popups=self.popups
                    )

    @view_config(route_name='estimation', request_param='action=duplicate',
            permission='edit', renderer='base/formpage.mako')
    def duplicate(self):
        """
            Duplicates current estimation
        """
        try:
            ret_dict = self._status()
        except ValidationFailure, err:
            log.exception(u"Error duplicating an estimation")
            ret_dict = dict(html_form=err.render(),
                    title=u"Duplication d'un document")
        return ret_dict

    def gen_invoices(self):
        """
            Called when an estimation status is changed
            ( when no form is displayed : the estimation itself is not
            editable anymore )
        """
        for invoice in self.task.gen_invoices(self.user.id):
            self.dbsession.merge(invoice)
        self.request.session.flash(u"Vos factures ont bien été générées",
                                queue='main')


class EstimationStatus(StatusView):
    """
        Handle the estimation status processing
    """

    def redirect(self):
        project_id = self.request.context.project.id
        return HTTPFound(self.request.route_path('project', id=project_id))

    def post_status_process(self, task, status, params):
        """
            Handle specific status changes
        """
        dbsession = self.request.session
        if status == "geninv":
            for invoice in params:
                dbsession.merge(invoice)
            msg = u"Vos factures ont bien été générées"
            self.session.flash(msg)

        elif status == "aboest":
            msg = u"Le devis {0} a été annulé (indiqué sans suite)."
            self.session.flash(msg.format(task.number))

        elif status == 'delete':
            msg = u"Le devis {0} a été supprimé"
            dbsession.delete(task)
            dbsession.flush()
            self.session.flash(msg.format(task.number))
            raise self.redirect()

        elif status == 'duplicate':
            estimation = params
            estimation = dbsession.merge(estimation)
            dbsession.flush()
            id_ = estimation.id

            mess = u"Le devis a bien été dupliqué, vous pouvez l'éditer \
<a href='{0}'>Ici</a>."
            fmess = mess.format(self.request.route_path("estimation", id=id_))
            self.session.flash(fmess)

def delete(request):
    """
        Delete an estimation
    """
    task = request.context
    project = task.project
    log.info(u"# Deleting estimation {0}".format(task.number))
    try:
        task.set_status("delete", request, request.user.id)
    except Forbidden, err:
        log.exception(u"Forbidden operation")
        request.session.flash(err.message, queue="error")
    except:
        log.exception(u"Unknown error")
        request.session.flash(u"Une erreur inconnue s'est produite",
                queue="error")
    else:
        request.dbsession.delete(task)
        message = u"Le devis {0} a bien été supprimé.".format(task.number)
        request.session.flash(message, queue='main')
    return HTTPFound(request.route_path('project', id=project.id))


def includeme(config):
    config.add_view(make_pdf_view("tasks/estimation.mako"),
                    route_name='estimation',
                    request_param='view=pdf',
                    permission='view')
    config.add_view(delete,
                    route_name='estimation',
                    request_param='action=delete',
                    permission='edit')
    config.add_view(EstimationStatus,
                    route_name="estimation",
                    request_param='action=status',
                    permission="edit")

