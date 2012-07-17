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

from sqlalchemy import desc, asc

from webhelpers import paginate
from webhelpers.html import tags
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound

from autonomie.models.model import Phase
from autonomie.models.model import Tva
from autonomie.utils.views import get_page_url
from autonomie.utils.widgets import ActionMenu
from autonomie.utils.widgets import Submit
from autonomie.utils.widgets import ViewLink
from autonomie.utils.widgets import StaticWidget
from autonomie.utils.exception import Forbidden
from autonomie.views.mail import StatusChanged
from autonomie.utils.pdf import write_pdf

log = logging.getLogger(__name__)

class BaseView(object):
    """
        Base View object
    """
    def __init__(self, request):
        self.request = request
        self.dbsession = request.dbsession()
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
    schema = None
    add_title = u""
    edit_title = u""
    taskname_tmpl = u""
    tasknumber_tmpl = u""
    route = u""

    def __init__(self, request):
        BaseView.__init__(self, request)
        if self.request.context.__name__ == 'project':
            self.project = self.request.context
            self.company = self.project.company
            self.taskid = None
            self.task = self.get_task()
        else:
            self.task = self.request.context
            self.taskid = self.task.IDTask
            self.project = self.task.project
            self.company = self.project.company
        self._set_actionmenu()
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

    def get_tasknumber(self, taskDate, tmpl=None, seq_number=None):
        """
            return the task number
        """
        pcode = self.project.code
        ccode = self.project.client.id
        if not tmpl:
            tmpl = self.tasknumber_tmpl
        if not seq_number:
            seq_number = self.get_sequencenumber()
        return tmpl.format( pcode,
                            ccode,
                            seq_number,
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

    def _draft_btns(self):
        """
            Return buttons used on a draft document
        """
        if self.task.is_draft():
            yield Submit(u"Enregistrer comme brouillon",
                                "edit",
                                value="draft",
                                request=self.request,
                                )
            if not self.task.is_cancelinvoice():
                yield Submit(u"Enregistrer et demander la validation",
                               "edit",
                               value="wait",
                               request=self.request
                               )

    def _est_btns(self):
        """
            Return the button used to generate invoices or abort an estimation
        """
        if self.task.is_estimation() and (self.task.is_valid()
                                          or self.task.is_sent()):
            yield Submit(u"Générer les factures",
                     "edit",
                      title=u"Générer les factures correspondantes au devis",
                      value="geninv",
                      request=self.request)
            yield Submit(u"Indiquer sans suite",
                    "edit",
                    title=u"Indiquer que le devis n'aura pas de suite",
                    value="aboest",
                    request=self.request)

    def _sent_to_client_btn(self):
        """
            Return a button to change the status to "sent"
        """
        if self.task.is_valid():
            yield Submit(u"Envoyé au client",
                "edit",
                title=u"Indiquer que le document a bien été envoyé au client",
                value="sent",
                request=self.request)

    def _call_client_btn(self):
        """
            Return a button to change the status to "client has been called"
        """
        # This button is displayed only for invoices (which have a
        # IDEstimation attr) and if the doc is valid
        if self.task.has_been_validated() and self.task.is_invoice():
            yield Submit(u"Client relancé",
                        "edit",
                        title=u"Indiquer que le client a été relancé",
                        value="recinv",
                        request=self.request)

    @staticmethod
    def _paid_mod_select():
        """
            Return a select object for paiment mode select
        """
        options = tags.Options((('CHEQUE', u"Par chèque",),
                                ('VIREMENT', u"Par virement")))
        select = tags.select('paymentMode', [], options, **{'class':'span2'})
        return select

    def _paid_btn(self):
        """
            Return a button to set a paid btn and a select to choose
            the payment mode
        """
        if self.task.has_been_validated() and \
                not self.task.is_estimation() and \
                not self.task.is_paid():
            if self.task.is_cancelinvoice():
                label = u"Avoir payé"
            else:
                label = u"Facture payée"
            yield Submit(label,
                         "manage",
                         value="paid",
                         request=self.request)
            yield StaticWidget(self._paid_mod_select(),
                        "manage")

    def _aboinv_btn(self):
        """
            Return a button to abort an invoice
        """
        if self.task.has_been_validated() and \
                self.task.is_invoice() and \
                not self.task.is_paid():
            yield Submit(u"Annuler cette facture",
                                "manage",
                                value="aboinv",
                                request=self.request)

    def _validate_btns(self):
        """
            Return the buttons to handle validation
        """
        if self.task.is_waiting() or (
                    self.task.is_cancelinvoice() and self.task.is_draft()):
            yield Submit(u"Valider le document",
                        "manage",
                        value="valid",
                        request=self.request)
        if self.task.is_waiting():
            yield Submit(u"Document invalide",
                        "manage",
                        value="invalid",
                        request=self.request)

    def _cancel_btn(self):
        """
            Return a cancel btn returning the user to the project view
        """
        yield ViewLink(u"Annuler",
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

    def get_buttons(self):
        """
            returns submit buttons for estimation/invoice form
        """
        btns = []
        btns.extend(self._draft_btns())
        btns.extend(self._est_btns())
        btns.extend(self._sent_to_client_btn())
        btns.extend(self._call_client_btn())
        btns.extend(self._paid_btn())
        btns.extend(self._aboinv_btn())
        btns.extend(self._validate_btns())
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

    def _can_change_status(self, status):
        """
            Called to check if the user can set the current status
        """
        raise Exception("Not implemented yet")

    def _status_process(self):
        """
            Change the current task's status
        """
        status = self.get_taskstatus()
        if not self._can_change_status(status):
            raise Forbidden(u"Vous n'êtes pas autorisé à \
effectuer à attribuer ce statut à ce document.")
        log.debug(u" + The status is set to {0}".format(status))
        if hasattr(self, "_post_status_process"):
            getattr(self, "_post_status_process")(status)
        self.task.statusPerson = self.user.id
        self.task.CAEStatus = status

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
        valid_msg = u"Le statut a bien été modifié"
        if 'submit' in self.request.params:
            try:
                self.request.session.flash(valid_msg, queue="main")
                self._status_process()
                self._set_modifications()
                self.request.registry.notify(StatusChanged(self.request,
                                                    self.task))
            except Forbidden, e:
                log.exception(" !! Unauthorized action by : {0}".format(
                                                        self.user.login))
                self.request.session.pop_flash("main")
                self.request.session.flash(e.message, queue='error')
        else:
            self.request.session.flash(u"Aucune modification n'a pu être \
    effectuée, des informations sont manquantes.", queue="error")
        return self.project_view_redirect()

    def _pdf(self):
        """
            Returns a page displaying an html rendering of the current task
        """
        log.debug("# Generating the pdf file #")
        filename = u"{0}.pdf".format(self.task.number)
        write_pdf(self.request, filename, self._html())
        return self.request.response
