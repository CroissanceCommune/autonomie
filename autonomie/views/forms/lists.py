# -*- coding: utf-8 -*-
# * File Name : search.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 06-11-2012
# * Last Modified :
#
# * Project :
#
import colander


@colander.deferred
def deferred_default_sort(node, kw):
    return kw['default_sort']


@colander.deferred
def deferred_sort_validator(node, kw):
    return colander.OneOf(kw['sort_columns'].keys())


@colander.deferred
def deferred_default_direction(node, kw):
    return kw['default_direction']


class BaseSearchSchema(colander.MappingSchema):
    """
        Base Search form schema
    """
    search = colander.SchemaNode(colander.String(), missing=u'')
    items_per_page = colander.SchemaNode(colander.Integer(), missing=10)
    page = colander.SchemaNode(colander.Integer(), missing=0)
    sort = colander.SchemaNode(colander.String(),
                               missing=deferred_default_sort,
                               validator=deferred_sort_validator)
    direction = colander.SchemaNode(colander.String(),
                            missing=deferred_default_direction,
                            validator=colander.OneOf(['asc', 'desc']))
