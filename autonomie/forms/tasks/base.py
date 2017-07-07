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
    Task form schemas (estimation, invoice ...)
    Note : since deform doesn't fit our form needs
            (estimation form is complicated and its structure
             is mixing many sqla tables)

    validation process:
        set all the line in the colander expected schema
        validate
        raise error on an adapted way
            build an error dict which is mako understandable

    merging process:
        get the datas
        build a factory
        merge estimation and task object
        commit
        merge all lines
        commit
        merge payment conditions
        commit

    formulaire :

    phase, course, displayUnits
    lignes de prestation descr, cout qtité, unité, tva
    lignes de remise descr, cout, tva (seulement les tvas utilisées dans
                                                    les lignes au-dessus)
    TOTAL HT
    for tva in used_tva:
        TOTAL TVA tva%
    TTC
    Frais de port
    TOTAL
"""
import logging

import colander
import deform

from autonomie.models.project import (
    build_customer_values,
    Project,
)


logger = logging.getLogger(__name__)
DAYS = (
    ('NONE', '-'),
    ('HOUR', u'Heure(s)'),
    ('DAY', u'Jour(s)'),
    ('WEEK', u'Semaine(s)'),
    ('MONTH', u'Mois'),
    ('FEUIL', u'Feuillet(s)'),
    ('PACK', u'Forfait'),
)


TASKTYPES_LABELS = {
    'invoice': u'Facture',
    u'estimation': u'Devis',
    'cancelinvoice': u'Avoir',
}


TEMPLATES_URL = 'autonomie:deform_templates/'


MAIN_INFOS_GRID = (
    (('date', 6), ('financial_year', 3), ('prefix', 3), ),
    (('address', 6),),
    (('description', 12),),
    (('workplace', 6), (('mention_ids', 6)),),
    (('course', 12),),
    (('display_units', 12),),
)


def get_customers_from_request(request):
    customers = []
    if request.context.type_ == 'project':
        customers = request.context.customers
    elif request.context.type_ in ('invoice', 'estimation', 'cancelinvoice'):
        if request.context.project is not None:
            customers = request.context.project.company.customers
    return customers


@colander.deferred
def deferred_default_customer(node, kw):
    """
    Return a default customer if there is one in the request GET params or if
    there is only one in the project
    """
    request = kw['request']
    res = 0
    if request.context.type_ == 'project':
        customers = request.context.customers
        if len(customers) == 1:
            res = customers[0].id

    elif request.context.type_ in ('invoice', 'estimation', 'cancelinvoice'):
        res = request.context.customer_id
    return res


@colander.deferred
def deferred_customer_list(node, kw):
    request = kw['request']
    customers = get_customers_from_request(request)
    return deform.widget.SelectWidget(
        values=build_customer_values(customers),
        placeholder=u"Sélectionner un client",
    )


@colander.deferred
def deferred_customer_validator(node, kw):
    request = kw['request']
    customers = get_customers_from_request(request)
    customer_ids = [customer.id for customer in customers]

    def customer_oneof(value):
        if value in ("0", 0):
            return u"Veuillez choisir un client"
        elif value not in customer_ids:
            return u"Entrée invalide"
        return True
    return colander.Function(customer_oneof)


def get_tasktype_from_request(request):
    route_name = request.matched_route.name
    for predicate in ('estimation', 'invoice', 'cancelinvoice'):
        # Matches estimation and estimations
        if route_name in [predicate, "project_%ss" % (predicate,)]:
            return predicate
    else:
        return request.context.type_
    raise Exception(u"You shouldn't have come here with the current route %s"
                    % route_name)


@colander.deferred
def deferred_course_title(node, kw):
    """
        deferred title
    """
    request = kw['request']
    tasktype = get_tasktype_from_request(request)
    if tasktype == "invoice":
        return u"Cette facture concerne-t-elle une formation professionnelle \
continue ?"
    elif tasktype == "cancelinvoice":
        return u"Cet avoir concerne-t-il une formation professionnelle \
continue ?"

    elif tasktype == "estimation":
        return u"Ce devis concerne-t-il une formation professionnelle \
continue ?"


@colander.deferred
def deferred_default_name(node, kw):
    """
    Return a default name for the new document
    """
    request = kw['request']
    tasktype = get_tasktype_from_request(request)
    method = "get_next_{0}_index".format(tasktype)

    if request.context.type_ == 'project':
        # e.g : project.get_next_invoice_number()
        number = getattr(request.context, method)()

        name = TASKTYPES_LABELS[tasktype] + ' %s' % number
    else:
        # Unusefull
        name = request.context.name
    return name


def get_phases_from_request(request):
    """
    Get the phases from the current project regarding request context
    """
    phases = []
    if request.context.type_ == 'project':
        phases = request.context.phases
    elif request.context.type_ in ('invoice', 'cancelinvoice', 'estimation'):
        phases = request.context.project.phases
    return phases


def get_phase_choices(phases):
    """
        Return data structure for phase select options
    """
    return ((phase.id, phase.name) for phase in phases)


@colander.deferred
def deferred_phases_widget(node, kw):
    """
        return phase select widget
    """
    request = kw['request']
    phases = get_phases_from_request(request)
    choices = get_phase_choices(phases)
    wid = deform.widget.SelectWidget(values=choices)
    return wid


@colander.deferred
def deferred_default_phase(node, kw):
    """
    Return the default phase if one is present in the request arguments
    """
    request = kw['request']
    phases = get_phases_from_request(request)
    phase = request.params.get('phase')
    if phase in [str(p.id) for p in phases]:
        return int(phase)
    else:
        return colander.null


def get_projects_from_request(request):
    """
    Return the projects regarding the current request
    """
    company_id = request.current_company
    projects = Project.query().filter_by(company_id=company_id).all()
    return projects


def get_project_choices(projects):
    """
    Return the choices for project selection
    """
    return ((project.id, project.name) for project in projects)


@colander.deferred
def deferred_project_widget(node, kw):
    """
        return phase select widget
    """
    request = kw['request']
    projects = get_projects_from_request(request)
    choices = get_project_choices(projects)
    wid = deform.widget.SelectWidget(values=choices)
    return wid


@colander.deferred
def deferred_default_project(node, kw):
    """
    Return the default project
    """
    res = None
    request = kw['request']
    if request.context.type_ == 'project':
        res = request.context.id
    elif request.context.type_ in ('estimation', 'invoice', 'cancelinvoice'):
        res = request.context.project.id
    return res


class NewTaskSchema(colander.Schema):
    """
    schema used to initialize a new task
    """
    name = colander.SchemaNode(
        colander.String(),
        title=u"Nom du document",
        description=u"Ce nom n'apparaît pas dans le document final",
        validator=colander.Length(max=255),
        default=deferred_default_name,
        missing="",
    )
    customer_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Choix du client",
        widget=deferred_customer_list,
        validator=deferred_customer_validator,
        default=deferred_default_customer,
    )
    project_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Projet dans lequel insérer le document",
        widget=deferred_project_widget,
        default=deferred_default_project
    )
    phase_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Dossier dans lequel insérer le document",
        widget=deferred_phases_widget,
        default=deferred_default_phase
    )
    course = colander.SchemaNode(
        colander.Integer(),
        title=u"Formation",
        label=deferred_course_title,
        widget=deform.widget.CheckboxWidget(true_val="1", false_val="0"),
        missing=0,
    )


def get_new_task_schema():
    """
    Return the schema for adding tasks

    :returns: The schema
    """
    return NewTaskSchema()


class DuplicateSchema(NewTaskSchema):
    """
    schema used to duplicate a task
    """
    pass


def get_duplicate_schema():
    """
    Return the schema for task duplication

    :returns: The schema
    """
    return DuplicateSchema()


#  Dans le formulaire de création de devis par exemple, on trouve
#  aussi bien des TaskLine que des Estimation ou des DiscountLine et leur
#  configuration est imbriquée. On a donc besoin de faire un mapping d'un
#  dictionnaire contenant les modèles {'estimation':..., 'tasklines':...}
#  vers un dictionnaire correspondant au formulaire en place.
# TASK_MATCHING_MAP = (
#     # ('name', 'common'),
#     # ('phase_id', 'common'),
#     ('date', 'common'),
#     ('financial_year', 'common'),
#     ('prefix', 'common'),
#     ('description', 'common'),
#     # ('customer_id', 'common'),
#     ('address', 'common'),
#     ('workplace', 'common'),
#     ('course', 'common'),
#     ('display_units', 'common'),
#     ('expenses_ht', 'lines'),
#     ('exclusions', 'notes'),
#     ('payment_conditions', 'payments'),
#     ('status_comment', 'communication'),
#     ('paymentDisplay', 'payments'),
# )
#
#
# def dbdatas_to_appstruct(dbdatas, matching_map=TASK_MATCHING_MAP):
#     """
#     convert db dict fashionned datas to the appropriate sections
#     to fit the form schema
#     """
#     appstruct = {}
#     for field, section in matching_map:
#         value = dbdatas.get(field)
#         if value is not None:
#             appstruct.setdefault(section, {})[field] = value
#
#     appstruct.setdefault('common', {})['mention_ids'] = [
#         str(a['id']) for a in dbdatas.get('mentions', [])
#     ]
#     return appstruct
#
#
# def appstruct_to_dbdatas(appstruct, matching_map=TASK_MATCHING_MAP):
#     """
#     convert colander deserialized datas to database dbdatas
#     """
#     dbdatas = {'task': {}}
#     task_datas = dbdatas['task']
#     for field, section in matching_map:
#         value = appstruct.get(section, {}).get(field, None)
#         if value not in (None, colander.null):
#             task_datas[field] = value
#
#     task_datas['mentions'] = [
#         TaskMention.get(id) for id in appstruct['common'].get('mention_ids', [])
#     ]
#     return dbdatas
#
#
# def get_lines_block_appstruct(appstruct, dbdatas):
#     """
#     Return the appstruct relatd to the task lines block of the the Task Schema
#
#     the task lines block groups :
#         task lines
#         task lines groups
#         discount lines
#
#     :param dbdatas: Datas coming from the database in dict format
#     """
#     appstruct.setdefault('lines', {})
#
#     for key in ('lines', 'groups', "discounts"):
#         if key in dbdatas:
#             appstruct['lines'][key] = dbdatas[key]
#
#     return appstruct
#
#
# def add_order_to_lines(appstruct):
#     """
#     add the order of the different lines coming from a submitted form
#     """
#     tasklines = appstruct.get('lines', {})
#
#     lines = tasklines.get('lines', [])
#     for index, line in enumerate(lines):
#         line['order'] = index + 1
#
#     groups = tasklines.get('groups', [])
#     for index, group in enumerate(groups):
#         group['order'] = index + 1
#         for jindex, line in enumerate(group.get('lines', [])):
#             line['order'] = jindex + 1
#
#     payment_lines = appstruct.get('payments', {}).get('payment_lines', [])
#     for index, line in enumerate(payment_lines):
#         line['order'] = index + 1
#
#     return appstruct
#
#
# def get_estimation_appstruct(dbdatas):
#     """
#         return EstimationSchema-compatible appstruct
#     """
#     appstruct = dbdatas_to_appstruct(dbdatas)
#
#     if "payment_lines" in dbdatas:
#         appstruct.setdefault('payments', {})['payment_lines'] = \
#             dbdatas['payment_lines']
#     appstruct = get_lines_block_appstruct(appstruct, dbdatas)
#     appstruct = add_payment_block_appstruct(appstruct, dbdatas)
#     appstruct = add_notes_block_appstruct(appstruct, dbdatas)
#     return appstruct
#
#
# def get_estimation_dbdatas(appstruct):
#     """
#         return dict with db compatible datas
#     """
#     dbdatas = appstruct_to_dbdatas(appstruct)
#
#     # Estimation specific keys
#     for key in ('paymentDisplay', 'deposit', ):
#         dbdatas['task'][key] = appstruct['payments'][key]
#     dbdatas.update(appstruct['notes'])
#
#     add_order_to_lines(appstruct)
#     dbdatas['lines'] = appstruct['lines']['lines']
#     dbdatas['groups'] = appstruct['lines']['groups']
#     dbdatas['discounts'] = appstruct['lines']['discounts']
#     dbdatas['payment_lines'] = appstruct['payments']['payment_lines']
#     dbdatas = set_manualDeliverables(appstruct, dbdatas)
#     return dbdatas
#
#
# def get_invoice_appstruct(dbdatas):
#     """
#         return InvoiceSchema compatible appstruct
#     """
#     appstruct = dbdatas_to_appstruct(dbdatas)
#     appstruct = get_lines_block_appstruct(appstruct, dbdatas)
#     return appstruct
#
#
# def get_invoice_dbdatas(appstruct):
#     """
#         return dict with db compatible datas
#     """
#     dbdatas = appstruct_to_dbdatas(appstruct)
#
#     add_order_to_lines(appstruct)
#     dbdatas['lines'] = appstruct['lines']['lines']
#     dbdatas['groups'] = appstruct['lines']['groups']
#     dbdatas['discounts'] = appstruct['lines']['discounts']
#     return dbdatas
#
#
# def get_cancel_invoice_appstruct(dbdatas):
#     """
#         return cancel invoice schema compatible appstruct
#     """
#     appstruct = dbdatas_to_appstruct(dbdatas)
#     appstruct = get_lines_block_appstruct(appstruct, dbdatas)
#     return appstruct
#
#
# def get_cancel_invoice_dbdatas(appstruct):
#     """
#         return dict with db compatible datas
#     """
#     dbdatas = appstruct_to_dbdatas(appstruct)
#
#     add_order_to_lines(appstruct)
#     dbdatas['lines'] = appstruct['lines']['lines']
#     dbdatas['groups'] = appstruct['lines']['groups']
#     return dbdatas
#
#
# def set_manualDeliverables(appstruct, dbdatas):
#     """
#         Hack the dbdatas to set the manualDeliverables value
#     """
#     # On s'assure que la clé task existe et on set le manualDeliverables par
#     # défaut
#     dbdatas.setdefault('task', {})['manualDeliverables'] = 0
#
#     # dans l'interface payment_times == -1 correspond à Configuration Manuelle
#     # des paiements
#     payment_times = appstruct.get('payments', {}).get('payment_times')
#     if payment_times == -1:
#         dbdatas['task']['manualDeliverables'] = 1
#     return dbdatas
#
#
# def add_payment_block_appstruct(appstruct, dbdatas):
#     """
#         Hack the appstruct to set the payment informations values
#     """
#     if dbdatas.get('manualDeliverables') == 1:
#         # dans l'interface payment_times == -1 correspond à Configuration
#         # Manuelle des paiements
#         appstruct.setdefault('payments', {})['payment_times'] = -1
#     else:
#         appstruct.setdefault(
#             'payments', {}
#         )['payment_times'] = max(1, len(dbdatas.get('payment_lines')))
#
#     appstruct['payments']['paymentDisplay'] = dbdatas['paymentDisplay']
#     appstruct['payments']['deposit'] = dbdatas['deposit']
#     return appstruct
#
#
# def add_notes_block_appstruct(appstruct, dbdatas):
#     """
#     Fill the notes block
#     """
#     appstruct.setdefault(
#         'notes', {
#         })['exclusions'] = dbdatas.get('exclusions', '')
#     return appstruct
