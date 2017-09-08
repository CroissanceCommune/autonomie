# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import deform
from autonomie.forms.export import (
    PeriodSchema,
    AllSchema,
    InvoiceNumberSchema,
    ExpenseIdSchema,
    ExpenseSchema,
    ExpenseAllSchema,
)


EXPORT_BTN = deform.Button(name="submit", type="submit", title=u"Exporter")


HELPMSG_CONFIG = u"""Des éléments de configuration sont manquants, veuillez
configurer les informations comptables nécessaires à l'export des documents,
<a href="{0}" target='_blank'>Ici</a>"""


def get_period_form(
    request,
    title=u"Exporter les factures sur une période donnée"
):
    """
        Return the period search form
    """
    schema = PeriodSchema(title=title)
    schema = schema.bind(request=request)
    return deform.Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid=u'period_form',
    )


def get_all_form(
    request,
    counter,
    title=u"Exporter les factures non exportées",
):
    """
    Return a void form used to export all non-exported documents

    :param obj counter: An iterator used for form id generation
    """
    schema = ExpenseAllSchema(title=title)
    schema = schema.bind(request=request)
    formid = u'all_form'
    return deform.Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid=formid,
        counter=counter,
    )


def get_expense_all_form(
    request,
    counter,
    title=u"Exporter les factures non exportées",
    prefix='',
):
    """
    Return a void form used to export all non-exported documents

    :param obj counter: An iterator used for form id generation
    """
    schema = ExpenseAllSchema(title=title)
    schema = schema.bind(request=request, prefix=prefix)
    formid = u'%s_all_form' % prefix
    return deform.Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid=formid,
        counter=counter,
    )


def get_invoice_number_form(
    request,
    counter,
    title=u"Exporter à partir d'un numéro"
):
    """
        Return the search form used to search invoices by number+year
    """
    schema = InvoiceNumberSchema(title=title)
    schema = schema.bind(request=request)
    return deform.Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid=u'invoice_number_form',
        counter=counter,
    )


def get_expense_id_form(request, counter, title, prefix='expense'):
    """
    Return a form for expense export by id
    :param counter: the iterator used to insert various forms in the same page
    """
    schema = ExpenseIdSchema(title=title)
    schema = schema.bind(request=request, prefix=prefix)
    return deform.Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid=u"%s_id_form" % prefix,
        counter=counter,
    )


def get_expense_form(request, title, prefix='expense'):
    """
    Return a form for expense export
    :param obj request: Pyramid request object
    :returns: class:`deform.Form`

    """
    schema = ExpenseSchema(title=title)
    schema = schema.bind(request=request, prefix=prefix)
    return deform.Form(
        schema=schema,
        buttons=(EXPORT_BTN,),
        formid=u"%s_main_form" % prefix,
    )
