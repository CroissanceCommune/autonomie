# -*- coding: utf-8 -*-
# * File Name : holiday.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 22-06-2012
# * Last Modified :
#
# * Project :
#

"""
    Simple stuff for handling holidays declaration/view
"""

import logging

from sqlalchemy import or_

from pyramid.httpexceptions import HTTPFound

from autonomie.models.holiday import Holiday
from autonomie.utils.forms import merge_session_with_post
from autonomie.views.forms.utils import BaseFormView
from autonomie.views.forms.holiday import HolidaysSchema
from autonomie.views.forms.holiday import searchSchema


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


class HolidayRegister(BaseFormView):
    """
        Page for holiday registering
    """
    schema = HolidaysSchema()
    title = u"Déclarer mes congés"

    def before(self, form):
        holidays = get_holidays(user_id=self.request.user.id)
        appstruct = {'holidays' : [{'start_date':holiday.start_date,
                                    'end_date':holiday.end_date}
                                              for holiday in holidays]}
        form.set_appstruct(appstruct)

    def submit_success(self, appstruct):
        """
            Set the user's holidays in the database
        """
        self._purge_holidays()
        for data in appstruct['holidays']:
            holiday = Holiday(user_id=self.request.user.id)
            merge_session_with_post(holiday, data)
            self.dbsession.merge(holiday)
        self.dbsession.flush()
        self.request.session.flash(
            u"Vos déclarations de congés ont bien été modifiées")
        return HTTPFound(self.request.route_path("holiday"))

    def _purge_holidays(self):
        """
            Purge the user's holidays
        """
        for holiday in get_holidays(user_id=self.request.user.id):
            self.dbsession.delete(holiday)
            self.dbsession.flush()


class HolidayView(BaseFormView):
    """
        Holiday search/consultation views
    """
    schema = searchSchema
    title = u"Les congés des entrepreneurs"

    def __init__(self, request):
        super(HolidayView, self).__init__(request)
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
    config.add_route('holiday', '/holiday')
    config.add_route('holidays', '/holidays')
    config.add_view(HolidayRegister,
                    route_name="holiday",
                    renderer="holiday.mako",
                    permission="view")
    config.add_view(HolidayView,
                    route_name="holidays",
                    renderer="holidays.mako",
                    permission="manage")
