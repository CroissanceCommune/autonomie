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
    Project,
)
from autonomie.models.task import (
    Task,
    TaskLine,
    TaskLineGroup,
)
from autonomie.models.customer import Customer
from autonomie.forms import today_node
from autonomie.forms.customer import get_customer_select_node


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


MAIN_INFOS_GRID = (
    (('date', 6), ('financial_year', 3), ('prefix', 3), ),
    (('address', 6),),
    (('description', 12),),
    (('workplace', 6), (('mention_ids', 6)),),
    (('course', 12),),
    (('display_units', 12),),
)


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


def get_customers_from_request(request):
    """
    Get customers options for new task and task duplicate form

    Find customers regarding the current context

    Project -> Project.customers
    ...

    :returns: A list of customers
    :rtype: list
    """
    customers = []
    context = request.context

    if isinstance(context, Project):
        customers = context.customers

    elif isinstance(context, Task):
        customers = [context.customer]

    elif isinstance(context, Customer):
        customers = [context]

    elif hasattr(context, 'project') and context.project is not None:
        customers = context.project.customers

    else:
        company_id = request.current_company
        customers = Customer.label_query()
        customers.filter_by(company_id=company_id).all()

    return customers


def get_company_customers(request):
    """
    Retrieve all customers attached to a context's company
    """
    company_id = request.context.get_company_id()
    customers = Customer.label_query()
    customers = customers.filter_by(company_id=company_id).all()
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


@colander.deferred
def deferred_company_customer_validator(node, kw):
    customers = get_company_customers(kw)
    customer_ids = [customer.id for customer in customers]

    def customer_oneof(value):
        if value not in customer_ids:
            return u"Entrée invalide"
        else:
            return True
    return colander.Function(customer_oneof)


def get_tasktype_from_request(request):
    route_name = request.matched_route.name
    result = request.context.type_
    for predicate in ('estimation', 'cancelinvoice', 'invoice'):
        # Matches estimation and estimations
        if predicate in route_name:
            result = predicate
            break
    return result


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
def deferred_customer_project_widget(node, kw):
    request = kw['request']
    projects = request.context.customer.projects
    logger.debug("### Getting the projects")
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
    customer_id = get_customer_select_node(
        title=u"Choix du client",
        default=deferred_default_customer,
        query_func=get_company_customers,
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


def validate_customer_project_phase(form, value):
    """
    Validate that customer project and phase are linked

    :param obj form: The form object
    :param dict value: The submitted values
    """
    customer_id = value['customer_id']
    project_id = value['project_id']
    phase_id = value['phase_id']

    if not Project.check_phase_id(project_id, phase_id):
        exc = colander.Invalid(form, u"Projet et dossier ne correspondent pas")
        exc['phase_id'] = u"Ne correspond pas au projet ci-dessus"
        raise exc
    if not Customer.check_project_id(customer_id, project_id):
        exc = colander.Invalid(form, u"Client et projet ne correspondent pas")
        exc['project_id'] = u"Ne correspond pas au client ci-dessus"
        raise exc


def get_new_task_schema():
    """
    Return the schema for adding tasks

    :returns: The schema
    """
    return NewTaskSchema(validator=validate_customer_project_phase)


def add_date_field_after_bind(schema, kw):
    """
    Add a date edition field if the current user has the appropriate rights
    """
    req = kw['request']
    ctx_type = req.context.__name__
    if req.has_permission('set_date.%s' % ctx_type):
        schema.add(
            today_node(
                default=req.context.date,
                name='date',
            )
        )


def get_task_metadatas_edit_schema():
    """
    Return the schema for editing tasks metadatas

    :returns: The schema
    """
    schema = NewTaskSchema().clone()
    del schema['course']
    schema['customer_id'].widget = deform.widget.HiddenWidget()
    schema['project_id'].widget = deferred_customer_project_widget
    schema['project_id'].title = u"Projet vers lequel déplacer ce document"
    schema['phase_id'].title = u"Dossier dans lequel déplacer ce document"
    schema.after_bind = add_date_field_after_bind
    return schema


class DuplicateSchema(NewTaskSchema):
    """
    schema used to duplicate a task
    """
    customer_id = get_customer_select_node(
        title=u"Choix du client",
        query_func=get_company_customers,
        default=deferred_default_customer,
    )


def get_duplicate_schema():
    """
    Return the schema for task duplication

    :returns: The schema
    """
    return DuplicateSchema(validator=validate_customer_project_phase)


def get_task_from_context(context):
    """
    Return the current task from the given context

    :param obj context: Instance of Task/TaskLine/TaskLineGroup
    :returns: The associated Task object
    """
    result = context
    if isinstance(context, (TaskLine, TaskLineGroup)):
        result = context.task
    return result


def remove_childnode(node, child_node_name):
    """
    Remove a schema childnode
    """
    if child_node_name in node:
        del node[child_node_name]


def has_set_treasury_perm(kw):
    """
    Return True if the current user has set_treasury perms on the current
    context
    :param dict kw: The bind keyword arguments
    """
    result = True
    request = kw.get('request')
    if request is None:
        result = False
    else:
        task = get_task_from_context(request.context)
        if task is None:
            result = False
        else:
            perm = 'set_treasury.%s' % task.type_
            result = request.has_permission(perm)

    return result


def taskline_after_bind(node, kw):
    """
    After bind method to pass to The tasklines fields

    Remove fields not allowed for edition

    :param obj node: The SchemaNode concerning the TaskLine
    :param dict kw: The bind arguments
    """
    if not has_set_treasury_perm(kw):
        remove_childnode(node, 'product_id')


def task_after_bind(node, kw):
    """
    After bind methods passed to the task schema

    Remove fields not allowed for edition

    :param obj node: The SchemaNode concerning the Task
    :param dict kw: The bind arguments
    """
    if not has_set_treasury_perm(kw):
        remove_childnode(node, 'prefix')
        remove_childnode(node, 'financial_year')
