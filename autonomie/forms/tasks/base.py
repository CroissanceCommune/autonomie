# -*- coding: utf-8 -*-
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

    phase, displayUnits
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
from autonomie.forms.customer import customer_choice_node_factory


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
    (('date', 6), ('financial_year', 3), ),
    (('address', 6),),
    (('description', 12),),
    (('workplace', 6), (('mention_ids', 6)),),
    (('display_units', 12),),
)


# NEW TASK SCHEMA
# 1 - Project is current context : OK
# 2 - Duplication : Task is current context
# 3 - Customer is current context
def _get_tasktype_from_request(request):
    route_name = request.matched_route.name
    result = request.context.type_
    for predicate in ('estimation', 'cancelinvoice', 'invoice'):
        # Matches estimation and estimations
        if predicate in route_name:
            result = predicate
            break
    return result


@colander.deferred
def deferred_default_name(node, kw):
    """
    Return a default name for the new document
    """
    request = kw['request']
    tasktype = _get_tasktype_from_request(request)
    method = "get_next_{0}_index".format(tasktype)

    if request.context.type_ == 'project':
        # e.g : project.get_next_invoice_number()
        number = getattr(request.context, method)()

        name = TASKTYPES_LABELS[tasktype] + ' %s' % number
    else:
        # Unusefull
        name = request.context.name
    return name


def _get_project_customers(project):
    """
    Return project customers

    :param obj project: The current project
    :returns: A list of Customer instances
    :rtype: list
    """
    query = Customer.label_query()
    customers = query.filter(Customer.projects.any(Project.id == project.id))
    return customers


def _get_company_customers(context):
    """
    Return company customers

    :param obj context: The current Pyramid context
    :returns: A list of Customer instances
    :rtype: list
    """
    company_id = context.get_company_id()
    customers = Customer.label_query()
    customers = customers.filter_by(company_id=company_id).all()

    if hasattr(context, "project_id"):
        # Si le contexte est attaché à un projet, on s'assure que les clients du
        # projet sont présentés en haut de la liste des clients en utilisant une
        # fonction de tri custom

        project_id = context.project_id

        def sort_pid_first(a, b):
            """
            Sort customers moving the customers belonging to the current project
            up in the list
            """
            if project_id in a.get_project_ids():
                return -1
            elif project_id in b.get_project_ids():
                return 1
            else:
                return 0

        customers = sorted(customers, cmp=sort_pid_first)
    return customers


def _get_customers_options(request):
    """
    Retrieve customers that should be presented to the end user

    Regarding the context we return :

        company customers
        project customers
    """
    context = request.context

    if isinstance(context, Project):
        customers = _get_project_customers(context)
    else:
        customers = _get_company_customers(context)

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


def _get_project_choices(projects):
    """
    Format project list to select options

    :param list projects: Project instances
    :returns: A list of 2-uple (id, label)
    :rtype: list
    """
    return [(project.id, project.name) for project in projects]


@colander.deferred
def deferred_project_widget(node, kw):
    """
        return phase select widget
    """
    if isinstance(kw['request'].context, Project):
        wid = deform.widget.HiddenWidget()
    else:
        customer_id = deferred_default_customer(node, kw)

        if customer_id != 0:
            projects = Project.get_customer_projects(customer_id)
        else:
            projects = []

        choices = _get_project_choices(projects)
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


def _get_phases_from_request(request):
    """
    Get the phases from the current project regarding request context
    """
    phases = []
    if request.context.type_ == 'project':
        phases = request.context.phases
    elif request.context.type_ in ('invoice', 'cancelinvoice', 'estimation'):
        phases = request.context.project.phases
    return phases


def _get_phase_choices(phases):
    """
        Return data structure for phase select options
    """
    return [(phase.id, phase.name) for phase in phases]


@colander.deferred
def deferred_phases_widget(node, kw):
    """
        return phase select widget
    """
    request = kw['request']
    phases = _get_phases_from_request(request)

    choices = _get_phase_choices(phases)
    choices.insert(1, ("", u"Aucun sous-dossier"))
    wid = deform.widget.SelectWidget(values=choices)
    return wid


@colander.deferred
def deferred_default_phase(node, kw):
    """
    Return the default phase if one is present in the request arguments
    """
    request = kw['request']
    phases = _get_phases_from_request(request)
    phase = request.params.get('phase')
    if phase in [str(p.id) for p in phases]:
        logger.debug("Found the current phase : %s" % phase)
        return int(phase)
    else:
        return colander.null


def get_business_types_from_request(request):
    """
    Collect available business types allowed for the current user/context

    :param obj request: The current Pyramid request
    """
    context = request.context
    if isinstance(context, Project):
        project = context
    elif hasattr(context, "project"):
        project = context.project
    else:
        return []

    result = []
    if project.project_type.default_business_type:
        result.append(project.project_type.default_business_type)

    for business_type in project.business_types:
        if business_type.allowed(request):
            result.append(business_type)
    return result


@colander.deferred
def business_type_id_validator(node, kw):
    allowed_ids = [
        i.id
        for i in get_business_types_from_request(kw['request'])
    ]
    return colander.OneOf(allowed_ids)


@colander.deferred
def deferred_business_type_description(node, kw):
    request = kw['request']
    business_types = get_business_types_from_request(request)
    if len(business_types) == 1:
        return ""
    else:
        return u"Type d'affaire",


@colander.deferred
def deferred_business_type_widget(node, kw):
    """
    Collect the widget to display for business type selection

    :param node: The node we affect the widget to
    :param dict kw: The colander schema binding dict
    :returns: A SelectWidget or an hidden one
    """
    request = kw['request']
    business_types = get_business_types_from_request(request)
    if len(business_types) == 0:
        return deform.widget.HiddenWidget()
    else:
        return deform.widget.SelectWidget(
            values=[
                (business_type.id, business_type.label)
                for business_type in business_types
            ]
        )


@colander.deferred
def deferred_business_type_default(node, kw):
    """
    Collect the default value to present to the end user
    """
    request = kw['request']
    project = request.context
    context = request.context
    if isinstance(context, Project):
        project = context
    elif hasattr(context, "project"):
        project = context.project
    else:
        raise KeyError(
            u"No project could be found starting from current : %s" % (
                context,
            )
        )

    if project.project_type.default_business_type:
        return project.project_type.default_business_type.id
    else:
        return get_business_types_from_request(request)[0].id


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
    customer_id = customer_choice_node_factory(
        default=deferred_default_customer,
        query_func=_get_customers_options,
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
        default=deferred_default_phase,
        missing=colander.drop,
    )
    business_type_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Type d'affaire",
        widget=deferred_business_type_widget,
        default=deferred_business_type_default,
    )


@colander.deferred
def deferred_customer_project_widget(node, kw):
    request = kw['request']
    projects = request.context.customer.projects
    logger.debug("### Getting the projects")
    choices = _get_project_choices(projects)
    wid = deform.widget.SelectWidget(values=choices)
    return wid


def _get_customers_from_request(request):
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


def validate_customer_project_phase(form, value):
    """
    Validate that customer project and phase are linked

    :param obj form: The form object
    :param dict value: The submitted values
    """
    customer_id = value['customer_id']
    project_id = value['project_id']
    phase_id = value.get('phase_id')

    if phase_id and not Project.check_phase_id(project_id, phase_id):
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
    schema['customer_id'].widget = deform.widget.HiddenWidget()
    schema['project_id'].widget = deferred_customer_project_widget
    schema['project_id'].title = u"Projet vers lequel déplacer ce document"
    schema['phase_id'].title = u"Dossier dans lequel déplacer ce document"
    del schema['business_type_id']
    schema.after_bind = add_date_field_after_bind
    return schema


class DuplicateSchema(NewTaskSchema):
    """
    schema used to duplicate a task
    """
    customer_id = customer_choice_node_factory(
        query_func=_get_customers_options,
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


def task_after_bind(node, kw):
    """
    After bind methods passed to the task schema

    Remove fields not allowed for edition

    :param obj node: The SchemaNode concerning the Task
    :param dict kw: The bind arguments
    """
    if not has_set_treasury_perm(kw):
        remove_childnode(node, 'financial_year')
