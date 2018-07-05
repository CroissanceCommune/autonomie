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
from autonomie.models.task import (
    Invoice,
    CancelInvoice,
)
from autonomie.utils.widgets import Link


def _get_item_url(request, item, subpath=None, action=None):
    """
    Build an url to access the item
    """
    route = "/%ss/{id}" % item.type_
    if subpath is not None:
        route += "%s" % subpath

    query = {}
    if action:
        query['action'] = action
    return request.route_path(
        route,
        id=item.id,
        _query=query
    )

def _stream_invoice_actions(request, item):
    """
    Stream actions available for invoices

    :param obj request: The Pyramid request object
    :param obj item: The Invoice or CancelInvoice instance
    """
    if request.has_permission('add_payment.invoice', item):
        yield Link(
            _get_item_url(request, item, subpath="/addpayment"),
            u"Enregistrer un encaissement",
            icon='money',
            popup=True,
        )



def _stream_estimation_actions(request, item):
    """
    Stream actions available for estimations

    :param obj request: The Pyramid request object
    :param obj item: The Estimation instance
    """
    # TODO : générer les factures ...
    pass


def stream_actions(request, item):
    yield Link(
        _get_item_url(request, item, subpath=".pdf"),
        u"PDF",
        icon='file-pdf-o',
        popup=True,
    )
    yield Link(
        _get_item_url(request, item),
        u"Voir",
        icon='pencil',
    )
    if request.has_permission('add.file', item):
        yield Link(
            _get_item_url(request, item, subpath="/addfile"),
            u"Ajouter un fichier",
            icon='file-text',
            popup=True,
        )
    yield Link(
        request.route_path("company", id=item.company_id),
        u"Voir l'enseigne %s" % item.company.name,
        icon="user",
    )
    yield Link(
        request.route_path("customer", id=item.customer_id),
        u"Voir le client %s" % item.customer.get_label(),
        icon="building-o",
    )

    if request.has_permission('delete.%s' % item.type_, item):
        yield Link(
            _get_item_url(request, item, subpath="/delete"),
            u"Supprimer",
            icon='trash',
            confirm=u"Êtes-vous sûr de vouloir supprimer ce document ?"
        )
    if isinstance(item, (Invoice, CancelInvoice)):
        func = _stream_invoice_actions
    else:
        func = _stream_estimation_actions

    for i in func(request, item):
        yield i


def task_list_panel(
    context,
    request,
    records,
    is_admin_view=False,
    is_project_view=False,
    is_business_view=False,
):
    """
    datas used to render a list of tasks (estimations/invoices)
    """
    ret_dict = dict(
        records=records,
        is_admin_view=is_admin_view,
        is_project_view=is_project_view,
        is_business_view=is_business_view,
        stream_actions=stream_actions,
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
        task_list_panel,
        'task_list',
        renderer='panels/task/task_list.mako',
    )
