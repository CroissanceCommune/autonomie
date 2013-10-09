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

import colander
from datetime import date
from deform import widget

from autonomie.views.forms.widgets import deferred_year_select_widget
from .custom_types import AmountType

@colander.deferred
def default_year(node, kw):
    return date.today().year


class CommercialFormSchema(colander.MappingSchema):
    year = colander.SchemaNode(colander.Integer(),
            widget=deferred_year_select_widget,
            default=default_year,
            missing=default_year,
            title=u"")


class CommercialSetFormSchema(colander.MappingSchema):
    month = colander.SchemaNode(colander.Integer(),
                                widget=widget.HiddenWidget(),
                                title=u'',
                                validator=colander.Range(1,12))
    value = colander.SchemaNode(AmountType(), title=u"CA prévisionnel")
    comment = colander.SchemaNode(colander.String(),
                                 widget=widget.TextAreaWidget(cols=25, rows=1),
                                    title=u"Commentaire",
                                    missing=u"")
