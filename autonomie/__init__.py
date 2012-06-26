# -*- coding: utf-8 -*-
# * File Name : __init__.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 11-01-2012
# * Last Modified : mer. 27 juin 2012 01:20:48 CEST
#
# * Project : autonomie
#
"""
    Main file for our pyramid application
"""
import locale
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from pyramid_beaker import set_cache_regions_from_settings
from sqlalchemy import engine_from_config, create_engine

from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from autonomie.models import initialize_sql
from autonomie.utils.avatar import get_groups
from autonomie.utils.avatar import get_avatar
from autonomie.utils.config import get_config
from autonomie.utils.forms import set_deform_renderer

def main(global_config, **settings):
    """
        Main function : returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    dbsession = initialize_sql(engine)
    from autonomie.models import model
    model.DBBASE.metadata.create_all(engine)
    # Many calls related to dbsession needs to be done after the initialize_sql
    # because of the autoload stuff we're using
    from autonomie.utils.security import RootFactory
    from autonomie.utils.security import BaseDBFactory
    from autonomie.utils.security import wrap_db_objects
    wrap_db_objects()
    BaseDBFactory.dbsession = dbsession

    session_factory = session_factory_from_settings(settings)
    set_cache_regions_from_settings(settings)
    auth_policy = SessionAuthenticationPolicy(callback=get_groups)
    acl_policy = ACLAuthorizationPolicy()


    config = Configurator(settings=settings,
                        authentication_policy=auth_policy,
                        authorization_policy=acl_policy,
                        session_factory=session_factory,
                        root_factory=RootFactory
                        )
    # Application main configuration
    config.set_default_permission('view')

    # Adding some properties to the request object
    config.set_request_property(lambda _:dbsession, 'dbsession', reify=True)
    config.set_request_property(get_avatar, 'user', reify=True)
    config.set_request_property(get_config, 'config')

    config.add_static_view('static', 'autonomie:static', cache_max_age=3600)
    config.add_static_view('deformstatic', "deform:static", cache_max_age=3600)

    # Adding a static view to the configured assets
    company_assets = get_config(None, dbsession).get('files_dir')
    if company_assets:
        config.add_static_view('assets', company_assets, cache_max_age=3600)

    # Common routes
    config.add_route('index', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('account',
                    '/account')

    # Holliday routes
    config.add_route('holliday', # Add
                    '/holliday')
    config.add_route('hollidays', # view
                    '/hollidays')
    # Company Routes
    config.add_route('company',
                     '/company/{id:\d+}',
                     traverse='/companies/{id}')
    # * Clients
    config.add_route('company_clients',
                     '/company/{id:\d+}/clients',
                     traverse='/companies/{id}')
    # * Projects
    config.add_route('company_projects',
                     '/company/{id:\d+}/projects',
                     traverse='/companies/{id}')
    # * Invoices
    config.add_route('company_invoices',
                     '/company/{id:\d+}/invoices',
                     traverse='/companies/{id}')
    # * Treasury
    config.add_route('company_treasury',
                     '/company/{id:\d+}/treasury',
                     traverse='/companies/{id}')

    # Client route
    config.add_route('client',
                     '/clients/{id}',
                     traverse='/clients/{id}')
    # Project route
    config.add_route('project',
                     '/projects/{id:\d+}',
                     traverse='/projects/{id}')

    #Tasks (estimation and invoice) routes
    config.add_route('estimations',
                     '/projects/{id:\d+}/estimations',
                      traverse='/projects/{id}')
    config.add_route('estimation',
                     '/estimations/{id:\d+}',
                      traverse='/estimations/{id}')

    config.add_route('project_invoices',
                     '/projects/{id:\d+}/invoices',
                     traverse='/projects/{id}')
    config.add_route('invoice',
                     '/invoices/{id:\d+}',
                     traverse='/invoices/{id}')

    config.add_route("invoices",
                    "/invoices")

    config.add_route("cancelinvoices",
                     "/projects/{id:\d+}/cancelinvoices",
                     traverse='/projects/{id}')
    config.add_route("cancelinvoice",
                    "/cancelinvoices/{id:\d+}",
                    traverse='/cancelinvoices/{id}')

    # Administration routes
    config.add_route("admin_index",
                     "/admin")
    config.add_route("admin_main",
                    "/admin/main")
    config.add_route("admin_tva",
                    "/admin/tva")

    # Main routes
    config.add_route("users",
                    "/users")
    config.add_route("user",
                     "/users/{id:\d+}",
                     traverse="/users/{id}")

    # Operations comptables
    config.add_route("operations",
                    "/operations")
    config.add_route("operation",
                    "/operations/{id:\d+}",
                    traverse="/operations/{id}")

    # Manage main view
    config.add_route("manage",
                    "/manage")

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
    locale.setlocale(locale.LC_ALL, "")
    return config.make_wsgi_app()
