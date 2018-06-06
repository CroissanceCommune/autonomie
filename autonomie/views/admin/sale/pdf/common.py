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

COMMON_ROUTE = os.path.join(PDF_URL, 'common')


class CommonConfigView(BaseConfigView):
    title = u"Informations communes aux devis et factures"
    description = u"Configurer les Conditions générales de vente, les pieds de \
page des sorties PDF"
    keys = [
        'coop_cgv',
        'coop_pdffootertitle',
        'coop_pdffootertext',
        'coop_pdffootercourse',
    ]
    schema = get_config_schema(keys)
    validation_msg = u"Vos modifications ont été enregistrées"
    route_name = COMMON_ROUTE


def includeme(config):
    config.add_route(COMMON_ROUTE, COMMON_ROUTE)
    config.add_admin_view(
        CommonConfigView,
        parent=PdfIndexView,
    )
