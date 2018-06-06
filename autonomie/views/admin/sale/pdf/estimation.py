# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
from autonomie.forms.admin import get_config_schema
from autonomie.views.admin.tools import BaseConfigView
from autonomie.views.admin.sale.pdf import (
    PdfIndexView,
    PDF_URL,
)

ESTIMATION_ROUTE = os.path.join(PDF_URL, 'estimation')


class EstimationConfigView(BaseConfigView):
    title = u"Informations spécifiques aux devis"
    description = u"Configurer les champs spécifiques aux devis dans les \
sorties PDF"
    keys = ["coop_estimationheader", "coop_estimationfooter"]
    schema = get_config_schema(keys)
    validation_msg = u"Vos modifications ont été enregistrées"
    route_name = ESTIMATION_ROUTE


def includeme(config):
    config.add_route(ESTIMATION_ROUTE, ESTIMATION_ROUTE)
    config.add_admin_view(
        EstimationConfigView,
        parent=PdfIndexView,
    )
