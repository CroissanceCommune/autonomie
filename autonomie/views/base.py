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
import itertools
from functools import partial
from deform import Form
from deform import Button

from sqlalchemy import desc, asc

from webhelpers import paginate
from webhelpers.html import tags
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from autonomie.models.model import Phase
from autonomie.models.model import Project
from autonomie.models.model import Tva
from autonomie.utils.views import get_page_url
from autonomie.utils.widgets import ActionMenu
from autonomie.utils.widgets import Submit
from autonomie.utils.widgets import ViewLink
from autonomie.utils.widgets import PopUp
from autonomie.exception import Forbidden
from autonomie.views.mail import StatusChanged
from autonomie.views.forms.task import Payment
from autonomie.views.forms.task import Duplicate
from autonomie.utils.pdf import write_pdf
from autonomie.utils.pdf import render_html


log = logging.getLogger(__name__)

class BaseView(object):
    """
        Base View object
    """
    def __init__(self, request):
        log.debug("We are in the view : %s"  %self)
        self.request = request
        self.context = request.context
        self.dbsession = request.dbsession()
        self.session = request.session
        self.user = request.user
        self.actionmenu = ActionMenu()

    def get_company_id(self):
        """
            Return current company Id
        """
        return self.request.matchdict.get('cid')

    def get_current_company(self):
        """
            Returns the current company
        """
        try:
            company = self.user.get_company(self.get_company_id())
        except KeyError:
            raise HTTPForbidden()
        return company

class ListView(BaseView):
    """
        Base view object for listing elements
    """
    columns = dict()
    default_sort = 'name'
    default_direction = 'asc'
    def _get_pagination_args(self):
        """
            Returns arguments for element listing
        """
        search = self.request.params.get("search", "")
        sort_key = self.request.params.get('sort', self.default_sort)
        if sort_key not in self.columns:
            sort_key = self.default_sort
        if isinstance(self.columns, dict):
            sort = self.columns[sort_key]
        else:
            sort = sort_key

        direction = self.request.params.get("direction",
                                    self.default_direction)
        if direction not in ['asc', 'desc']:
            direction = self.default_direction

        default_item_pp = int(self.request.cookies.get('items_per_page', 10))
        items_per_page = int(self.request.params.get('nb', default_item_pp))
        self.request.response.set_cookie("items_per_page", str(items_per_page))
        self.request.cookies['items_per_page'] = str(items_per_page)

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

    @staticmethod
    def _sort(query, column, direction):
        """
            Return a sorted query
        """
        if direction == 'asc':
            func = asc
        else:
            func = desc
        return query.order_by(func(column))

class TaskView(BaseView):
    """
        BaseTask related view
        Base object for estimation and invoice views
    """
    type_ = u""
    model = None
    schema = None
    add_title = u""
    edit_title = u""
    route = u""
    template = u""

    def __init__(self, request):
        BaseView.__init__(self, request)
        if self.request.context.__name__ == 'project':
            self.project = self.request.context
            self.company = self.project.company
            self.taskid = None
            self.task = self.get_task()
        else:
            self.task = self.request.context
            self.taskid = self.task.id
            self.project = self.task.project
            self.company = self.project.company
        self._set_actionmenu()
        self.popups = {}
        self.set_lines()
        self.formcounter = itertools.count()

    def get_task(self):
        """
            should return the current task
        """
        if self.model:
            task = self.model()
            log.debug(" + A new task has been built")
        else:
            raise Exception("Not implemented yet")
        phaseid = self.request.params.get('phase')
        task.phase_id = phaseid
        task.owner_id = self.user.id
        return task

    def set_lines(self):
        """
            add task lines to self
        """
        raise Exception("Not implemented yet")

    def redirect_to_view_only(self):
        """
            redirect the user to the view only url
        """
        return HTTPFound(self.request.route_path(
                            self.route,
                            id=self.taskid,
                            _query=dict(view='html')
                            ))

    def add_default_phase(self):
        """
            Adds a default phase to an existing project
        """
        default_phase = Phase(name=u"Phase par défaut")
        default_phase.project_id = self.project.id
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
        return getattr(self.project, "get_next_%s_number" % self.type_)()

    def get_taskname(self):
        """
            set the current taskname
        """
        return self.model.get_name(self.get_sequencenumber())

    def get_tasknumber(self, taskDate):
        """
            return the task number
        """
        return self.model.get_number(self.project,
                                     self.get_sequencenumber(),
                                     taskDate)

    def get_taskstatus(self):
        """
            get the status asked when validating the form
        """
        return self.request.params['submit']

    def get_tvas(self):
        """
            return all configured tva amounts
        """
        tvas = Tva.query(self.dbsession)
        return [(tva.value, tva.name)for tva in tvas]

    def _aboest_btn(self):
        """
            Return a button to abort an estimation
        """
        yield Submit(u"Indiquer sans suite",
                     title=u"Indiquer que le devis n'aura pas de suite",
                     value="aboest",
                     request=self.request)

    def _geninv_btn(self):
        """
            Return a button for invoice generation
        """
        yield Submit(u"Générer les factures",
                  title=u"Générer les factures correspondantes au devis",
                  value="geninv",
                  request=self.request)

    def _paid_form(self):
        """
            return the form for payment registration
        """
        valid_btn = Button(name='submit', value="paid", type='submit',
                                                        title=u"Valider")
        schema = Payment().bind(task=self.task)
        action = self.request.route_path(self.route,
                                         id=self.context.id,
                                        _query=dict(action='payment'))
        form = Form(schema=schema, buttons=(valid_btn,), action=action,
                counter=self.formcounter)
        return form

    def _cancel_btn(self):
        """
            Return a cancel btn returning the user to the project view
        """
        yield ViewLink(u"Revenir en arrière",
                          "view",
                          path="project",
                          css="btn btn-primary",
                          request=self.request,
                          id=self.project.id)

    def _pdf_btn(self):
        """
            Return a PDF view btn
        """
        if self.task.id:
            yield ViewLink(u"Voir le PDF", "view",
               path=self.route, css="btn btn-primary", request=self.request,
               id=self.task.id, _query=dict(view="pdf"))

    def _draft_btn(self):
        """
            Return the draft btn
        """
        yield Submit(u"Enregistrer comme brouillon",
                            value="draft",
                            request=self.request,
                            )

    def _wait_btn(self):
        """
            Return the btn for asking wait status
        """
        yield Submit(u"Enregistrer et demander la validation",
                       value="wait",
                       request=self.request
                       )

    def _duplicate_form(self):
        """
            Return the form for task duplication
        """
        self.request.js_require.add('duplicate')
        # création du schéma pour le formulaire
        clients = self.company.clients
        clients_options = [(cli.id, u"%s (%s)" % (cli.name, cli.code))
                                                for cli in clients]
        projects = self.project.client.projects
        projects_options = [(pro.id, u"%s (%s)" % (pro.name, pro.code))
                                                    for pro in projects]
        all_projects = []
        all_phases = []
        for client in self.company.clients:
            for project in client.projects:
                all_projects.append(project)
                all_phases.extend(project.phases)

        phases = self.project.phases
        phases_options = [(phase.id, phase.name) for phase in phases]
        schema = Duplicate().bind(
                clients=clients_options,
                current_client=self.project.client.id,
                projects=projects_options,
                current_project=self.project.id,
                phases=phases_options,
                current_phase=self.context.phase.id,
                all_projects=all_projects,
                all_phases=all_phases)

        # Création de la popup pour le formulaire
        action = self.request.route_path(self.route,
                                         id=self.context.id,
                                         _query=dict(action='duplicate'))
        valid_btn = Button(name='submit', value="duplicate", type='submit',
                                                        title=u"Valider")
        form = Form(schema=schema, buttons=(valid_btn,), action=action,
                formid="duplicate_form", counter=self.formcounter)
        return form

    def _duplicate_btn(self):
        """
            Return the button for asking duplication of the current document
        """
        title = u"Dupliquer un document"
        form = self._duplicate_form()
        popup = PopUp("duplicate_form_container", title, form.render())
        self.popups[popup.name] = popup
        yield popup.open_btn(css='btn btn-primary')

    def _valid_btn(self):
        """
            Return the valid button
        """
        yield Submit(u"Valider le document",
                    value="valid",
                    request=self.request)

    def _invalid_btn(self):
        """
            Return the invalid button
        """
        yield Submit(u"Document invalide",
                     value="invalid",
                     request=self.request)

    def _paid_btn(self):
        """
            Return a button to set a paid btn and a select to choose
            the payment mode
        """

        if has_permission("manage", self.context, self.request):
            form = self._paid_form()
            title = u"Notifier un paiement"
            popup = PopUp("paidform", title, form.render())
            self.popups[popup.name] = popup
            yield popup.open_btn(css='btn btn-primary')

    def _aboinv_btn(self):
        """
            Return a button to abort an invoice
        """
        yield Submit(u"Annuler cette facture",
                 value="aboinv",
                 request=self.request,
                 confirm=u"Êtes-vous sûr de vouloir annuler cette facture ?")

    def _gencinv_btn(self):
        """
            Return a button for generating a cancelinvoice
        """
        yield Submit(u"Générer un avoir",
                     value="gencinv",
                     request=self.request)

    def _delete_btn(self):
        """
            Return a button for deleting a document
        """
        yield Submit(u"Supprimer ce document",
                  value="delete",
                  request=self.request,
                  confirm=u"Êtes-vous sûr de vouloir supprimer ce document ?")


    def get_buttons(self):
        """
            returns submit buttons for estimation/invoice form
        """
        btns = []
        actions = self.task.get_next_actions()
        log.debug("   + Available actions :")
        for action in actions:
            log.debug("    * {0}".format(action.name))
            if action.allowed(self.context, self.request):
                log.debug("     -> is allowed for the current user")
                if hasattr(self, "_%s_btn" % action.name):
                    func = getattr(self, "_%s_btn" % action.name)
                    btns.extend(func())
        btns.extend(self._cancel_btn())
        btns.extend(self._pdf_btn())
        return btns

    def _set_actionmenu(self):
        """
            Build the action menu for the task views
        """
        self.actionmenu.add(
                ViewLink(u"Revenir au projet", "edit",
                    path="project", id=self.project.id))

    def project_view_redirect(self):
        """
            return a http redirect object to the project page
        """
        return HTTPFound(self.request.route_path(
                            'project',
                            id=self.project.id))

    def _status_process(self):
        """
            Change the current task's status
        """
        status = self.get_taskstatus()
        params = dict(self.request.params.items())

        if hasattr(self, "_pre_status_process"):
            params = getattr(self, "_pre_status_process")(status, params)

        log.debug(" pre status process is OK")

        data = self.task.set_status(status,
                                    self.request,
                                    self.user.id,
                                    **params)

        log.debug(u" + The status is set to {0}".format(status))

        if hasattr(self, "_post_status_process"):
            getattr(self, "_post_status_process")(status, data)

    def _pre_status_process(self, status, params):
        """
            Validates the duplication form before duplicating
        """
        log.debug("# In pre Status process #")
        if status == "duplicate":
            log.debug(" * Duplicating the current task")
            form = self._duplicate_form()
            appstruct = form.validate(params.items())
            log.debug(" * Form has been validated")
            project_id = appstruct.get('project')
            project = Project.get(project_id)
            phase_id = appstruct.get('phase')
            phase = Phase.get(phase_id)
            log.debug(" * Phase : %s" % phase)
            log.debug(" * Project : %s" % project)
            appstruct['phase'] = phase
            appstruct['project'] = project
            appstruct['user'] = self.user
            log.debug("Appstruct : %s" % appstruct)
            return appstruct
        return params

    def _set_modifications(self):
        """
            Set the modifications in the database
        """
        log.debug(" = > Flushing modification to the database")
        self.task = self.dbsession.merge(self.task)
        self.dbsession.flush()

    def _status(self):
        """
            Change the status of the document
        """
        log.debug("# Document status modification #")
        log.debug(self.request.params)
        valid_msg = u"Le statut a bien été modifié"
        if 'submit' in self.request.params:
            try:
                self._status_process()
                self._set_modifications()
                self.request.registry.notify(StatusChanged(self.request,
                                                    self.task))
                self.request.session.flash(valid_msg, queue="main")
            except Forbidden, e:
                log.exception(u" !! Unauthorized action by : {0}".format(
                                                        self.user.login))
                self.request.session.pop_flash("main")
                self.request.session.flash(e.message, queue='error')
        return self.project_view_redirect()

    def _html(self):
        """
            Returns an html version of the current document
        """
        template = self.template
        config = self.request.config
        datas = dict(
                    company=self.company,
                    project=self.project,
                    task=self.task,
                    config=config
                    )
        return render_html(self.request, template, datas)

    def _pdf(self):
        """
            Returns a page displaying an html rendering of the current task
        """
        log.debug("# Generating the pdf file #")
        filename = u"{0}.pdf".format(self.task.number)
        write_pdf(self.request, filename, self._html())
        return self.request.response
