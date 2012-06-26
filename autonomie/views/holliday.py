# -*- coding: utf-8 -*-
# * File Name : holliday.py
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
    Simple stuff for handling hollidays declaration/view
"""

import logging

from sqlalchemy import or_

from deform import Form
from deform import ValidationFailure

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from autonomie.models.model import Holliday
from autonomie.models.model import User
from autonomie.utils.forms import merge_session_with_post
from autonomie.views.forms.holliday import HollidaysSchema
from autonomie.views.forms.holliday import searchSchema
from .base import BaseView

log = logging.getLogger(__file__)

def get_user_choices(dbsession):
    choices = [(0, u'Tous les entrepreneurs')]
    choices.extend([(unicode(user.id),
                     u"{0} {1}".format(user.lastname, user.firstname),)
                        for user in User.query(dbsession).all()])
    return choices

class HollidayView(BaseView):
    """
        All hollidays-related views
    """
    @view_config(route_name="holliday", renderer="holliday.mako",
                                                            permission="view")
    def holliday(self):
        """
            Allows a simple user to set his hollidays
        """
        schema = HollidaysSchema()
        form = Form(schema, buttons=('submit',))
        hollidays = Holliday.query(self.dbsession,user_id=self.request.user.id)
        if 'submit' in self.request.params:
            datas = self.request.params.items()
            log.debug(datas)
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, errform:
                html_form = errform.render()
            else:
                # Validation OK
                for holliday in hollidays:
                    self.dbsession.delete(holliday)
                    self.dbsession.flush()
                for data in appstruct['hollidays']:
                    holliday = Holliday(user_id=self.request.user.id)
                    merge_session_with_post(holliday, data)
                    self.dbsession.merge(holliday)
                self.dbsession.flush()
                self.request.session.flash(
                        u"Vos déclarations de congés ont bien été modifiées",
                        queue="main")
                return HTTPFound(self.request.route_path("holliday"))
        else:
            appstruct = [{'start_date':holliday.start_date,
                         'end_date':holliday.end_date}
                         for holliday in hollidays]
            html_form = form.render({'hollidays':appstruct})
        return dict(title=u"Déclarer mes congés",
                    html_form=html_form)

    @view_config(route_name="hollidays", renderer="hollidays.mako",
                                        permission="manage")
    def hollidays(self):
        """
            Display the hollidays of the current month
        """
        schema = searchSchema.bind(
                choices=get_user_choices(self.dbsession))
        form = Form(schema, buttons=('submit',))
        hollidays = []
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
                hollidays = Holliday.query(self.dbsession)
                hollidays = hollidays.filter(
                                or_(Holliday.start_date.between(start_date,
                                                                end_date),
                                    Holliday.end_date.between(start_date,
                                                                    end_date)))
                if user_id:
                    hollidays = hollidays.filter(Holliday.user_id==user_id)
                hollidays=hollidays.all()
                html_form = form.render(appstruct)
                log.debug("Rendering with appstruct : %s" % appstruct)
        else:
            html_form = form.render()
        return dict(
                    title=u"Les congés des entrepreneurs",
                    html_form=html_form,
                    hollidays=hollidays,
                    start_date=start_date,
                    end_date=end_date
                    )
