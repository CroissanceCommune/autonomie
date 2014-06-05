# -*- coding: utf-8 -*-
# * File Name : payments.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 02-06-2014
# * Last Modified :
#
# * Project :
#
"""
Views related to payments edition
"""
import logging
import deform

from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission
from autonomie.views.forms import (
        BaseFormView,
        merge_session_with_post,
        )
from autonomie.views.forms.task import PaymentSchema
from autonomie.utils.widgets import ViewLink

log = logging.getLogger(__name__)


def payment_view(context, request):
    """
    Simple payment view
    """
    populate_actionmenu(request)
    return dict(title=u"Paiement pour la facture {0}"\
            .format(context.task.officialNumber))


class PaymentEdit(BaseFormView):
    """
    Edit payment view
    """
    title = u"Édition d'un paiement"
    schema = PaymentSchema()

    def before(self, form):
        form.set_appstruct(self.request.context.appstruct())
        populate_actionmenu(self.request)
        return form

    def submit_success(self, appstruct):
        """
        handle successfull submission of the form
        """
        context = self.request.context
        was_resulted = context.task.is_resulted()
        prec_amount = context.amount
        force_resulted = appstruct.pop('resulted', False)

        total = context.task.total()

        # Edit the payment and flush to be able to update the invoice payment
        # status afterwards
        merge_session_with_post(context, appstruct)
        self.dbsession.merge(context)
        self.dbsession.flush(context)

        come_from = appstruct.pop('come_from', None)

        user_id = self.request.user.id
        if force_resulted or context.amount == total:
            context.task.CAEStatus = 'resulted'
            self.dbsession.merge(context.task)
        elif was_resulted and not prec_amount > context.amount:
            # On a baissé le montant => plus soldée
            context.task.CAEStatus = 'paid'
            self.dbsession.merge(context.task)
        elif context.amount == context.task.total:
            # le montant est égal au total
            context.task.CAEStatus = 'resulted'
            self.dbsession.merge(context.task)

        if come_from is not None:
            redirect = come_from
        else:
            redirect = self.request.route_path("payment", id=context.id)
        return HTTPFound(redirect)


def populate_actionmenu(request):
    """
    Set the menu items in the request context
    """
    link = ViewLink(
        u"Voir la facture",
        "view",
        path="invoice",
        id=request.context.task.id,
        )
    request.actionmenu.add(link)
    if has_permission('manage', request.context, request):
        link = ViewLink(
                u"Éditer",
                "manage",
                path="payment",
                id=request.context.id,
                _query=dict(action="edit")
                )
        request.actionmenu.add(link)
        link = ViewLink(
                u"Supprimer",
                "manage",
                path="payment",
                confirm=u"Êtes-vous sûr de vouloir supprimer ce paiement ?",
                id=request.context.id,
                _query=dict(action="delete")
                )
        request.actionmenu.add(link)


def payment_delete(context, request):
    """
    Payment deletion view
    """
    invoice = context.task
    user_id = request.user.id
    if len(invoice.payments) == 1:
        invoice.CAEStatus = "valid"
        request.dbsession.merge(invoice)
    elif invoice.is_resulted():
        invoice.CAEStatus = "paid"
        request.dbsession.merge(invoice)

    request.dbsession.delete(context)

    redirect = request.route_path("invoice", id=invoice.id)
    return HTTPFound(redirect)


def includeme(config):
    config.add_route(
        "payment",
        "/payment/{id:\d+}",
        traverse="/payments/{id}",
        )

    config.add_view(payment_view,
        route_name="payment",
        permission="view",
        renderer="/payment.mako",
        )
    config.add_view(PaymentEdit,
        route_name="payment",
        permission="manage",
        request_param='action=edit',
        renderer="/base/formpage.mako",
        )
    config.add_view(payment_delete,
        route_name="payment",
        permission="manage",
        request_param="action=delete",
        )
