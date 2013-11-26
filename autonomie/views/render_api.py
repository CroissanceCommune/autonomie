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
import datetime
import locale
import calendar
import bleach
from copy import deepcopy

ALLOWED_HTML_TAGS = bleach.ALLOWED_TAGS + ['font', 'br', 'p']
ALLOWED_HTML_ATTRS = deepcopy(bleach.ALLOWED_ATTRIBUTES)
ALLOWED_HTML_ATTRS['font'] = ['color']
ALLOWED_HTML_ATTRS['*'] = ['class', 'style']
ALLOWED_CSS_STYLES = ['color', 'text-align', 'font-weight']

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

def format_status(task):
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
    return status_str + suffix


def format_expense_status(expense):
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
    return status_str + suffix


def format_account(account, reverse=False):
    """
        return {firstname} {lastname}
    """
    if account:
        firstname = account.firstname
        lastname = account.lastname
    else:
        firstname = "Inconnu"
        lastname = ""
    return format_name(firstname, lastname, reverse)


def format_name(firstname, lastname, reverse=False):
    """
        format firstname and lastname in a common format
    """
    if firstname is None:
        firstname = ""
    if lastname is None:
        lastname = ""
    firstname = firstname.capitalize()
    lastname = lastname.upper()
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


def format_short_date(date):
    """
        return a short printable version of the date obj
    """
    if isinstance(date, datetime.date):
        resp = date.strftime("%e/%m/%Y")
    elif not date:
        resp = u""
    else:
        resp = datetime.datetime.fromtimestamp(float(date)).strftime(
                                                            "%d/%m/%Y %H:%M")
    return resp


def format_long_date(date):
    """
        return a long printable version of the date obj
    """
    if isinstance(date, datetime.date):
        resp = u"{0}".format(
            date.strftime("%e %B %Y").decode('utf-8').capitalize()
        )
    elif not date:
        resp = u""
    else:
        date = datetime.datetime.fromtimestamp(float(date))
        resp = u"{0}".format(
            date.strftime("%e %B %Y").decode('utf-8').capitalize()
        )
    return resp


def format_date(date, short=True):
    """
        return a pretty print version of the date object
    """
    if short:
        return format_short_date(date)
    else:
        return format_long_date(date)


def format_paymentmode(paymentmode):
    """
       format payment modes for display
       Since #662 ( Permettre la configuration des modes de paiement )
       no formatting is necessary
    """
    return paymentmode


def urlupdate(request, args_dict):
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
    get_args = request.GET.copy()
    get_args.update(args_dict)
    path = request.current_route_path(_query=get_args)
    return path


def month_name(index):
    """
        Return the name of the month number "index"
    """
    if index in range(1,13):
        return calendar.month_name[index].decode('utf-8')
    else:
        return u""


def clean_html(text):
    """
        Return a sanitized version of an html code keeping essential html tags
        and allowing only a few attributes
    """
    return bleach.clean(
            text,
            tags=ALLOWED_HTML_TAGS,
            attributes=ALLOWED_HTML_ATTRS,
            )


class Api(object):
    """
        Api object passed to the templates hosting all commands we will use
    """
    def __init__(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

api = Api(format_amount=format_amount,
          format_date=format_date,
          format_status=format_status,
          format_expense_status=format_expense_status,
          format_account=format_account,
          format_name=format_name,
          format_paymentmode=format_paymentmode,
          format_short_date=format_short_date,
          format_long_date=format_long_date,
          format_quantity=format_quantity,
          urlupdate=urlupdate,
          month_name=month_name,
          clean_html=clean_html,
          )
