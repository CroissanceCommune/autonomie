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

from deform import Form
from deform import ValidationFailure

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from autonomie.models.model import Holiday
from autonomie.models.model import User
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.views import submit_btn
from autonomie.views.forms.holiday import HolidaysSchema
from autonomie.views.forms.holiday import searchSchema
from .base import BaseView

log = logging.getLogger(__name__)


def get_user_choices(dbsession):
    choices = [(0, u'Tous les entrepreneurs')]
    choices.extend([(unicode(user.id),
                     u"{0} {1}".format(user.lastname, user.firstname),)
                        for user in User.query().all()])
    return choices


class HolidayView(BaseView):
    """
        All holidays-related views
    """
    @view_config(route_name="holiday", renderer="holiday.mako",
                                                            permission="view")
    def holiday(self):
        """
            Allows a simple user to set his holidays
        """
        schema = HolidaysSchema()
        form = Form(schema, buttons=(submit_btn,))
        holidays = Holiday.query(self.dbsession,user_id=self.request.user.id)
        if 'submit' in self.request.params:
            datas = self.request.params.items()
            log.debug(datas)
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, errform:
                html_form = errform.render()
            else:
                # Validation OK
                for holiday in holidays:
                    self.dbsession.delete(holiday)
                    self.dbsession.flush()
                for data in appstruct['holidays']:
                    holiday = Holiday(user_id=self.request.user.id)
                    merge_session_with_post(holiday, data)
                    self.dbsession.merge(holiday)
                self.dbsession.flush()
                self.request.session.flash(
                        u"Vos déclarations de congés ont bien été modifiées",
                        queue="main")
                return HTTPFound(self.request.route_path("holiday"))
        else:
            appstruct = [{'start_date':holiday.start_date,
                         'end_date':holiday.end_date}
                         for holiday in holidays]
            html_form = form.render({'holidays': appstruct})
        return dict(title=u"Déclarer mes congés",
                    html_form=html_form)

    @view_config(route_name="holidays", renderer="holidays.mako",
                                        permission="manage")
    def holidays(self):
        """
            Display the holidays of the current month
        """
        schema = searchSchema.bind(
                choices=get_user_choices(self.dbsession))
        form = Form(schema, buttons=(submit_btn,))
        holidays = []
        start_date = None
        end_date = None
        if 'submit' in self.request.params:
            datas = self.request.params.items()
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, errform:
                html_form = errform.render()
            else:
                # Validation OK
                start_date = appstruct.get('start_date')
                end_date = appstruct.get('end_date')
                user_id = appstruct.get('user_id')
                holidays = Holiday.query(self.dbsession)
                holidays = holidays.filter(
                                or_(Holiday.start_date.between(start_date,
                                                                end_date),
                                    Holiday.end_date.between(start_date,
                                                                    end_date)))
                if user_id:
                    holidays = holidays.filter(Holiday.user_id == user_id)
                holidays = holidays.all()
                html_form = form.render(appstruct)
                log.debug(u"Rendering with appstruct : %s" % appstruct)
        else:
            html_form = form.render()
        return dict(
                    title=u"Les congés des entrepreneurs",
                    html_form=html_form,
                    holidays=holidays,
                    start_date=start_date,
                    end_date=end_date
                    )
