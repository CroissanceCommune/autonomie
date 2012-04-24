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

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_path

from autonomie.models.model import Project
from autonomie.utils.forms import merge_session_with_post
from autonomie.views.forms import ProjectSchema
from .base import ListView

log = logging.getLogger(__name__)

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

class ProjectView(ListView):
    """
        All the projects views are grouped in this class
    """
    columns = ("code", "name")
    @view_config(route_name='company_projects',
                 renderer='company_projects.mako',\
                 request_method='GET')
    def company_projects(self):
        """
            Return the list of projects
        """
        log.debug("Getting projects")
        search, sort, direction, current_page, items_per_page = \
                                                self._get_pagination_args()

        company = self.get_current_company()

    #    toquery = (Project.id, Project.client, Project.name)
        #TODO : handle join tables to search by client

        if company is not None:
            projects = self.dbsession.query(Project).filter(
                                Project.name.like(search+"%"),
                                Project.id_company == company.id
                        ).order_by(sort + " " + direction)
        else:
            projects = self.dbsession.query(Project).filter(
                                Project.name.like(search+"%")
                        ).order_by(sort + " " + direction)

        records = self._get_pagination(projects, current_page, items_per_page)

        clients = company.clients
        form = get_project_form(clients=clients,
                                path=route_path('company_projects',
                                                self.request,
                                                cid=company.id))
        return dict(title=u"Projets",
                    projects=records,
                    company=company,
                    html_form=form.render())

    @view_config(route_name='company_projects',  \
                 renderer='company_project.mako', \
                 request_method='POST')
    @view_config(route_name='company_project', \
                 renderer='company_project.mako', \
                 request_param='edit')
    def company_project(self):
        """
            Returns:
            * the company edit form
            or
            * the company add form when an error has occured
        """
        company = self.get_current_company()


        project_id = self.request.matchdict.get('id')
        if project_id: # edition
            project = company.get_project(project_id)
            edit = True
            default_client = project.client
        else: # new project
            project = Project()
            project.id_company = company.id
            edit = False
            default_client = None

        clients = company.clients
        form = get_project_form(clients,
                                default_client,
                                edit=edit)
        if 'submit' in self.request.params:
            # form POSTed
            datas = self.request.params.items()
            try:
                app_datas = form.validate(datas)
                log.debug(app_datas)
            except ValidationFailure, errform:
                html_form = errform.render()
            else:
                log.debug(app_datas)
                project = merge_session_with_post(project, app_datas)
                # The returned project is a persistent object
                project = self.dbsession.merge(project)
                if edit:
                    message = u"Le projet <b>{0}</b> a été édité avec \
succès".format(project.name)
                else:
                    message = u"Le projet <b>{0}</b> a été ajouté avec \
succès".format(project.name)
                self.request.session.flash(message, queue='main')
                # Flusing the session launches sql queries
                self.dbsession.flush()
                return HTTPFound(route_path('company_project',
                                            self.request,
                                            cid=company.id,
                                            id=project.id))
        else:
            html_form = form.render(project.appstruct())
        return dict(title=project.name,
                    project=project,
                    html_form=html_form,
                    company=company)

    @view_config(route_name='company_project', renderer='project_view.mako')
    def company_project_view(self):
        """
            Company's project view
        """
        company = self.get_current_company()
        project_id = self.request.matchdict.get('id')
        project = company.get_project(project_id)
        return dict(title=project.name,
                    project=project,
                    company=company)

