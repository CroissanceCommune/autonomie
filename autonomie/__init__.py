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
    Main file for our pyramid application
"""
import locale
locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

from sqlalchemy import engine_from_config

from pyramid.config import Configurator
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.path import DottedNameResolver

from pyramid_beaker import set_cache_regions_from_settings

from autonomie.utils.security import (
    RootFactory,
    TraversalDbAccess,
    set_models_acls,
)

from autonomie.models.initialize import initialize_sql
from autonomie.models.config import get_config
from autonomie.utils.avatar import get_groups
from autonomie.utils.avatar import get_avatar
from autonomie.utils.session import get_session_factory


AUTONOMIE_MODULES = (
    "autonomie.views.activity",
    "autonomie.views.auth",
    "autonomie.views.cancelinvoice",
    "autonomie.views.commercial",
    "autonomie.views.company",
    "autonomie.views.company_invoice",
    "autonomie.views.competence",
    "autonomie.views.csv_import",
    "autonomie.views.customer",
    "autonomie.views.estimation",
    "autonomie.views.expense",
    "autonomie.views.files",
    "autonomie.views.holiday",
    "autonomie.views.index",
    "autonomie.views.invoice",
    "autonomie.views.job",
    "autonomie.views.json",
    "autonomie.views.manage",
    "autonomie.views.payment",
    "autonomie.views.sale_product",
    "autonomie.views.project",
    "autonomie.views.sage",
    "autonomie.views.static",
    "autonomie.views.statistics",
    "autonomie.views.taskaction",
    "autonomie.views.tests",
    "autonomie.views.treasury_files",
    "autonomie.views.user",
    "autonomie.views.workshop",
)

AUTONOMIE_PANELS_MODULES = (
    "autonomie.panels.menu",
    "autonomie.panels.task",
    "autonomie.panels.company",
    "autonomie.panels.invoicetable",
)

AUTONOMIE_EVENT_MODULES = (
    "autonomie.events.tasks",
    "autonomie.events.expense",
)
AUTONOMIE_REQUEST_SUBSCRIBERS = (
    "autonomie.subscribers.new_request",
    "autonomie.subscribers.before_render",
)

AUTONOMIE_ADMIN_MODULES = (
    "autonomie.views.admin.main",
    "autonomie.views.admin.competence",
    "autonomie.views.admin.expense",
    "autonomie.views.admin.vente",
)

AUTONOMIE_SERVICE_FACTORIES = (
    (
        "services.treasury_invoice_producer",
        "autonomie.compute.sage.InvoiceExport",
        "autonomie.interfaces.ITreasuryInvoiceProducer",
    ),
    (
        "services.treasury_invoice_writer",
        "autonomie.export.sage.SageInvoiceCsvWriter",
        "autonomie.interfaces.ITreasuryInvoiceWriter",
    ),
    (
        "services.treasury_expense_producer",
        "autonomie.compute.sage.ExpenseExport",
        "autonomie.interfaces.ITreasuryExpenseProducer",
    ),
    (
        "services.treasury_expense_writer",
        "autonomie.export.sage.SageExpenseCsvWriter",
        "autonomie.interfaces.ITreasuryExpenseWriter",
    ),
    (
        "services.treasury_payment_producer",
        "autonomie.compute.sage.PaymentExport",
        "autonomie.interfaces.ITreasuryPaymentProducer",
    ),
    (
        "services.treasury_payment_writer",
        "autonomie.export.sage.SagePaymentCsvWriter",
        "autonomie.interfaces.ITreasuryPaymentWriter",
    ),
)
AUTONOMIE_SERVICES = (
    (
        "services.IInvoiceService",
        "autonomie.models.task.invoice.InvoiceService",
        "autonomie.interfaces.IInvoiceService",
    ),
)


def resolve(dotted_path):
    """
    Return the module or the python variable matching the dotted_path
    """
    return DottedNameResolver().resolve(dotted_path)


def add_static_views(config, settings):
    """
        Add the static views used in Autonomie
    """
    statics = settings.get('autonomie.statics', 'static')
    config.add_static_view(
        statics,
        "autonomie:static",
        cache_max_age=3600,
    )


def main(global_config, **settings):
    """
        Main function : returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    config = prepare_config(**settings)

    dbsession = initialize_sql(engine)

    config = base_configure(config, dbsession, **settings)
    from autonomie.utils.filedepot import (
        configure_filedepot,
    )
    configure_filedepot(settings)
    config.configure_celery(global_config['__file__'])

    config.commit()
    # for i in config.introspector.get_category('permissions'):
    #     print(i['introspectable'].discriminator)

    return config.make_wsgi_app()


def prepare_config(**settings):
    """
    Prepare the configuration object to setup the main application elements
    """
    session_factory = get_session_factory(settings)
    set_cache_regions_from_settings(settings)
    auth_policy = SessionAuthenticationPolicy(callback=get_groups)
    acl_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        authentication_policy=auth_policy,
        authorization_policy=acl_policy,
        session_factory=session_factory,
    )
    config.begin()
    config.commit()
    return config


def setup_services(config, settings):
    """
    Setup the services (pyramid_services) used in Autonomie
    """
    for service_name, default, interface_path in AUTONOMIE_SERVICES:
        module_path = settings.get("autonomie." + service_name, default)
        interface = resolve(interface_path)
        module = resolve(module_path)
        config.register_service(module(), interface)

    for service_name, default, interface_path in AUTONOMIE_SERVICE_FACTORIES:
        module_path = settings.get("autonomie." + service_name, default)
        interface = resolve(interface_path)
        module = resolve(module_path)
        config.register_service_factory(module, interface)


def base_configure(config, dbsession, **settings):
    """
    All plugin and others configuration stuff
    """
    set_models_acls()
    from autonomie.models.base import model_services_init
    model_services_init()
    TraversalDbAccess.dbsession = dbsession

    # Application main configuration
    config._set_root_factory(RootFactory)
    config.set_default_permission('view')

    # Adding some usefull properties to the request object
    config.set_request_property(lambda _: dbsession(), 'dbsession', reify=True)
    config.set_request_property(get_avatar, 'user', reify=True)
    config.set_request_property(lambda _: get_config(), 'config', reify=True)

    add_static_views(config, settings)

    for module in AUTONOMIE_REQUEST_SUBSCRIBERS:
        config.include(module)

    for module in AUTONOMIE_MODULES:
        config.include(module)

    for module in AUTONOMIE_PANELS_MODULES:
        config.include(module)

    for module in AUTONOMIE_EVENT_MODULES:
        config.include(module)

    for module in AUTONOMIE_ADMIN_MODULES:
        config.include(module)

    setup_services(config, settings)

    from autonomie.utils.renderer import (
        customize_renderers,
    )
    customize_renderers(config)

    for module in settings.get('autonomie.includes', '').split():
        if module.strip():
            config.include(module)
    return config


def version():
    """
    Return Autonomie's version number (as defined in setup.py)
    """
    import pkg_resources
    version = pkg_resources.require(__name__)[0].version
    return version


__author__ = "Arezki Feth, Miotte Julien, Pettier Gabriel and Tjebbes Gaston"
__copyright__ = "Copyright 2012-2013, Croissance Commune"
__license__ = "GPL"
__version__ = "3.0"
