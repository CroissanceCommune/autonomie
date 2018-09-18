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
from autonomie.utils.widgets import (
    Link,
    Column,
)


class TaskListPanel(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _get_item_url(self, item, subpath=None, action=None, _anchor=None):
        """
        Build an url to access the item
        """
        route = "/%ss/{id}" % item.type_
        if subpath is not None:
            route += "%s" % subpath

        query = {}
        if action:
            query['action'] = action
        return self.request.route_path(
            route, id=item.id, _query=query, _anchor=_anchor
        )

    def _stream_main_actions(self, item):
        """
        Yield common actions
        """
        yield Link(
            self._get_item_url(item, subpath=".pdf"),
            u"PDF",
            icon='file-pdf-o',
            popup=True,
        )
        yield Link(
            self._get_item_url(item),
            u"Voir le document",
            icon='pencil',
        )
        if self.request.has_permission('add.file', item):
            yield Link(
                self._get_item_url(item, subpath="/addfile"),
                u"Ajouter un fichier",
                icon='file-text',
                popup=True,
            )
        if self.is_admin_view:
            yield Link(
                self.request.route_path("company", id=item.company_id),
                u"Voir l'enseigne %s" % item.company.name,
                icon="user",
            )
        yield Link(
            self.request.route_path("customer", id=item.customer_id),
            u"Voir le client %s" % item.customer.label,
            icon="building-o",
        )

        if self.request.has_permission('delete.%s' % item.type_, item):
            yield Link(
                self._get_item_url(item, subpath="/delete"),
                u"Supprimer",
                icon='trash',
                confirm=u"Êtes-vous sûr de vouloir supprimer ce document ?"
            )

    def _stream_invoice_actions(self, item):
        """
        Stream actions available for invoices

        :param obj request: The Pyramid request object
        :param obj item: The Invoice or CancelInvoice instance
        """
        for i in self._stream_main_actions(item):
            yield i

        yield Link(
            self._get_item_url(item, subpath=".html", _anchor="payment"),
            u"Voir les encaissements",
            icon="money",
        )
        if self.request.has_permission('add_payment.invoice', item):
            yield Link(
                self._get_item_url(item, subpath="/addpayment"),
                u"Enregistrer un encaissement",
                icon='money',
                popup=True,
            )

    def _invoice_columns(self):
        """
        Columns used to display an invoice list
        """
        result = []
        result.append(Column("<span class='fa fa-comment'></span>"))
        result.append(Column(u"Identifiant", u"official_number"))
        if self.is_admin_view:
            result.append(Column(u"Enseigne", u"company"))
        result.append(Column(u"Émise le", 'date'))
        result.append(Column(u"Nom de la facture", 'internal_number'))
        result.append(Column(u"Client", 'customer'))
        result.append(Column(u"Montant HT", "ht"))
        result.append(Column(u"TVA", "ht"))
        result.append(Column(u"TTC", "ttc"))
        result.append(Column(u"Paiement", "payment"))
        result.append(Column(u"Fichiers attachés"))
        return result

    def __call__(
        self,
        records,
        datatype="invoice",
        is_admin_view=False,
        is_project_view=False,
        is_business_view=False,
    ):
        """
        datas used to render a list of tasks (estimations/invoices)
        """
        self.is_admin_view = is_admin_view
        self.is_project_view = is_project_view
        self.is_business_view = is_business_view
        ret_dict = dict(
            records=records,
            is_admin_view=is_admin_view,
            is_project_view=is_project_view,
            is_business_view=is_business_view,
            is_invoice_list=not (is_business_view or is_project_view)
        )
        if datatype == "invoice":
            ret_dict['stream_actions'] = self._stream_invoice_actions
            ret_dict['columns'] = self._invoice_columns()
        else:
            raise Exception(u"Only invoices are supported")
        ret_dict['totalht'] = sum(r.ht for r in records)
        ret_dict['totaltva'] = sum(r.tva for r in records)
        ret_dict['totalttc'] = sum(r.ttc for r in records)
        return ret_dict


def includeme(config):
    """
        Pyramid's inclusion mechanism
    """
    config.add_panel(
        TaskListPanel,
        'task_list',
        renderer='panels/task/task_list.mako',
    )
