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
    Comptability associated form schemas
"""
import colander

from deform import widget

from autonomie.views.forms.widgets import deferred_autocomplete_widget


class OperationSchema(colander.MappingSchema):
    """
        Schéma for comptability operations insertion/edition
    """
    company_id = colander.SchemaNode(colander.String(),
                                     title=u"Entreprise",
                                     default="",
                                     widget=deferred_autocomplete_widget)
    year = colander.SchemaNode(colander.Integer(),
                                     title=u"Année")
    label = colander.SchemaNode(colander.String(),
                                    title=u"Libellé")
    amount = colander.SchemaNode(colander.String(),
                                    title=u"Montant")
    charge = colander.SchemaNode(colander.Integer(),
                                 title=u"Négatif",
                                 widget=widget.CheckboxWidget(true_val="1",
                                                             false_val="0"))
