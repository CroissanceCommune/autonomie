# -*- coding: utf-8 -*-
# * File Name : auth.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : ven. 06 sept. 2013 12:48:33 CEST
#
# * Project :
#
"""
    All Authentication views
"""
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

from autonomie.views.forms.user import get_auth_schema

log = logging.getLogger(__name__)


def forbidden_view(request):
    """
        The forbidden view (handles the redirection to login form)
    """
    log.debug("We are in a forbidden view")
    login = authenticated_userid(request)
    if login:
        log.warn(u"An access has been forbidden to '{0}'".format(login))
        redirect = HTTPForbidden()
    else:
        log.debug(u"An access has been forbidden to an unauthenticated user")
        #redirecting to the login page with the current path as param
        loc = request.route_url('login', _query=(('nextpage', request.path),))
        if request.is_xhr:
            redirect = dict(redirect=loc)
        else:
            redirect = HTTPFound(location=loc)
    return redirect


def get_longtimeout():
    settings = get_current_registry().settings
    default = 3600
    longtimeout = settings.get("session.longtimeout", default)
    try:
        longtimeout = int(longtimeout)
    except:
        longtimeout = default
    return longtimeout


def login_view(request):
    """
        The login view
    """
    form = Form(get_auth_schema(),
                buttons=(Button(name="submit",
                                title="Connexion",
                                type='submit'),))
    nextpage = request.params.get('nextpage') or request.route_url('index')
    # avoid redirection looping
    if nextpage == request.route_url('login'):
        nextpage = request.route_url('index')
    app_struct = {'nextpage': nextpage}
    myform = form.render(app_struct)
    fail_message = None
    if 'submit' in request.params:
        controls = request.params.items()
        log.info(u"Authenticating : '{0}'".format(request.params.get('login')))
        try:
            datas = form.validate(controls)
        except ValidationFailure, err:
            log.exception(u" - Authentication error")
            myform = err.render()
            fail_message = u"Erreur d'authentification"
            return {'title': "Authentification",
                    'html_form': myform,
                    'message': fail_message
                    }
        else:
            login = datas['login']
            log.info(u" + '{0}' has been authenticated".format(login))
            # Storing the datas in the request object
            remember(request, login)
            remember_me = datas.get('remember_me', False)
            response = HTTPFound(location=nextpage)
            if remember_me:
                log.debug("  * The user wants to be remembered")
                longtimeout = get_longtimeout()
                response.set_cookie('remember_me', "ok", max_age=longtimeout)
            return response
    return {
            'title': "Bienvenue dans Autonomie",
            'html_form': myform,
            'message': fail_message
            }


def logout_view(request):
    """
        The logout view
    """
    loc = request.route_url('index')
    headers = forget(request)
    response = HTTPFound(location=loc, headers=headers)
    response.delete_cookie("remember_me")
    return response


def includeme(config):
    """
        Add auth related routes/views
    """
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_view(forbidden_view,
                    context=HTTPForbidden,
                    permission=NO_PERMISSION_REQUIRED,
                    xhr=True,
                    renderer='json')
    config.add_view(forbidden_view,
                    context=HTTPForbidden,
                    permission=NO_PERMISSION_REQUIRED)
    config.add_view(logout_view,
                    route_name='logout',
                    permission=NO_PERMISSION_REQUIRED)
    config.add_view(login_view,
                    route_name='login',
                    permission=NO_PERMISSION_REQUIRED,
                    renderer='login.mako')
