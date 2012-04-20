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
import logging
from deform import ValidationFailure
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden

from deform import Form
from autonomie.models import DBSESSION
from autonomie.models.model import Estimation
from autonomie.views.forms import CompanySchema
from autonomie.utils.forms import merge_session_with_post

log = logging.getLogger(__name__)
@view_config(route_name='company', renderer='company_index.mako')
def company_index(request):
    """
        index page for the company shows latest news :
            #TODO
            - last validated estimation/invoice
            - To be relaunched bill
    """
    cid = request.matchdict.get('cid')
    avatar = request.session['user']
    try:
        company = avatar.get_company(cid)
        ret_val = dict(title=u"{0}".format(company.name,),
                                            company=company)
        all_statuses = []
        for project in company.projects:
            for estimation in project.estimations:
                all_statuses.extend(estimation.taskstatus)
            for invoice in project.invoices:
                all_statuses.extend(invoice.taskstatus)
        sorted(all_statuses, key=lambda a:a.statusDate, reverse=True)
        ret_val['status'] = all_statuses[:10]

        dbsession = DBSESSION()
        a = dbsession.query(Estimation).filter(Estimation.IDTask==6495).first()

    except KeyError:
        ret_val = HTTPForbidden()
    return ret_val

@view_config(route_name='company', renderer='company_edit.mako',
                                                request_param='edit')
def company_edit(request):
    """
        Company edition page
    """
    cid = request.matchdict.get('cid')
    avatar = request.session['user']
    try:
        company = avatar.get_company(cid)
    except KeyError:
        return HTTPForbidden()
    schema = CompanySchema().bind(edit=True, rootpath='/tmp/%s'%company.id,
                                    session=request.session)
    form = Form(schema, buttons=('submit', ))
    if 'submit' in request.params:
        dbsession = DBSESSION()
        datas = request.params.items()
        print datas
        try:
            app_datas = form.validate(datas)
        except ValidationFailure, errform:
            html_form = errform.render()
        else:
            company = merge_session_with_post(company, app_datas)
            dbsession.merge(company)
            message = u"Votre entreprise a bien été éditée"
            request.session.flash(message, queue='main')
            html_form = form.render(company.appstruct())
    else:
        html_form = form.render(company.appstruct())
    return dict(title=company.name,
                company=company,
                html_form=html_form)
