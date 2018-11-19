# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Delalande Jocelyn;
"""
Common translation strings
"""
import locale
import calendar
import unicodedata

from autonomie.compute import math_utils
from autonomie_base.utils.date import (
    format_date,
)
from autonomie_base.utils.ascii import force_ascii


SINGLE_STATUS_LABELS = {
    'draft': u"Brouillon",
    'wait': u"En attente de validation",
    "valid": u"Validé{genre}",
    "invalid": u"Invalidé{genre}",
}

DEF_STATUS = u"Statut inconnu"

STATUS = dict(
    (
        ("draft", u"Brouillon modifié",),
        ("wait", u"Validation demandée",),
        ("valid", u"Validé{genre}"),
        ('invalid', u"Invalidé{genre}",),
    )
)

ESTIMATION_STATUS = dict(
    (
        ("aborted", u"Annulé",),
        ("sent", u"Envoyé",),
        ('signed', u'Signé',),
        ('geninv', u"Factures générées"),
    )
)

INVOICE_STATUS = dict(
    (
        ('paid', u"Payée partiellement",),
        ("resulted", u"Soldée",),
    )
)

EXPENSE_STATUS = dict(
    (
        ('paid', u"Payée partiellement"),
        ('resulted', u"Payée intégralement"),
        ("justified", u"Justificatifs reçus"),
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


def format_status_string(status, genre=''):
    """
    Return a label for the given status

    :param str status: One the available status (draft/wait/valid/invalid)
    :param str genre: '' or 'e'
    """
    if status in ESTIMATION_STATUS:
        result = ESTIMATION_STATUS[status]
    elif status in INVOICE_STATUS:
        result = INVOICE_STATUS[status]
    else:
        result = STATUS.get(status, status)
    return result.format(genre=genre)


def format_main_status(task, full=True):
    """
        return a formatted status string
    """
    status = task.status

    if task.type_ == 'invoice':
        genre = u"e"
    else:
        genre = u""

    if full:
        status_str = STATUS.get(status, DEF_STATUS).format(genre=genre)
        suffix = u" par {0} le {1}".format(
            format_account(task.status_person),
            format_date(task.status_date)
        )
        status_str += suffix
    else:
        status_str = SINGLE_STATUS_LABELS.get(status, DEF_STATUS).format(
            genre=genre
        )

    return status_str


def format_estimation_status(estimation, full=True):
    """
    Return a formatted string for estimation specific status
    """
    if estimation.geninv:
        return ESTIMATION_STATUS.get('geninv')
    elif estimation.signed_status in ('sent', 'aborted', 'signed'):
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
    elif expense.status == 'waiting' and expense.justified:
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


def format_amount(amount, trim=True, grouping=True, precision=2, dividor=None):
    """
        return a pretty printable amount
    """
    resp = u""
    if amount is not None:
        if dividor is None:
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
            resp = resp.replace(' ', '&nbsp;').replace(u"\xe2\x80\xaf", "&nbsp;")

        if isinstance(resp, str):
            resp = resp.decode('utf-8')

    return resp


def format_float(value, precision=None, grouping=True, html=True):
    """
    Format a float value :
        * Localized version with grouped values
        * trim datas to precision if asked for

    :param float value: The value to format
    :param int precision: If set, the value will be trimmed to that precision
    :param bool grouping: Should the datas be grouped (by thousands)
    :param bool html: Should the resulting string be html-friendly (using
    &nbsp;)
    :returns: A formatted string that can be used in html outputs
    :rtype: str
    """
    if isinstance(value, (float, int)):
        if precision is not None:
            formatter = "%.{0}f".format(precision)
        else:
            formatter = "%s"
        value = locale.format(formatter, value, grouping=grouping)

        if html:
            value = value.replace(" ", "&nbsp;")
            value = value.replace(u"\xe2\x80\xaf", "&nbsp;")
    return value


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


def format_civilite(civilite_str):
    """
    Shorten the civilite string

    :param str civilite_str: Monsieur/Madame
    :returns: Mr/Mme
    :rtype: str
    """
    res = civilite_str
    if civilite_str.lower() == u'monsieur':
        res = u"M."
    elif civilite_str.lower() == u'madame':
        res = u"Mme"
    elif civilite_str.lower() == u'mr&mme':
        res = u"M. et Mme"
    return res


def format_lower_ascii(original_str):
    """
    Generate a lower ascii only string from the original one
    :param str original_str: The string to modify
    :returns: A modified string
    :rtype: str
    """
    result = original_str.lower()
    result = force_ascii(result)
    result = result.replace(' ', '_')
    return result


def safe_unicode(unicode_str):
    """
    Replace special chars to their ascii counterpart.

    This does modify the string (remove accents…) and is only intended for
    non-human-facing strings.

    :type unicode_str: unicode
    :rtype: unicode
    """
    normalized = unicodedata.normalize('NFKD', unicode_str)
    return normalized.encode('ascii', 'ignore').decode()


def compile_template_str(template_string, template_context):
    """
    Compile the template string and merge the context

    :param str template_string: The string to templatize
    :param dict template: templating context
    :rtype: str
    """
    return template_string.format(**template_context)
