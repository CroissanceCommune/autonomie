# -*- coding: utf-8 -*-
# * File Name :
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
    Estimation form schema
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
import colander
import datetime

from deform import ValidationFailure

from autonomie.models import DBSESSION
from autonomie.models.model import Estimation
from autonomie.models.model import EstimationLine
from autonomie.models.model import Task
from autonomie.utils.forms import merge_session_with_post
#from autonomie.models import PaymentConditions

log = logging.getLogger(__name__)

def get_percents():
    """
        Return percents for select widget
    """
    percent_options = [('0','Aucun'), ('5','5%')]
    for i in range(10,110,10):
        percent_options.append(("%d" % i, "%d %%" % i))
    return percent_options

def get_payment_times():
    """
        Return options for payment times select
    """
    payment_times = [('-1', u'Configuration manuel')]
    for i in range(1,12):
        payment_times.append(('%d' % i, '%d fois' % i))
    return payment_times


import colander
from deform import widget

days = (
        ('NONE', '-'),
        ('HOUR', u'Heure(s)'),
        ('DAY', u'Jour(s)'),
        ('WEEK', u'Semaine(s)'),
        ('MONTH', u'Mois'),
        ('FEUIL', u'Feuillet(s)'),
        ('PACK', u'Forfait'),
        )

def specialfloat(self, value):
    """
        preformat the value before passing it to the float function
    """
    if isinstance(value, unicode):
        value = value.replace(u'€', '').replace(u',', '.').replace(u' ', '')
    return float(value)

class AmountType(colander.Number):
    """
        preformat an amount before considering it as a float object
    """
    num = specialfloat

class EstimationLine(colander.MappingSchema):
    """
        A single estimation line
    """
    prestation = colander.SchemaNode(colander.String(),
         widget=widget.TextAreaWidget(cols=80, rows=4,
             template='autonomie:deform_templates/lineblock/prestation.mako',
             css_class='span5'
             ),
         missing=u'',
         css_class='span5')
    cost = colander.SchemaNode(AmountType(),
            widget=widget.TextInputWidget(
                template='autonomie:deform_templates/lineblock/lineinput.mako',
                ),
            css_class='span1'
            )
    quantity = colander.SchemaNode(AmountType(),
            widget=widget.TextInputWidget(
                template='autonomie:deform_templates/lineblock/lineinput.mako',
                ),
            css_class='span1'
            )
    unity = colander.SchemaNode(
                colander.String(),
                widget=widget.SelectWidget(
                    values=days,
                    template='autonomie:deform_templates/lineblock/unity.mako',
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
lineblock/estimationline_mapping.mako',
               item_template='autonomie:deform_templates/\
lineblock/estimationline_mapping_item.mako'
                     )
            )

def get_deferred_choices_widget(keyword, **options):
    @colander.deferred
    def deferred_choices_widget(node, kw):
        """
            Returns a dynamically generated Select widget
            with choices passed at bind
        """
        choices = kw.get(keyword)
        if choices:
            wid = widget.SelectWidget(values=choices, **options)
        else:
            wid = widget.TextInputWidget(**options)
        return wid
    return deferred_choices_widget

class EstimationLinesBlock(colander.MappingSchema):
    """
        Fieldset containing the "Détail de la prestation" block
        with estimation lines and all the stuff
    """
    lines = EstimationLines(
            widget=widget.SequenceWidget(
                template='autonomie:deform_templates/\
lineblock/estimationlines_sequence.mako',
                item_template='autonomie:deform_templates/\
lineblock/estimationlines_sequence_item.mako',
                min_len=1
                ),
            title=u''
            )
    discount = colander.SchemaNode(AmountType(),
            widget=widget.TextInputWidget(
         template='autonomie:deform_templates/lineblock/wrappable_input.mako',
         before='autonomie:deform_templates/lineblock/staticinput.mako',
         before_options={'label':u'Total HT avant Remise', 'id':'linestotal'},
         after='autonomie:deform_templates/lineblock/staticinput.mako',
         after_options={'label':u'Total HT', 'id':'httotal'}
                ),
            title=u"Remise",
            missing=0)
    tva = colander.SchemaNode(colander.String(),
            widget=get_deferred_choices_widget("tvas", css_class='span1'),
            title=u'TVA')

    expenses = colander.SchemaNode(AmountType(),
            widget=widget.TextInputWidget(
         template='autonomie:deform_templates/lineblock/wrappable_input.mako',
         before='autonomie:deform_templates/lineblock/staticinput.mako',
         before_options={'label':u'Montant TVA', 'id':'tvapart'},
         after='autonomie:deform_templates/lineblock/staticinput.mako',
         after_options={'label':u'Total TTC', 'id':'total'}
                ),
            title=u'Frais TTC',
            missing=0)

class EstimationConfiguration(colander.MappingSchema):
    """
        Main fields to be configured
    """
    id_phase = colander.SchemaNode(
                colander.String(),
                widget=get_deferred_choices_widget('phases'),
#                description=u"La phase du projet auquel ce document appartient"
                )
    taskDate = colander.SchemaNode(
                colander.Date(),
                title=u"Date du devis",
                widget=widget.DateInputWidget(),
#                description=u"Date d'émission du devis"
                )
    descripton = colander.SchemaNode(
                colander.String(),
                title=u"Objet du devis",
                widget=widget.TextAreaWidget()
                )
    course = colander.SchemaNode(colander.String(),
                title=u"Formation ?",
                description=u"Ce devis concerne-t-il une formation ?",
                widget=widget.CheckboxWidget(true_val='1', false_val='0'))
    displayedUnits = colander.SchemaNode(colander.String(),
                title=u"Afficher le détail",
                description=u"Afficher le détail des prestations dans le devis ?",
                widget=widget.CheckboxWidget(true_val='1', false_val='0'))

class EstimationNotes(colander.MappingSchema):
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
            template='autonomie:deform_templates/lineblock/prestation.mako',
            css_class='span5'),
                            css_class='span5',)
    paymentDate = colander.SchemaNode(
                colander.Date(),
                title=u'',
                widget=widget.DateInputWidget(css_class='span2'),
                default=datetime.date.today(),
                css_class='span2',)
    amount = colander.SchemaNode(
            AmountType(),
            title=u'',
            widget=widget.TextInputWidget(
                template='autonomie:deform_templates/lineblock/amount.mako',
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
lineblock/paymentline_mapping.mako',
               item_template='autonomie:deform_templates/\
lineblock/paymentline_mapping_item.mako'
)
            )


class EstimationPayments(colander.MappingSchema):
    """
        Gestion des accomptes
    """
    deposit = colander.SchemaNode(
                        colander.String(),
                        title=u"Accompte à la commande",
                        default="0",
                        widget=widget.SelectWidget(values=get_percents(),
                             css_class='span2'))
    payment_times = colander.SchemaNode(
                        colander.String(),
                        title=u"Paiement en ",
                        default='1',
                        widget = widget.SelectWidget(values=get_payment_times(),
                                     css_class='span2'))
    payment_lines = EstimationPaymentLines(
               widget=widget.SequenceWidget(
                   template='autonomie:deform_templates/\
lineblock/paymentlines_sequence.mako',
                   item_template='autonomie:deform_templates/\
lineblock/paymentlines_sequence_item.mako',
                   min_len=1
                   ),
               title=u'',
               description=u"Définissez les échéances de paiement"
               )
class EstimationComment(colander.MappingSchema):
    """
        Commentaires
    """
    paymentConditions = colander.SchemaNode(
                    colander.String(),
                    missing=u'',
                    title=u'Commentaires',
                    widget=widget.TextAreaWidget(css_class='span10'),
                    description=u"Ajoutez des commentaires à votre document")

class EstimationCommunication(colander.MappingSchema):
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

class EstimationSchema(colander.MappingSchema):
    """
        colander Estimation form schema
    """
    common = EstimationConfiguration()
    lines = EstimationLinesBlock(title=u"Détail des prestations",
            widget=widget.MappingWidget(
           item_template='autonomie:deform_templates/lineblock/\
estimationdetails_item.mako'
            )
            )
    notes = EstimationNotes(title=u"Notes")
    payments = EstimationPayments(title=u'Conditions de paiement',
            widget=widget.MappingWidget(
                item_template='autonomie:deform_templates/lineblock/\
paymentdetails_item.mako'))
    comments = EstimationComment(title=u"Commentaires")
    communication = EstimationCommunication(
                        title=u'Communication Entrepreneur/CAE')

def serialize(dbdatas):
    """
        build a EstimationSchema compatible dict
        enter :
        {'task':{'id_phase':
                 'name':
                 'CAEStatus':
                 'statusComment':
                 'statusPerson':
                 'statusDate':
                 'customerStatus':
                 'taskDate':
                 'IDEmployee':
                 'description': },
         'estimation':{
                tva
                deposit
                paymentConditions
                exclusions
                manualDeliverables
                course
                displayedUnits
                discountHT
                expenses
                paymentDisplay
                }
          'estimationlines':[{
                rowIndex
                description
                cost
                quantity
                unity
            }...],
            "paymentconditions":[{
                rowIndex
                description
                amount
                paymentDate
            }...],
            }
        {'common':{'id_phase':}
    """
    datas = {}
    merge_task_in_datas(datas, dbdatas['task'])
    merge_estimation_in_datas(datas, dbdatas['estimation'])
    merge_estimationlines_in_datas(datas, dbdatas['estimation_lines'])
    if dbdatas['estimation']['manualDeliverables'] == '1':
        merge_paymentlines_in_datas(datas, dbdatas['payment_lines'])
    return datas

def merge_task_in_datas(datas, taskdict):
    """
        merge the task dict in datas to match EstimationSchema
    """
    for field in ["id_phase", "taskDate", "description"]:
        value = taskdict.get(field)
        if value is not None:
            datas.setdefault('common', {})[field] = value
    return datas

def merge_estimation_in_datas(datas, estimationdict):
    """
        merge an estimation dict in datas to match EstimationSchema
    """
    for field in ['course', 'displayedUnits']:
        value = estimationdict.get(field)
        if value is not None:
            datas.setdefault('common', {})[field] = value

    for field in ["tva", "discountHT", "expenses"]:
        value = estimationdict.get(field)
        if value is not None:
            datas.setdefault('lines', {})[field] = value

    exclusions = estimationdict.get('exclusions')
    if exclusions:
        datas.setdefault('notes', {})['exclusions'] = exclusions

    for field in ('paymentDisplay', 'deposit',):
        value = estimationdict.get(field)
        if value is not None:
            datas.setdefault('payments', {})[field] = value

    paymentConditions = estimationdict.get('paymentConditions')
    if paymentConditions:
        datas.setdefault('comments', {})['paymentConditions'] = paymentConditions

    return datas

def merge_estimationlines_in_datas(datas, lineslist):
    """
        merge estimationlines objects into datas dict to fit EstimationSchema
    """
    for line in sorted(lineslist, key=lambda line:int(line['rowIndex'])):
        datas.setdefault('lines', {}).setdefault('lines', []).append(
                     dict((key, value)for key, value in line.items()
                        if key in ('description', 'cost', 'quantity', 'unity'))
            )
    return datas

def merge_paymentlines_in_datas(datas, lineslist):
    """
        merge paymentlines objects into datas dict to fit EstimationSchema
    """
    for line in sorted(lineslist, key=lambda line:int(line['rowIndex'])):
        datas.setdefault('payments', {}).setdefault('payment_lines', []).append(
                    dict((key, value)for key, value in line.items()
                        if key in ('description', 'paymentDate', 'amount'))
                    )
    return datas


#def collect_indexes(keys, identifier):
#    """
#        return estimation line indexes
#    """
#    return [int(key[len(identifier):]) for key in keys if key.startswith(identifier)]
#
#def format_lines(datas):
#    """
#        get all the estimation lines configured in datas and
#        return a colander friendly data structure
#    """
#    keys = datas.keys()
#    # keys :
#    # prestation_id
#    # price_id
#    # quantity_id
#    # unity_id
#    indexes = collect_indexes(keys, "prestation_")
#    lines = []
#    for index in indexes:
#        prestation = datas['prestation_%d' % index]
#        quantity = datas['quantity_%d' % index]
#        price = datas['price_%d' % index]
#        unity = datas['unity_%d' % index]
#        lines.append(dict(description=prestation,
#                          cost=price,
#                          quantity=quantity,
#                          unity=unity))
#    return lines
#
#def format_task(datas):
#    """
#        return all the task related fields
#    """
#    keys = ['id_phase','description','taskDate',]
#    return dict((key, datas.get(key)) for key in keys)
#
#def format_estimation(datas):
#    """
#        return the estimation related fields
#    """
#    keys = ["tva",
#            "deposit",
#            "paymentConditions",
#            "exclusions",
#            "course",
#            "displayedUnits",
#            "discountHT",
#            "expenses",
#            "paymentDisplay",]
#    return dict((key, datas.get(key)) for key in keys)
#
#def format_payment_conditions(datas):
#    """
#        format all payment conditions related datas
#        to fit colander schema's expected structure
#    """
#    keys = datas.keys()
#    payments = []
#    indexes = collect_indexes(keys, "description_")
#    indexes.sort()
#    for index in indexes:
#        description = datas["description_%d" % index]
#        amount = datas["amount_%d" % index]
#        paymentDate = datas["paymentDate_%s" % index]
#        payments.append(dict(description=description,
#                             amount=amount,
#                             paymentDate=paymentDate,
#                             rowIndex=index))
#    return payments
#
#def format_datas(datas):
#    """
#        format all estimation form datas to fit the colander schema
#    """
#    log.debug("Formatting datas : %s" % (datas,))
#    tovalid = dict(estimation=format_estimation(datas),
#                   task=format_task(datas),
#                   estimation_lines=format_lines(datas),
#                   payment_conditions=format_payment_conditions(datas),
#                   )
#    return tovalid
#
#class EstimationForm():
#    """
#        Estimation Form makes the glue beetween
#        colander (form validation),
#        sqla (database orm)
#        user-input
#        user inputted datas are formatted;
#        sent to colander;
#        once validated, returns the appropriate elements
#        to insert into the database
#    """
#    def __init__(self, schema):
#        self.schema = schema
#
#    def validate(self, datas):
#        """
#            Launch datas validation
#        """
#        cstruct = format_datas(datas)
#        try:
#            validated = self.schema.deserialize(cstruct)
#        except colander.Invalid, e:
#            errors = e.asdict()
#            log.warn(errors)
#            raise ValidationFailure(errors)
#        return validated
#
#def get_estimation_line(lines, _id):
#    """
#        Return an estimation_line object matching the _id
#    """
#    for line in lines:
#        if line['id'] == _id:
#            return line
#    return EstimationLine()
#
#def merge_line(line, estimation_lines):
#    """
#        Merge a line with an estimation_line sqla object if needed
#    """
#    pass
#
#def merge_appstruct_todatabase(datas, task=None,
#                                      estimation=None,
#                                      estimation_lines=[],
#                                      payment_conditions=None):
#    """
#        Build/update sqla elements from validated datas
#        Input : datas and sqla objects
#        Output : updated sqla objects
#        Note: find a way to match estimation_lines with workline ids
#    """
#    estimation.name = datas['estimation']['name']
#    for line in datas['estimation_line']:
#        if line.has_key('idworkline'):
#            merge_line(line, estimation_lines)
