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

from autonomie.models.task import (
    WorkUnit,
    PaymentConditions,
)
from autonomie.models.payments import (
    PaymentMode,
)

from autonomie.views.admin.tools import (
    get_model_admin_view,
)
from autonomie.views.admin.sale import (
    SaleIndexView,
    SALE_URL,
)

logger = logging.getLogger(__name__)


BaseWorkUnitAdminView = get_model_admin_view(WorkUnit, r_path=SALE_URL)


class WorkUnitAdminView(BaseWorkUnitAdminView):
    disable = False


BasePaymentModeAdminView = get_model_admin_view(PaymentMode, r_path=SALE_URL)


class PaymentModeAdminView(BasePaymentModeAdminView):
    disable = False


PaymentConditionsAdminView = get_model_admin_view(
    PaymentConditions,
    r_path=SALE_URL,
)


def includeme(config):
    for view in (
        WorkUnitAdminView,
        PaymentModeAdminView, PaymentConditionsAdminView
    ):
        config.add_route(view.route_name, view.route_name)
        config.add_admin_view(view, parent=SaleIndexView)
