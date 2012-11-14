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


ITEMS_PER_PAGE_OPTIONS = (('10 par page', u'10'),
                          ('20 par page', u'20'),
                          ('30 par page', u'30'),
                          ("40 par page", u'40'),
                          ('50 par page', u'50'),
                          ('Tous', u'10000'))


@colander.deferred
def deferred_default_sort(node, kw):
    return kw['default_sort']


@colander.deferred
def deferred_sort_validator(node, kw):
    return colander.OneOf(kw['sort_columns'].keys())


@colander.deferred
def deferred_default_direction(node, kw):
    return kw['default_direction']


@colander.deferred
def deferred_items_per_page(node, kw):
    """
        get the default items_per_page value from the request cookies
    """
    req = kw['request']
    item_per_page = req.cookies.get('items_per_page', 10)
    try:
        item_per_page = int(item_per_page)
    except:
        item_per_page = 10
    return item_per_page


@colander.deferred
def deferred_items_per_page_validator(node, kw):
    """
        Return a fake validator that only set a cookie in the session
    """
    req = kw['request']
    def set_cookie(node, value):
        req.response.set_cookie("items_per_page", str(value))
        req.cookies['items_per_page'] = str(value)
    return set_cookie


class BaseListsSchema(colander.MappingSchema):
    """
        Base List schema used to validate the common list view options
        raw search
        pagination arguments
        sort parameters
    """
    search = colander.SchemaNode(colander.String(), missing=u'')
    items_per_page = colander.SchemaNode(colander.Integer(),
                               missing=deferred_items_per_page,
                               validator=deferred_items_per_page_validator)
    page = colander.SchemaNode(colander.Integer(), missing=0)
    sort = colander.SchemaNode(colander.String(),
                               missing=deferred_default_sort,
                               validator=deferred_sort_validator)
    direction = colander.SchemaNode(colander.String(),
                            missing=deferred_default_direction,
                            validator=colander.OneOf(['asc', 'desc']))
