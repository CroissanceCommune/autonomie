# -*- coding: utf-8 -*-
# * File Name : cancelinvoice.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    View for assets
"""
import logging

from deform import Form

from pyramid.view import view_config

from autonomie.views.forms.task import get_cancel_invoice_schema
from autonomie.models.model import CancelInvoice

from .base import TaskView
log = logging.getLogger(__name__)

class CancelInvoiceView(TaskView):
    """
        all views for cancelled invoices
    """
    schema = get_cancel_invoice_schema()
    add_title = u"Nouvel avoir"
    edit_title = u"Édition de l'avoir {task.number}"
    taskname_tmpl = u"Avoir {0}"
    tasknumber_tmpl = "{0}_{1}_A{2}_{3}"
    route = "cancelinvoice"

    @view_config(route_name="cancelinvoices",
                 renderer="tasks/form.mako",
                 permission="manage")
    @view_config(route_name="cancelinvoice", renderer="tasks/form.mako",
                permission='manage')
    def form(self):
        """
            Cancel invoice add/edit
        """
        log.debug("# CancelInvoice Form #")
        if self.taskid:
            title = self.edit_title.format(task=self.task)
            edit = True
            valid_msg = u"L'avoir a bien été édité."
        else:
            title = self.add_title
            edit = False
            valid_msg = u"L'avoir a bien été ajouté."

        appstruct = {}

        schema = self.schema.bind(phases=self.get_phases_choice(),
                                  tvas=self.get_tvas(),
                                  tasktype='cancelinvoice')
        form = Form(schema, buttons=self.get_buttons())
        form.widget.template = "autonomie:deform_templates/form.pt"
        if 'submit' in self.request.params:
            log.debug(" + Values have been submitted")
            datas = self.request.params.items()
            log.debug(datas)
        else:
            html_form = form.render(appstruct)
        return dict(title=title,
                    client=self.project.client,
                    company=self.company,
                    html_form=html_form,
                    action_menu=self.actionmenu)

    def get_task(self):
        """
            return the current task
        """
        document = CancelInvoice()
        document.CAEStatus = "draft"
        phaseid = self.request.params.get('phase')
        document.IDPhase = phaseid
        document.IDEmployee = self.user.id
        return document

    def set_lines(self):
        """
            set the lines
        """
        #TODO
        pass

