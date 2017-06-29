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
    render api, usefull functions usable inside templates
"""
import locale
import calendar

from pyramid.security import has_permission as base_has_permission

from autonomie.compute import math_utils

from autonomie_base.utils.date import (
    format_date,
    format_short_date,
    format_long_date,
    format_datetime,
)
from autonomie.utils.html import clean_html

DEF_STATUS = u"Statut inconnu"
STATUS = dict(
    (
        ("draft", u"Brouillon modifié",),
        ("wait", u"Validation demandée",),
        ("valid", u"Validé{genre}"),
        ('invalid', u"Invalidé{genre}",),
    )
)
STATUS_ICON = dict(
    (
        ('draft', u"bold"),
        ('wait', u'time'),
        ('valid', u''),
        ('invalid', u'remove'),
    )
)

ESTIMATION_STATUS = dict(
    (
        ("aborted", u"Annulé",),
        ('signed', u'Signé',),
        ('geninv', u"Factures générées"),
    )
)
ESTIMATION_STATUS_ICON = dict(
    (
        ('aborted', 'trash'),
        ('signed', 'ok'),
        ('geninv', 'tasks'),
    )
)

INVOICE_STATUS = dict(
    (
        ('paid', u"Payée partiellement",),
        ("resulted", u"Soldée",),
    )
)
INVOICE_STATUS_ICON = dict(
    (
        ('paid', u""),
        ("resulted", u"ok"),
    )
)
EXPENSE_STATUS = dict(
    (
        ('paid', u"Payée partiellement"),
        ('resulted', u"Payée intégralement"),
        ("justified", u"Justificatifs reçus"),
    )
)
EXPENSE_STATUS_ICON = dict(
    (
        ('paid', u""),
        ('resulted', u"ok"),
        ("justified", u"tasks"),
    )
)

ACTIVITY_STATUS = dict((
    ("closed", u"Terminée",),
    ("planned", u"Planifiée",),
    ))


TASKTYPES_LABEL = dict(
    invoice=u"Facture",
    estimation=u"Devis",
    cancelinvoice=u"Avoir",
)


def format_main_status(task, full=True):
    """
        return a formatted status string
    """
    status = task.status

    if task.type_ == 'invoice':
        genre = u"e"
    else:
        genre = u""

    status_str = STATUS.get(status, DEF_STATUS).format(genre=genre)
    if full:
        suffix = u" par {0} le {1}".format(
            format_account(task.statusPersonAccount),
            format_date(task.statusDate)
        )
        status_str += suffix

    return status_str


def format_estimation_status(estimation, full=True):
    """
    Return a formatted string for estimation specific status
    """
    if estimation.geninv:
        return ESTIMATION_STATUS.get('geninv')
    elif estimation.signed_status in ('aborted', 'signed'):
        return ESTIMATION_STATUS.get(estimation.signed_status)
    else:
        return format_main_status(estimation, full)


def format_invoice_status(invoice, full=True):
    """
    Return a formatted string for invoice specific status

    :param obj invoice: An invoice instance
    """
    if invoice.paid_status in ('paid', 'resulted'):
        return INVOICE_STATUS.get(invoice.paid_status)
    else:
        return format_main_status(invoice, full)


def format_cancelinvoice_status(cinvoice, full=True):
    """
    Return a string representing the state of this cancelinvoice

    :param obj cinvoice: A CancelInvoice instance
    """
    return format_main_status(cinvoice, full)


def format_expense_status(expense, full=True):
    """
        Return a formatted status string for the expense
    """
    if expense.paid_status in ('paid', 'resulted'):
        status_str = EXPENSE_STATUS.get(expense.paid_status)
    else:
        status_str = STATUS.get(expense.status, DEF_STATUS).format(genre='e')
        if full:
            if expense.status_user:
                account = format_account(expense.status_user)
            else:
                account = format_account(expense.user)
            date = format_date(expense.status_date)
            suffix = u" par {0} le {1}.".format(account, date)

            status_str += suffix

    return status_str


def format_status(element):
    if element.type_ == 'estimation':
        return format_estimation_status(element)
    elif element.type_ == 'invoice':
        return format_invoice_status(element)
    elif element.type_ == 'cancelinvoice':
        return format_cancelinvoice_status(element)
    elif element.type_ == 'expensesheet':
        return format_expense_status(element)


def estimation_status_icon(estimation):
    """
    Return the name of the bootstrap icon matching the status
    """
    if estimation.geninv:
        return ESTIMATION_STATUS_ICON.get("geninv")
    elif estimation.signed_status != 'waiting':
        return ESTIMATION_STATUS_ICON.get(estimation.signed_status)
    else:
        return STATUS_ICON.get(estimation.status)


def invoice_status_icon(invoice):
    """
    Return the name of the bootstrap icon matching the status
    """
    if invoice.paid_status != 'waiting':
        return INVOICE_STATUS_ICON.get(invoice.paid_status)
    else:
        return STATUS_ICON.get(invoice.status)


def cancelinvoice_status_icon(cinvoice):
    """
    Return the name of the bootstrap icon matching the status
    """
    return STATUS_ICON.get(cinvoice.status)


def expense_status_icon(expense):
    """
    Return the name of the bootstrap icon matching the status
    """
    if expense.paid_status != 'waiting':
        return EXPENSE_STATUS_ICON.get(expense.paid_status)
    elif expense.justified:
        return EXPENSE_STATUS_ICON.get("justified")
    else:
        return STATUS_ICON.get(expense.status)


def status_icon(element):
    if element.type_ == 'estimation':
        return estimation_status_icon(element)
    elif element.type_ == 'invoice':
        return invoice_status_icon(element)
    elif element.type_ == 'cancelinvoice':
        return cancelinvoice_status_icon(element)
    elif element.type_ == 'expensesheet':
        return expense_status_icon(element)


def estimation_get_major_status(estimation):
    """
    Return the most significant status for the given task
    """
    res = 'draft'
    if estimation.geninv:
        res = 'geninv'
    elif estimation.signed_status != 'waiting':
        res = estimation.signed_status
    else:
        res = estimation.status
    return res


def invoice_get_major_status(invoice):
    """
    Return the most significant status for the given task
    """
    res = 'draft'
    if invoice.paid_status != 'waiting':
        res = invoice.paid_status
    else:
        res = invoice.status
    return res


def cancelinvoice_get_major_status(cinvoice):
    """
    Return the most significant status for the given task
    """
    return cinvoice.status

def expense_get_major_status(expense):
    if expense.paid_status != 'waiting':
        return expense.paid_status
    elif expense.justified:
        return 'justified'
    else:
        return expense.status


def major_status(element):
    if element.type_ == 'estimation':
        return estimation_get_major_status(element)
    elif element.type_ == 'invoice':
        return invoice_get_major_status(element)
    elif element.type_ == 'cancelinvoice':
        return cancelinvoice_get_major_status(element)
    elif element.type_ == 'expensesheet':
        return expense_get_major_status(element)


def format_activity_status(activity):
    """
        Return a formatted status string for the given activity
    """
    status_str = ACTIVITY_STATUS.get(activity.status, DEF_STATUS)
    return status_str


def format_account(account, reverse=True, upper=True):
    """
        return {firstname} {lastname}
    """
    if hasattr(account, 'firstname'):
        firstname = account.firstname
        lastname = account.lastname
    elif hasattr(account, 'coordonnees_firstname'):
        firstname = account.coordonnees_firstname
        lastname = account.coordonnees_lastname
    else:
        firstname = "Inconnu"
        lastname = ""
    return format_name(firstname, lastname, reverse, upper)


def format_name(firstname, lastname, reverse=True, upper=True):
    """
        format firstname and lastname in a common format
    """
    if firstname is None:
        firstname = ""
    if lastname is None:
        lastname = ""
    firstname = firstname.capitalize()
    if upper:
        lastname = lastname.upper()
    else:
        lastname = lastname.capitalize()
    if reverse:
        return u"{0} {1}".format(lastname, firstname)
    else:
        return u"{0} {1}".format(firstname, lastname)


def add_trailing_zeros(amount):
    """
    Ensure an amount has sufficient trailing zeros
    """
    if ',' in amount:
        dec = len(amount) - amount.index(',')
        if dec <= 2:
            for i in range(0, 2 - dec):
                amount += '0'
    return amount


def format_amount(amount, trim=True, grouping=True, precision=2):
    """
        return a pretty printable amount
    """
    resp = u""
    if amount is not None:
        dividor = 10.0 ** precision

        # Limit to 2 trailing zeros
        if isinstance(amount, float) and precision <= 2:
            if amount == int(amount):
                trim = True
        elif precision > 2:
            if math_utils.floor_to_precision(
                amount,
                precision=2,
                dialect_precision=precision
            ) == amount:
                trim = True

        if trim:
            formatter = "%.2f"
            amount = int(amount) / dividor
            resp = locale.format(formatter, amount, grouping=grouping)
        else:
            formatter = "%.{0}f".format(precision)
            amount = amount / dividor
            resp = locale.format(formatter, amount, grouping=grouping)
            resp = resp.rstrip('0')
            resp = add_trailing_zeros(resp)

    if grouping:
        resp = resp.replace(' ', '&nbsp;')
    return resp


def format_quantity(quantity):
    """
        format the quantity
    """
    if quantity is not None:
        return locale.format('%g', quantity, grouping=True)
    else:
        return ""


def format_paymentmode(paymentmode):
    """
       format payment modes for display
       Since #662 ( Permettre la configuration des modes de paiement )
       no formatting is necessary
    """
    return paymentmode


def month_name(index):
    """
        Return the name of the month number "index"
    """
    result = u""
    if not isinstance(index, int):
        try:
            index = int(index)
        except ValueError:
            return u""

    if index in range(1, 13):
        result = calendar.month_name[index].decode('utf-8')

    return result


def human_readable_filesize(size):
    """
        Return a human readable file size
    """
    result = u"Inconnu"
    try:
        size = float(size)
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                result = u"%3.1f %s" % (size, x)
                break
            size /= 1024.0
    except ValueError:
        pass
    return result


def format_task_type(task):
    return TASKTYPES_LABEL.get(task.type_)


class Api(object):
    """
        Api object passed to the templates hosting all commands we will use
    """
    format_amount = staticmethod(format_amount)
    format_date = staticmethod(format_date)
    format_status = staticmethod(format_status)
    format_expense_status = staticmethod(format_expense_status)
    format_activity_status = staticmethod(format_activity_status)
    format_account = staticmethod(format_account)
    format_name = staticmethod(format_name)
    format_paymentmode = staticmethod(format_paymentmode)
    format_short_date = staticmethod(format_short_date)
    format_long_date = staticmethod(format_long_date)
    format_quantity = staticmethod(format_quantity)
    format_datetime = staticmethod(format_datetime)
    format_task_type = staticmethod(format_task_type)

    format_estimation_status = staticmethod(format_estimation_status)
    format_invoice_status = staticmethod(format_invoice_status)
    format_cancelinvoice_status = staticmethod(format_cancelinvoice_status)
    estimation_status_icon = staticmethod(estimation_status_icon)
    estimation_get_major_status = staticmethod(estimation_get_major_status)
    invoice_status_icon = staticmethod(invoice_status_icon)
    invoice_get_major_status = staticmethod(invoice_get_major_status)
    cancelinvoice_status_icon = staticmethod(cancelinvoice_status_icon)
    cancelinvoice_get_major_status = staticmethod(
        cancelinvoice_get_major_status)
    major_status = staticmethod(major_status)
    status_icon = staticmethod(status_icon)

    human_readable_filesize = staticmethod(human_readable_filesize)
    month_name = staticmethod(month_name)
    clean_html = staticmethod(clean_html)

    def __init__(self, context, request):
        self.request = request
        self.context = context
        if getattr(request, 'template_api', None) is None:
            request.template_api = self

    def has_permission(self, perm_name, context=None):
        context = context or self.context
        return base_has_permission(perm_name, context, self.request)

    def urlupdate(self, args_dict={}):
        """
            Return the current url with updated GET params
            It allows to keep url params when :
            * sorting
            * searching
            * moving from one page to another

            if current url ends with :
                <url>?foo=1&bar=2
            when passing {'foo':5}, we get :
                <url>?foo=5&bar=2
        """
        get_args = self.request.GET.copy()
        get_args.update(args_dict)
        path = self.request.current_route_path(_query=get_args)
        return path

    def file_url(self, fileobj):
        """
        Return the url to access the given fileobj
        """
        if fileobj is not None and fileobj.id is not None:
            return self.request.route_path('file', id=fileobj.id)
        else:
            return ""

    def img_url(self, fileobj):
        """
        Return the url to access the given fileobj as an image
        """
        if fileobj is not None and fileobj.id is not None:
            return self.request.route_path('filepng', id=fileobj.id)
        else:
            return ""
