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


def invoicetable_panel(context, request, records, is_admin_view=False):
    """
        Return datas for the invoicetable panel
    """
    ret_dict = dict(
        records=records,
        is_admin_view=is_admin_view,
    )
    ret_dict['totalht'] = sum(r.ht for r in records)
    ret_dict['totaltva'] = sum(r.tva for r in records)
    ret_dict['totalttc'] = sum(r.ttc for r in records)
    return ret_dict


def includeme(config):
    """
        Pyramid's inclusion mechanism
    """
    config.add_panel(
        invoicetable_panel,
        'invoicetable',
        renderer='panels/invoicetable.mako',
    )
