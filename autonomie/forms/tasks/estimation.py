# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
from colanderalchemy import SQLAlchemySchemaNode
from autonomie.forms.custom_types import (
    QuantityType,
    AmountType,
    Integer,
)

from autonomie_base.models.base import DBSESSION
from autonomie.models.task import Estimation
from autonomie import forms
from autonomie.models.task import (
    WorkUnit,
    TaskMention,
)
from autonomie.models.tva import (
    Tva,
    Product,
)
from autonomie.models.task.estimation import (
    PAYMENTDISPLAYCHOICES
)


@colander.deferred
def deferred_unity_validator(node, kw):
    return colander.OneOf([workunit.label for workunit in WorkUnit.query()])


@colander.deferred
def deferred_tva_validator(node, kw):
    query = DBSESSION().query(Tva.value).all()
    options = [option[0] for option in query]
    return colander.OneOf(options)


@colander.deferred
def deferred_product_validator(node, kw):
    return colander.OneOf([item.id for item in Product.query()])


def taskline_validator(form, value):
    product_id = value['product_id']
    product = Product.get(product_id)
    tva = value['tva']
    if tva.value != product.tva.value:
        exc = colander.Invalid(form, u"Le produit ne correspond pas à la TVA")
        raise exc


class TaskLine(colander.MappingSchema):
    """
        A single estimation line
    """
    description = colander.SchemaNode(
        colander.String(),
        title=u"Prestation"
    )
    cost = colander.SchemaNode(AmountType(5), title=u"Prix/unité")
    quantity = colander.SchemaNode(
        QuantityType(),
        validator=forms.positive_validator
    )
    unity = colander.SchemaNode(
        colander.String(),
        title=u"Unité",
        validator=deferred_unity_validator,
    )
    tva = colander.SchemaNode(
        Integer(),
        validator=deferred_tva_validator,
        title=u'TVA',
    )
    product_id = colander.SchemaNode(
        colander.Integer(),
        validator=deferred_product_validator,
        title=u"Produit",
    )


class DiscountLine(colander.MappingSchema):
    """
        A single estimation line
    """
    description = colander.SchemaNode(
        colander.String(),
        title=u"Prestation"
    )
    amount = colander.SchemaNode(
        AmountType(5),
        title=u"Prix/unité",
        validator=forms.positive_validator,
    )

    tva = colander.SchemaNode(
        Integer(),
        title=u'TVA',
        validator=deferred_tva_validator
    )


class TaskLines(colander.SequenceSchema):
    """
        Sequence of task lines
    """
    taskline = TaskLine(validator=taskline_validator)


class DiscountLines(colander.SequenceSchema):
    """
        Sequence of discount lines
    """
    discountline = DiscountLine()


class TaskLineGroupMapping(colander.MappingSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=u"Titre de l'ouvrage",
        missing=u""
    )
    description = colander.SchemaNode(
        colander.String(),
        title=u"Description",
        missing=u'',
    )
    lines = TaskLines()


class TaskLineGroupSeq(colander.SequenceSchema):
    groups = TaskLineGroupMapping(
        title=u"Ouvrage",
    )


class TaskLinesBlock(colander.MappingSchema):
    """
        Fieldset containing the "Détail de la prestation" block
        with estimation and invoice lines and all the stuff
    """
    groups = TaskLineGroupSeq(
        title=u"",
        validator=colander.Length(min=1),
    )
    discounts = DiscountLines(
        title=u'',
    )
    expenses_ht = colander.SchemaNode(
        AmountType(5),
        title=u"Frais forfaitaires (HT)",
        missing=0,
        validator=forms.positive_validator,
    )


@colander.deferred
def deferred_mention_validator(node, kw):
    return colander.ContainsOnly(
        [item.id for item in DBSESSION().query(TaskMention.id)]
    )


class TaskSchema(colander.MappingSchema):
    """
        Main fields to be configured
    """
    address = forms.textarea_node(
        title=u"Nom et adresse du client",
        widget_options={'rows': 4},
        validator=forms.textarea_node_validator
    )
    workplace = forms.textarea_node(
        title=u"Lieu d'exécution des travaux",
        widget_options={'rows': 3},
        missing=colander.drop,
    )
    mention_ids = colander.SchemaNode(
        colander.Set(),
        title=u"Mentions facultatives",
        description=u"Choisissez les mentions à ajouter au document",
        missing=colander.drop,
        validator=deferred_mention_validator
    )
    date = forms.today_node(title=u"Date du devis")
    description = colander.SchemaNode(
        colander.String(),
        title=u"Objet du devis",
        validator=forms.textarea_node_validator,
    )
    course = colander.SchemaNode(
        colander.Integer(),
        title=u"",
        missing=0,
    )
    display_units = colander.SchemaNode(
        colander.Integer(),
        title="Afficher le détail des prestations dans la sortie PDF ?",
        missing=0,
    )
    exclusions = forms.textarea_node(
        title=u'Notes',
        missing=u"",
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


class EstimationPaymentLine(colander.MappingSchema):
    """
        Payment line
    """
    description = colander.SchemaNode(
        colander.String(),
        default=u"Solde",
    )
    date = forms.today_node()
    amount = colander.SchemaNode(AmountType(5), default=0)


class EstimationPaymentLines(colander.SequenceSchema):
    """
        Sequence of payment lines
    """
    line = EstimationPaymentLine()


class EstimationSchema(TaskSchema):
    """
        Gestion des acomptes
    """
    deposit = colander.SchemaNode(
        colander.Integer(),
        title=u"Acompte à la commande",
        default=0,
    )
    payment_times = colander.SchemaNode(
        colander.Integer(),
        title=u"Paiement en ",
        default=1,
    )
    paymentDisplay = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf([x[0] for x in PAYMENTDISPLAYCHOICES]),
        title=u"Affichage des paiements",
        default="SUMMARY",
    )
    payment_lines = EstimationPaymentLines(
        title=u'',
        description=u"Définissez les échéances de paiement"
    )
    payment_conditions_select = colander.SchemaNode(
        colander.String(),
        title=u"Conditions de paiement prédéfinies",
        missing=colander.drop,
    )

    payment_conditions = forms.textarea_node(
        title=u"Conditions de paiement",
        validator=forms.textarea_node_validator
    )


def validate_estimation(estimation_object, request):
    """
    Globally validate an estimation_object

    :param obj estimation_object: An instance of Estimation
    :param obj request: The pyramid request
    :raises: colander.Invalid

    try:
        validate_estimation(est, self.request)
    except colander.Invalid as err:
        error_messages = err.messages
    """
    schema = SQLAlchemySchemaNode(Estimation)
    schema = schema.bind(request=request)
    appstruct = estimation_object.__json__(request)
    cstruct = schema.deserialize(appstruct)
    return cstruct
