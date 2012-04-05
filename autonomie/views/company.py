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
from autonomie.views.forms import CompanySchema

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
        ret_val = dict(title=u"Autonomie", company=company)
    except KeyError:
        ret_val = HTTPForbidden()
    return ret_val

@view_config(route_name='company', renderer='company_edit.mako', request_param='edit')
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
    schema = CompanySchema().bind(edit=True)
    form = Form(schema, buttons=('submit', ))
    if 'submit' in request.params:
        datas = request.params.items()
        print datas
        try:
            app_datas = form.validate(datas)
        except ValidationFailure, errform:
            html_form = errform.render()
        else:
            company = merge_session_with_post(client, app_datas)
            dbsession.merge(client)
            request.session.flash(message, queue='main')
            html_form = form.render(company.appstruct())
    else:
        html_form = form.render(company.appstruct())
    return dict(title=company.name,
                company=company,
                html_form=html_form)
