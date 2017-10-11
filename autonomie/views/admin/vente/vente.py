# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2016 Croissance Commune
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Configuration générale du module vente:

    Mise en forme des PDFs
    Unité de prestation
"""
import logging

from autonomie.views.admin.tools import (
    get_model_admin_view,
)

from autonomie.models.task import (
    TaskMention,
    WorkUnit,
    PaymentConditions,
)
from autonomie.models.payments import (
    PaymentMode,
)

logger = logging.getLogger(__name__)

(
    mention_admin_class,
    mention_route,
    mention_tmpl,
) = get_model_admin_view(
    TaskMention,
    r_path="admin_vente",
)

(
    work_unit_admin_class,
    work_unit_route,
    work_unit_tmpl,
) = get_model_admin_view(
    WorkUnit,
    r_path="admin_vente",
)

(
    payment_mode_admin_class,
    payment_mode_route,
    payment_mode_tmpl,
) = get_model_admin_view(
    PaymentMode,
    r_path="admin_vente",
)

(
    payment_condition_admin_class,
    payment_condition_route,
    payment_condition_tmpl,
) = get_model_admin_view(
    PaymentConditions,
    r_path="admin_vente",
)


class WorkUnitAdmin(work_unit_admin_class):
    title = u"Configuration des unités de prestation"
    disable = False
    description = u"Les unités de prestation proposées lors de la création \
d'un devis/d'une facture"


class TaskMentionAdmin(mention_admin_class):
    title = u"Configuration des mentions facultatives des devis/factures"
    description = u"Des mentions facultatives que les entrepreneurs peuvent \
faire figurer dans leurs devis/factures"
    widget_options = {'min_len': 0}


class PaymentModeAdmin(payment_mode_admin_class):
    title = u"Configuration des modes de paiement"
    description = u"Les modes de paiement que l'on peut sélectionner pour \
enregistrer le paiement d'un devis/ d'une facture"
    disable = False


class PaymentConditionAdmin(payment_condition_admin_class):
    title = u"Configuration des conditions de paiement"
    description = u"Les conditions que les entrepreneurs peuvent sélectionner \
lors de la création d'un devis/d'une facture"


def includeme(config):
    config.add_route("admin_vente_print", "admin/vente/print")
    config.add_route("admin_vente_mention", "admin/vente/mention")
    config.add_route("admin_vente_workunit", "admin/vente/workunit")
    config.add_route("admin_vente_payment_mode", "admin/vente/payment_mode")
    config.add_route(
        "admin_vente_payment_condition",
        "admin/vente/payment_condition"
    )

    config.add_admin_view(
        TaskMentionAdmin,
        route_name="admin_vente_mention",
    )

    config.add_admin_view(
        WorkUnitAdmin,
        route_name="admin_vente_workunit",
    )

    config.add_admin_view(
        PaymentModeAdmin,
        route_name="admin_vente_payment_mode",
    )

    config.add_admin_view(
        PaymentConditionAdmin,
        route_name='admin_vente_payment_condition',
    )
