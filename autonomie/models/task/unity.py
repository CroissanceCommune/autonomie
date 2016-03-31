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
    Models for work unit (days, ...)
"""
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from autonomie.models.base import default_table_args
from autonomie.models.base import DBBASE
from autonomie.forms import (
    get_hidden_field_conf,
    EXCLUDED,
)


class WorkUnit(DBBASE):
    """
        Work unit, used to build the price list
    """
    __colanderalchemy_config__ = {
        "title": u"unité de prestation",
        "help_msg": u"Configurer les unités de prestation proposées dans les \
formulaires d'édition des devis/factures",
        "validation_msg": u"Les unités de prestation ont bien été configurées"
    }
    __tablename__ = "workunity"
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': get_hidden_field_conf()},
    )
    label = Column(
        String(100),
        info={'colanderalchemy': {'title': u"Intitulé"}}
    )

    def __json__(self, request):
        return dict(id=self.id, label=self.label, value=self.label)
