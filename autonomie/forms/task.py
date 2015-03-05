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
import datetime

import colander
import deform

from deform_extensions import (
    DisabledInput,
    GridMappingWidget,
)
from autonomie import forms
from autonomie.models.task.invoice import PaymentMode
from autonomie.models.task import WorkUnit
from autonomie.models.tva import (
    Tva,
    Product,
)
from .custom_types import (
    QuantityType,
    AmountType,
    Integer,
)


log = logging.getLogger(__name__)
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


PAYMENTDISPLAYCHOICES = (
        ('NONE', u"Les paiments ne sont pas affichés dans le PDF",),
        ('SUMMARY', u"Le résumé des paiements apparaît dans le PDF",),
        ('ALL', u"Le détail des paiements apparaît dans le PDF",),)


TEMPLATES_URL = 'autonomie:deform_templates/'


MAIN_INFOS_GRID = (
    (('name', 6), ('phase_id', 6),),
    (('taskDate', 6), ('financial_year', 6),),
    (('customer_id', 6), ('address', 6),),
    (('description', 12),),
    (('course', 12),),
    (('displayedUnits', 12),),
)


def get_percents():
    """
        Return percents for select widget
    """
    percent_options = [(0, 'Aucun'), (5, '5%')]
    for i in range(10, 110, 10):
        percent_options.append((i, "%d %%" % i))
    return percent_options


def get_payment_times():
    """
        Return options for payment times select
    """
    payment_times = [(-1, u'Configuration manuelle')]
    for i in range(1, 12):
        payment_times.append((i, '%d fois' % i))
    return payment_times


@colander.deferred
def deferred_default_year(node, kw):
    """
        Return the current year
    """
    return datetime.date.today().year


def build_customer_value(customer=None):
    """
        return the tuple for building customer select
    """
    if customer:
        return (str(customer.id), customer.name)
    else:
        return ("0", u"Sélectionner un client")


def build_customer_values(customers):
    """
        Build human understandable customer labels
        allowing efficient discrimination
    """
    options = [build_customer_value()]
    options.extend([build_customer_value(customer)
                            for customer in customers])
    return options


def get_customers_from_request(request):
    customers = []
    if request.context.__name__ == 'project':
        customers = request.context.customers
    elif request.context.__name__ in ('invoice', 'estimation', 'cancelinvoice'):
        if request.context.project is not None:
            customers = request.context.project.customers
    return customers


@colander.deferred
def deferred_customer_list(node, kw):
    request = kw['request']
    customers = get_customers_from_request(request)
    return deform.widget.Select2Widget(
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
    raise Exception(u"You shouldn't have come here with the current route %s"\
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


def get_tva_choices():
    """
        Return data structure for tva select widget options
    """
    return [(unicode(tva.value), tva.name)for tva in Tva.query()]


def get_product_choices():
    """
        Return data structure for product code select widget options
    """
    return [(p.id, u"{0} ({1})".format(p.name, p.compte_cg),)\
            for p in Product.query()]


def get_unities():
    unities =  ["",]
    unities.extend([workunit.label  for workunit in WorkUnit.query()])
    return unities


@colander.deferred
def deferred_unity_widget(node, kw):
    unities = get_unities()
    return deform.widget.SelectWidget(values=zip(unities, unities))


def _is_in(datas):
    def func(value):
        return value in datas
    return func


@colander.deferred
def deferred_unity_validator(node, kw):
    return colander.Function(_is_in(get_unities()))


@colander.deferred
def deferred_tva_validator(node, kw):
    options = [int(option[0]) for option in get_tva_choices()]
    return colander.Function(_is_in(options))


@colander.deferred
def deferred_product_validator(node, kw):
    options = [option[0] for option in get_product_choices()]
    return colander.Function(_is_in(options))


@colander.deferred
def deferred_financial_year_widget(node, kw):
    request = kw['request']
    if request.user.is_admin() or request.user.is_manager():
        return deform.widget.TextInputWidget(mask='9999')
    else:
        return deform.widget.HiddenWidget()


@colander.deferred
def deferred_tvas_widget(node, kw):
    """
        return a tva widget
    """
    tvas = get_tva_choices()
    wid = deform.widget.SelectWidget(values=tvas)
    return wid


@colander.deferred
def deferred_product_widget(node, kw):
    """
        return a widget for product selection
    """
    products = get_product_choices()
    wid = deform.widget.SelectWidget(values=products)
    return wid


@colander.deferred
def deferred_default_tva(node, kw):
    """
        return a tva widget
    """
    default_tva = Tva.get_default()
    if default_tva is not None:
        return unicode(default_tva.value)
    else:
        return colander.null


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


def get_phase_choices(phases):
    """
        Return data structure for phase select options
    """
    return ((phase.id, phase.name) for phase in phases)


def get_phases_from_request(request):
    """
        Get the phases from the current project regarding request context
    """
    phases = []
    if request.context.__name__ == 'project':
        phases = request.context.phases
    elif request.context.__name__ in ('invoice', 'cancelinvoice', 'estimation'):
        phases = request.context.project.phases
    return phases

@colander.deferred
def deferred_default_name(node, kw):
    """
    Return a default name for the new document
    """
    request = kw['request']
    tasktype = get_tasktype_from_request(request)
    method = "get_next_{0}_number".format(tasktype)

    if request.context.__name__ == 'project':
        # e.g : project.get_next_invoice_number()
        number = getattr(request.context, method)()

        name = TASKTYPES_LABELS[tasktype] + ' %s' % number
    else:
        # Unusefull
        name = request.context.name
    return name


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


class TaskLine(colander.MappingSchema):
    """
        A single estimation line
    """
    description = forms.textarea_node(
        missing=u'',
        richwidget=True,
        css_class='col-md-3',
    )
    cost = colander.SchemaNode(
        AmountType(),
        widget=deform.widget.TextInputWidget(),
        validator=forms.positive_validator,
        css_class='col-md-1')
    quantity = colander.SchemaNode(
        QuantityType(),
        widget=deform.widget.TextInputWidget(),
        validator=forms.positive_validator,
        css_class='col-md-1')
    unity = colander.SchemaNode(
        colander.String(),
        widget=deferred_unity_widget,
        validator=deferred_unity_validator,
        missing=u"",
        css_class='col-md-2')
    tva = colander.SchemaNode(
        Integer(),
        widget=deferred_tvas_widget,
        default=deferred_default_tva,
        validator=deferred_tva_validator,
        css_class='col-md-1',
        title=u'TVA')
    product_id = colander.SchemaNode(
        colander.Integer(),
        widget=deferred_product_widget,
        validator=deferred_product_validator,
        missing="",
        css_class="col-md-2",
        title=u"Code produit",
    )


class DiscountLine(colander.MappingSchema):
    """
        A single estimation line
    """
    description = forms.textarea_node(
        missing=u'',
        richwidget=True,
        css_class='col-md-4',
    )
    amount = colander.SchemaNode(
        AmountType(),
        widget=deform.widget.TextInputWidget(),
        css_class='col-md-1',
        validator=forms.positive_validator,
    )
    tva = colander.SchemaNode(
        Integer(),
        widget=deferred_tvas_widget,
        default=deferred_default_tva,
        css_class='col-md-2 col-md-offset-3',
        title=u'TVA',
    )


class TaskLines(colander.SequenceSchema):
    """
        Sequence of task lines
    """
    taskline = TaskLine(
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + 'inline_mapping.pt',
            item_template=TEMPLATES_URL + 'inline_mapping_item.pt',
            item_css_class="taskline",
        )
    )


class DiscountLines(colander.SequenceSchema):
    """
        Sequence of discount lines
    """
    discountline = DiscountLine(
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + 'inline_mapping.pt',
            item_template=TEMPLATES_URL + 'inline_mapping_item.pt',
            item_css_class="discountline",
        ),
    )


class TaskLinesBlock(colander.MappingSchema):
    """
        Fieldset containing the "Détail de la prestation" block
        with estimation and invoice lines and all the stuff
    """
    lines = TaskLines(
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + 'tasklines_sequence.pt',
            orderable=True,
            min_len=1,
            add_subitem_text_template=u"Ajouter une ligne",
        ),
        title=u'',
    )
    discounts = DiscountLines(
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + 'discountlines_sequence.pt',
            orderable=True,
            add_subitem_text_template=u"Ajouter une remise",
        ),
        title=u'',
    )
    expenses_ht = colander.SchemaNode(
        AmountType(),
        widget=deform.widget.TextInputWidget(
            template=TEMPLATES_URL + 'wrappable_input.pt'
        ),
        title=u"Frais forfaitaires (HT)",
        missing=0,
        validator=forms.positive_validator,
    )

    default_tva = colander.SchemaNode(
        colander.Integer(),
        title=u"",
        widget=deform.widget.HiddenWidget(),
        default=deferred_default_tva,
    )
    expenses = colander.SchemaNode(
        AmountType(),
        widget=deform.widget.TextInputWidget(
            template=TEMPLATES_URL + 'wrappable_input.pt',
            before=TEMPLATES_URL + 'tvalist.pt',
            before_options={'label': u'Montant TVA', 'id': 'tvapart'},
            after=TEMPLATES_URL + 'staticinput.pt',
            after_options={'label': u'Total TTC', 'id': 'total'}
        ),
        title=u'Frais Réel (TTC)',
        missing=0,
        validator=forms.positive_validator,
    )


class TaskConfiguration(colander.MappingSchema):
    """
        Main fields to be configured
    """
    name = colander.SchemaNode(
        colander.String(),
        title=u"Libellé du document",
        validator=colander.Length(max=255),
        default=deferred_default_name,
        missing="",
        )
    customer_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Choix du client",
        widget=deferred_customer_list,
        validator=deferred_customer_validator
        )
    address = forms.textarea_node(
        title=u"Nom et adresse du client",
        widget_options={'rows':4}
    )
    phase_id = colander.SchemaNode(
        colander.String(),
        title=u"Phase où insérer le devis",
        widget=deferred_phases_widget,
        default=deferred_default_phase
        )
    taskDate = forms.today_node(title=u"Date du devis")
    description = forms.textarea_node(title=u"Objet du devis")
    course = colander.SchemaNode(
        colander.Integer(),
        title=u"",
        label=deferred_course_title,
        widget=deform.widget.CheckboxWidget(true_val="1", false_val="0"),
        missing=0,
    )
    displayedUnits = colander.SchemaNode(
        colander.Integer(),
        title="",
        label=u"Afficher le détail des prestations dans la sortie PDF ?",
        widget=deform.widget.CheckboxWidget(true_val="1", false_val="0"),
        missing=0,
    )


class TaskNotes(colander.MappingSchema):
    """
        Notes
    """
    exclusions = forms.textarea_node(
        title=u'Notes',
        missing=u"",
        description=u"Note complémentaires concernant les prestations décrites"
    )


class TaskCommunication(colander.MappingSchema):
    """
        Communication avec la CAE
    """
    statusComment = forms.textarea_node(
        title=u'',
        missing=u'',
        description=u"Message à destination des membres de la CAE qui \
valideront votre document (n'apparaît pas dans le PDF)",
    )


class TaskSchema(colander.MappingSchema):
    """
        colander base Schema for task edition
    """
    common = TaskConfiguration(
        title=u"",
        widget=GridMappingWidget(named_grid=MAIN_INFOS_GRID),
    )
    lines = TaskLinesBlock(
        title=u"Détail des prestations",
        widget=deform.widget.MappingWidget(
            item_template=TEMPLATES_URL + 'taskdetails_mapping_item.pt'
        )
    )


def remove_admin_fields(schema, kw):
    doctype = schema['lines']['lines'].doctype
    if kw['request'].user.is_contractor():
        # Non admin users doesn't edit products
        if doctype != 'estimation':
            del schema['lines']['lines']['taskline']['product_id']
        schema['lines']['lines'].is_admin = False
        schema['lines']['lines']['taskline']['description'].css_class = 'col-md-4'
        schema['lines']['lines']['taskline']['tva'].css_class = 'col-md-2'
    else:
        schema['lines']['lines'].is_admin = True
        if doctype != 'estimation':
            schema['lines']['lines']['taskline']['description'].css_class = 'col-md-3'
            schema['lines']['lines']['taskline']['tva'].css_class = 'col-md-1'
        else:
            schema['lines']['lines']['taskline']['description'].css_class = 'col-md-4'
            schema['lines']['lines']['taskline']['tva'].css_class = 'col-md-2'


TASKSCHEMA = TaskSchema(after_bind=remove_admin_fields)


class EstimationPaymentLine(colander.MappingSchema):
    """
        Payment line
    """
    description = colander.SchemaNode(
        colander.String(),
        default=u"Solde",
    )
    paymentDate = forms.today_node()
    amount = colander.SchemaNode(AmountType(), default=0)


class EstimationPaymentLines(colander.SequenceSchema):
    """
        Sequence of payment lines
    """
    line = EstimationPaymentLine(
        widget=deform.widget.MappingWidget()
#            template=TEMPLATES_URL + 'paymentline_mapping.mako',
#            item_template=TEMPLATES_URL + 'paymentline_mapping_item.mako')
    )


class EstimationPayments(colander.MappingSchema):
    """
        Gestion des acomptes
    """
    deposit = colander.SchemaNode(
        colander.Integer(),
        title=u"Acompte à la commande",
        default=0,
        widget=deform.widget.SelectWidget(
            values=get_percents(),
            css_class='col-md-2')
    )
    payment_times = colander.SchemaNode(
        colander.Integer(),
        title=u"Paiement en ",
        default=1,
        widget=deform.widget.SelectWidget(values=get_payment_times(),
                                     css_class='col-md-2')
    )
    paymentDisplay = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf([x[0] for x in PAYMENTDISPLAYCHOICES]),
        widget=deform.widget.RadioChoiceWidget(values=PAYMENTDISPLAYCHOICES),
        title=u"Affichage des paiements",
        default="SUMMARY")
    payment_lines = EstimationPaymentLines(
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + 'paymentlines_sequence.pt',
            item_template=TEMPLATES_URL + 'paymentlines_sequence_item.pt',
            min_len=1),
        title=u'',
        description=u"Définissez les échéances de paiement")
    paymentConditions = forms.textarea_node(title=u"Conditions de paiement")


class InvoicePayments(colander.MappingSchema):
    """
        Conditions de paiement de la facture
    """
    paymentConditions = forms.textarea_node(title="")


def get_estimation_schema():
    """
        Return the schema for estimation add/edit
    """
    schema = TASKSCHEMA.clone()
    schema['lines']['lines'].doctype = "estimation"
    tmpl = 'autonomie:deform_templates/paymentdetails_item.pt'
    schema.add(TaskNotes(title=u"Notes", name="notes"))
    schema.add(
        EstimationPayments(title=u'Conditions de paiement',
                           widget=deform.widget.MappingWidget(
                               item_template=tmpl
                           ),
                           name='payments')
    )
    schema.add(
        TaskCommunication(title=u'Communication Entrepreneur/CAE',
                          name='communication')
    )
    del schema['lines']['lines']['taskline']['product_id']
    return schema


FINANCIAL_YEAR = colander.SchemaNode(colander.Integer(),
        name="financial_year", title=u"Année comptable de référence",
        widget=deferred_financial_year_widget,
        default=deferred_default_year)


def get_invoice_schema():
    """
        Return the schema for invoice add/edit
    """
    schema = TASKSCHEMA.clone()
    schema['lines']['lines'].doctype = "invoice"
    title = u"Phase où insérer la facture"
    schema['common']['phase_id'].title = title
    # Ref #689
    schema['common'].add_before('description', FINANCIAL_YEAR)
    title = u"Date de la facture"
    schema['common']['taskDate'].title = title
    title = u"Objet de la facture"
    schema['common']['description'].title = title
    title = u"Conditions de paiement"
    schema.add(InvoicePayments(title=title, name='payments'))
    schema.add(
        TaskCommunication(title=u'Communication Entrepreneur/CAE',
                          name='communication')
    )
    return schema


def get_cancel_invoice_schema():
    """
        return the cancel invoice form schema
    """
    schema = TASKSCHEMA.clone()
    schema['lines']['lines'].doctype = "taskschema"
    title = u"Phase où insérer l'avoir"
    schema['common']['phase_id'].title = title
    # Ref #689
    schema['common'].add_before('description', FINANCIAL_YEAR)
    title = u"Date de l'avoir"
    schema['common']['taskDate'].title = title
    title = u"Objet de l'avoir"
    schema['common']['description'].title = title
    del schema['common']['course']
    title = u"Conditions de remboursement"
    del schema['lines']['discounts']
    payments = InvoicePayments(title=title, name='payments').clone()
    payments['paymentConditions'].title = title
    payments['paymentConditions'].description = u""

    schema['lines']['expenses_ht'].validator = forms.negative_validator
    schema['lines']['expenses'].validator = forms.negative_validator
    # cancelinvoice costs can both be positive or negative paiments and
    # discounts
    schema['lines']['lines']['taskline']['cost'].validator = None

    schema.add(payments)
    return schema


def get_amount_topay(kw):
    """
    Retrieve the amount to be paid regarding the context
    """
    context = kw['request'].context
    if context.__name__ == 'invoice':
        task = context
        topay = task.topay()
    else:
        task = context.task
        topay = task.topay()
        topay += context.amount
    return topay


@colander.deferred
def deferred_amount_default(node, kw):
    """
        default value for the payment amount
    """
    return get_amount_topay(kw)


@colander.deferred
def deferred_total_validator(node, kw):
    """
        validate the amount to keep the sum under the total
    """
    topay = get_amount_topay(kw)
    max_msg = u"Le montant ne doit pas dépasser %s (total ttc - somme \
des paiements + montant d'un éventuel avoir)" % (topay / 100.0)
    min_msg = u"Le montant doit être positif"
    return colander.Range(
        min=0, max=topay, min_err=min_msg, max_err=max_msg,
    )


@colander.deferred
def deferred_payment_mode_widget(node, kw):
    """
        dynamically retrieves the payment modes
    """
    modes = [(mode.label, mode.label) for mode in PaymentMode.query()]
    return deform.widget.SelectWidget(values=modes)


@colander.deferred
def deferred_payment_mode_validator(node, kw):
    return colander.OneOf([mode.label for mode in PaymentMode.query()])


class PaymentSchema(colander.MappingSchema):
    """
        colander schema for payment recording
    """
    come_from = forms.come_from_node()
    amount = colander.SchemaNode(AmountType(),
        title=u"Montant",
        validator=deferred_total_validator,
        default=deferred_amount_default)
    mode = colander.SchemaNode(colander.String(),
        title=u"Mode de paiement",
        widget=deferred_payment_mode_widget,
        validator=deferred_payment_mode_validator)
    resulted = colander.SchemaNode(
        colander.Boolean(),
        title=u"Soldé",
        description="""Indique que le document est soldé (
ne recevra plus de paiement), si le montant indiqué correspond au
montant de la facture celle-ci est soldée automatiquement""",
        default=False)


class FinancialYearSchema(colander.MappingSchema):
    """
        colander Schema for financial year setting
    """
    financial_year = FINANCIAL_YEAR


class ProductTaskLine(colander.MappingSchema):
    """
        A single estimation line
    """
    id = colander.SchemaNode(
            colander.Integer(),
            widget=deform.widget.HiddenWidget(),
            missing=u"",
            css_class="span0")
    description = colander.SchemaNode(
        colander.String(),
        widget=DisabledInput(),
         missing=u'',
         css_class='col-md-3')
    tva = colander.SchemaNode(
        AmountType(),
        widget=DisabledInput(),
        css_class='col-md-1',
        title=u'TVA')
    product_id = colander.SchemaNode(
            colander.Integer(),
            widget=deferred_product_widget,
            validator=deferred_product_validator,
            missing="",
            css_class="col-md-2",
            title=u"Code produit")


class ProductTaskLines(colander.SequenceSchema):
    taskline = ProductTaskLine(missing="", title=u"")


class SetProductsSchema(colander.MappingSchema):
    """
        Form schema used to configure Products
    """
    lines = ProductTaskLines(
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + 'product_tasklines.pt',
            item_template=TEMPLATES_URL + 'product_tasklines_item.pt',
            min_len=1),
        missing="",
        title=u'')


#  Mapper tools used to move from dbdatas format to an appstruct fitting the
#  form schema.
#  Dans le formulaire de création de devis par exemple, on trouve
#  aussi bien des TaskLine que des Estimation ou des DiscountLine et leur
#  configuration est imbriquée. On a donc besoin de faire un mapping d'un
#  dictionnaire contenant les modèles {'estimation':..., 'tasklines':...}
#  vers un dictionnaire correspondant au formulaire en place.


class MappingWrapper:
    """
        Allows moving from one dict to another
        allowing to map databases models and colander Mapping schemas
        when db datas are dispatched through different mapping schemas
        @param matching_map: matching_map as (
                                  (field, colanderschemaname,multi_boolean),
                                                                ...)
        @param dbtype: internal dbtype name (like 'estimation', 'task' ...)
                        corresponding to a database table
    """
    matching_map = None
    dbtype = None

    def toschema(self, dbdatas, appstruct):
        """
            convert db dict fashionned datas to the appropriate sections
            to fit the EstimationSchema
        """
        for field, section in self.matching_map:
            value = dbdatas.get(self.dbtype, {}).get(field)
            if value is not None:
                appstruct.setdefault(section, {})[field] = value
        return appstruct

    def todb(self, appstruct, dbdatas):
        """
            convert colander deserialized datas to database dbdatas
        """
        for field, section in self.matching_map:
            value = appstruct.get(section, {}).get(field, None)
            if value is not None or colander.null:
                dbdatas.setdefault(self.dbtype, {})[field] = value
        return dbdatas


class SequenceWrapper:
    """
        Maps the db models with colander Sequence Schemas
    """
    mapping_name = ''
    sequence_name = ''
    dbtype = ''
    fields = None
    sort_key = 'rowIndex'

    def toschema(self, dbdatas, appstruct):
        """
            Build schema expected datas from list of elements
        """
        lineslist = dbdatas.get(self.dbtype, [])
        if self.sort_key:
            lines = sorted(lineslist,
                           key=lambda line: int(line[self.sort_key]))
        else:
            lines = lineslist
        for line in lines:
            appstruct.setdefault(self.mapping_name, {})
            appstruct[self.mapping_name].setdefault(
                self.sequence_name, []).append(
                    dict((key, value)
                         for key, value in line.items()
                         if key in self.fields)
                )
        return appstruct

    def todb(self, appstruct, dbdatas):
        """
            convert colander deserialized datas to database dbdatas
        """
        all_ = appstruct.get(self.mapping_name, {}).get(self.sequence_name, [])
        for index, line in enumerate(all_):
            dbdatas.setdefault(self.dbtype, [])
            if self.sort_key:
                line[self.sort_key] = index + 1
            dbdatas[self.dbtype].append(line)
        return dbdatas


class InvoiceMatch(MappingWrapper):
    matching_map = (
        #task attrs
        ('name', 'common'),
        ('phase_id', 'common'),
        ('taskDate', 'common'),
        ('financial_year', 'common'),
        ('description', 'common'),
        #both estimation and invoice attrs
        ('customer_id', 'common'),
        ('address', 'common'),
        ('course', 'common'),
        ('displayedUnits', 'common'),
        ('expenses', 'lines'),
        ('expenses_ht', 'lines'),
        ('paymentConditions', 'payments'),
        ('statusComment', 'communication'),
    )
    dbtype = 'invoice'


class EstimationMatch(MappingWrapper):
    matching_map = (
        ('name', 'common'),
        ('phase_id', 'common'),
        ('taskDate', 'common'),
        ('description', 'common'),
        ('customer_id', 'common'),
        ('address', 'common'),
        ('course', 'common'),
        ('displayedUnits', 'common'),
        ('expenses', 'lines'),
        ('expenses_ht', 'lines'),
        ('exclusions', 'notes'),
        ('paymentConditions', 'payments'),

        # estimation only attrs
        ('paymentDisplay', 'payments'),
        ('deposit', 'payments'),
        ('statusComment', 'communication'),
    )
    dbtype = 'estimation'


class CancelInvoiceMatch(MappingWrapper):
    matching_map = (
        #task attrs
        ('name', 'common'),
        ('phase_id', 'common'),
        ('taskDate', 'common'),
        ('financial_year', 'common'),
        ('description', 'common'),
        ('customer_id', 'common'),
        ('address', 'common'),
        ('displayedUnits', 'common'),
        ('expenses', 'lines'),
        ('expenses_ht', 'lines'),
        ('reimbursementConditions', 'payments'),
    )
    dbtype = 'cancelinvoice'


class TaskLinesMatch(SequenceWrapper):
    mapping_name = 'lines'
    sequence_name = 'lines'
    fields = ('description', 'cost', 'quantity', 'unity', 'tva', 'product_id')
    dbtype = 'lines'


class PaymentLinesMatch(SequenceWrapper):
    mapping_name = 'payments'
    sequence_name = 'payment_lines'
    fields = ('description', 'paymentDate', 'amount', 'tva')
    dbtype = "payment_lines"


class DiscountLinesMatch(SequenceWrapper):
    mapping_name = 'lines'
    sequence_name = 'discounts'
    fields = ('description', 'amount', 'tva')
    dbtype = "discounts"
    sort_key = None


def get_estimation_appstruct(dbdatas):
    """
        return EstimationSchema-compatible appstruct
    """
    appstruct = {}
    for matchobj in (EstimationMatch, TaskLinesMatch, PaymentLinesMatch,
                                                        DiscountLinesMatch):
        appstruct = matchobj().toschema(dbdatas, appstruct)
    appstruct = set_payment_times(appstruct, dbdatas)
    return appstruct


def get_estimation_dbdatas(appstruct):
    """
        return dict with db compatible datas
    """
    dbdatas = {}
    for matchobj in (EstimationMatch, TaskLinesMatch, PaymentLinesMatch,
                                                      DiscountLinesMatch):
        dbdatas = matchobj().todb(appstruct, dbdatas)
    dbdatas = set_manualDeliverables(appstruct, dbdatas)
    return dbdatas


def get_invoice_appstruct(dbdatas):
    """
        return InvoiceSchema compatible appstruct
    """
    appstruct = {}
    for matchobj in (InvoiceMatch, TaskLinesMatch, DiscountLinesMatch):
        appstruct = matchobj().toschema(dbdatas, appstruct)
    return appstruct


def get_invoice_dbdatas(appstruct):
    """
        return dict with db compatible datas
    """
    dbdatas = {}
    for matchobj in (InvoiceMatch, TaskLinesMatch, DiscountLinesMatch):
        dbdatas = matchobj().todb(appstruct, dbdatas)
    return dbdatas


def get_cancel_invoice_appstruct(dbdatas):
    """
        return cancel invoice schema compatible appstruct
    """
    appstruct = {}
    for matchobj in (CancelInvoiceMatch, TaskLinesMatch):
        appstruct = matchobj().toschema(dbdatas, appstruct)
    return appstruct


def get_cancel_invoice_dbdatas(appstruct):
    """
        return dict with db compatible datas
    """
    dbdatas = {}
    for matchobj in (CancelInvoiceMatch, TaskLinesMatch):
        dbdatas = matchobj().todb(appstruct, dbdatas)
    return dbdatas


def set_manualDeliverables(appstruct, dbdatas):
    """
        Hack the dbdatas to set the manualDeliverables value
    """
    if dbdatas['estimation']:
        if appstruct.get('payments', {}).get('payment_times') == -1:
            dbdatas['estimation']['manualDeliverables'] = 1
        else:
            dbdatas['estimation']['manualDeliverables'] = 0
    return dbdatas


def set_payment_times(appstruct, dbdatas):
    """
        Hack the appstruct to set the payment_times value
    """
    if dbdatas.get('estimation', {}).get('manualDeliverables') == 1:
        appstruct.setdefault('payments', {})['payment_times'] = -1
    else:
        appstruct.setdefault('payments', {})['payment_times'] = max(1,
                                        len(dbdatas.get('payment_lines')))
    return appstruct


