# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
from sqlalchemy import (
    Column,
    Boolean,
)
from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)


class PaymentConditions(ConfigurableOption):
    __colanderalchemy_config__ = {
        'title': u"des conditions de paiement",
        'help_msg': u"Configurer les conditions de paiement prédéfinies que \
les entrepreneurs pourront sélectionner lors de la création de leur devis.",
        'validation_msg': u"Les conditions de paiement ont bien \
été configurées",
    }
    id = get_id_foreignkey_col('configurable_option.id')
    default = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Valeur par défaut",
                'description': u"Utiliser cette condition pour pré-remplir \
le champ 'Conditions de paiement' du formulaire de création de devis ?",
            }
        }
    )
