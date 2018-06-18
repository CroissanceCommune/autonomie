# -*- coding: utf-8 -*-
import os

from autonomie.forms.admin import get_config_schema
from autonomie.views.admin.tools import BaseConfigView
from autonomie.views.admin.sale import (
    SALE_URL,
    SaleIndexView,
)


NUMBERING_CONFIG_URL = os.path.join(SALE_URL, 'numbering')


class NumberingConfigView(BaseConfigView):
    title = u"Numérotation des factures"
    description = u"Configurer la manière dont son numérotées les factures"

    route_name = NUMBERING_CONFIG_URL

    validation_msg = u"Les informations ont bien été enregistrées"

    keys = (
        'invoice_number_template',

        'global_sequence_init_value',

        'year_sequence_init_value',
        'year_sequence_init_date',

        'month_sequence_init_value',
        'month_sequence_init_date',
    )

    schema = get_config_schema(keys)

    info_message = u"""
<p>Il est possible de personaliser le format du numéro de facture.</p>\
<p>Plusieurs variables et séquences chronologiques sont à disposition.</p>\
<h3>Variables :</h3>\
<ul>\
<li><code>{YYYY}</code> : année, sur 4 digits</li>\
<li><code>{YY}</code> : année, sur 2 digits</li>\
<li><code>{MM}</code> : mois, sur 2 digits</li>\
<li><code>{ANA}</code> : code analytique de l'activité</li>\
</ul>\
<h3>Numéros de séquence :</h3>\
<ul>\
<li><code>{SEQGLOBAL}</code> : numéro de séquence global (aucun ràz)</li>\
<li><code>{SEQYEAR}</code> : numéro de séquence annuel (ràz chaque année)</li>\
<li><code>{SEQMONTH}</code> : numéro de séquence mensuel (ràz chaque mois)</li>\
<li><code>{SEQMONTHANA}</code>: numéro de séquence par activité et par mois (ràz chaque mois)</li>\
</ul>\
<p>Dans le cas d'une migration depuis un autre outil de gestion, il est possible d'initialiser les séquences à une valeur différente de zéro.</p>\
    """


def add_routes(config):
    config.add_route(NUMBERING_CONFIG_URL, NUMBERING_CONFIG_URL)


def includeme(config):
    add_routes(config)
    config.add_admin_view(NumberingConfigView, parent=SaleIndexView)
