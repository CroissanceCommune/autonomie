# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os


from autonomie.views.admin.sale import (
    SaleIndexView,
    SALE_URL
)
from autonomie.views.admin.tools import BaseAdminIndexView


PDF_URL = os.path.join(SALE_URL, "pdf")


class PdfIndexView(BaseAdminIndexView):
    title = u"Sorties PDF"
    description = u"Configurer les mentions générales des sorties pdf"
    route_name = PDF_URL


def includeme(config):
    config.add_route(PDF_URL, PDF_URL)
    config.add_admin_view(
        PdfIndexView,
        parent=SaleIndexView,
    )
    config.include('.common')
    config.include('.estimation')
    config.include('.invoice')
