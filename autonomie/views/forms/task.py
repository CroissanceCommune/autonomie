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
"""
import logging
import datetime

import colander
from deform import widget

from autonomie.utils.forms import get_date_input
from .custom_types import QuantityType
from .custom_types import AmountType

log = logging.getLogger(__name__)

def get_percents():
    """
        Return percents for select widget
    """
    percent_options = [(0,'Aucun'), (5,'5%')]
    for i in range(10, 110, 10):
        percent_options.append((i, "%d %%" % i))
    return percent_options

def get_payment_times():
    """
        Return options for payment times select
    """
    payment_times = [(-1, u'Configuration manuel')]
    for i in range(1, 12):
        payment_times.append((i, '%d fois' % i))
    return payment_times

@colander.deferred
def deferred_course_title(node, kw):
    """
        deferred title
    """
    if kw.get('tasktype') == "invoice":
        return u"Cette facture concerne-t-elle une formation ?"
    else:
        return u"Ce devis concerne-t-il une formation ?"

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

class EstimationLine(colander.MappingSchema):
    """
        A single estimation line
    """
    description = colander.SchemaNode(colander.String(),
         widget=widget.TextAreaWidget(cols=80, rows=4,
             template='autonomie:deform_templates/prestation.mako',
             css_class='span5'
             ),
         missing=u'',
         css_class='span5')
    cost = colander.SchemaNode(AmountType(),
            widget=widget.TextInputWidget(
                template='autonomie:deform_templates/lineinput.mako',
                ),
            css_class='span1'
            )
    quantity = colander.SchemaNode(QuantityType(),
            widget=widget.TextInputWidget(
                template='autonomie:deform_templates/lineinput.mako',
                ),
            css_class='span1'
            )
    unity = colander.SchemaNode(
                colander.String(),
                widget=widget.SelectWidget(
                    values=DAYS,
                    template='autonomie:deform_templates/unity.mako',
                    ),
                css_class='span2'
                )

class EstimationLines(colander.SequenceSchema):
    """
        Sequence of estimation lines
    """
    estimationline = EstimationLine(
            widget=widget.MappingWidget(
                    template='autonomie:deform_templates/\
estimationline_mapping.mako',
               item_template='autonomie:deform_templates/\
estimationline_mapping_item.mako'
                     )
            )

@colander.deferred
def deferred_tvas_widget(node, kw):
    """
        return a tva widget
    """
    tvas = kw.get('tvas')
    wid = widget.SelectWidget(values=tvas,
                                  css_class='span1')
    return wid


@colander.deferred
def deferred_phases_widget(node, kw):
    """
        return phase select widget
    """
    choices = kw.get("phases")
    if choices:
        wid = widget.SelectWidget(values=choices)
    else:
        wid = widget.TextInputWidget()
    return wid

class TaskLinesBlock(colander.MappingSchema):
    """
        Fieldset containing the "Détail de la prestation" block
        with estimation and invoice lines and all the stuff
    """
    lines = EstimationLines(
            widget=widget.SequenceWidget(
     template='autonomie:deform_templates/tasklines_sequence.mako',
     item_template='autonomie:deform_templates/tasklines_sequence_item.mako',
     min_len=1
     ),
            title=u'')
    discountHT = colander.SchemaNode(AmountType(),
            widget=widget.TextInputWidget(
         template='autonomie:deform_templates/wrappable_input.mako',
         before='autonomie:deform_templates/staticinput.mako',
         before_options={'label':u'Total HT avant Remise', 'id':'linestotal'},
         after='autonomie:deform_templates/staticinput.mako',
         after_options={'label':u'Total HT', 'id':'httotal'}
                ),
            title=u"Remise",
            missing=0)
    tva = colander.SchemaNode(colander.String(),
            widget=deferred_tvas_widget,
            default=1960,
            title=u'TVA')

    expenses = colander.SchemaNode(AmountType(),
            widget=widget.TextInputWidget(
         template='autonomie:deform_templates/wrappable_input.mako',
         before='autonomie:deform_templates/staticinput.mako',
         before_options={'label':u'Montant TVA', 'id':'tvapart'},
         after='autonomie:deform_templates/staticinput.mako',
         after_options={'label':u'Total TTC', 'id':'total'}
                ),
            title=u'Frais TTC',
            missing=0)

class TaskConfiguration(colander.MappingSchema):
    """
        Main fields to be configured
    """
    IDPhase = colander.SchemaNode(
                colander.String(),
                title=u"Phase où insérer le devis",
                widget=deferred_phases_widget,
                )
    taskDate = colander.SchemaNode(
                colander.Date(),
                title=u"Date du devis",
                widget=get_date_input(),
                default=datetime.date.today()
                )
    description = colander.SchemaNode(
                colander.String(),
                title=u"Objet du devis",
                widget=widget.TextAreaWidget(css_class="span8"),
                )
    course = colander.SchemaNode(colander.Integer(),
                title=u"Formation ?",
                description=deferred_course_title,
                widget=widget.CheckboxWidget(true_val="1", false_val="0"))
    displayedUnits = colander.SchemaNode(colander.Integer(),
                title=u"Afficher le détail",
                description=u"Afficher le détail des prestations dans le PDF ?",
                widget=widget.CheckboxWidget(true_val="1", false_val="0"))

class TaskNotes(colander.MappingSchema):
    """
        Notes
    """
    exclusions = colander.SchemaNode(
                colander.String(),
                title=u'Notes',
                widget=widget.TextAreaWidget(css_class='span10'),
                missing=u"",
                description=u"Note complémentaires concernant \
les prestations décrites")

class EstimationPaymentLine(colander.MappingSchema):
    """
        Payment line
    """
    description = colander.SchemaNode(
                            colander.String(),
                            title=u'',
                            widget=widget.TextInputWidget(
            template='autonomie:deform_templates/prestation.mako',
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
                template='autonomie:deform_templates/amount.mako',
                css_class='span5'
                ),
            css_class='span2 offset2',
            )

class EstimationPaymentLines(colander.SequenceSchema):
    """
        Sequence of payment lines
    """
    line = EstimationPaymentLine(
            widget=widget.MappingWidget(
                    template='autonomie:deform_templates/\
paymentline_mapping.mako',
               item_template='autonomie:deform_templates/\
paymentline_mapping_item.mako'
)
            )


class EstimationPayments(colander.MappingSchema):
    """
        Gestion des accomptes
    """
    deposit = colander.SchemaNode(
                        colander.Integer(),
                        title=u"Accompte à la commande",
                        default=0,
                        widget=widget.SelectWidget(values=get_percents(),
                             css_class='span2'))
    payment_times = colander.SchemaNode(
                        colander.Integer(),
                        title=u"Paiement en ",
                        default=1,
                        widget = widget.SelectWidget(values=get_payment_times(),
                                     css_class='span2'))
    paymentDisplay = colander.SchemaNode(
               colander.String(),
              validator=colander.OneOf([x[0] for x in PAYMENTDISPLAYCHOICES]),
         widget=widget.RadioChoiceWidget(values=PAYMENTDISPLAYCHOICES),
         title=u"Affichage des paiements",
         default="SUMMARY"
                        )
    payment_lines = EstimationPaymentLines(
               widget=widget.SequenceWidget(
                   template='autonomie:deform_templates/\
paymentlines_sequence.mako',
                   item_template='autonomie:deform_templates/\
paymentlines_sequence_item.mako',
                   min_len=1
                   ),
               title=u'',
               description=u"Définissez les échéances de paiement"
               )
    paymentConditions = colander.SchemaNode(
                    colander.String(),
                    missing=u'',
                    title=u'Conditions de paiement',
                    widget=widget.TextAreaWidget(css_class='span10'),
                     description=u"Précisez les conditions de paiement \
dans votre devis")

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


class TaskCommunication(colander.MappingSchema):
    """
        Communication avec la CAE
    """
    statusComment = colander.SchemaNode(
                        colander.String(),
                        missing=u'',
                        title=u'Communication Entrepreneur/CAE',
                        widget=widget.TextAreaWidget(css_class='span10'),
                        description=u"Message à destination des membres de \
la CAE qui validderont votre document (n'apparaît pas dans le PDF)")

class TaskSchema(colander.MappingSchema):
    """
        colander base Schema for task edition
    """
    common = TaskConfiguration( title=u"")
    lines = TaskLinesBlock(title=u"Détail des prestations",
                           widget=widget.MappingWidget(
      item_template='autonomie:deform_templates/estimationdetails_item.mako'))
    notes = TaskNotes(title=u"Notes")

def get_estimation_schema():
    """
        Return the schema for estimation add/edit
    """
    schema = TaskSchema().clone()
    tmpl = 'autonomie:deform_templates/paymentdetails_item.mako'
    schema.add(
            EstimationPayments(title=u'Conditions de paiement',
                              widget=widget.MappingWidget(item_template=tmpl),
                              name='payments'))
    schema.add(TaskCommunication(title=u'Communication Entrepreneur/CAE',
                                 name='communication'))
    return schema

def get_invoice_schema():
    """
        Return the schema for invoice add/edit
    """
    schema = TaskSchema().clone()
    title = u"Phase où insérer la facture"
    schema['common']['IDPhase'].title = title
    title = u"Date de la facture"
    schema['common']['taskDate'].title = title
    title = u"Objet de la facture"
    schema['common']['description'].title = title
    title = u"Conditions de paiement"
    schema.add(InvoicePayments(title=title, name='payments'))
    schema.add(TaskCommunication(title=u'Communication Entrepreneur/CAE',
                                 name='communication'))
    return schema

def get_cancel_invoice_schema():
    """
        return the cancel invoice form schema
    """
    schema = TaskSchema().clone()
    title = u"Phase où insérer l'avoir"
    schema['common']['IDPhase'].title = title
    title = u"Date de l'avoir"
    schema['common']['taskDate'].title = title
    title = u"Objet de l'avoir"
    schema['common']['description'].title = title
    del schema['common']['course']
    title = u"Conditions de remboursement"
    payments = InvoicePayments(title=title, name='payments').clone()
    payments['paymentConditions'].title = title
    payments['paymentConditions'].description = u""
    schema.add(payments)
    del schema["lines"]["discountHT"]
    return schema

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
        for line in sorted(lineslist, key=lambda line:int(line[self.sort_key])):
            appstruct.setdefault(self.mapping_name, {})
            appstruct[self.mapping_name].setdefault(self.sequence_name, []
                                                    ).append(
                    dict((key, value)for key, value in line.items()
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
            line[self.sort_key] = index+1
            dbdatas[self.dbtype].append(line)
        return dbdatas


class InvoiceMatch(MappingWrapper):
    matching_map = (
                        #task attrs
                         ('IDPhase','common'),
                         ('taskDate','common'),
                         ('description', 'common'),
                        #both estimation and invoice attrs
                         ('course', 'common'),
                         ('displayedUnits', 'common'),
                         ('tva', 'lines'),
                         ('discountHT', 'lines'),
                         ('expenses', 'lines'),
                         ('exclusions', 'notes'),
                         ('paymentConditions', 'payments'),
            )
    dbtype = 'invoice'

class EstimationMatch(MappingWrapper):
    matching_map = (
                         ('IDPhase','common'),
                         ('taskDate','common'),
                         ('description', 'common'),

                         ('course', 'common'),
                         ('displayedUnits', 'common'),
                         ('tva', 'lines'),
                         ('discountHT', 'lines'),
                         ('expenses', 'lines'),
                         ('exclusions', 'notes'),
                         ('paymentConditions', 'payments'),

                        #estimation only attrs
                         ('paymentDisplay', 'payments'),
                         ('deposit', 'payments'),
                         )
    dbtype = 'estimation'

class CancelInvoiceMatch(MappingWrapper):
    matching_map = (
                        #task attrs
                         ('IDPhase','common'),
                         ('taskDate','common'),
                         ('description', 'common'),
                        #both estimation and invoice attrs
                         ('displayedUnits', 'common'),
                         ('tva', 'lines'),
                         ('expenses', 'lines'),
                         ('exclusions', 'notes'),
                         ('reimbursementConditions', 'payments'),
            )
    dbtype = 'cancelinvoice'

class TaskLinesMatch(SequenceWrapper):
    mapping_name = 'lines'
    sequence_name = 'lines'
    fields = ('description', 'cost', 'quantity', 'unity',)
    dbtype = 'lines'

class PaymentLinesMatch(SequenceWrapper):
    mapping_name = 'payments'
    sequence_name = 'payment_lines'
    fields = ('description', 'paymentDate', 'amount',)
    dbtype = "payment_lines"

def get_estimation_appstruct(dbdatas):
    """
        return EstimationSchema-compatible appstruct
    """
    appstruct = {}
    for matchobj in (EstimationMatch, TaskLinesMatch, PaymentLinesMatch):
        appstruct = matchobj().toschema(dbdatas, appstruct)
    appstruct = set_payment_times(appstruct, dbdatas)
    return appstruct

def get_estimation_dbdatas(appstruct):
    """
        return dict with db compatible datas
    """
    dbdatas = {}
    for matchobj in (EstimationMatch, TaskLinesMatch, PaymentLinesMatch):
        dbdatas = matchobj().todb(appstruct, dbdatas)
    dbdatas = set_manualDeliverables(appstruct, dbdatas)
    return dbdatas

def get_invoice_appstruct(dbdatas):
    """
        return InvoiceSchema compatible appstruct
    """
    appstruct = {}
    for matchobj in (InvoiceMatch, TaskLinesMatch):
        appstruct = matchobj().toschema(dbdatas, appstruct)
    return appstruct

def get_invoice_dbdatas(appstruct):
    """
        return dict with db compatible datas
    """
    dbdatas = {}
    for matchobj in (InvoiceMatch, TaskLinesMatch):
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
