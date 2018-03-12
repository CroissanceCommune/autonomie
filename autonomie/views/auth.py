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
    All Authentication views
"""
import colander
import logging

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden,
    HTTPUnauthorized,
)

from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.threadlocal import get_current_registry

from deform import Form
from deform import Button
from deform import ValidationFailure

from js.bootstrap import bootstrap

from autonomie.models.user.login import Login
from autonomie.views import BaseView
from autonomie.forms.user.login import (
    get_auth_schema,
    get_json_auth_schema,
)
from autonomie.utils.rest import (
    RestError,
    Apiv1Resp,
    Apiv1Error,
)

log = logging.getLogger(__name__)


LOGIN_TITLE = u"Bienvenue dans Autonomie"
LOGIN_ERROR_MSG = u"Erreur d'authentification"
LOGIN_SUCCESS_MSG = u"Authentification réussie"


def forbidden_view(request):
    """
    The forbidden view :
        * handles the redirection to login form
        * return a json dict in case of xhr requests

    :param obj request: The pyramid request object
    """
    log.debug("We are in a forbidden view")
    login = authenticated_userid(request)

    if login:
        log.warn(u"An access has been forbidden to '{0}'".format(login))
        if request.is_xhr:
            return_datas = HTTPForbidden()
        else:
            bootstrap.need()
            return_datas = {"title": u"Accès refusé", }

    else:
        log.debug(u"An access has been forbidden to an unauthenticated user")
        # redirecting to the login page with the current path as param
        nextpage = request.path

        # If it's an api call, we raise HTTPUnauthorized
        if nextpage.startswith('/api'):
            return_datas = HTTPUnauthorized()
        else:
            loc = request.route_url('login', _query=(('nextpage', nextpage),))
            if request.is_xhr:
                return_datas = dict(redirect=loc)
            else:
                return_datas = HTTPFound(location=loc)

    return return_datas


def get_longtimeout():
    """
        Return the configured session timeout for people keeping connected
    """
    settings = get_current_registry().settings
    default = 3600
    longtimeout = settings.get("session.longtimeout", default)
    try:
        longtimeout = int(longtimeout)
    except:
        longtimeout = default
    return longtimeout


def connect_user(request, form_datas):
    """
    Effectively connect the user

    :param obj request: The pyramid Request object
    :pram dict form_datas: Validated form_datas
    """
    login = form_datas['login']
    login_id = Login.id_from_login(login)
    log.info(
        u" + '{0}' id : {1} has been authenticated".format(
            login, login_id
        )
    )
    # Storing the form_datas in the request object
    remember(request, login)
    remember_me = form_datas.get('remember_me', False)
    if remember_me:
        log.info("  * The user wants to be remembered")
        longtimeout = get_longtimeout()
        request.response.set_cookie(
            'remember_me',
            "ok",
            max_age=longtimeout,
        )


def api_login_post_view(request):
    """
    A Json login view
    expect a login and a password element (in json format)
    returns a json dict :
        success : {'status':'success'}
        error : {'status':'error', 'errors':{'field':'error message'}}
    """
    schema = get_json_auth_schema()
    appstruct = request.json_body
    try:
        appstruct = schema.deserialize(appstruct)
    except colander.Invalid, err:
        log.exception("  - Erreur")
        raise RestError(err.asdict(), 400)
    else:
        connect_user(request, appstruct)
    return Apiv1Resp(request)


def _get_login_form(request, use_ajax=False):
    """
    Return the login form object

    :param obj request: The pyramid request object
    :param bool use_ajax: Is this form called through xhr (should it be an ajax
        form) ?
    """
    if use_ajax:
        action = request.route_path('login')
        ajax_options = """{
            'dataType': 'json',
            'success': ajaxAuthCallback
            }"""
    else:
        action = None
        ajax_options = "{}"

    form = Form(
        get_auth_schema(),
        action=action,
        use_ajax=use_ajax,
        formid="authentication",
        ajax_options=ajax_options,
        bootstrap_form_style="authentication-form",
        buttons=(
            Button(
                name="submit",
                title="Connexion",
                type='submit',
            ),
        ),
    )
    return form


def api_login_get_view(request):
    """
    View used to check if the user is authenticated

    :returns:
        A json dict :
            user should login :
                {'status': 'error', 'datas': {'login_form': <html string>}}
            user is logged in:
                {'status': 'success', 'datas': {}}
    """
    login = authenticated_userid(request)

    if login is not None:
        result = Apiv1Resp(request)
    else:
        login_form = _get_login_form(request, use_ajax=True)
        form = login_form.render()
        result = Apiv1Error(request, datas={'login_form': form})
    return result


class LoginView(BaseView):
    """
    the login view
    """

    def get_next_page(self):
        """
        Return the next page to be visited after login, get it form the request
        or returns index
        """
        nextpage = self.request.params.get('nextpage')
        # avoid redirection looping or set default
        if nextpage in [None, self.request.route_url('login')]:
            nextpage = self.request.route_url('index')

        return nextpage

    def xhr_response(self, html_form):
        """
        Return the response in case of xhr form validation
        """
        return Apiv1Error(self.request, datas={'login_form': html_form})

    def response(self, html_form, failed=False):
        """
        Return the response
        """
        if self.request.is_xhr:
            result = self.xhr_response(html_form)
        else:
            result = {
                'title': LOGIN_TITLE,
                'html_form': html_form,
            }
            if failed:
                result['message'] = LOGIN_ERROR_MSG
        return result

    def success_response(self):
        """
        Return the result to send on successfull authentication
        """
        if self.request.is_xhr:
            result = Apiv1Resp(self.request)
        else:
            result = HTTPFound(
                location=self.get_next_page(),
                headers=self.request.response.headers,
            )
        return result

    def __call__(self):
        if self.request.user is not None:
            return self.success_response()

        form = _get_login_form(self.request, use_ajax=self.request.is_xhr)

        if 'submit' in self.request.params:
            controls = self.request.params.items()
            log.info(u"Authenticating : '{0}' (xhr : {1})".format(
                self.request.params.get('login'),
                self.request.is_xhr
            )
            )
            try:
                form_datas = form.validate(controls)
            except ValidationFailure, err:
                log.exception(u" - Authentication error")
                err_form = err.render()
                result = self.response(err_form, failed=True)
            else:
                connect_user(self.request, form_datas)
                result = self.success_response()
        else:
            if not self.request.is_xhr:
                form.set_appstruct({'nextpage': self.get_next_page()})
            result = self.response(form.render())
        return result


def logout_view(request):
    """
        The logout view
    """
    loc = request.route_url('index')
    forget(request)
    request.response.delete_cookie("remember_me")
    response = HTTPFound(location=loc, headers=request.response.headers)
    return response


def includeme(config):
    """
        Add auth related routes/views
    """
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_view(
        forbidden_view,
        context=HTTPForbidden,
        permission=NO_PERMISSION_REQUIRED,
        xhr=True,
        renderer='json',
    )
    config.add_view(
        forbidden_view,
        context=HTTPForbidden,
        permission=NO_PERMISSION_REQUIRED,
        renderer="forbidden.mako"
    )
    config.add_view(
        logout_view,
        route_name='logout',
        permission=NO_PERMISSION_REQUIRED
    )
    config.add_view(
        LoginView,
        route_name='login',
        permission=NO_PERMISSION_REQUIRED,
        renderer='login.mako',
        layout='login',
    )
    config.add_view(
        LoginView,
        route_name='login',
        xhr=True,
        permission=NO_PERMISSION_REQUIRED,
        renderer='json',
        layout="default",
    )

    # API v1
    config.add_route('apiloginv1', '/api/v1/login')
    config.add_view(
        api_login_get_view,
        route_name='apiloginv1',
        permission=NO_PERMISSION_REQUIRED,
        xhr=True,
        renderer='json',
        request_method='GET',
    )
    config.add_view(
        api_login_post_view,
        route_name='apiloginv1',
        permission=NO_PERMISSION_REQUIRED,
        xhr=True,
        renderer='json',
        request_method='POST',
    )
