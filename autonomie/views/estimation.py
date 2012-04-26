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
from pyramid.url import route_path

from autonomie.models import DBSESSION
from autonomie.models.model import Tva
from autonomie.models.model import Estimation
from autonomie.models.model import Phase
from autonomie.views.forms.estimation import EstimationSchema
from autonomie.views.forms.estimation import get_appstruct
from autonomie.views.forms.estimation import get_dbdatas
from autonomie.views.forms.estimation import EstimationComputingModel
from autonomie.utils.pdf import render_html
from autonomie.utils.pdf import write_pdf
from autonomie.utils.config import load_config

from .base import BaseView

log = logging.getLogger(__name__)
def get_tvas():
    """
        return all configured tva amounts
    """
    tvas = DBSESSION().query(Tva).all()
    return [(tva.value, tva.name)for tva in tvas]

class EstimationView(BaseView):
    """
        All estimation related views
        form
        pdf
        html
    """

    def __init__(self, request):
        BaseView.__init__(self, request)
        self.company = self.get_current_company()
        self.project = self.get_current_project(self.company)
        self.taskid = self.request.matchdict.get('taskid')

    def redirect_to_view_only(self):
        """
            redirect the user to the view only url
        """
        return HTTPFound(route_path('estimation',
                            self.request,
                            cid=self.company.id,
                            id=self.project.id,
                            taskid=self.taskid,
                            _query=dict(view='html')))

    def get_current_project(self, company):
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


    @view_config(route_name="estimations", renderer='estimation.mako')
    @view_config(route_name='estimation', renderer='estimation.mako')
    def estimation_form(self):
        """
            Return the estimation edit view
        """
        if self.taskid:
            estimation = self.get_estimation()
            if not estimation.is_editable():
                return self.redirect_to_view_only()
            estimation_lines = estimation.lines
            payment_lines = estimation.payment_lines
            title = u"Édition du devis"
        else:
            # In case we've provided a phase argument in the url
            phaseid = self.request.params.get('phase')
            estimation = Estimation()
            estimation.IDPhase = phaseid
            estimation_lines = []
            payment_lines = []
            title = u"Nouveau devis"

        dbdatas = {'estimation':estimation.appstruct(),
                   'estimation_lines':[line.appstruct()
                                        for line in estimation_lines],
                   'payment_lines':[line.appstruct()
                                        for line in payment_lines]}
        # Get colander's schema compatible datas
        appstruct = get_appstruct(dbdatas)

        phase_choices = self.get_phases_choice()
        schema = EstimationSchema().bind(phases=phase_choices,
                                        tvas=get_tvas())
        form = Form(schema, buttons=("submit", ))

        if 'submit' in self.request.params:
            datas = self.request.params.items()
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, e:
                html_form = e.render()
            else:
                dbdatas = get_dbdatas(appstruct)
                html_form = form.render(appstruct)
        else:
            html_form = form.render(appstruct)
        return dict(title=title,
                    client=self.project.client,
                    company=self.company,
                    html_form = html_form
                    )

    def get_estimation(self):
        """
            get the current estimation
        """
        if self.taskid:
            return self.project.get_estimation(self.taskid)
        else:
            return Estimation()

    def html(self, estimation):
        """
            Returns an html version of the current estimation
        """
        estimationcompute = EstimationComputingModel(estimation)
        template = "estimation_html.mako"
        config = load_config(self.dbsession)
        datas = dict(
                    company=self.company,
                    project=self.project,
                    estimation=estimationcompute,
                    config=config
                    )
        return render_html(self.request, template, datas)

    @view_config(route_name='estimation',
                renderer='html_view.mako',
                request_param='view=html')
    def html_estimation(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        estimation = self.get_estimation()
        title = u"Devis numéro : {0}".format(estimation.number)
        return dict(
                    title=title,
                    company=self.company,
                    html_datas=self.html(estimation)
                    )

    @view_config(route_name='estimation',
                renderer='html_view.mako',
                request_param='view=pdf')
    def estimation_pdf(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        estimation = self.get_estimation()
        filename = "{0}.pdf".format(estimation.number)
        write_pdf(self.request, filename, self.html(estimation))
        return self.request.response
