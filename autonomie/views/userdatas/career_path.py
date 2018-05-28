# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * MICHEAU Paul <paul@kilya.biz>
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
    Views for career path
"""

import logging
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.orm import (
    load_only,
    Load,
    joinedload,
)
from autonomie.views import (
    BaseFormView,
    BaseView,
)
from autonomie.utils.strings import format_account
from autonomie.models.career_path import CareerPath
from autonomie.models.career_stage import CareerStage 
from autonomie.forms.user.career_path import StageSchema

logger = logging.getLogger(__name__)


class CareerPathList(BaseView):
    """
    List of career path stages
    """

    @property
    def current_userdatas(self):
        return self.context

    def __call__(self):
        path_query = CareerPath.query(self.current_userdatas.id)
        path_query = path_query.options(
            Load(CareerPath).load_only("start_date", "id"),
            joinedload("career_stage").load_only("name"),
        )
        return dict(
            career_path=path_query.all(),
            user=self.current_userdatas.user,
            title=u"Parcours de {0}".format(
                format_account(self.current_userdatas.user, False)
            )
        )

class UserCareerPathList(CareerPathList):
    @property
    def current_userdatas(self):
        return self.context.userdatas


class CareerPathAddStage(BaseFormView):
    """
    Career path add stage view
    """
    title = u"Ajout d'une nouvelle étape"
    schema = StageSchema()

    @property
    def current_userdatas(self):
        return self.context

    def submit_success(self, appstruct):
        model = self.schema.objectify(appstruct)
        model.userdatas_id = self.current_userdatas.id
        model = self.dbsession.merge(model)
        self.dbsession.flush()
        self.session.flash(
            u"L'étape a bien été ajoutée au parcours"
        )
        return HTTPFound(self.request.current_route_path(_query=''))

class UserCareerPathAddStage(CareerPathAddStage):
    @property
    def current_userdatas(self):
        return self.context.userdatas


class CareerPathEditStage(BaseFormView):
    """
    Career path edit stage view
    """
    title = u"Modification d'une étape de parcours"
    schema = StageSchema()

    @property
    def current_userdatas(self):
        return self.context

    def before(self, form):
        #form.set_appstruct(self.schema.dictify(self.current_userdatas))
        print "AAAAAAAAAAAAAAAAAAA"
        print self
        print self.context
        print self.request.context
        print "AAAAAAAAAAAAAAAAAAA"
        appstruct = self.request.context.appstruct()
        form.set_appstruct(appstruct)

    def submit_success(self, appstruct):
        model = self.schema.objectify(appstruct)
        model.userdatas_id = self.current_userdatas.id
        model = self.dbsession.merge(model)
        self.dbsession.flush()
        self.session.flash(
            u"L'étape de parcours a bien été modifiée"
        )
        return HTTPFound(self.request.current_route_path(_query=''))

class UserCareerPathEditStage(CareerPathEditStage):
    @property
    def current_userdatas(self):
        return self.context.userdatas


def add_routes(config):
    """
    Add career path related routes
    """
    config.add_route(
        '/userdatas/{id}/career_path',
        '/userdatas/{id}/career_path',
        traverse='/userdatas/{id}',
    )
    config.add_route(
        '/users/{id}/userdatas/career_path',
        '/users/{id}/userdatas/career_path',
        traverse='/users/{id}',
    )
    config.add_route(
        'career_path',
        '/career_path/{id:\d+}',
        traverse='/career_path/{id}'
    )
    return config


def add_views(config):
    """
    Add career path related views
    """
    config.add_view(
        CareerPathList,
        route_name="/userdatas/{id}/career_path",
        permission="view.userdatas",
        renderer="/userdatas/career_path.mako",
        layout="user"
    )
    config.add_view(
        UserCareerPathList,
        route_name="/users/{id}/userdatas/career_path",
        permission="view.userdatas",
        renderer="/userdatas/career_path.mako",
        layout="user"
    )
    config.add_view(
        CareerPathAddStage,
        route_name="/userdatas/{id}/career_path",
        permission="edit.userdatas",
        request_param='action=add_stage',
        renderer="/userdatas/career_path_form.mako",
        layout="user"
    )
    config.add_view(
        UserCareerPathAddStage,
        route_name="/users/{id}/userdatas/career_path",
        permission="edit.userdatas",
        request_param='action=add_stage',
        renderer="/userdatas/career_path_form.mako",
        layout="user"
    )
    config.add_view(
        CareerPathEditStage,
        route_name="career_path",
        permission="edit.userdatas",
        renderer="/userdatas/career_path_form.mako",
        layout="user"
    )

    # config.add_view(
    #     UserCareerPathEditStage,
    #     route_name="/users/{id}/userdatas/career_path",
    #     permission="edit.userdatas",
    #     request_param='action=edit_stage',
    #     renderer="/userdatas/career_path_form.mako",
    #     layout="user"
    # )

    # config.add_view(
    #     CareerPathDeleteStage,
    #     route_name="/userdatas/{id}/career_path",
    #     permission="edit.userdatas",
    #     request_param='action=del_stage',
    #     renderer="/userdatas/career_path.mako",
    #     layout="user"
    # )
    # config.add_view(
    #     UserCareerPathDeleteStage,
    #     route_name="/users/{id}/userdatas/career_path",
    #     permission="edit.userdatas",
    #     request_param='action=del_stage',
    #     renderer="/userdatas/career_path.mako",
    #     layout="user"
    # )


def includeme(config):
    add_routes(config)
    add_views(config)