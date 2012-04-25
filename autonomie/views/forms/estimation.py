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
import datetime

import colander
from deform import widget

from .utils import get_date_input

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

def specialfloat(self, value):
    """
        preformat the value before passing it to the float function
    """
    if isinstance(value, unicode):
        value = value.replace(u'€', '').replace(u',', '.').replace(u' ', '')
    return float(value)

class QuantityType(colander.Number):
    """
        Preformat unicode supposed to be numeric entries
    """
    num = specialfloat

class AmountType(colander.Number):
    """
        preformat an amount before considering it as a float object
        then *100 to store it into database
    """
    num = specialfloat
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null

        try:
            return str(self.num(appstruct) / 100.0)
        except Exception:
            raise colander.Invalid(node,
                          u"\"${val}\" n'est pas un montant valide".format(
                                val=appstruct),
                          )
    def deserialize(self, node, cstruct):
        if cstruct != 0 and not cstruct:
            return colander.null

        try:
            return self.num(cstruct) * 100.0
        except Exception:
            raise colander.Invalid(node,
                          u"\"${val}\" n'est pas un montant valide".format(
                            val=cstruct)
                          )

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
    quantity = colander.SchemaNode(QuantityType(),
            widget=widget.TextInputWidget(
                template='autonomie:deform_templates/lineblock/lineinput.mako',
                ),
            css_class='span1'
            )
    unity = colander.SchemaNode(
                colander.String(),
                widget=widget.SelectWidget(
                    values=DAYS,
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
    IDPhase = colander.SchemaNode(
                colander.String(),
                title=u"Phase où insérer le devis",
                widget=get_deferred_choices_widget('phases'),
                )
    taskDate = colander.SchemaNode(
                colander.Date(),
                title=u"Date du devis",
                widget=get_date_input(),
                default=datetime.date.today()
#                description=u"Date d'émission du devis"
                )
    description = colander.SchemaNode(
                colander.String(),
                title=u"Objet du devis",
                widget=widget.TextAreaWidget(css_class="span8"),
                )
    course = colander.SchemaNode(colander.Integer(),
                title=u"Formation ?",
                description=u"Ce devis concerne-t-il une formation ?",
                widget=widget.CheckboxWidget(true_val=1, false_val=0))
    displayedUnits = colander.SchemaNode(colander.Integer(),
                title=u"Afficher le détail",
                description=u"Afficher le détail des prestations dans le PDF ?",
                widget=widget.CheckboxWidget(true_val=1, false_val=0))

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
                         ('paymentDisplay', 'payments'),
                         ('deposit', 'payments'),
                         ('paymentConditions', 'comments')
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

def get_appstruct(dbdatas):
    """
        return EstimationSchema-compatible appstruct
    """
    appstruct = {}
    for matchobj in (EstimationMatch, EstimationLinesMatch, PaymentLinesMatch):
        appstruct = matchobj().toschema(dbdatas, appstruct)
    appstruct = set_payment_times(appstruct, dbdatas)
    return appstruct

def get_dbdatas(appstruct):
    """
        return dict with db compatible datas
    """
    dbdatas = {}
    for matchobj in (EstimationMatch, EstimationLinesMatch, PaymentLinesMatch):
        dbdatas = matchobj().todb(appstruct, dbdatas)
    dbdatas = set_manualDeliverables(appstruct, dbdatas)
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

# NOTE ON COMPUTING
#
# Since the datas stored in the database are stored in *100 format
# We are now working with integers only
#
# TVA is stored as an integer too,
#
class EstimationComputingModel:

    def __init__(self, estimation_model):
        self.model = estimation_model

    @staticmethod
    def compute_line_total(line):
        """
            compute estimation line total
        """
        cost = line.cost
        quantity = line.quantity
        return cost * quantity

    def compute_lines_total(self):
        """
            compute the estimations line total
        """
        return sum(self.compute_line_total(line) for line in self.model.lines)

    def compute_totalht(self):
        """
            compute the ht total
        """
        return self.compute_lines_total() - self.model.discountHT

    def compute_ttc(self):
        """
            compute the ttc value before expenses
        """
        totalht = self.compute_totalht()
        tva_amount = int(totalht * (max(self.model.tva, 0.0) / 10000.0))
        return totalht + tva_amount

    def compute_total(self):
        """
            compute the total amount
        """
        return self.compute_ttc() - self.model.expenses

    def compute_deposit(self):
        """
            Compute the amount of the deposit
        """
        if self.model.deposit > 0:
            total = self.compute_total()
            return int(total * self.model.deposit / 100.0)
        return 0

    def get_nb_payment_lines(self):
        return len(self.model.payment_lines)

    def compute_line_amount(self):
        """
            Compute payment lines amounts in case of equal division
            (when manualDeliverables is 0)
            (when the user has checked 3 times)
        """
        total = self.compute_total()
        deposit = self.compute_deposit()
        rest = total - deposit
        return int(rest / self.get_nb_payment_lines())

    def compute_sold(self):
        """
            Compute the sold amount to finish on an exact value
            if we divide 10 in 3, we'd like to have something like :
                3.33 3.33 3.34
        """
        total = self.compute_total()
        deposit = self.compute_deposit()
        rest = total - deposit
        payment_lines_num = self.get_nb_payment_lines()
        if payment_lines_num == 1:
            print "passing Here"
            return rest
        else:
            if self.model.manualDeliverables == 0:
                print "passing there"
                line_amount = self.compute_line_amount()
                return rest - ((payment_lines_num-1) * line_amount)
            else:
                print "passing everywhere"
                print rest
                return rest - sum(line.amount \
                        for line in self.model.payment_lines[:-1])
