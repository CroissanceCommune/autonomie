# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 01-02-2013
# * Last Modified :
#
# * Project :
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
