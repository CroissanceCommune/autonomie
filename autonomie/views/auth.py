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

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden

from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.threadlocal import get_current_registry

from deform import Form
from deform import Button
from deform import ValidationFailure

from js.bootstrap import bootstrap

from autonomie.views import BaseView
from autonomie.forms.user import (
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
        bootstrap.need()
        return_datas = {"title": u"Accès refusé", }

    else:
        log.debug(u"An access has been forbidden to an unauthenticated user")
        # redirecting to the login page with the current path as param
        loc = request.route_url('login', _query=(('nextpage', request.path),))
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
    log.info(u"Authenticating : '{0}'".format(appstruct.get('login')))
    try:
        appstruct = schema.deserialize(appstruct)
    except colander.Invalid, err:
        log.exception("  - Erreur")
        raise RestError(err.asdict(), 400)
    else:
        login = appstruct['login']
        log.info(u" + '{0}' has been authenticated".format(login))
        remember(request, login)
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
#    if use_ajax:
#        form.widget = deform.widget.FormWidget(
#            template='autonomie:deform_templates/formajax.pt'
#        )
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
        form = _get_login_form(self.request, use_ajax=self.request.is_xhr)

        if 'submit' in self.request.params:
            controls = self.request.params.items()
            log.info(u"Authenticating : '{0}'".format(
                self.request.params.get('login'))
            )

            try:
                datas = form.validate(controls)
            except ValidationFailure, err:
                log.exception(u" - Authentication error")
                err_form = err.render()
                result = self.response(err_form, failed=True)

            else:
                login = datas['login']
                log.info(u" + '{0}' has been authenticated".format(login))
                # Storing the datas in the request object
                remember(self.request, login)
                remember_me = datas.get('remember_me', False)
                if remember_me:
                    print(self.request.session._headers)
                    print(dir(self.request.session._headers))
                    log.info("  * The user wants to be remembered")
                    longtimeout = get_longtimeout()
                    self.request.response.set_cookie(
                        'remember_me',
                        "ok",
                        max_age=longtimeout,
                    )
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
    headers = forget(request)
    print(headers)
    request.response.delete_cookie("remember_me")
    print(headers)
    response = HTTPFound(location=loc, headers=headers)
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
    config.add_view(logout_view,
                    route_name='logout',
                    permission=NO_PERMISSION_REQUIRED)
    config.add_view(
        LoginView,
        route_name='login',
        permission=NO_PERMISSION_REQUIRED,
        renderer='login.mako',
    )
    config.add_view(
        LoginView,
        route_name='login',
        xhr=True,
        permission=NO_PERMISSION_REQUIRED,
        renderer='json',
    )

    # API v1
    config.add_route('apiloginv1', '/api/v1/login')
    config.add_view(
        api_login_post_view,
        route_name='apiloginv1',
        permission=NO_PERMISSION_REQUIRED,
        xhr=True,
        renderer='json',
        request_method='POST',
    )
    config.add_view(
        api_login_get_view,
        route_name='apiloginv1',
        permission=NO_PERMISSION_REQUIRED,
        xhr=True,
        renderer='json',
        request_method='GET',
    )
