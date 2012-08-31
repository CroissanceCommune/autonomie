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
            ("sent", u"Document envoyé",),
            ("paid", u"Paiement partiel reçu",),
            ("resulted", u"Paiement reçu",),
            ("recinv", u"Client relancé",),
            ('gencinv', u"Avoir généré",),
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
            status_str = u"Réglé"
        elif task.is_paid():
            status_str = u"Payé partiellement"
    suffix = u" par {0} le {1}"\
            .format(format_account(task.statusPersonAccount),
                                        format_date(task.statusDate))
    return status_str + suffix

def format_account(account):
    """
        return {firstname} {lastname}
    """
    if account:
        firstname = account.firstname
        lastname = account.lastname
    else:
        firstname = "Inconnu"
        lastname = ""
    return u"{0} {1}".format(lastname.upper(), firstname.capitalize())

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
            amount = int(amount)/100.0
            resp = locale.format("%.2f", amount, grouping=True)
        else:
            resp = locale.format("%g", amount/100.0, grouping=True)
    resp = resp.replace(' ', '&nbsp;')
    return resp

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
        resp = u"{0}".format(date.strftime("%e %B %Y")\
                                            .decode('utf-8')\
                                            .capitalize())
    elif not date:
        resp = u""
    else:
        date = datetime.datetime.fromtimestamp(float(date))
        resp = u"{0}".format(date.strftime("%e %B %Y")\
                                            .decode('utf-8')\
                                            .capitalize())
    return resp

def format_date(date, short=False):
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
    """
    if paymentmode in ("CHEQUE", u"chèque"):
        return u"par chèque"
    elif paymentmode in ("VIREMENT", u"virement"):
        return u"par virement"
    else:
        return u"mode paiement inconnu"

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
          format_paymentmode=format_paymentmode,
          format_short_date=format_short_date,
          format_long_date=format_long_date)

