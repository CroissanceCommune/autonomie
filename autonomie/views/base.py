# -*- coding: utf-8 -*-
# * File Name : base.py
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
    Base views with commonly used utilities
"""
import logging
from functools import partial

from webhelpers import paginate
from deform import Button
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_path

from autonomie.models import DBSESSION
from autonomie.models.model import Phase
from autonomie.models.model import Tva
from autonomie.utils.views import get_page_url

log = logging.getLogger(__file__)

class BaseView(object):
    """
        Base View object
    """
    def __init__(self, request):
        self.request = request
        self.dbsession = DBSESSION()
        self.user = self.get_avatar()

    def get_company_id(self):
        """
            Return current company Id
        """
        return self.request.matchdict.get('cid')

    def get_avatar(self):
        """
            Return the user's avatar
        """
        return self.request.session['user']

    def get_current_company(self):
        """
            Returns the current company
        """
        #FIXME : Handle admin or not here ?
        try:
            company = self.user.get_company(self.get_company_id())
        except KeyError:
            raise HTTPForbidden()
        return company

class ListView(BaseView):
    """
        Base view object for listing elements
    """
    columns = ()
    def _get_pagination_args(self):
        """
            Returns arguments for element listing
        """
        search = self.request.params.get("search", "")
        sort = self.request.params.get('sort', 'name')
        if sort not in self.columns:
            sort = "name"

        direction = self.request.params.get("direction", 'asc')
        if direction not in ['asc', 'desc']:
            direction = 'asc'

        items_per_page = int(self.request.params.get('nb', 10))

        current_page = int(self.request.params.get("page", 1))
        return search, sort, direction, current_page, items_per_page

    def _get_pagination(self, records, current_page, items_per_page):
        """
            return a pagination object
        """
        page_url = partial(get_page_url, request=self.request)
        return paginate.Page(records,
                             current_page,
                             url=page_url,
                             items_per_page=items_per_page)

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

    def get_task(self):
        """
            should return the current task
        """
        raise Exception("Not implemented yet")

    def set_lines(self):
        """
            add task lines to self
        """
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

    def get_sequencenumber(self):
        """
            set the sequence number
            don't know really if this column matters
        """
        return len(self.project.estimations) + 1

    def get_taskname(self):
        """
            set the current taskname
        """
        return self.taskname_tmpl.format(self.get_sequencenumber())

    def get_tasknumber(self, taskDate):
        """
            return the task number
        """
        date = "{0}{1}".format(
                               taskDate.month,
                               str(taskDate.year)[2:])
        pcode = self.project.code
        ccode = self.project.client.id
        return self.tasknumber_tmpl.format(
                                  pcode,
                                  ccode,
                                  self.get_sequencenumber(),
                                  date)
    def get_taskstatus(self):
        """
            Set all status related attributes
        """
        return self.request.params['submit']

    def get_tvas(self):
        """
            return all configured tva amounts
        """
        tvas = self.dbsession.query(Tva).all()
        return [(tva.value, tva.name)for tva in tvas]

    def get_buttons(self):
        """
            returns submit buttons for estimation/invoice form
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


