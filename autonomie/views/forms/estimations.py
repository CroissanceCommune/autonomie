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
    forms schemas for estimation list related views
"""
import colander
from deform import widget as deform_widget

from autonomie.views.forms.lists import BaseListsSchema
from autonomie.views.forms import main


STATUS_OPTIONS = (('all', u"Tous les devis", ),
                ('geninv', u"Devis concrétisés (avec facture)", ),
                ('aboest', u"Devis annulés", ),
                ('valid', u"Devis en cours", ),
                )


def get_list_schema():
    schema = BaseListsSchema().clone()

    del schema['search']

    schema.insert(0, main.customer_node())

    schema.insert(0, colander.SchemaNode(
        colander.String(),
        name='status',
        widget=deform_widget.SelectWidget(values=STATUS_OPTIONS),
        validator=colander.OneOf([s[0] for s in STATUS_OPTIONS]),
        missing='all'
    ))

    schema.insert(0, main.year_select_node(name='year'))

    return schema
