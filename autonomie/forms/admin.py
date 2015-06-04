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
    Form schemes for administration
"""
import os
import colander
import logging
import simplejson as json
import deform

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.config import Config
from autonomie.models.competence import (
    CompetenceScale,
)
from autonomie import forms
from autonomie.forms import files
from autonomie.forms.validators import validate_image_mime
from autonomie.utils.image import ImageResizer


from .custom_types import AmountType

log = logging.getLogger(__name__)


HEADER_RESIZER = ImageResizer(4, 1)


TEMPLATES_URL = 'autonomie:deform_templates/'


def get_deferred_upload_widget(filename, filters=None):
    @colander.deferred
    def deferred_upload_widget(node, kw):
        """
            Returns a fileupload widget to allow logo upload
        """
        request = kw['request']

        root_url = "/assets/"
        store_url = os.path.join(root_url, "main")

        root_path = request.registry.settings.get('autonomie.assets')
        store_path = os.path.join(root_path, "main")

        return forms.get_fileupload_widget(
            store_url,
            store_path,
            request.session,
            default_filename=filename,
            filters=filters)

    return deferred_upload_widget


class EstimationConfig(colander.MappingSchema):
    """
        Schema for estimation configuration
    """
    header = forms.textarea_node(
        title=u"Cadre d'information spécifique (en entête des devis)",
        missing=u"",
    )
    footer = forms.textarea_node(
        title=u"Informations sur l'acceptation des devis",
        missing=u"",
    )


class InvoiceConfig(colander.MappingSchema):
    """
        Schema for invoice configuration
    """
    prefix = colander.SchemaNode(
        colander.String(),
        title=u"Préfixer les numéros de facture",
        missing=u"")
    header = forms.textarea_node(
        title=u"Cadre d'information spécifique (en entête des factures)",
        missing=u"",
    )
    payment = forms.textarea_node(
        title=u"Information de paiement pour les factures",
        missing=u"",
    )
    late = forms.textarea_node(
        title=u"Informations sur les délais de paiement",
        missing=u"",
    )


class DocumentConfig(colander.MappingSchema):
    """
        Schema for document (estimation/invoice ...) configuration
    """
    cgv = forms.textarea_node(
        title=u"Conditions générales de vente",
        description=u"Les conditions générales sont placées en dernière \
page des documents (devis/factures/avoirs)",
        missing=u'',
        richwidget=True,
    )
    footertitle = forms.textarea_node(
        title=u"Titre du pied de page",
        missing=u"",
    )
    footercourse = forms.textarea_node(
        title=u"Pied de page des documents liées aux formations",
        missing=u"",
    )
    footercontent = forms.textarea_node(
        title=u"Contenu du pied de page",
        missing=u"",
    )

    estimation = EstimationConfig(title=u'Devis')
    invoice = InvoiceConfig(title=u"Factures")


class FileTypeConfig(colander.SequenceSchema):
    name = colander.SchemaNode(
        colander.String(),
        title=u"",
    )


class FileTypesConfig(colander.MappingSchema):
    """
        Configure file types that may be attached
    """
    types = FileTypeConfig(
        title=u"Libellé",
        description=u"Utilisé dans les interfaces de dépôt de document pour \
spécifier un type (PV de travaux, Bdc ...). Ces libellés permettent \
d'identifier plus facilement les documents attachés aux factures",
    )


class SiteConfig(colander.MappingSchema):
    """
        Site configuration
        logos ...
    """
    logo = colander.SchemaNode(
        deform.FileData(),
        widget=files.deferred_upload_widget,
        title=u"Choisir un logo",
        validator=validate_image_mime,
        missing=colander.drop,
        description=u"Charger un fichier de type image *.png *.jpeg \
*.jpg ...")
    welcome = forms.textarea_node(
        title=u"Texte d'accueil",
        richwidget=True,
        missing=u'',
        admin=True,
    )


class MainConfig(colander.MappingSchema):
    """
        Schema for forms.site configuration
    """
    site = SiteConfig()
    document = DocumentConfig(title=u'Document (devis et factures)')
    attached_filetypes = FileTypesConfig(title=u"Type des documents attachés")


class Product(colander.MappingSchema):
    """
        Form schema for a single product configuration
    """
    id = forms.id_node()
    name = colander.SchemaNode(colander.String(), title=u"Libellé")
    compte_cg = colander.SchemaNode(colander.String(), title=u"Compte CG")


class ProductSequence(colander.SequenceSchema):
    product = Product(
        title=u"Compte produit",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )


class TvaItem(colander.MappingSchema):
    """
        Allows Tva configuration
    """
    id = forms.id_node()
    name = colander.SchemaNode(
        colander.String(),
        title=u"Libellé du taux de TVA",
        css_class='col-md-2')
    value = colander.SchemaNode(
        AmountType(),
        title=u"Montant",
        css_class='col-md-2')
    compte_cg = colander.SchemaNode(
        colander.String(),
        missing="",
        title=u"Compte CG de Tva")
    code = colander.SchemaNode(
        colander.String(),
        missing="",
        title=u"Code de Tva")
    default = colander.SchemaNode(
        colander.Integer(),
        title=u"Valeur par défaut ?",
        widget=deform.widget.CheckboxWidget(true_val="1", false_val="0"))
    products = ProductSequence(
        title=u"",
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + "clean_sequence.pt",
            orderable=False,
        ),
    )


class TvaSequence(colander.SequenceSchema):
    tva = TvaItem(
        title=u"Taux de Tva",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )


class TvaConfig(colander.MappingSchema):
    tvas = TvaSequence(
        title=u"",
        missing=u'',
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + "clean_sequence.pt",
            orderable=True,
        ),
    )


TVA_UNIQUE_VALUE_MSG = u"Veillez à utiliser des valeurs différentes pour les \
différents taux de TVA. Pour les tvas de valeurs nulles, merci d'utiliser des \
valeurs négatives pour les distinguer (-1, -2...), elles seront ramenées à 0 \
pour toutes les opérations de calcul."


TVA_NO_DEFAULT_SET_MSG = u"Veuillez définir au moins une tva par défaut."


def tva_form_validator(form, values):
    """
    Ensure we've got a unique tva value and at least one default tva in our form
    """
    vals = []
    default = False
    for tva in values['tvas']:
        if tva['value'] in vals:
            message = TVA_UNIQUE_VALUE_MSG
            raise colander.Invalid(form, message)
        vals.append(tva['value'])

        if tva['default'] == 1:
            default = True
    if not default:
        message = TVA_NO_DEFAULT_SET_MSG
        raise colander.Invalid(form, message)


def get_tva_config_schema():
    return TvaConfig(
        title=u"Configuration des taux de TVA",
        validator=tva_form_validator
    )


class PaymentModeSequence(colander.SequenceSchema):
    """
        Single payment mode configuration scheme
    """
    label = colander.SchemaNode(
        colander.String(),
        title=u"Libellé",
    )


class PaymentModeConfig(colander.MappingSchema):
    """
        Main configuration form model
    """
    paymentmodes = PaymentModeSequence(
        title=u"",
        missing=u"",
        widget=deform.widget.SequenceWidget(
            orderable=True,
            template=TEMPLATES_URL + "clean_sequence.pt",
        )
    )


class WorkUnitSequence(colander.SequenceSchema):
    """
        Single work untit configuration scheme
    """
    label = colander.SchemaNode(
        colander.String(),
        title=u"Libellé"
    )


class WorkUnitConfig(colander.MappingSchema):
    """
        Main configuration form model
    """
    workunits = WorkUnitSequence(
        title=u"",
        missing=u"",
        widget=deform.widget.SequenceWidget(
            orderable=True,
            template=TEMPLATES_URL + "clean_sequence.pt",
        )
    )


class ExpenseConfig(colander.MappingSchema):
    """
        Schema for the configuration of different expense types
    """
    id = forms.id_node()
    active = colander.SchemaNode(
        colander.Boolean(),
        title=u"Actif",
        default=True,
        description=u"En décochant cette entrée, elle n'apparaîtra plus dans \
l'interface, mais restera associée aux notes de frais existantes."
    )

    label = colander.SchemaNode(
        colander.String(),
        title=u"Libellé",
        validator=colander.Length(max=50))

    code = colander.SchemaNode(
        colander.String(),
        title=u"Compte de charge de la dépense",
        validator=colander.Length(max=15))

    code_tva = colander.SchemaNode(
        colander.String(),
        title=u"Code TVA (si nécessaire)",
        missing="",
        validator=colander.Length(max=15))

    compte_tva = colander.SchemaNode(
        colander.String(),
        title=u"Compte de TVA déductible",
        missing="",
        validator=colander.Length(max=15))

    contribution = colander.SchemaNode(
        colander.Boolean(),
        title=u"Contribution",
        description=u"Ce type de frais est-il intégré dans la contribution \
à la CAE ?",
        )


class ExpenseKmConfig(ExpenseConfig):
    """
        Schema for the configuration of vehicle related expenses
    """
    amount = colander.SchemaNode(
        colander.Float(),
        title=u"Tarif",
        description=u"Tarif au km")


class ExpenseTelConfig(ExpenseConfig):
    """
        Schema for telefonic expenses
    """
    percentage = colander.SchemaNode(
        colander.Integer(),
        title=u"Pourcentage remboursé",
        validator=colander.Range(1, 100))
    initialize = colander.SchemaNode(
        colander.Boolean(),
        title=u"Créer une entrée par défaut ?",
        description=u"Une ligne sera automatiquement ajoutée à la feuille \
de notes de frais",
        default=True)


class ExpensesConfig(colander.SequenceSchema):
    """
        The sequence Schema associated with the ExpenseConfig
    """
    expense = ExpenseConfig(
        title=u"",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        ),
    )


class ExpensesKmConfig(colander.SequenceSchema):
    """
        The sequence Schema associated with the ExpenseKmConfig
    """
    expense = ExpenseKmConfig(
        title=u"",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        ),
    )


class ExpensesTelConfig(colander.SequenceSchema):
    """
        The sequence Schema associated with the ExpenseTelConfig
    """
    expense = ExpenseTelConfig(
        title=u"",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        ),
    )


class ExpenseTypesConfig(colander.MappingSchema):
    """
        Expense Configuration form schema
    """
    code_journal = colander.SchemaNode(
        colander.String(),
        title=u"Code journal utilisés pour notes de dépenses",
        description=u"Le code journal pour les notes de frais",
        missing="",
    )
    compte_cg = colander.SchemaNode(
        colander.String(),
        title=u"Compte de tiers (classe 4) pour dépenses dues aux \
entrepreneurs",
        description=u"Le compte général pour les notes de frais",
        missing="",
        )
    expenses = ExpensesConfig(
        title=u'Dépenses',
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + "clean_sequence.pt",
            add_subitem_text_template=u"Ajouter une dépense",
        )
    )
    expenseskm = ExpensesKmConfig(
        title=u"Frais kilométriques",
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + "clean_sequence.pt",
            add_subitem_text_template=u"Ajouter des frais kilométriques",
        )
    )
    expensestel = ExpensesTelConfig(
        title=u"Frais téléphoniques",
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + "clean_sequence.pt",
            add_subitem_text_template=u"Ajouter des frais téléphoniques",
        )
    )


class ActivityTypeConfig(colander.MappingSchema):
    """
        Schema for the configuration of different activity types
    """
    id = forms.id_node()

    label = colander.SchemaNode(
        colander.String(),
        title=u"Libellé",
        validator=colander.Length(max=100)
        )


class ActivityTypesSeqConfig(colander.SequenceSchema):
    """
        The sequence Schema associated with the ActivityTypeConfig
    """
    activity_type = ActivityTypeConfig(
        title=u"Nature du rendez-vous",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )


class ActivityModeConfig(colander.MappingSchema):
    label = colander.SchemaNode(
        colander.String(),
        title=u"libellé",
        validator=colander.Length(max=100)
        )


class ActivityModesSeqConfig(colander.SequenceSchema):
    """
    Sequence schema for activity modes configuration
    """
    activity_mode = ActivityModeConfig(
        title=u"Mode d'entretien",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )


class ActionConfig(colander.MappingSchema):
    id = forms.id_node()
    label = colander.SchemaNode(
        colander.String(),
        title=u"Sous-titre",
        description=u"Sous-titre dans la sortie pdf",
        validator=colander.Length(max=100)
        )


class ActivitySubActionSeq(colander.SequenceSchema):
    subaction = ActionConfig(
        title=u"",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )


class ActivityActionConfig(colander.Schema):
    id = forms.id_node()
    label = colander.SchemaNode(
        colander.String(),
        title=u"Titre",
        description=u"Titre dans la sortie pdf",
        validator=colander.Length(max=255)
    )
    children = ActivitySubActionSeq(
        title=u"",
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + "clean_sequence.pt",
            add_subitem_text_template=u"Ajouter un sous-titre",
        )
    )


class ActivityActionSeq(colander.SequenceSchema):
    action = ActivityActionConfig(
        title=u"Titre",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )


class WorkshopInfo3(colander.MappingSchema):
    id = forms.id_node()
    label = colander.SchemaNode(
        colander.String(),
        title=u"Sous-titre 2",
        description=u"Sous-titre 2 dans la sortie pdf",
        validator=colander.Length(max=100)
    )


class WorkshopInfo3Seq(colander.SequenceSchema):
    child = WorkshopInfo3(
        title=u"Sous-titre 2",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )


class WorkshopInfo2(colander.Schema):
    id = forms.id_node()
    label = colander.SchemaNode(
        colander.String(),
        title=u"Sous-titre",
        description=u"Sous-titre dans la sortie pdf",
        validator=colander.Length(max=255)
    )
    children = WorkshopInfo3Seq(
        title=u"",
        widget=deform.widget.SequenceWidget(
            add_subitem_text_template=u"Ajouter un sous-titre 2",
            orderable=True,
            template=TEMPLATES_URL + "clean_sequence.pt",
        )
    )


class WorkshopInfo2Seq(colander.SequenceSchema):
    child = WorkshopInfo2(
        title=u"Sous-titre",
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )


class WorkshopInfo1(colander.Schema):
    id = forms.id_node()
    label = colander.SchemaNode(
        colander.String(),
        title=u"Titre",
        description=u"Titre dans la sortie pdf",
        validator=colander.Length(max=255)
    )
    children = WorkshopInfo2Seq(
        title=u'',
        widget=deform.widget.SequenceWidget(
            add_subitem_text_template=u"Ajouter un sous-titre",
            orderable=True,
            template=TEMPLATES_URL + "clean_sequence.pt",
        )
    )


class WorkshopInfo1Seq(colander.SequenceSchema):
    actions = WorkshopInfo1(
        title=u'Titre',
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )


def get_file_dl_node(title, additionnal_description=""):
    """
    Return a file download node
    """
    description = u"Charger un fichier de type image *.png *.jpeg *.jpg ... \
{0}".format(additionnal_description)

    return colander.SchemaNode(
        deform.FileData(),
        widget=files.deferred_upload_widget,
        title=title,
        validator=validate_image_mime,
        missing=colander.drop,
        description=description,
    )


class ActivityConfigSchema(colander.Schema):
    """
    The schema for activity types configuration
    """
    header_img = get_file_dl_node(title=u'En-tête des sortie PDF')
    footer_img = get_file_dl_node(
        u'Image du pied de page des sorties PDF',
        u"Vient se placer au-dessus du texte du pied de page",
    )
    footer = forms.textarea_node(
        title=u"Texte du pied de page des sorties PDF",
        missing=u"",
    )
    types = ActivityTypesSeqConfig(
        title=u"Configuration des natures de rendez-vous",
        widget=deform.widget.SequenceWidget(
            add_subitem_text_template=u"Ajouter une nature de rendez-vous ",
            orderable=True,
            template=TEMPLATES_URL + "clean_sequence.pt",
        )
    )
    modes = ActivityModesSeqConfig(
        title=u"Configuration des modes d'entretien",
        widget=deform.widget.SequenceWidget(
            add_subitem_text_template=u"Ajouter un mode d'entretien",
            orderable=True,
            template=TEMPLATES_URL + "clean_sequence.pt",
        )
    )
    actions = ActivityActionSeq(
        title=u"Configuration des titres disponibles pour la sortie PDF",
        widget=deform.widget.SequenceWidget(
            add_subitem_text_template=u"Ajouter un titre",
            orderable=True,
            template=TEMPLATES_URL + "clean_sequence.pt",
        )
    )


class WorkshopConfigSchema(colander.Schema):
    header_img = get_file_dl_node(title=u'En-tête des sortie PDF')
    footer_img = get_file_dl_node(
        u'Image du pied de page des sorties PDF',
        u"Vient se placer au-dessus du texte du pied de page",
    )
    footer = forms.textarea_node(
        title=u"Texte du pied de page des sorties PDF",
        missing=u"",
    )
    actions = WorkshopInfo1Seq(
        title=u"Configuration des titres disponibles pour la sortie PDF",
        widget=deform.widget.SequenceWidget(
            add_subitem_text_template=u"Ajouter une titre",
            orderable=True,
            template=TEMPLATES_URL + "clean_sequence.pt",
        )
    )


class CaeConfig(colander.MappingSchema):
    """
        Cae configuration form schema
    """
    pass


class SageExportConfig(colander.MappingSchema):
    """
        Sage export modules selection form schema
    """
    pass


def build_cae_config_schema():
    fields = (
        (
            'code_journal',
            u"Code journal ventes",
            u"Le code du journal dans Sage",
        ),
        (
            'numero_analytique',
            u"Numéro analytique de la CAE",
            "",
        ),

        (
            'compte_cg_contribution',
            u"Compte CG contribution",
            u"Compte CG correspondant à la contribution des entrepreneurs à \
la CAE"
        ),
        (
            'compte_rrr',
            u"Compte RRR",
            u"Compte Rabais, Remises et Ristournes",
        ),
        (
            'compte_frais_annexes',
            u"Compte de frais annexes",
            '',
        ),
        (
            'compte_cg_banque',
            u"Compte banque de l'entrepreneur",
            "",
        ),

        (
            'compte_cg_assurance',
            u"Compte de charge assurance",
            u"Requis pour le module d'écritures Assurance",
        ),
        (
            'compte_cgscop',
            u"Compte de charge CG Scop",
            u"Requis pour le module d'écritures CGSCOP",
        ),
        (
            'compte_cg_debiteur',
            u"Compte de contrepartie pour CG Scop et Assurance",
            u"Requis pour le module d'écritures CGSCOP",
        ),
        (
            'compte_cg_organic',
            u"Compte de charge Organic",
            u"Compte CG pour la contribution à l'Organic (requis pour le module \
    d'écritures Contribution Organic)",
        ),
        (
            'compte_cg_debiteur_organic',
            u"Compte de contrepartie Organic",
            u"Compte CG de débiteur pour la contribution à l'Organic (requis pour \
    le module d'écritures Contribution Organic)",
        ),
        (
            'compte_rg_interne',
            u"Compte RG Interne",
            u"Requis pour les écritures RG Interne",
        ),
        (
            'compte_rg_externe',
            u"Compte RG Externe",
            u"Requis pour le module d'écriture RG Client",
        ),
        (
            'compte_cg_tva_rrr',
            u"Compte CG de TVA spécifique aux RRR",
            u"Facultatif, les remises apparaitront dans les écritures si cette \
    valeur et le code tva sont renseignés.",
        ),
        (
            'code_tva_rrr',
            u"Code de TVA spécifique aux RRR",
            u"Facultatif, les remises apparaitront dans les écritures si cette \
    valeur et le compte CG sont renseignés.",
        ),


        (
            "contribution_cae",
            u"Pourcentage de la contribution",
            u"Valeur par défaut de la contribution (nombre entre 0 et 100). \
            Elle peut être individualisée sur les pages entreprises",
        ),
        (
            "taux_assurance",
            u"Taux d'assurance",
            u"(nombre entre 0 et 100) Requis pour le module d'écritures \
Assurance",
        ),
        (
            "taux_cgscop",
            u"Taux CGSCOP",
            u"(nombre entre 0 et 100) Requis pour le module d'écritures CGSCOP",
        ),
        (
            "taux_contribution_organic",
            u"Taux de Contribution à l'Organic",
            u"(nombre entre 0 et 100) Requis pour le module d'écritures \
    Contribution Organic",
        ),
        (
            "taux_rg_interne",
            u"Taux RG Interne",
            u"(nombre entre 0 et 100) Requis pour les écritures RG Interne",
        ),
        (
            "taux_rg_client",
            u"Taux RG Client",
            u"(nombre entre 0 et 100) Requis pour le module d'écriture RG \
Client",
        ),
    )
    schema = CaeConfig().clone()
    for key, title, description in fields:
        schema.add(
            colander.SchemaNode(
                colander.String(),
                title=title,
                description=description,
                missing=u"",
                name=key
            )
        )

    export_modules = (
        (
            "sage_contribution",
            u"Module contribution",
            u"",),
        (
            'sage_assurance',
            u"Module assurance",
            u"",),
        (
            'sage_cgscop',
            u"Module CGSCOP",
            u"",),
        (
            'sage_organic',
            u"Module Contribution organic",
            u"",),
        (
            'sage_rginterne',
            u"Module RG Interne",
            u"",),
        (
            'sage_rgclient',
            u"Module RG Client",
            u"",
        ),
    )
    export_schema = SageExportConfig(
        title=u"Activation des modules d'export Sage",
        name='sage_export').clone()
    export_schema.add(
        colander.SchemaNode(
            colander.String(),
            widget=deform.widget.CheckboxWidget(
                template='autonomie:deform_templates/checkbox_readonly.pt',
                ),
            title=u"Module facturation",
            description=u"activé par défaut",
            name="sage_facturation_not_used",
            )
        )
    for key, title, description in export_modules:
        export_schema.add(
            colander.SchemaNode(
                colander.String(),
                widget=deform.widget.CheckboxWidget(
                    true_val="1",
                    false_val="0",
                ),
                title=title,
                description=description,
                name=key)
        )
    schema.add(export_schema)

    return schema


CAECONFIG = build_cae_config_schema()


def get_config_appstruct(request, config_dict, logo):
    """
        transform Config datas to ConfigSchema compatible appstruct
    """
    appstruct = {
        'site':     {'welcome': ''},
        'document': {'estimation':  {
                                    'header': '',
                                    'footer': '',
                                    },
                     'invoice':     {
                                    'prefix': '',
                                    'header': '',
                                    'payment': '',
                                     'late': ''},
                     'footertitle': '',
                     'footercourse': '',
                     'footercontent': '',
                     'cgv': ''},
        "attached_filetypes": {}
    }
    if logo is not None:
        appstruct['site']['logo'] = {
            'uid': logo.id,
            'filename': logo.name,
            'preview_url': request.route_path(
                'public',
                name="logo.png",
            )
        }
    appstruct['site']['welcome'] = config_dict.get('welcome', '')
    appstruct['document']['footertitle'] = config_dict.get(
        'coop_pdffootertitle', ''
    )
    appstruct['document']['footercourse'] = config_dict.get(
        'coop_pdffootercourse', ''
    )
    appstruct['document']['footercontent'] = config_dict.get(
        'coop_pdffootertext', ''
    )
    appstruct['document']['cgv'] = config_dict.get('coop_cgv', '')

    appstruct['document']['estimation']['header'] = config_dict.get(
        'coop_estimationheader', ''
    )
    appstruct['document']['estimation']['footer'] = config_dict.get(
        'coop_estimationfooter', ''
    )

    appstruct['document']['invoice']['prefix'] = config_dict.get(
        'invoiceprefix', ''
    )
    appstruct['document']['invoice']['header'] = config_dict.get(
        'coop_invoiceheader', ''
    )
    appstruct['document']['invoice']['payment'] = config_dict.get(
        'coop_invoicepayment', ''
    )
    appstruct['document']['invoice']['late'] = config_dict.get(
        'coop_invoicelate', ''
    )

    appstruct["attached_filetypes"]['types'] = json.loads(
            config_dict.get('attached_filetypes', "[]")
            )
    return appstruct


def load_filetypes_from_config(config):
    """
        Return filetypes configured in databas
    """
    attached_filetypes = json.loads(config.get('attached_filetypes', '[]'))
    if not isinstance(attached_filetypes, list):
        attached_filetypes = []
    return attached_filetypes


def get_config_dbdatas(appstruct):
    """
        Returns dict with db compatible datas
    """
    dbdatas = {}
    dbdatas['coop_pdffootertitle'] = appstruct.get('document', {}).get(
                                                             'footertitle')
    dbdatas['coop_pdffootercourse'] = appstruct.get('document', {}).get(
                                                             'footercourse')
    dbdatas['coop_pdffootertext'] = appstruct.get('document', {}).get(
                                                             'footercontent')
    dbdatas['coop_cgv'] = appstruct.get('document', {}).get('cgv')

    dbdatas['coop_estimationheader'] = appstruct.get('document', {}).get(
                                           'estimation', {}).get('header')
    dbdatas['coop_estimationfooter'] = appstruct.get('document', {}).get(
                                                'estimation', {}).get('footer')

    dbdatas['invoiceprefix'] = appstruct.get('document', {})\
            .get('invoice', {})\
            .get('prefix')
    dbdatas['coop_invoiceheader'] = appstruct.get('document', {}).get(
                                           'invoice', {}).get('header')
    dbdatas['coop_invoicepayment'] = appstruct.get('document', {}).get(
                                                'invoice', {}).get('payment')
    dbdatas['coop_invoicelate'] = appstruct.get('document', {}).get(
                                                'invoice', {}).get('late')
    dbdatas['welcome'] = appstruct.get('site', {}).get('welcome')

    dbdatas['attached_filetypes'] = json.dumps(
            appstruct.get('attached_filetypes', {}).get('types',  []))
    return dbdatas


def get_element_by_name(list_, name):
    """
        Return an element from list_ which has the name "name"
    """
    found = None
    for element in list_:
        if element.name == name:
            found = element
    return found


def merge_config_datas(dbdatas, appstruct):
    """
        Merge the datas returned by form validation and the original dbdatas
    """
    flat_appstruct = forms.flatten_appstruct(appstruct)
    for name, value in flat_appstruct.items():
        dbdata = get_element_by_name(dbdatas, name)
        if not dbdata:
            # The key 'name' doesn't exist in the database, adding new one
            dbdata = Config(name=name, value=value)
            dbdatas.append(dbdata)
        else:
            dbdata.value = value
    return dbdatas


def get_sequence_model_admin(model, title=u""):
    """
    Return a schema for configuring sequence of models

        model

            The SQLAlchemy model to configure
    """
    node_schema = SQLAlchemySchemaNode(
        model,
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )
    node_schema.name = 'data'

    schema = colander.SchemaNode(colander.Mapping())
    schema.add(
        colander.SchemaNode(
            colander.Sequence(),
            node_schema,
            widget=deform.widget.SequenceWidget(
                orderable=True,
                template=TEMPLATES_URL + "clean_sequence.pt",
            ),
            title=title,
            name='datas')
    )
    def dictify(models):
        return {'datas': [node_schema.dictify(model) for model in models]}

    def objectify(datas):
        return [node_schema.objectify(data) for data in datas]

    schema.dictify = dictify
    schema.objectify = objectify
    return schema


class SubCompetenceConfigSchema(colander.MappingSchema):
    id = forms.id_node()
    label = colander.SchemaNode(
        colander.String(),
        title=u"Libellé",
    )


class SubCompetencesConfigSchema(colander.SequenceSchema):
    subcompetence = SubCompetenceConfigSchema(
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        )
    )


class CompetenceRequirement(colander.MappingSchema):
    deadline_id = forms.id_node()
    deadline_label = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextInputWidget(readonly=True),
        title=u"Pour l'échéance",
        missing=colander.drop,
    )
    scale_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Niveau requis",
        description=u"Sera mis en évidence dans l'interface",
        widget=forms.get_deferred_select(CompetenceScale)
    )


class CompetenceRequirementSeq(colander.SequenceSchema):
    requirement = CompetenceRequirement(
        title=u'',
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + 'clean_mapping.pt'
        )
    )


@colander.deferred
def deferred_seq_widget(nodex, kw):
    elements = kw['deadlines']
    return deform.widget.SequenceWidget(
        add_subitem_text_template=u"-",
        template=TEMPLATES_URL + "clean_sequence.pt",
        min_len=len(elements),
        max_len=len(elements),
    )


@colander.deferred
def deferred_deadlines_default(node, kw):
    """
    Return the defaults to ensure there is a requirement for each configured
    deadline
    """
    return [
        {
            'deadline_label': deadline.label,
            'deadline_id': deadline.id,
        }
        for deadline in kw['deadlines']
    ]


class CompetencePrintConfigSchema(colander.Schema):
    header_img = get_file_dl_node(title=u'En-tête de la sortie imprimable')
