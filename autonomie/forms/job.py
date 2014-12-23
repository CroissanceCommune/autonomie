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
"""
Job related forms
"""
import colander
import deform
from autonomie import forms


STATUS_OPTIONS = (
    ('', u"Toutes les tâches", ),
    ('planned', u"Les tâches plannifiées", ),
    ('failed', u"Les tâches ayant échouées", ),
    ('completed', u"Les tâches terminées", ),
)
TYPES_OPTIONS = (
    ('', u"Tout type de tâche", ),
    ('csv_import', u"Importation de données csv"),
)


def get_list_schema():
    """
    Return the schema for the job list search form
    """
    schema = forms.lists.BaseListsSchema().clone()
    del schema['search']
    schema.insert(
        0,
        colander.SchemaNode(
            colander.String(),
            name='status',
            widget=deform.widget.SelectWidget(values=STATUS_OPTIONS),
            validator=colander.OneOf([s[0] for s in STATUS_OPTIONS]),
            missing=colander.drop,
        )
    )
    schema.insert(
        0,
        colander.SchemaNode(
            colander.String(),
            name='type_',
            widget=deform.widget.SelectWidget(values=TYPES_OPTIONS),
            validator=colander.OneOf([s[0] for s in TYPES_OPTIONS]),
            missing=colander.drop,
        )
    )

    return schema
