# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
"""
Workshop related views
"""
import logging
import peppercorn
import colander
import datetime

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden,
)
from sqlalchemy import (
    or_,
    func,
)
from pyramid.security import has_permission

from js.deform import auto_need
from js.jquery_timepicker_addon import timepicker_fr

from autonomie.models import workshop as models
from autonomie.models.activity import Attendance
from autonomie.models import user
from autonomie.utils.pdf import (
    render_html,
    write_pdf,
)
from sqla_inspect.csv import CsvExporter
from sqla_inspect.excel import XlsExporter
from sqla_inspect.ods import OdsExporter
from autonomie.utils.widgets import ViewLink
from autonomie.forms.workshop import (
    Workshop as WorkshopSchema,
    get_list_schema,
    ATTENDANCE_STATUS,
    Attendances as AttendanceSchema,
)
from autonomie.views import (
    BaseListView,
    BaseCsvView,
    BaseFormView,
    DuplicateView,
)
from autonomie.forms import(
    merge_session_with_post,
)
from autonomie.views.render_api import (
    format_datetime,
    format_date,
    format_account,
)


log = logging.getLogger(__name__)


WORKSHOP_SUCCESS_MSG = u"L'atelier a bien été programmée : \
<a href='{0}'>Voir</a>"


def get_new_datetime(now, hour, minute=0):
    """
    Return a new datetime object based on the 'now' element

        hour

            The hour we'd like to set

        minute

            The minute value we want to set (default 0)
    """
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)


def get_default_timeslots():
    """
    Return default timeslots for workshop creation
    """
    now = datetime.datetime.now()
    morning = {
        'name': u'Matinée',
        'start_time': get_new_datetime(now, 9),
        'end_time': get_new_datetime(now, 12, 30),
    }
    afternoon = {
        'name': u'Après-midi',
        'start_time': get_new_datetime(now, 14),
        'end_time': get_new_datetime(now, 18),
    }
    return [morning, afternoon]


class WorkshopAddView(BaseFormView):
    """
    View for adding workshop
    """
    title = u"Créer un nouvel atelier"
    schema = WorkshopSchema()

    def before(self, form):
        auto_need(form)
        timepicker_fr.need()
        default_timeslots = get_default_timeslots()
        form.set_appstruct({'timeslots': default_timeslots})

    def submit_success(self, appstruct):
        """
        Create a new workshop
        """
        come_from = appstruct.pop('come_from')

        timeslots_datas = appstruct.pop('timeslots')
        for i in timeslots_datas:
            i.pop('id', None)

        timeslots_datas.sort(key=lambda val: val['start_time'])

        appstruct['datetime'] = timeslots_datas[0]['start_time']
        appstruct['timeslots'] = [
            models.Timeslot(**data) for data in timeslots_datas
        ]

        participants_ids = set(appstruct.pop('participants', []))
        appstruct['participants'] = [
            user.User.get(id_) for id_ in participants_ids
        ]

        for timeslot in appstruct['timeslots']:
            timeslot.participants = appstruct['participants']

        workshop_obj = models.Workshop(**appstruct)
        self.dbsession.add(workshop_obj)
        self.dbsession.flush()

        workshop_url = self.request.route_path(
            "workshop",
            id=workshop_obj.id,
            _query=dict(action="edit")
            )

        if not come_from:
            redirect = workshop_url
        else:
            msg = WORKSHOP_SUCCESS_MSG.format(workshop_url)
            self.session.flash(msg)
            redirect = come_from
        return HTTPFound(redirect)


class WorkshopEditView(BaseFormView):
    """
    Workshop edition view

    Provide edition functionnality and display a form for attendance recording
    """
    schema = WorkshopSchema()
    add_template_vars = ('title', 'available_status', )

    @property
    def title(self):
        return self.context.title

    @property
    def available_status(self):
        return ATTENDANCE_STATUS

    def before(self, form):
        """
        Populate the form before rendering

            form

                The deform form object used in this form view (see parent class
                in pyramid_deform)
        """
        populate_actionmenu(self.request)
        auto_need(form)
        timepicker_fr.need()

        appstruct = self.context.appstruct()
        participants = self.context.participants
        appstruct['participants'] = [p.id for p in participants]

        timeslots = self.context.timeslots
        appstruct['timeslots'] = [t.appstruct() for t in timeslots]

        form.set_appstruct(appstruct)
        return form

    def _retrieve_workshop_timeslot(self, id_):
        """
        Retrieve an existing workshop model from the current context
        """
        for timeslot in self.context.timeslots:
            if timeslot.id == id_:
                return timeslot
        log.warn(u"Possible break in attempt : On essaye d'éditer un timeslot \
qui n'appartient pas au contexte courant !!!!")
        raise HTTPForbidden()

    def _get_timeslots(self, appstruct):
        datas = appstruct.pop('timeslots')
        objects = []
        datas.sort(key=lambda val: val['start_time'])

        for data in datas:
            id_ = data.pop('id', None)
            if id_ is None:
                # New timeslots
                objects.append(models.Timeslot(**data))
            else:
                # existing timeslots
                obj = self._retrieve_workshop_timeslot(id_)
                merge_session_with_post(obj, data)
                objects.append(obj)

        return objects

    def submit_success(self, appstruct):
        """
        Handle successfull submission of our edition form
        """
        come_from = appstruct.pop('come_from')
        appstruct['timeslots'] = self._get_timeslots(appstruct)
        appstruct['datetime'] = appstruct['timeslots'][0].start_time

        participants_ids = set(appstruct.pop('participants', []))
        appstruct['participants'] = [
            user.User.get(id_) for id_ in participants_ids
        ]

        for timeslot in appstruct['timeslots']:
            timeslot.participants = appstruct['participants']

        merge_session_with_post(self.context, appstruct)
        self.dbsession.merge(self.context)

        workshop_url = self.request.route_path(
            "workshop",
            id=self.context.id,
            _query=dict(action="edit")
            )

        if not come_from:
            redirect = workshop_url
        else:
            msg = WORKSHOP_SUCCESS_MSG.format(workshop_url)
            self.session.flash(msg)
            redirect = come_from

        return HTTPFound(redirect)


def record_attendances_view(context, request):
    """
    Record attendances for the given context (workshop)

    Special Note : Since we need a special layout in the form (with tabs and
        lines with the username as header, we can't render it with deform.  We
        use peppercorn's parser and we build an appropriate form in the template
    """
    schema = AttendanceSchema().bind(request=request)
    if 'submit' in request.params:
        controls = request.params.items()
        values = peppercorn.parse(controls)
        try:
            appstruct = schema.deserialize(values)
        except colander.Invalid as e:
            log.error(u"Error while validating workshop attendance")
            log.error(e)
        else:
            for datas in appstruct['attendances']:
                account_id = datas['account_id']
                timeslot_id = datas['timeslot_id']
                obj = Attendance.get((account_id, timeslot_id))
                obj.status = datas['status']
                request.dbsession.merge(obj)
            request.session.flash(u"L'émargement a bien été enregistré")

    url = request.route_path(
        'workshop',
        id=context.id,
        _query=dict(action="edit"),
        )

    return HTTPFound(url)


class WorkshopListTools(object):
    """
    Tools for listing workshops
    """
    title = u"Liste des ateliers"
    schema = get_list_schema()
    sort_columns = dict(datetime=models.Workshop.datetime)
    default_sort = 'datetime'
    default_direction = 'desc'

    def query(self):
        query = models.Workshop.query()
        return query

    def filter_participant(self, query, appstruct):
        participant_id = appstruct.get('participant_id')
        if participant_id is not None:
            query = query.filter(
                models.Workshop.attendances.any(
                    Attendance.account_id == participant_id
                )
            )
        return query

    def filter_search(self, query, appstruct):
        search = appstruct['search']
        if search:
            query = query.filter(
                or_(models.Workshop.name.like('%{0}%'.format(search)),
                    models.Workshop.leaders.like('%{0}%'.format(search))
                    ))
        return query

    def filter_date(self, query, appstruct):
        date = appstruct.get('date')
        year = appstruct.get('year')
        if date is not None:
            query = query.filter(
                models.Workshop.timeslots.any(
                    func.date(models.Timeslot.start_time) == date
                )
            )
        # Only filter by year if no date filter is set
        elif year is not None:
            query = query.filter(
                models.Workshop.timeslots.any(
                    func.extract('YEAR', models.Timeslot.start_time) == year
                )
            )

        return query


class WorkshopListView(WorkshopListTools, BaseListView):
    """
    Workshop listing view
    """
    pass


class WorkshopCsvWriter(CsvExporter):
    headers = (
        {'name': 'date', 'label': 'Date'},
        {'name': 'label', 'label': "Intitulé"},
        {'name': 'participant', 'label': "Participant"},
        {'name': 'leaders', 'label': "Formateur(s)"},
        {'name': 'duration', 'label': "Durée"},
    )


class WorkshopXlsWriter(XlsExporter):
    headers = (
        {'name': 'date', 'label': 'Date'},
        {'name': 'label', 'label': "Intitulé"},
        {'name': 'participant', 'label': "Participant"},
        {'name': 'leaders', 'label': "Formateur(s)"},
        {'name': 'duration', 'label': "Durée"},
    )


class WorkshopOdsWriter(OdsExporter):
    headers = (
        {'name': 'date', 'label': u'Date'},
        {'name': 'label', 'label': u"Intitulé"},
        {'name': 'participant', 'label': u"Participant"},
        {'name': 'leaders', 'label': u"Formateur(s)"},
        {'name': 'duration', 'label': u"Durée"},
    )


def stream_workshop_entries_for_export(query):
    """
    Stream workshop datas for csv export
    """
    for workshop in query.all():

        hours = sum(t.duration[0] for t in workshop.timeslots)
        minutes = sum(t.duration[1] for t in workshop.timeslots)

        duration = hours * 60 + minutes

        for participant in workshop.participants:

            attended = False
            for timeslot in workshop.timeslots:
                # On exporte une ligne que si le user était là au moins une
                # fois
                if timeslot.user_status(participant.id) == u'Présent':
                    attended = True
                    break

            if attended:
                yield {
                    "date": workshop.timeslots[0].start_time.date(),
                    "label": workshop.name,
                    "participant": format_account(participant),
                    "leaders": '\n'.join(workshop.leaders),
                    "duration": duration,
                }


class WorkshopCsvView(WorkshopListTools, BaseCsvView):
    """
    Workshop csv export view
    """
    writer = WorkshopCsvWriter

    @property
    def filename(self):
        return "ateliers.csv"

    def _init_writer(self):
        return self.writer()

    def _stream_rows(self, query):
        return stream_workshop_entries_for_export(query)


class WorkshopXlsView(WorkshopCsvView):
    """
    Workshop excel export view
    """
    writer = WorkshopXlsWriter

    @property
    def filename(self):
        return "ateliers.xls"


class WorkshopOdsView(WorkshopCsvView):
    writer = WorkshopOdsWriter

    @property
    def filename(self):
        return "ateliers.ods"


class CompanyWorkshopListView(WorkshopListView):
    """
    View for listing company's workshops
    """
    schema = get_list_schema(company=True)

    def filter_participant(self, query, appstruct):
        company = self.context
        employees_id = [u.id for u in company.employees]
        query = query.filter(
            models.Workshop.participants.any(
                user.User.id.in_(employees_id)
                ))
        return query


def timeslots_pdf_output(timeslots, workshop, request):
    """
    write the pdf output of an attendance sheet to the current request response

        timeslots

            The timeslots to render in the attendance sheet (one timeslot = one
            column)

        workshop

            The workshop object

        request

            The current request object
    """
    if not hasattr(timeslots, '__iter__'):
        timeslots = [timeslots]

    date = workshop.datetime.strftime("%e_%m_%Y")
    filename = u"atelier_{0}_{1}.pdf".format(date, workshop.id)

    template = u"autonomie:templates/accompagnement/workshop_pdf.mako"
    rendering_datas = dict(
        timeslots=timeslots,
        workshop=workshop,
        config=request.config,
        participants=workshop.sorted_participants,
        )
    html_str = render_html(request, template, rendering_datas)

    write_pdf(request, filename, html_str)

    return request.response


def timeslot_pdf_view(timeslot, request):
    """
    Return a pdf attendance sheet for the given timeslot

        timeslot

            A timeslot object returned as a current context by traversal
    """
    return timeslots_pdf_output(timeslot, timeslot.workshop, request)


def workshop_pdf_view(workshop, request):
    """
    Return a pdf attendance sheet for all the timeslots of the given workshop

        workshop

            A workshop object returned as a current context by traversal
    """
    return timeslots_pdf_output(workshop.timeslots, workshop, request)


def workshop_view(workshop, request):
    """
    Workshop view_only view

        workshop

            the context returned by the traversal tree
    """
    if has_permission('manage', workshop, request):
        url = request.route_path(
            'workshop',
            id=workshop.id,
            _query=dict(action='edit'),
        )
        return HTTPFound(url)
    populate_actionmenu(request)

    timeslots_datas = []

    for timeslot in workshop.timeslots:
        if timeslot.start_time.day == timeslot.end_time.day:
            time_str = u"le {0} de {1} à {2}".format(
                format_date(timeslot.start_time),
                format_datetime(timeslot.start_time, timeonly=True),
                format_datetime(timeslot.end_time, timeonly=True)
                )
        else:
            time_str = u"du {0} au {1}".format(
                format_datetime(timeslot.start_time),
                format_datetime(timeslot.end_time)
                )

        status = timeslot.user_status(request.user.id)
        timeslots_datas.append((timeslot.name, time_str, status))

    return dict(title=workshop.title, timeslots_datas=timeslots_datas)


def workshop_delete_view(workshop, request):
    """
    Workshop deletion view
    """
    url = request.referer
    request.dbsession.delete(workshop)
    request.session.flash(u"L'atelier a bien été supprimé")
    if not url:
        url = request.route_path('workshops')
    return HTTPFound(url)


class WorkShopDuplicateView(DuplicateView):
    """
    Workshop duplication view
    """
    message = u"L'atelier a bien été dupliqué, vous pouvez le modifier ici \
<a href='{0}'>Ici</a>."
    route_name = "workshop"


def populate_actionmenu(request):
    """
    Add elements in the actionmenu regarding the current context
    """
    company_id = request.GET.get('company_id')

    if company_id is not None:
        link = ViewLink(
            u"Liste des ateliers",
            "view",
            path='company_workshops',
            id=company_id
        )
    else:
        link = ViewLink(u"Liste des ateliers", "manage", path='workshops')

    request.actionmenu.add(link)


def add_routes(config):
    """
    Add module's related routes
    """
    config.add_route(
        'workshop',
        "/workshops/{id:\d+}",
        traverse='/workshops/{id}',
    )

    config.add_route(
        'workshop.pdf',
        "/workshops/{id:\d+}.pdf",
        traverse='/workshops/{id}',
    )

    config.add_route(
        'timeslot.pdf',
        "/timeslots/{id:\d+}.pdf",
        traverse='/timeslots/{id}',
    )

    config.add_route('workshops', "/workshops")
    config.add_route('workshops.csv', "/workshops.csv")
    config.add_route('workshops.xls', "/workshops.xls")
    config.add_route('workshops.ods', "/workshops.ods")

    config.add_route(
        'company_workshops',
        "/company/{id}/workshops",
        traverse="/companies/{id}",
        )


def includeme(config):
    """
    Add view to the pyramid registry
    """
    add_routes(config)
    config.add_view(
        WorkshopAddView,
        route_name='workshops',
        permission='add_workshop',
        request_param='action=new',
        renderer="/base/formpage.mako",
    )

    config.add_view(
        WorkshopListView,
        route_name='workshops',
        permission='admin_workshop',
        renderer="/accompagnement/workshops.mako",
    )

    config.add_view(
        CompanyWorkshopListView,
        route_name='company_workshops',
        permission='list_workshops',
        renderer="/accompagnement/workshops.mako",
    )

    config.add_view(
        WorkshopEditView,
        route_name='workshop',
        permission='edit_workshop',
        request_param='action=edit',
        renderer="/accompagnement/workshop_edit.mako",
    )

    config.add_view(
        record_attendances_view,
        route_name='workshop',
        permission='edit_workshop',
        request_param='action=record',
    )

    config.add_view(
        workshop_delete_view,
        route_name='workshop',
        permission='edit_workshop',
        request_param='action=delete',
    )

    config.add_view(
        WorkShopDuplicateView,
        route_name='workshop',
        permission='edit_workshop',
        request_param='action=duplicate',
    )

    config.add_view(
        workshop_view,
        route_name='workshop',
        permission='view_workshop',
        renderer='/accompagnement/workshop_view.mako',
    )

    config.add_view(
        WorkshopCsvView,
        route_name='workshops.csv',
        permission='list_workshops',
    )

    config.add_view(
        WorkshopXlsView,
        route_name='workshops.xls',
        permission='list_workshops',
    )

    config.add_view(
        WorkshopOdsView,
        route_name='workshops.ods',
        permission='list_workshops',
    )

    config.add_view(
        timeslot_pdf_view,
        route_name='timeslot.pdf',
        permission="view_workshop",
    )

    config.add_view(
        workshop_pdf_view,
        route_name='workshop.pdf',
        permission="view_workshop",
    )
