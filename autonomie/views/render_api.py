# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 31-08-2012
# * Last Modified :
#
# * Project :
#
"""
    render api, usefull functions usable inside templates
"""
import datetime
import locale

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


def format_amount(amount, trim=True):
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
            resp = locale.format("%.2f", amount, grouping=True)
        else:
            resp = locale.format("%g", amount / 100.0, grouping=True)
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


def format_unity(unity, pretty=False):
    """
        format the unity of a document (days, weeks ...)
    """
    if pretty:
        default = u""
    else:
        default = u"-"
    labels = dict(
            NONE=default,
            HOUR=u"heure(s)",
            DAY=u"jour(s)",
            WEEK=u"semaine(s)",
            MONTH=u"mois",
            FEUIL=u"feuillet(s)",
            PACK=u"forfait",
            )
    return labels.get(unity, default)


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
          format_account=format_account,
          format_name=format_name,
          format_paymentmode=format_paymentmode,
          format_short_date=format_short_date,
          format_long_date=format_long_date,
          format_quantity=format_quantity,
          format_unity=format_unity,
          urlupdate=urlupdate)
