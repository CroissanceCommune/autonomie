# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging

from autonomie.models.project.business import Business
from autonomie.utils.menu import (
    MenuItem,
    Menu,
)
from autonomie.default_layouts import DefaultLayout
from autonomie.views.business.routes import (
    BUSINESS_ITEM_ROUTE,
    BUSINESS_ITEM_ESTIMATION_ROUTE,
    BUSINESS_ITEM_INVOICE_ROUTE,
    BUSINESS_ITEM_FILE_ROUTE,
)


logger = logging.getLogger(__name__)

BusinessMenu = Menu(name="businessmenu")
BusinessMenu.add(
    MenuItem(
        name='overview',
        label=u"Vue générale",
        route_name=BUSINESS_ITEM_ROUTE,
        icon="fa fa-line-chart",
        perm="view.business",
    )
)
BusinessMenu.add(
    MenuItem(
        name='business_estimations',
        label=u"Devis",
        route_name=BUSINESS_ITEM_ESTIMATION_ROUTE,
        icon=u"fa fa-files-o",
        perm="list.estimations",
    )
)
BusinessMenu.add(
    MenuItem(
        name='business_invoices',
        label=u"Factures",
        route_name=BUSINESS_ITEM_INVOICE_ROUTE,
        icon=u"fa fa-files-o",
        perm="list.invoices",
    )
)
BusinessMenu.add(
    MenuItem(
        name='business_files',
        label=u"Fichiers rattachés",
        route_name=BUSINESS_ITEM_FILE_ROUTE,
        icon=u"fa fa-folder-open",
    )
)


class BusinessLayout(DefaultLayout):
    """
    Layout for business related pages

    Provide the main page structure for project view
    """

    def __init__(self, context, request):
        DefaultLayout.__init__(self, context, request)

        if isinstance(context, Business):
            self.current_business_object = context
        elif hasattr(context, "business"):
            self.current_business_object = context.business
        else:
            raise Exception(
                u"Can't retrieve the current business used in the "
                u"business layout, context is : %s" % context
            )

    @property
    def edit_url(self):
        return self.request.route_path(
            BUSINESS_ITEM_ROUTE,
            id=self.current_business_object.id,
            _query={'action': 'edit'}
        )

    @property
    def businessmenu(self):
        BusinessMenu.set_current(self.current_business_object)
        return BusinessMenu


def includeme(config):
    config.add_layout(
        BusinessLayout,
        template="autonomie:templates/business/layout.mako",
        name='business',
    )
