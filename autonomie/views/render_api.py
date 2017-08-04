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

from pyramid.security import has_permission as base_has_permission

from autonomie_base.utils.date import (
    format_date,
    format_short_date,
    format_long_date,
    format_datetime,
)
from autonomie.utils.strings import (
    format_amount,
    format_status,
    format_activity_status,
    format_expense_status,
    format_account,
    format_name,
    format_paymentmode,
    format_quantity,
    format_task_type,
    format_estimation_status,
    format_invoice_status,
    format_cancelinvoice_status,
    estimation_get_major_status,
    invoice_get_major_status,
    cancelinvoice_get_major_status,
    major_status,
    human_readable_filesize,
    month_name,
)
from autonomie.utils.html import clean_html


STATUS_ICON = dict(
    (
        ('draft', u"bold"),
        ('wait', u'time'),
        ('valid', u''),
        ('invalid', u'remove'),
    )
)
ESTIMATION_STATUS_ICON = dict(
    (
        ('aborted', 'trash'),
        ('sent', "send"),
        ('signed', 'ok'),
        ('geninv', 'tasks'),
    )
)
INVOICE_STATUS_ICON = dict(
    (
        ('paid', u""),
        ("resulted", u"ok"),
    )
)
EXPENSE_STATUS_ICON = dict(
    (
        ('paid', u""),
        ('resulted', u"ok"),
        ("justified", u"tasks"),
    )
)


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
