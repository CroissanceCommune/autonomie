# -*- coding: utf-8 -*-
# * File Name : auth.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : mar. 03 avril 2012 14:31:27 CEST
#
# * Project :
#
import logging

from pyramid.view import view_config
from pyramid.url import route_url
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden

from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember
from pyramid.security import NO_PERMISSION_REQUIRED

from deform import Form
from deform import Button
from deform import ValidationFailure

from autonomie.models import DBSESSION
from autonomie.views.forms import authSchema
from autonomie.views.forms import pwdSchema

log = logging.getLogger(__name__)

@view_config(context=HTTPForbidden, permission=NO_PERMISSION_REQUIRED)
def forbidden_view(request):
    """
        The forbidden view (handles the redirection to login form)
    """
    log.debug("# Forbidden view")
    if authenticated_userid(request):
        log.debug(" + Authenticated but not allowed")
        return HTTPForbidden()
    log.debug(" + Not authenticated : try again")
    #redirecting to the login page with the current path as param
    loc = request.route_url('login', _query=(('nextpage', request.path),))
    return HTTPFound(location=loc)

@view_config(route_name='login', permission=NO_PERMISSION_REQUIRED,
                                                        renderer='login.mako')
def login_view(request):
    """
        The login view
    """
    log.debug("# Login page")
    form = Form(authSchema,
                buttons=(Button(name="submit",
                                title="Connexion",
                                type='submit'),))
    nextpage = request.params.get('nextpage') or request.route_url('index')
    app_struct = {'nextpage':nextpage}
    myform = form.render(app_struct)
    fail_message = None
    if 'submit' in request.params:
        log.debug(" + Validating authentication")
        controls = request.params.items()
        try:
            datas = form.validate(controls)
        except ValidationFailure, e:
            log.debug("Erreur d'authentification")
            myform = e.render()
            fail_message = u"Erreur d'authentification"
            return {'title':"Authentification",
                    'html_form':myform,
                    'message':fail_message
                    }
        log.debug("  + Validation ok, redirecting")
        log.debug("     -> {0}".format(nextpage))
        login = datas['login']
        # Storing the datas in the session
        remember(request, login)
        return HTTPFound(location=nextpage)
    return {
            'title':"Bienvenu sur Autonomie",
            'html_form':myform,
            'message':fail_message
            }

@view_config(route_name='logout', permission=NO_PERMISSION_REQUIRED)
def logout_view(request):
    """
        The logout view
    """
    headers = forget(request)
    loc = request.route_url('index')
    return HTTPFound(location=loc, headers=headers)

@view_config(route_name='account', renderer='account.mako')
def account(request):
    """
        Account handling page
    """
    avatar = request.session['user']
    pwdformschema = pwdSchema.bind(check=True)
    pwdform = Form(pwdformschema, buttons=("submit",))
    html_form = pwdform.render({'login':avatar.login})
    if "submit" in request.params:
        controls = request.params.items()
        try:
            datas = pwdform.validate(controls)
        except ValidationFailure, e:
            log.debug("Erreur d'authentification")
            html_form = e.render()
        else:
            dbsession = DBSESSION()
            new_pass = datas['pwd']
            avatar.set_password(new_pass)
            dbsession.merge(avatar)
            dbsession.flush()
            request.session.flash(u"Votre mot de passe a bien été modifié",
                                                                    'main')

    return dict(title="Mon compte",
                html_form=html_form,
                account=avatar
                )
