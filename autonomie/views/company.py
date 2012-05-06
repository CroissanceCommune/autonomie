# -*- coding: utf-8 -*-
# * File Name : company.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 27-03-2012
# * Last Modified :
#
# * Project : autonomie
#
"""
    Views for the company handling
    Entry point for the main users
"""
import os
import logging
from deform import ValidationFailure
from pyramid.view import view_config

from deform import Form
from autonomie.views.forms import CompanySchema
from autonomie.views.forms.estimation import TaskComputing
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.config import load_config

from .base import BaseView

log = logging.getLogger(__name__)

class CompanyViews(BaseView):
    """
        all company related views
    """
    @view_config(route_name='company', renderer='company_index.mako')
    def company_index(self):
        """
            index page for the company shows latest news :
                - last validated estimation/invoice
                - To be relaunched bill
        """
        company = self.get_current_company()
        ret_val = dict(title=u"{0}".format(company.name,),
                    company=company)
        # recovering last activities
        all_tasks = []
        all_invoices = []
        for project in company.projects:
            all_tasks.extend(project.estimations)
            all_tasks.extend(project.invoices)
            all_invoices.extend(project.invoices)

        all_tasks = sorted(all_tasks,
                            key=lambda a:a.statusDate,
                            reverse=True)
        ret_val['tasks'] = all_tasks[:10]

        # recovering elapsed invoices for warning
        elapsed_invoices = [TaskComputing(invoice) \
                        for invoice in all_invoices if invoice.is_tolate()]
        elapsed_invoices = sorted(elapsed_invoices,
                                key=lambda a:a.model.taskDate,
                                reverse=True)
        ret_val['elapsed_invoices'] = elapsed_invoices
        return ret_val

    @view_config(route_name='company', renderer='company_edit.mako',
                                                    request_param='edit')
    def company_edit(self):
        """
            Company edition page
        """
        company = self.get_current_company()
        root_path = load_config(self.dbsession, "files_dir").get('files_dir',
                                                                        '/tmp')
        company_path = os.path.join(root_path, company.get_path())
        company_url = os.path.join("/assets", company.get_path())
        schema = CompanySchema().bind(edit=True,
                                    rootpath=company_path,
                                    rooturl=company_url,
                                    session=self.request.session)
        form = Form(schema, buttons=('submit', ))
        if 'submit' in self.request.params:
            datas = self.request.params.items()
            try:
                app_datas = form.validate(datas)
            except ValidationFailure, errform:
                html_form = errform.render()
            else:
                company = merge_session_with_post(company, app_datas)
                self.dbsession.merge(company)
                message = u"Votre entreprise a bien été éditée"
                self.request.session.flash(message, queue='main')
                html_form = form.render(company.appstruct())
        else:
            html_form = form.render(company.appstruct())
        return dict(title=company.name,
                    company=company,
                    html_form=html_form)
