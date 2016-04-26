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

from pyramid.httpexceptions import HTTPFound

from autonomie.utils.widgets import ViewLink
from autonomie.models.task import Invoice
from autonomie.models.expense import ExpenseSheet
from autonomie.forms.payments import (
    PaymentSchema,
    ExpensePaymentSchema,
)
from autonomie.forms import (
    merge_session_with_post,
)
from autonomie.views import (
    BaseFormView,
)

log = logging.getLogger(__name__)


def populate_invoice_payment_actionmenu(context, request):
    """
    Set the menu items in the request context
    """
    link = ViewLink(
        u"Voir la facture",
        path="invoice",
        id=context.parent.id,
    )
    request.actionmenu.add(link)
    link = ViewLink(
        u"Modifier",
        "edit_payment",
        path="payment",
        id=context.id,
        _query=dict(action="edit")
    )
    request.actionmenu.add(link)
    link = ViewLink(
        u"Supprimer",
        "delete_payment",
        path="payment",
        confirm=u"Êtes-vous sûr de vouloir supprimer ce paiement ?",
        id=context.id,
        _query=dict(action="delete", come_from=request.referer)
    )
    request.actionmenu.add(link)


def payment_view(context, request):
    """
    Simple payment view
    """
    populate_invoice_payment_actionmenu(context, request)
    return dict(title=u"Paiement pour la facture {0}"
                .format(context.task.official_number))


class PaymentEdit(BaseFormView):
    """
    Edit payment view
    """
    title = u"Modification d'un paiement"
    schema = PaymentSchema()

    def populate_actionmenu(self):
        return populate_invoice_payment_actionmenu(self.context, self.request)

    def before(self, form):
        form.set_appstruct(self.context.appstruct())
        self.populate_actionmenu()
        return form

    def get_default_redirect(self):
        """
        Get the default redirection path
        """
        return self.request.route_path(
            "payment",
            id=self.context.id
        )

    def submit_success(self, appstruct):
        """
        handle successfull submission of the form
        """
        payment_obj = self.context

        # update the payment
        merge_session_with_post(payment_obj, appstruct)
        self.dbsession.merge(payment_obj)

        # Check the invoice status
        force_resulted = appstruct.pop('resulted', False)
        parent = payment_obj.parent
        parent = parent.check_resulted(
            force_resulted=force_resulted,
            user_id=self.request.user.id
        )
        self.dbsession.merge(parent)

        come_from = appstruct.pop('come_from', None)

        if come_from is not None:
            redirect = come_from
        else:
            redirect = self.get_default_redirect()
        return HTTPFound(redirect)


def populate_expense_payment_actionmenu(context, request):
    link = ViewLink(
        u"Voir la feuille de notes de dépense",
        path="expensesheet",
        id=context.parent.id,
    )
    request.actionmenu.add(link)
    link = ViewLink(
        u"Modifier",
        "edit_expense_payment",
        path="expense_payment",
        id=context.id,
        _query=dict(action="edit")
    )
    request.actionmenu.add(link)
    link = ViewLink(
        u"Supprimer",
        "edit_expense_payment",
        path="expense_payment",
        confirm=u"Êtes-vous sûr de vouloir supprimer ce paiement ?",
        id=context.id,
        _query=dict(action="delete", come_from=request.referer)
    )
    request.actionmenu.add(link)


def expense_payment_view(context, request):
    """
    Simple expense payment view
    """
    populate_expense_payment_actionmenu(context, request)
    return dict(title=u"Paiement pour la note de dépense {0}"
                .format(context.parent.id))


class ExpensePaymentEdit(PaymentEdit):
    schema = ExpensePaymentSchema()

    def populate_actionmenu(self):
        return populate_expense_payment_actionmenu(
            self.context,
            self.request,
        )

    def get_default_redirect(self):
        """
        Get the default redirection path
        """
        return self.request.route_path(
            "expense_payment",
            id=self.context.id
        )


def payment_delete(context, request):
    """
    Payment deletion view
    """
    parent = context.parent

    request.dbsession.delete(context)

    parent = parent.check_resulted(user_id=request.user.id)
    request.dbsession.merge(parent)
    request.session.flash(u"Le paiement a bien été supprimé")

    if 'come_from' in request.GET:
        redirect = request.GET['come_from']
    elif isinstance(parent, Invoice):
        redirect = request.route_path("invoice", id=parent.id)
    elif isinstance(parent, ExpenseSheet):
        redirect = request.route_path("expensesheet", id=parent.id)
    return HTTPFound(redirect)


def add_routes(config):
    """
    Add module's related routes
    """
    config.add_route(
        "payment",
        "/payments/{id:\d+}",
        traverse="/payments/{id}",
    )
    config.add_route(
        "expense_payment",
        "/expense_payments/{id:\d+}",
        traverse="/expense_payments/{id}",
    )


def includeme(config):
    add_routes(config)
    config.add_view(
        payment_view,
        route_name="payment",
        permission="view_payment",
        renderer="/payment.mako",
    )
    config.add_view(
        PaymentEdit,
        route_name="payment",
        permission="edit_payment",
        request_param='action=edit',
        renderer="/base/formpage.mako",
    )
    config.add_view(
        payment_delete,
        route_name="payment",
        permission="delete_payment",
        request_param="action=delete",
    )

    config.add_view(
        expense_payment_view,
        route_name="expense_payment",
        permission="view_expense_payment",
        renderer="/payment.mako",
    )
    config.add_view(
        ExpensePaymentEdit,
        route_name="expense_payment",
        permission="edit_expense_payment",
        request_param='action=edit',
        renderer="/base/formpage.mako",
    )
    config.add_view(
        payment_delete,
        route_name="expense_payment",
        permission="edit_payment",
        request_param="action=delete",
    )
