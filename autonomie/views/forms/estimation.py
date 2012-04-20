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

    def toschema(self, dbdatas, dest_dict):
        """
            convert db dict fashionned datas to the appropriate sections
            to fit the EstimationSchema
        """
        for field, section in self.matching_map:
            value = dbdatas.get(self.dbtype,{}).get(field)
            if value is not None:
                dest_dict.setdefault(section, {})[field] = value
        return dest_dict

    def todb(self, schemadatas, dest_dict):
        """
            convert colander deserialized datas to database dest_dict
        """
        for field, section in self.matching_map:
            value = schemadatas.get(section, {}).get(field, None)
            if value is not None or colander.null:
                dest_dict.setdefault(self.dbtype, {})[field] = value
        return dest_dict

class EstimationMatch(MappingWrapper):
    matching_map = (
                         ('id_phase','common'),
                         ('taskDate','common'),
                         ('description', 'common'),
                         ('course', 'common'),
                         ('tva', 'lines'),
                         ('discountHT', 'lines'),
                         ('expenses', 'lines'),
                         ('exclusions', 'notes'),
                         ('paymentDisplay', 'payments'),
                         ('deposit', 'payments'),
                         )
    dbtype = 'estimation'

class SequenceWrapper:
    """
        Maps the db models with colander Sequence Schemas
    """
    mapping_name = ''
    sequence_name = ''
    dbtype = ''
    fields = None
    sort_key = 'rowIndex'
    def toschema(self, dbdatas, dest_dict):
        """
            Build schema expected datas from list of elements
        """
        lineslist = dbdatas.get(self.dbtype, [])
        print lineslist
        for line in sorted(lineslist, key=lambda line:int(line[self.sort_key])):
            dest_dict.setdefault(self.mapping_name, {})
            dest_dict[self.mapping_name].setdefault(self.sequence_name, []).append(
                    dict((key, value)for key, value in line.items()
                                              if key in self.fields)
                    )
        return dest_dict

    def todb(self, shemadatas, dest_dict):
        """
            convert colander deserialized datas to database dest_dict
        """
        all_ = dest_dict.get(self.mapping_name, {}).get(self.sequence_name, [])
        for index, line in enumerate(all_):
            dest_dict.setdefault(self.dbtype, [])
            line[self.sort_key] = str(index)
            dest_dict[self.db_type].append(line)
        return dest_dict

class EstimationLinesMatch(SequenceWrapper):
    mapping_name = 'lines'
    sequence_name = 'lines'
    fields = ('description', 'cost', 'quantity', 'unity',)
    dbtype = 'estimation_lines'

class PaymentLinesMatch(SequenceWrapper):
    mapping_name = 'payments'
    sequence_name = 'payment_lines'
    fields = ('description', 'paymentDate', 'amount',)
    dbtype = "payment_lines"

def get_schemadata(dbdatas):
    """
        return Estimation-compatible schemadatas
    """
    datas = {}
    for matchobj in (EstimationMatch, EstimationLinesMatch, \
                                                        PaymentLinesMatch):
        datas = matchobj().toschema(dbdatas, datas)
    return datas
