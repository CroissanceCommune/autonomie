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
    DeleteView,
)
from autonomie.utils.strings import format_account
from autonomie.models.career_path import CareerPath
from autonomie.models.career_stage import CareerStage 
from autonomie.models.user.login import Login
from autonomie.forms.user.career_path import (
    get_add_stage_schema,
    get_edit_stage_schema,
)

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
    schema = get_add_stage_schema()

    @property
    def current_userdatas(self):
        return self.context

    def submit_success(self, appstruct):
        model = self.schema.objectify(appstruct)
        model.userdatas_id = self.current_userdatas.id
        model = self.dbsession.merge(model)
        self.dbsession.flush()

        # Update CareerPath with chosen CareerStage's data
        model.cae_situation_id = model.career_stage.cae_situation_id
        model.stage_type = model.career_stage.stage_type
        model = self.dbsession.merge(model)
        self.dbsession.flush()

        # Redirect to login or stage's edition if needed
        dest_route = self.request.current_route_path(_query='')
        if model.career_stage.cae_situation.is_integration:
            login = Login.query().filter(Login.user_id==self.context.userdatas.user_id).first()
            if login is None:
                dest_route = self.request.route_path('/users/{id}/login', id=self.context.userdatas.id)
        if model.stage_type is not None:
            if model.stage_type in ("contract", "amendment", "exit") : 
                dest_route = self.request.route_path('career_path', id=model.id, _query='')

        self.session.flash(u"L'étape de parcours a bien été ajoutée")
        return HTTPFound(dest_route)


class UserCareerPathAddStage(CareerPathAddStage):
    @property
    def current_userdatas(self):
        return self.context.userdatas


class CareerPathEditStage(BaseFormView):
    """
    Career path edit stage view
    """
    title = u"Modification d'une étape de parcours"
    _schema = None

    @property
    def current_userdatas(self):
        return self.context.userdatas

    # Schema is here a property since we need to build it dynamically 
    # regarding the current request
    @property
    def schema(self):
        """
        The getter for our schema property
        """
        if self._schema is None:
            self._schema = get_edit_stage_schema(self.context.stage_type)
        self._schema.title = self.context.career_stage.name
        if self.context.cae_situation is not None:
            self._schema.title += ' ( => ' + self.context.cae_situation.label + ' )'
        return self._schema

    @schema.setter
    def schema(self, value):
        """
        A setter for the schema property
        The BaseClass in pyramid_deform gets and sets the schema attribute 
        that is here transformed as a property
        """
        self._schema = value

    def before(self, form):
        appstruct = self.request.context.appstruct()
        form.set_appstruct(appstruct)

    def submit_success(self, appstruct):
        model = self.schema.objectify(appstruct)
        model.userdatas_id = self.current_userdatas.id
        model = self.dbsession.merge(model)
        self.dbsession.flush()
        self.session.flash(u"L'étape de parcours a bien été enregistrée")
        dest = u"userdatas/career_path"

        # Redirect to login management if new CAE situation is integration and no active login
        if self.context.cae_situation is not None:
            if self.context.cae_situation.is_integration:
                login = Login.query().filter(Login.user_id==self.context.userdatas.user_id).first()
                if login is None:
                    dest = u"login"

        return HTTPFound(
            self.request.route_path('/users/{id}/%s' % dest, id=self.context.userdatas_id)
        )


class UserCareerPathEditStage(CareerPathEditStage):
    @property
    def current_userdatas(self):
        return self.context.userdatas


class CareerPathDeleteStage(DeleteView):
    """
    Career path delete stage view
    """
    delete_msg = u"L'étape a bien été supprimée"
    
    def redirect(self):
        return HTTPFound(
            self.request.route_path('/users/{id}/userdatas/career_path', id=self.context.userdatas_id)
        )


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
    config.add_view(
        CareerPathDeleteStage,
        route_name="career_path",
        permission="edit.userdatas",
        request_param='action=delete',
        renderer="/userdatas/career_path.mako",
        layout="user"
    )


def includeme(config):
    add_routes(config)
    add_views(config)