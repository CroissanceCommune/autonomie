# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 10-04-2012
# * Last Modified :
#
# * Project : autonomie
#
"""
    Form schemas for project edition
"""
import colander
import logging

from deform import widget

from autonomie.utils.forms import deferred_edit_widget
from autonomie.utils.forms import deferred_autocomplete_widget

log = logging.getLogger(__name__)

timeinput = widget.DateInputWidget
#timeinput.options = {'dateFormat':'dd / mm / yy', "altFormat": "yy-mm-dd",
#                     "altfield"}
class ProjectSchema(colander.MappingSchema):
    """
        Schema for project
    """
    name = colander.SchemaNode(colander.String(),
            title=u"Nom du projet",
            validator=colander.Length(max=150), css_class='floatted')
    code = colander.SchemaNode(colander.String(),
            title=u"Code du projet",
            widget=deferred_edit_widget,
            validator=colander.Length(4))
    type = colander.SchemaNode(colander.String(),
            title="Type de projet",
            validator=colander.Length(max=150),
            missing=u'')
    definition = colander.SchemaNode(colander.String(),
                         widget=widget.TextAreaWidget(cols=80, rows=4),
                         title=u'Définition',
                         missing=u'')
    startingDate = colander.SchemaNode(colander.Date(),
                                        title=u"Date de début",
                                        missing=u"",
                                        widget=timeinput())
    endingDate = colander.SchemaNode(colander.Date(),
                                        title=u"Date de fin",
                                    missing=u"",
                                    widget=timeinput())
    code_client = colander.SchemaNode(colander.String(),
                                        title=u"Client",
                                        widget=deferred_autocomplete_widget)

class PhaseSchema(colander.MappingSchema):
    """
        Schema for phase
    """
    name = colander.SchemaNode(colander.String(),
                               validator=colander.Length(max=150))
phaseSchema = PhaseSchema()
