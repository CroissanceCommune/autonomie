# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
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
#


"""
    Simple stuff for handling holidays declaration/view
"""

import logging
import colander

from sqlalchemy import or_


from autonomie.models.holiday import Holiday
from autonomie.views.forms import merge_session_with_post
from autonomie.utils.rest import RestJsonRepr
from autonomie.utils.rest import RestError
from autonomie.utils.rest import add_rest_views
from autonomie.utils.rest import make_redirect_view
from autonomie.views.base import BaseView
from autonomie.views.forms import BaseFormView
from autonomie.views.forms.holiday import HolidaySchema
from autonomie.views.forms.holiday import searchSchema
from autonomie.resources import holiday_js


log = logging.getLogger(__name__)


def get_holidays(start_date=None, end_date=None, user_id=None):
    """
        Return the user's declared holidays
    """
    holidays = Holiday.query()
    if start_date and end_date:
        holidays = holidays.filter(
            or_(Holiday.start_date.between(start_date, end_date),
                Holiday.end_date.between(start_date, end_date)))
    if user_id:
        holidays = holidays.filter(Holiday.user_id==user_id)
    holidays.order_by("start_date")
    return holidays


class HolidayJson(RestJsonRepr):
    """
        Wraps a holiday to a json representation
    """
    schema = HolidaySchema()


class RestHoliday(BaseView):
    """
        Json-Rest api for holidays handling
        /holidays/{id}
    """
    _schema = HolidaySchema()
    factory = Holiday
    model_wrapper = HolidayJson

    @property
    def schema(self):
        # Ensure all our colander.deferred values are set
        return self._schema.bind()

    def getOne(self):
        """
            get an expense line
        """
        lid = self.request.matchdict.get('lid')
        for holiday in self.request.context.holidays:
            if holiday.id == int(lid):
                return holiday
        raise RestError({}, 404)

    def get(self):
        """
            Rest get method : return a line
        """
        log.debug("In the get method")
        return self.model_wrapper(self.getOne())

    def post(self):
        """
            Rest post method : add a line
        """
        log.debug("In the post method")
        appstruct = self.request.json_body
        try:
            appstruct = self.schema.deserialize(appstruct)
        except colander.Invalid, err:
            import traceback
            traceback.print_exc()
            log.exception("  - Erreur")
            raise RestError(err.asdict(), 400)
        line = self.factory(**appstruct)
        line.user = self.request.context
        self.request.dbsession.add(line)
        self.request.dbsession.flush()
        return self.model_wrapper(line)

    def delete(self):
        """
            Rest delete method : delete a line
        """
        log.debug("In the delete method")
        line = self.getOne()
        self.request.dbsession.delete(line)
        return dict(status="success")

    def put(self):
        """
            Rest put method : update a line
        """
        log.debug("In the put method")
        line = self.getOne()
        appstruct = self.request.json_body
        try:
            appstruct = self.schema.deserialize(appstruct)
        except colander.Invalid, err:
            import traceback
            traceback.print_exc()
            log.exception("  - Erreur")
            raise RestError(err.asdict(), 400)
        line = merge_session_with_post(line, appstruct)
        self.request.dbsession.merge(line)
        self.request.dbsession.flush()
        return self.model_wrapper(line)


def holidays_json(request):
    """
        json view for holidays
    """
    holidays = [HolidayJson(holiday) for holiday in Holiday.query()\
            .filter(Holiday.user_id==request.context.id)]
    return dict(holidays=holidays,
            user_id=str(request.context.id))


def user_holidays_index(request):
    """
        Base view for holidays editing
    """
    load_url = request.route_path("user_holidays", id=request.context.id)
    holiday_js.need()
    return dict(title=u"Déclarer mes congés", loadurl=load_url)


class AdminHolidayView(BaseFormView):
    """
        Holiday search/consultation views
    """
    schema = searchSchema
    title = u"Les congés des entrepreneurs"

    def __init__(self, request):
        super(AdminHolidayView, self).__init__(request)
        self._start_date = None
        self._end_date = None
        self.search_result = []

    def submit_success(self, appstruct):
        start_date = appstruct.get('start_date')
        end_date = appstruct.get('end_date')
        user_id = appstruct.get('user_id')
        search_result = get_holidays(start_date, end_date, user_id)
        result = dict(holidays=search_result,
                    start_date=start_date,
                    end_date=end_date)
        form = self.form_class(self.schema, buttons=self.buttons)
        result['form'] = form.render(appstruct)
        return result


def includeme(config):
    # Manager View
    config.add_route(
            'holidays',
            '/holidays')
    config.add_view(AdminHolidayView,
                    route_name="holidays",
                    renderer="holidays.mako",
                    permission="manage")
    # User views
    # Here we use the users traversal to provide acl checks
    config.add_route(
            'user_holidays',
            '/user/{id:\d+}/holidays',
            traverse="/users/{id}")
    config.add_route(
            'user_holiday',
            '/user/{id:\d+}/holidays/{lid:\d+}',
            traverse="/users/{id}")

    config.add_view(user_holidays_index,
                    route_name="user_holidays",
                    renderer="user_holidays.mako",
                    permission="edit")

    config.add_view(holidays_json,
                    route_name='user_holidays',
                    xhr=True,
                    renderer="json")
    add_rest_views(config, "user_holiday", RestHoliday,
            view_rights='add',
            add_rights='add')
    config.add_view(
            make_redirect_view("user_holidays"),
            route_name="user_holiday")
