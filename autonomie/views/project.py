# -*- coding: utf-8 -*-
# * File Name : project.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 29-03-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Project views
"""
import logging

from functools import partial

from deform import ValidationFailure
from deform import Form
from deform import Button
from webhelpers import paginate

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_path
from pyramid.url import current_route_url

from autonomie.models import DBSESSION
from autonomie.models.model import Project
from autonomie.models.model import Tva
from autonomie.utils.forms import merge_session_with_post
from autonomie.views.forms import ProjectSchema
from autonomie.views.forms.estimation import EstimationSchema

log = logging.getLogger(__name__)

def get_tvas():
    """
        return all configured tva amounts
    """
    tvas = DBSESSION().query(Tva).all()
    return [(tva.value, tva.name)for tva in tvas]

def get_page_url(request, page):
    """
        Return a url generator for pagination
    """
    args = request.GET
    args['page'] = str(page)
    return current_route_url(request, page=page, _query=args)

def build_client_value(client):
    """
        return the tuple for building client select
    """
    if client:
        return (client.id, client.name)
    else:
        return (u" - ", u"Sélectionnez")

def build_client_values(clients):
    """
        Build human understandable client labels
        allowing efficient discrimination
    """
    return [build_client_value(client)
                            for client in clients]
def get_project_form(clients, default_client=None, edit=False, path=""):
    """
        Returns the project add/edit form
    """
    choices = build_client_values(clients)
    default = build_client_value(default_client)
    schema = ProjectSchema().bind(edit=edit, choices=choices, default=default)
    form = Form(schema, actions=path, buttons=(Button(name='submit',
                                        title=u'Validez',
                                        type='submit'),))
    return form

@view_config(route_name='company_projects', renderer='company_projects.mako',
                                            request_method='GET')
def company_projects(request):
    """
        Return the list of projects
    """
    log.debug("Getting projects")
    search = request.params.get("search", "")
    sort = request.params.get('sort', 'name')

    direction = request.params.get("direction", 'asc')
    if direction not in ['asc', 'desc']:
        direction = 'asc'


    cid = request.matchdict.get('cid')
    avatar = request.session['user']
    company = avatar.get_company(cid)
#    toquery = (Project.id, Project.client, Project.name)
    dbsession = DBSESSION()
    projects = dbsession.query(Project).filter(
            Project.name.like(search+"%"),
            Project.id_company == cid).order_by(sort + " " + direction)
    page_url = partial(get_page_url, request=request)
    current_page = int(request.params.get("page", 1))
    records = paginate.Page(projects,
                    current_page,
                    url=page_url,
                    items_per_page=15,)
#    projects = company.projects
    clients = company.clients
    form = get_project_form(clients=clients,
                            path=route_path('company_projects',
                                            request,
                                            cid=cid))
    return dict(title=u"Projets",
                projects=records,
                company=company,
                html_form=form.render())

@view_config(route_name='company_projects', renderer='company_project.mako',
                                                        request_method='POST')
@view_config(route_name='company_project', renderer='company_project.mako')
def company_project(request):
    """
        Returns the company edit view and add-error
    """
    cid = request.matchdict.get('cid')
    project_id = request.matchdict.get('id')
    avatar = request.session['user']
    company = avatar.get_company(cid)
    clients = company.clients
    if project_id: # edition
        project = company.get_project(project_id)
        edit = True
        default_client = project.client
    else: # new project
        project = Project()
        project.id_company = cid
        edit = False
        default_client = None
    form = get_project_form(clients,
                            default_client,
                            edit=edit)
    dbsession = DBSESSION()
    if 'submit' in request.params:
        # form POSTed
        datas = request.params.items()
        log.debug("Datas")
        log.debug(datas)
        try:
            app_datas = form.validate(datas)
            log.debug(app_datas)
        except ValidationFailure, errform:
            html_form = errform.render()
        else:
            log.debug(app_datas)
            project = merge_session_with_post(project, app_datas)
            dbsession.merge(project)
            if edit:
                message = u"Le projet <b>%s</b> a été édité avec succès" % (
                                                                project.name,)
            else:
                message = u"Le projet <b>%s</b> a été ajouté avec succès" % (
                                                                project.name,)
            request.session.flash(message, queue='main')
            return HTTPFound(route_path('company_projects', request, cid=cid))
    else:
        html_form = form.render(project.appstruct())
    return dict(title=project.name,
                project=project,
                html_form=html_form,
                company=company)

@view_config(route_name='estimation', renderer='estimation.mako')
def estimation(request):
    """
        Return the estimation edit view
    """
    log.debug("## In Estimation ##")
    cid = request.matchdict.get('cid')
    project_id = request.matchdict.get('id')
    avatar = request.session['user']

    company = avatar.get_company(cid)
    clients = company.clients
    project = company.get_project(project_id)


    phases = project.phases
    phase_choices = ((phase.id, phase.name) for phase in phases)
    form = Form(EstimationSchema().bind(phases=phase_choices,
                                     tvas=get_tvas()),
                buttons=('submit',))
    if 'submit' in request.params:
        log.debug('***** Submitted')
        datas = request.params.items()
        log.debug(datas)
        try:
            app_struct = form.validate(datas)
            log.debug("   + Validated : app_struct")
            log.debug(app_struct)
        except ValidationFailure, e:
            log.debug("   - Error in validation")
            html_form = e.render()
        else:
            html_form = form.render(app_struct)
    else:
        html_form = form.render()
#    schema = EstimationFormSchema()
#    form = EstimationForm(schema)
#
#    #TODO : add sequenceNumber regarding the project
#    #TODO : add task status (history)
#    #TODO : handle status (CAEStatus)
#    if 'submit' in request.params:
#        datas = request.params
#        try:
#            app_struct = form.validate(datas)
#        except ValidationFailure, e:
#            errors = e
#        else:
#            estimation, task = merge_appstruct_to_estimation(app_struct)
#            dbsession = DBSESSION()
#            dbsession.merge(estimation)
#            dbsession.merge(task)
#            #dbsession.merge(
#            dbsession.commit()
#            return HTTPFound(route_path(company_projects,
#                                        cid=cid,
#                                        project_id=project_id))
#
    #form = Form(EstimationSchema(), buttons=('submit','cancel',))

    return dict(title=u'Nouveau devis',
                client=project.client,
                company=company,
                html_form = html_form
                )
