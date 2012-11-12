# -*- coding: utf-8 -*-
# * File Name : auth.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : lun. 12 nov. 2012 11:04:15 CET
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

from deform import Form
from deform import Button
from deform import ValidationFailure

from autonomie.views.forms import get_auth_schema

log = logging.getLogger(__name__)


def forbidden_view(request):
    """
        The forbidden view (handles the redirection to login form)
    """
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
        redirect = HTTPFound(location=loc)
    return redirect


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
            return HTTPFound(location=nextpage)
    return {
            'title': "Bienvenue dans Autonomie",
            'html_form': myform,
            'message': fail_message
            }


def logout_view(request):
    """
        The logout view
    """
    headers = forget(request)
    loc = request.route_url('index')
    return HTTPFound(location=loc, headers=headers)


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
