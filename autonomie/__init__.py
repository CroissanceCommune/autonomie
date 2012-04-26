# -*- coding: utf-8 -*-
# * File Name : __init__.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 11-01-2012
# * Last Modified : jeu. 26 avril 2012 17:16:35 CEST
#
# * Project : autonomie
#
"""
    Main file for our pyramid application
"""
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config, create_engine

from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from autonomie.models import initialize_sql
from autonomie.utils.avatar import get_build_avatar
from autonomie.utils.forms import set_deform_renderer


def main(global_config, **settings):
    """
        Main function : returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    dbsession = initialize_sql(engine)
    from autonomie.utils.security import RootFactory

    avatar_builder = get_build_avatar(dbsession)

    session_factory = session_factory_from_settings(settings)
    auth_policy = SessionAuthenticationPolicy(callback=avatar_builder)
    acl_policy = ACLAuthorizationPolicy()


    config = Configurator(settings=settings,
                        authentication_policy=auth_policy,
                        authorization_policy=acl_policy,
                        session_factory=session_factory,
                        root_factory=RootFactory
                        )
    config.set_default_permission('view')
    config.add_static_view('static', 'autonomie:static', cache_max_age=3600)
    config.add_static_view('deformstatic', "deform:static", cache_max_age=3600)
    company_assets = settings['autonomie.assets']
    config.add_static_view('assets', company_assets, cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('account', '/account')
    config.add_route('company', '/company/{cid}')
    config.add_route('company_clients', '/company/{cid}/clients')
    config.add_route('company_client', '/company/{cid}/clients/{id}')
    config.add_route('company_projects', '/company/{cid}/projects')
    config.add_route('company_project', '/company/{cid}/projects/{id}')
    config.add_route('estimations',
                        '/company/{cid}/projects/{id}/estimations')
    config.add_route('estimation',
                        '/company/{cid}/projects/{id}/estimations/{taskid}')
    config.add_route('invoices',
                        '/company/{cid}/projects/{id}/invoices')
    config.add_route('invoice',
                        '/company/{cid}/projects/{id}/invoices/{taskid}')
#    config.add_route('useradd', '/user/add')
#    config.add_route('userpass', '/user/pwd')
#    config.add_route('userdel', '/user/del')
#
#    config.add_route('usermodpass', '/profile/pwd')
#
#    config.add_route("clientdel", "/user/{id}/delform")
#    config.add_route("clientedit", "/user/{id}/editform")
#    config.add_route("clientadd", "/user/addform")
#
#    config.add_route('estimationlist', '/estimation/list')
#    config.add_route('estimation_pdf', '/estimation/pdf')
#
#    # REST API
#    config.add_route("users", "/users")
#    config.add_route("user", "/users/{uid}")
#    config.add_route("clients", "/company/{cid}/clients")
#    config.add_route('client', "/company/{cid}/clients/{id}")
    set_deform_renderer()
    config.scan('autonomie.views')
    config.add_translation_dirs("colander:locale/", "deform:locale")
    import locale
    locale.setlocale(locale.LC_ALL, "")
    return config.make_wsgi_app()
