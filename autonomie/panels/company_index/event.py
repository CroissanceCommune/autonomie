# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from webhelpers import paginate
from sqlalchemy import desc
from autonomie.models.activity import (
    Event,
    Attendance,
    Activity,
)
from autonomie.models.workshop import (
    Timeslot,
)
from autonomie import resources
from autonomie.panels.company_index import utils


def _user_events_query(user_id):
    """
    Return a sqla query for the user's events
    """
    query = Event.query().with_polymorphic([Timeslot, Activity])
    query = query.filter(Event.type_.in_(['timeslot', 'activity']))
    query = query.filter(
        Event.attendances.any(Attendance.account_id == user_id)
    )
    query = query.order_by(desc(Event.datetime))
    return query


def coming_events_panel(context, request):
    """
        Return the list of the upcoming events
    """
    if not request.is_xhr:
        resources.event_list_js.need()

    query = _user_events_query(request.user.id)
    page_nb = utils.get_page_number(request, 'events_page_nb')
    items_per_page = utils.get_items_per_page(request, 'events_per_page')

    paginated_events = paginate.Page(
        query,
        page_nb,
        items_per_page=items_per_page,
        url=utils.make_get_list_url('events'),
    )

    result_data = {'events': paginated_events}
    return result_data


def includeme(config):
    config.add_panel(
        coming_events_panel,
        'company_coming_events',
        renderer='panels/company_index/coming_events.mako',
    )
