# -*- coding: utf-8 -*-
# * File Name : auth.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : mar. 02 oct. 2012 18:57:08 CEST
#
# * Project :
#
"""
    All Authentication views
"""
import logging

from pyramid.view import view_config
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


@view_config(context=HTTPForbidden, permission=NO_PERMISSION_REQUIRED,
        xhr=True, renderer='json')
@view_config(context=HTTPForbidden, permission=NO_PERMISSION_REQUIRED)
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


@view_config(route_name='login', permission=NO_PERMISSION_REQUIRED,
                                                        renderer='login.mako')
def login_view(request):
    """
        The login view
    """
    form = Form(get_auth_schema(),
                buttons=(Button(name="submit",
                                title="Connexion",
                                type='submit'),))
    nextpage = request.params.get('nextpage') or request.route_url('index')
    # avoid looping
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
        except ValidationFailure, e:
            log.exception(" - Authentication error")
            myform = e.render()
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


@view_config(route_name='logout', permission=NO_PERMISSION_REQUIRED)
def logout_view(request):
    """
        The logout view
    """
    headers = forget(request)
    loc = request.route_url('index')
    return HTTPFound(location=loc, headers=headers)
