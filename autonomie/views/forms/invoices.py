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
    form schemas for invoices related views
"""
from datetime import date
import colander

from autonomie.views.forms.lists import BaseListsSchema


STATUS_OPTIONS = ((u"Toutes les factures", "both"),
                  (u"Les factures payées", "paid"),
                  (u"Seulement les impayés", "notpaid"))

@colander.deferred
def default_year(node, kw):
    return date.today().year

class InvoicesListSchema(BaseListsSchema):
    # We override the search param, it needs to be an integer in our case
    # (officialNumber)
#    search = colander.SchemaNode(colander.Integer(), missing=None)
    status = colander.SchemaNode(colander.String(),
            validator=colander.OneOf([s[1] for s in STATUS_OPTIONS]),
            missing='both')
    year = colander.SchemaNode(colander.Integer(), missing=default_year)
    customer_id = colander.SchemaNode(colander.Integer(), missing=-1)
    company_id = colander.SchemaNode(colander.Integer(), missing=-1)
