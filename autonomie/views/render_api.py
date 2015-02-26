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
import bleach

from copy import deepcopy
from pyramid.security import has_permission as base_has_permission

from autonomie.utils.date import (
    format_date,
    format_short_date,
    format_long_date,
    format_datetime,
)

ALLOWED_HTML_TAGS = bleach.ALLOWED_TAGS + ['font', 'br', 'p', 'span', 'h1',
                                            'h2', 'h3', 'h4', 'h5', 'hr',
                                            'img']
ALLOWED_HTML_ATTRS = deepcopy(bleach.ALLOWED_ATTRIBUTES)
ALLOWED_HTML_ATTRS['font'] = ['color']
ALLOWED_HTML_ATTRS['*'] = ['class', 'style']
ALLOWED_HTML_ATTRS['img'] = ['src', 'width', 'height', 'alt']
ALLOWED_CSS_STYLES = ['color', 'text-align', 'font-weight', 'font-family']

DEF_STATUS = u"Statut inconnu"
STATUS = dict((
            ("draft", u"Brouillon modifié",),
            ("wait", u"Validation demandée",),
            ("valid", u"Validé{genre}"),
            ('invalid', u"Invalidé{genre}",),
            ("abort", u"Annulé{genre}",),
            ("geninv", u"Facture générée",),
            ("aboinv", u"Facture annulée",),
            ("aboest", u"Devis annulé",),
            ("paid", u"Paiement partiel reçu",),
            ("resulted", u"Paiement reçu",),
            ))
EXPENSE_STATUS = dict((
    ("draft", u"Brouillon modifié",),
    ("wait", u"Validation demandée",),
    ("valid", u"Validé{genre}"),
    ('invalid', u"Invalidé{genre}",),
    ("resulted", u"Paiement notifié",),
    ))
ACTIVITY_STATUS = dict((
    ("closed", u"Terminée",),
    ("planned", u"Planifiée",),
    ))


TASKTYPES_LABEL = dict(
    invoice=u"Facture",
    estimation=u"Devis",
    cancelinvoice=u"Avoir",
)


def format_status(task, full=True):
    """
        return a formatted status string
    """
    if task.type_ == 'invoice':
        genre = u"e"
    else:
        genre = u""
    status_str = STATUS.get(task.CAEStatus, DEF_STATUS).format(genre=genre)
    if task.type_ == 'cancelinvoice':
        if task.is_resulted():
            status_str = u"Validé"
        elif task.is_paid():
            status_str = u"Payé partiellement"
    suffix = u" par {0} le {1}"\
            .format(format_account(task.statusPersonAccount),
                                        format_date(task.statusDate))
    if full:
        status_str += suffix

    return status_str


def format_expense_status(expense, full=True):
    """
        Return a formatted status string for the expense
    """
    status_str = EXPENSE_STATUS.get(expense.status, DEF_STATUS)\
            .format(genre=u"e")
    if expense.status_user:
        account = format_account(expense.status_user)
    else:
        account = format_account(expense.user)
    date = format_date(expense.status_date)
    suffix = u" par {0} le {1}".format(account, date)

    if full:
        status_str += suffix

    return status_str


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


def format_amount(amount, trim=True, grouping=True):
    """
        return a pretty printable amount
    """
    resp = u""
    if amount is not None:
        if isinstance(amount, float) or isinstance(amount, int):
            if amount == int(amount):
                # On a 2 chiffres après la virgule (pas plus)
                trim = True
        if trim:
            amount = int(amount) / 100.0
            resp = locale.format("%.2f", amount, grouping=grouping)
        else:
            resp = locale.format("%g", amount / 100.0, grouping=grouping)
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
        except ValueError as e:
            return u""

    if index in range(1, 13):
        result = calendar.month_name[index].decode('utf-8')

    return result


def clean_html(text):
    """
        Return a sanitized version of an html code keeping essential html tags
        and allowing only a few attributes
    """
    return bleach.clean(
            text,
            tags=ALLOWED_HTML_TAGS,
            attributes=ALLOWED_HTML_ATTRS,
            styles=ALLOWED_CSS_STYLES,
            )


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
    format_amount  = staticmethod(format_amount)
    format_date  = staticmethod(format_date)
    format_status  = staticmethod(format_status)
    format_expense_status  = staticmethod(format_expense_status)
    format_activity_status  = staticmethod(format_activity_status)
    format_account  = staticmethod(format_account)
    format_name  = staticmethod(format_name)
    format_paymentmode  = staticmethod(format_paymentmode)
    format_short_date  = staticmethod(format_short_date)
    format_long_date  = staticmethod(format_long_date)
    format_quantity  = staticmethod(format_quantity)
    format_datetime = staticmethod(format_datetime)
    format_task_type = staticmethod(format_task_type)
    human_readable_filesize  = staticmethod(human_readable_filesize)
    month_name  = staticmethod(month_name)
    clean_html  = staticmethod(clean_html)

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
