# -*- coding: utf-8 -*-
# * File Name : task.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 09-04-2012
# * Last Modified :
#
# * Project :
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
from deform import widget

from autonomie.views.forms.widgets import (
        DisabledInput,
        deferred_autocomplete_widget,
        deferred_today,
        get_date_input,
        CustomSequenceWidget,
        )
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
PAYMENTDISPLAYCHOICES = (
        ('NONE', u"Les paiments ne sont pas affichés dans le PDF",),
        ('SUMMARY', u"Le résumé des paiements apparaît dans le PDF",),
        ('ALL', u"Le détail des paiements apparaît dans le PDF",),)

TEMPLATES_URL = 'autonomie:deform_templates/'


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


def build_client_value(client=None):
    """
        return the tuple for building client select
    """
    if client:
        return (str(client.id), client.name)
    else:
        return ("0", u"Sélectionnez")


def build_client_values(clients):
    """
        Build human understandable client labels
        allowing efficient discrimination
    """
    options = [build_client_value()]
    options.extend([build_client_value(client)
                            for client in clients])
    return options


def get_clients_from_request(request):
    clients = []
    if request.context.__name__ == 'project':
        clients = request.context.clients
    elif request.context.__name__ in ('invoice', 'estimation', 'cancelinvoice'):
        if request.context.project is not None:
            clients = request.context.project.clients
    return clients


@colander.deferred
def deferred_client_list(node, kw):
    request = kw['request']
    clients = get_clients_from_request(request)
    return deferred_autocomplete_widget(node,
            {'choices':build_client_values(clients)})


@colander.deferred
def deferred_client_validator(node, kw):
    request = kw['request']
    clients = get_clients_from_request(request)
    client_ids = [client.id for client in clients]
    def client_oneof(value):
        if value in ("0", 0):
            return u"Veuillez choisir un client"
        elif value not in client_ids:
            return u"Entrée invalide"
        return True
    return colander.Function(client_oneof)


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
    return widget.SelectWidget(
                     values=zip(unities, unities),
                     template=TEMPLATES_URL + 'unity.mako')


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
        return widget.TextInputWidget(mask='9999')
    else:
        return widget.HiddenWidget()


@colander.deferred
def deferred_tvas_widget(node, kw):
    """
        return a tva widget
    """
    tvas = get_tva_choices()
    wid = widget.SelectWidget(
        values=tvas,
        css_class='span1',
        template=TEMPLATES_URL + 'select.mako')
    return wid


@colander.deferred
def deferred_product_widget(node, kw):
    """
        return a widget for product selection
    """
    products = get_product_choices()
    wid = widget.SelectWidget(
        values=products,
        css_class='span2',
        template=TEMPLATES_URL + 'select.mako')
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
        return None


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
def deferred_phases_widget(node, kw):
    """
        return phase select widget
    """
    request = kw['request']
    phases = get_phases_from_request(request)
    choices = get_phase_choices(phases)
    wid = widget.SelectWidget(values=choices)
    return wid


class TaskLine(colander.MappingSchema):
    """
        A single estimation line
    """
    description = colander.SchemaNode(
        colander.String(),
        widget=widget.TextAreaWidget(
            cols=45, rows=4,
            template=TEMPLATES_URL + 'prestation.mako',
            css_class='span3'),
         missing=u'',
         css_class='span3')
    cost = colander.SchemaNode(
        AmountType(),
        widget=widget.TextInputWidget(
            template=TEMPLATES_URL + 'lineinput.mako'),
        css_class='span1')
    quantity = colander.SchemaNode(
        QuantityType(),
        widget=widget.TextInputWidget(
            template=TEMPLATES_URL + 'lineinput.mako'),
        css_class='span1')
    unity = colander.SchemaNode(
        colander.String(),
        widget=deferred_unity_widget,
        validator=deferred_unity_validator,
        missing=u"",
        css_class='span2')
    tva = colander.SchemaNode(
        Integer(),
        widget=deferred_tvas_widget,
        default=deferred_default_tva,
        validator=deferred_tva_validator,
        css_class='span1',
        title=u'TVA')
    product_id = colander.SchemaNode(
            colander.Integer(),
            widget=deferred_product_widget,
            validator=deferred_product_validator,
            missing="",
            css_class="span2",
            title=u"Code produit")


class DiscountLine(colander.MappingSchema):
    """
        A single estimation line
    """
    description = colander.SchemaNode(
        colander.String(),
        widget=widget.TextAreaWidget(
            cols=60, rows=4,
            template=TEMPLATES_URL + 'prestation.mako',
            css_class='span4'),
         missing=u'',
         css_class='span4')
    amount = colander.SchemaNode(
        AmountType(),
        widget=widget.TextInputWidget(
            template=TEMPLATES_URL + 'lineinput.mako'),
        css_class='span1')
    tva = colander.SchemaNode(
        Integer(),
        widget=deferred_tvas_widget,
        default=deferred_default_tva,
        css_class='span2 offset3',
        title=u'TVA')


class TaskLines(colander.SequenceSchema):
    """
        Sequence of estimation lines
    """
    taskline = TaskLine(
        widget=widget.MappingWidget(
            template=TEMPLATES_URL + 'taskline_mapping.mako',
            item_template=TEMPLATES_URL + 'taskline_mapping_item.mako')
    )


class DiscountLines(colander.SequenceSchema):
    """
        Sequence of estimation lines
    """
    discountline = DiscountLine(
        widget=widget.MappingWidget(
            template=TEMPLATES_URL + 'discountline_mapping.mako',
            item_template=TEMPLATES_URL + 'discountline_mapping_item.mako')
    )


class TaskLinesBlock(colander.MappingSchema):
    """
        Fieldset containing the "Détail de la prestation" block
        with estimation and invoice lines and all the stuff
    """
    lines = TaskLines(
        widget=CustomSequenceWidget(
            template=TEMPLATES_URL + 'tasklines_sequence.mako',
            item_template=TEMPLATES_URL + 'tasklines_sequence_item.mako',
            min_len=1),
        title=u'')
    discounts = DiscountLines(
        widget=CustomSequenceWidget(
            template=TEMPLATES_URL + 'discountlines_sequence.mako',
            item_template=TEMPLATES_URL + 'discountlines_sequence_item.mako'),
        title=u'')
    expenses_ht = colander.SchemaNode(
            AmountType(),
            widget=widget.TextInputWidget(
                template=TEMPLATES_URL + 'wrappable_input.mako',
                ),
            title=u"Frais forfaitaires (HT)",
            missing=0)
    default_tva = colander.SchemaNode(colander.Integer(),
            title=u"",
            widget=widget.HiddenWidget(
                template=TEMPLATES_URL + 'hiddeninput.mako',
                ), default=deferred_default_tva)
    expenses = colander.SchemaNode(
        AmountType(),
        widget=widget.TextInputWidget(
            template=TEMPLATES_URL + 'wrappable_input.mako',
            before=TEMPLATES_URL + 'tvalist.mako',
            before_options={'label': u'Montant TVA', 'id': 'tvapart'},
            after=TEMPLATES_URL + 'staticinput.mako',
            after_options={'label': u'Total TTC', 'id': 'total'}
        ),
        title=u'Frais Réel (TTC)',
        missing=0)


class TaskConfiguration(colander.MappingSchema):
    """
        Main fields to be configured
    """
    client_id = colander.SchemaNode(
                colander.Integer(),
                title=u"Choix du client",
                widget=deferred_client_list,
                validator=deferred_client_validator)
    address = colander.SchemaNode(
            colander.String(),
            title=u"Nom et adresse du client",
            widget=widget.TextAreaWidget(rows=4, cols=60))
    phase_id = colander.SchemaNode(
        colander.String(),
        title=u"Phase où insérer le devis",
        widget=deferred_phases_widget,
        default=deferred_default_phase)
    taskDate = colander.SchemaNode(
        colander.Date(),
        title=u"Date du devis",
        widget=get_date_input(),
        default=deferred_today
    )
    description = colander.SchemaNode(
        colander.String(),
        title=u"Objet du devis",
        widget=widget.TextAreaWidget(css_class="span8"),
    )
    course = colander.SchemaNode(
        colander.Integer(),
        title=u"Formation ?",
        description=deferred_course_title,
        widget=widget.CheckboxWidget(true_val="1", false_val="0")
    )
    displayedUnits = colander.SchemaNode(
        colander.Integer(),
        title=u"Afficher le détail",
        description=u"Afficher le détail des prestations dans le PDF ?",
        widget=widget.CheckboxWidget(true_val="1", false_val="0")
    )


class TaskNotes(colander.MappingSchema):
    """
        Notes
    """
    exclusions = colander.SchemaNode(
        colander.String(),
        title=u'Notes',
        widget=widget.TextAreaWidget(css_class='span10'),
        missing=u"",
        description=u"Note complémentaires concernant les prestations décrites"
    )


class TaskCommunication(colander.MappingSchema):
    """
        Communication avec la CAE
    """
    statusComment = colander.SchemaNode(
        colander.String(),
        missing=u'',
        title=u'Communication Entrepreneur/CAE',
        widget=widget.TextAreaWidget(css_class='span10'),
        description=u"Message à destination des membres de la CAE qui \
valideront votre document (n'apparaît pas dans le PDF)")


class TaskSchema(colander.MappingSchema):
    """
        colander base Schema for task edition
    """
    common = TaskConfiguration(title=u"")
    lines = TaskLinesBlock(
        title=u"Détail des prestations",
        widget=widget.MappingWidget(
            item_template=TEMPLATES_URL + 'estimationdetails_item.mako')
    )


def remove_admin_fields(schema, kw):
    doctype = schema['lines']['lines'].doctype
    if kw['request'].user.is_contractor():
        # Non admin users doesn't edit products
        if doctype != 'estimation':
            del schema['lines']['lines']['taskline']['product_id']
        schema['lines']['lines'].is_admin = False
        schema['lines']['lines']['taskline']['description'].css_class = 'span4'
        schema['lines']['lines']['taskline']['description'].widget.css_class = 'span4'
        schema['lines']['lines']['taskline']['tva'].css_class = 'span2'
        schema['lines']['lines']['taskline']['tva'].widget.css_class = 'span2'
    else:
        schema['lines']['lines'].is_admin = True
        if doctype != 'estimation':
            schema['lines']['lines']['taskline']['description'].css_class = 'span3'
            schema['lines']['lines']['taskline']['description'].widget.css_class = 'span3'
            schema['lines']['lines']['taskline']['tva'].css_class = 'span1'
            schema['lines']['lines']['taskline']['tva'].widget.css_class = 'span1'
        else:
            schema['lines']['lines']['taskline']['description'].css_class = 'span4'
            schema['lines']['lines']['taskline']['description'].widget.css_class = 'span4'
            schema['lines']['lines']['taskline']['tva'].css_class = 'span2'
            schema['lines']['lines']['taskline']['tva'].widget.css_class = 'span2'


TASKSCHEMA = TaskSchema(after_bind=remove_admin_fields)


class EstimationPaymentLine(colander.MappingSchema):
    """
        Payment line
    """
    description = colander.SchemaNode(
        colander.String(),
        title=u'',
        widget=widget.TextInputWidget(
            template=TEMPLATES_URL + 'prestation.mako',
            css_class='span5'),
        css_class='span5',)
    paymentDate = colander.SchemaNode(
        colander.Date(),
        title=u'',
        widget=get_date_input(css_class='span2'),
        default=datetime.date.today(),
        css_class='span2',)
    amount = colander.SchemaNode(
        AmountType(),
        title=u'',
        widget=widget.TextInputWidget(
            template=TEMPLATES_URL + 'amount.mako',
            css_class='span5'),
        css_class='span2 offset2')


class EstimationPaymentLines(colander.SequenceSchema):
    """
        Sequence of payment lines
    """
    line = EstimationPaymentLine(
        widget=widget.MappingWidget(
            template=TEMPLATES_URL + 'paymentline_mapping.mako',
            item_template=TEMPLATES_URL + 'paymentline_mapping_item.mako')
    )


class EstimationPayments(colander.MappingSchema):
    """
        Gestion des acomptes
    """
    deposit = colander.SchemaNode(
        colander.Integer(),
        title=u"Acompte à la commande",
        default=0,
        widget=widget.SelectWidget(
            values=get_percents(),
            css_class='span2')
    )
    payment_times = colander.SchemaNode(
        colander.Integer(),
        title=u"Paiement en ",
        default=1,
        widget=widget.SelectWidget(values=get_payment_times(),
                                     css_class='span2')
    )
    paymentDisplay = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf([x[0] for x in PAYMENTDISPLAYCHOICES]),
        widget=widget.RadioChoiceWidget(values=PAYMENTDISPLAYCHOICES),
        title=u"Affichage des paiements",
        default="SUMMARY")
    payment_lines = EstimationPaymentLines(
        widget=CustomSequenceWidget(
            template=TEMPLATES_URL + 'paymentlines_sequence.mako',
            item_template=TEMPLATES_URL + 'paymentlines_sequence_item.mako',
            min_len=1),
        title=u'',
        description=u"Définissez les échéances de paiement")
    paymentConditions = colander.SchemaNode(
        colander.String(),
        missing=u'',
        title=u'Conditions de paiement',
        widget=widget.TextAreaWidget(css_class='span10'),
        description=u"Précisez les conditions de paiement dans votre devis")


class InvoicePayments(colander.MappingSchema):
    """
        Conditions de paiement de la facture
    """
    paymentConditions = colander.SchemaNode(
        colander.String(),
        missing=u'',
        title=u'Conditions de paiement',
        widget=widget.TextAreaWidget(css_class='span10'),
        description=u"Les conditions de paiement sont requises \
dans les factures")


def get_estimation_schema():
    """
        Return the schema for estimation add/edit
    """
    schema = TASKSCHEMA.clone()
    schema['lines']['lines'].doctype = "estimation"
    tmpl = 'autonomie:deform_templates/paymentdetails_item.mako'
    schema.add(TaskNotes(title=u"Notes", name="notes"))
    schema.add(
        EstimationPayments(title=u'Conditions de paiement',
                           widget=widget.MappingWidget(item_template=tmpl),
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
    schema.add(payments)
    return schema


@colander.deferred
def deferred_amount_default(node, kw):
    """
        default value for the payment amount
    """
    task = kw['request'].context
    return task.topay()


@colander.deferred
def deferred_total_validator(node, kw):
    """
        validate the amount to keep the sum under the total
    """
    task = kw['request'].context
    max_msg = u"Le montant ne doit pas dépasser %s\
(total ttc - somme des paiements enregistrés)" % (task.topay() / 100.0)
    min_msg = u"Le montant doit être positif"
    return colander.Range(min=0, max=task.topay(), min_err=min_msg,
                                                   max_err=max_msg)


@colander.deferred
def deferred_payment_mode_widget(node, kw):
    """
        dynamically retrieves the payment modes
    """
    modes = [(mode.label, mode.label) for mode in PaymentMode.query()]
    return widget.SelectWidget(values=modes)


@colander.deferred
def deferred_payment_mode_validator(node, kw):
    return colander.OneOf([mode.label for mode in PaymentMode.query()])


class PaymentSchema(colander.MappingSchema):
    """
        colander schema for payment recording
    """
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
            widget=widget.HiddenWidget(),
            missing=u"",
            css_class="span0")
    description = colander.SchemaNode(
        colander.String(),
        widget=DisabledInput(),
         missing=u'',
         css_class='span3')
    tva = colander.SchemaNode(
        AmountType(),
        widget=DisabledInput(),
        css_class='span1',
        title=u'TVA')
    product_id = colander.SchemaNode(
            colander.Integer(),
            widget=deferred_product_widget,
            validator=deferred_product_validator,
            missing="",
            css_class="span2",
            title=u"Code produit")


class ProductTaskLines(colander.SequenceSchema):
    taskline = ProductTaskLine(missing="", title=u"")


class SetProductsSchema(colander.MappingSchema):
    """
        Form schema used to configure Products
    """
    lines = ProductTaskLines(
        widget=widget.SequenceWidget(
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
        ('phase_id', 'common'),
        ('taskDate', 'common'),
        ('financial_year', 'common'),
        ('description', 'common'),
        #both estimation and invoice attrs
        ('client_id', 'common'),
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
        ('phase_id', 'common'),
        ('taskDate', 'common'),
        ('description', 'common'),
        ('client_id', 'common'),
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
        ('phase_id', 'common'),
        ('taskDate', 'common'),
        ('financial_year', 'common'),
        ('description', 'common'),
        ('client_id', 'common'),
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
