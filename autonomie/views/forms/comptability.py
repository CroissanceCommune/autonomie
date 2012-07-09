# -*- coding: utf-8 -*-
# * File Name : comptability.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 12-06-2012
# * Last Modified :
#
# * Project : Autonomie
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
