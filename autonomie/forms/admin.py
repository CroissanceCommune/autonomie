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


CONFIGURATION_KEYS = {
    'receipts_code_journal': {
        "title": u"Code journal encaissements",
        "description": u"Le code journal pour l'export des encaissements \
vers votre logiciel de comptabilité",
    },
    'receipts_active_tva_module': {
        "title": u"Activer le module TVA pour les encaissements",
        "description": u"Inclue les écritures pour le paiement de la TVA \
sur encaissement",
        "widget": deform.widget.CheckboxWidget(true_val='1', false_val='0')
    },
    'code_journal': {
        'title': u"Code journal ventes",
        'description': u"Le code du journal dans votre logiciel de \
comptabilité",
    },
    'numero_analytique': {
        'title': u"Numéro analytique de la CAE",
    },
    'compte_cg_contribution': {
        'title': u"Compte CG contribution",
        'description': u"Compte CG correspondant à la contribution des \
entrepreneurs à la CAE",
    },
    "compte_frais_annexes": {
        "title": u"Compte de frais annexes",
    },
    "compte_cg_banque": {
        "title": u"Compte banque de l'entrepreneur",
    },
    'compte_rrr': {
        "title": u"Compte RRR",
        "description": u"Compte Rabais, Remises et Ristournes",
        "section": u"Module RRR"
    },
    'compte_cg_tva_rrr': {
        "title": u"Compte CG de TVA spécifique aux RRR",
        "description": u"",
        "section": u"Module RRR"
    },
    'code_tva_rrr': {
        "title": u"Code de TVA spécifique aux RRR",
        "description": u"",
        "section": u"Module RRR"
    },
    "compte_cg_assurance": {
        "title": u"Compte de charge assurance",
        "description": u"",
        "section": u"Module Assurance",
    },
    "compte_cgscop": {
        "title": u"Compte de charge CG Scop",
        "description": u"",
        "section": u"Module CGSCOP",
    },
    'compte_cg_debiteur': {
        "title": u"Compte de contrepartie CGSCOP",
        "description": u"",
        "section": u"Module CGSCOP",
    },
    "compte_cg_organic": {
        "title": u"Compte de charge Organic",
        "description": u"Compte CG pour la contribution à l'Organic",
        "section": u"Module Contribution à l'Organic",
    },
    "compte_cg_debiteur_organic": {
        "title": u"Compte de contrepartie Organic",
        "description": u"Compte CG de débiteur pour la contribution à \
l'Organic",
        "section": u"Module Contribution à l'Organic",
    },
    'compte_rg_interne': {
        "title": u"Compte RG Interne",
        "description": u"",
        "section": u"Module RG Interne",
    },
    'compte_rg_externe': {
        "title": u"Compte RG Externe",
        "description": u"",
        "section": u"Module RG Externe",
    },
    'contribution_cae': {
        "title": u"Pourcentage de la contribution",
        "description": u"Valeur par défaut de la contribution (nombre entre \
0 et 100). Elle peut être individualisée sur les pages entreprises.",
        "section": u"Module Contribution",
    },
    'taux_assurance': {
        "title": u"Taux d'assurance",
        "description": u"(nombre entre 0 et 100) Requis pour le module \
d'écritures Assurance",
        "section": u"Module Assurance",
    },
    'taux_cgscop': {
        "title": u"Taux CGSCOP",
        "description": u"(nombre entre 0 et 100) Requis pour le module \
d'écritures CGSCOP",
        "section": u"Module CGSCOP",
    },
    'taux_contribution_organic': {
        "title": u"Taux de Contribution à l'Organic",
        "description": "(nombre entre 0 et 100) Requis pour le module \
d'écritures Contribution Organic",
        "section": u"Module Contribution à l'Organic",
    },
    'taux_rg_interne': {
        "title": u"Taux RG Interne",
        "description": u"(nombre entre 0 et 100) Requis pour les écritures \
RG Interne",
        "section": u"Module RG Interne",
    },
    'taux_rg_client': {
        "title": u"Taux RG Client",
        "description": u"(nombre entre 0 et 100) Requis pour le module \
d'écriture RG Client",
        "section": u"Module RG Client",
    },
    'sage_contribution': {
        "title": u"Module contribution",
        "widget": deform.widget.CheckboxWidget(true_val='1', false_val='0'),
        "section": u"Activation des modules d'export Sage",
    },
    'sage_assurance': {
        "title": u"Module assurance",
        "widget": deform.widget.CheckboxWidget(true_val='1', false_val='0'),
        "section": u"Activation des modules d'export Sage",
    },
    'sage_cgscop': {
        "title": u"Module CGSCOP",
        "widget": deform.widget.CheckboxWidget(true_val='1', false_val='0'),
        "section": u"Activation des modules d'export Sage",
    },
    'sage_organic': {
        "title": u"Module Contribution organic",
        "widget": deform.widget.CheckboxWidget(true_val='1', false_val='0'),
        "section": u"Activation des modules d'export Sage",
    },
    'sage_rginterne': {
        "title": u"Module RG Interne",
        "widget": deform.widget.CheckboxWidget(true_val='1', false_val='0'),
        "section": u"Activation des modules d'export Sage",
    },
    'sage_rgclient': {
        "title": u"Module RG Client",
        "widget": deform.widget.CheckboxWidget(true_val='1', false_val='0'),
        "section": u"Activation des modules d'export Sage",
    },
    'sage_facturation_not_used': {
        "title": u"Module facturation",
        "description": u"Activé par défaut",
        "widget": deform.widget.CheckboxWidget(
            template='autonomie:deform_templates/checkbox_readonly.pt'
        ),
        "section": u"Activation des modules d'export Sage",
    },
    # NDF
    "code_journal_ndf": {
        "title": u"Code journal utilisé pour les notes de dépense",
    },
    "compte_cg_ndf":{
        "title": u"Compte de tiers (classe 4) pour les dépenses dues aux \
entrepreneurs",
        "description": u"Le compte général pour les notes de dépense",
    },
    "code_tva_ndf": {
        "title": u"Code TVA spécifique aux notes de dépense",
        "description": u"Le code TVA utilisé pour l'export des paiements \
des notes de dépense.",
    }
}


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


def get_config_key_schemanode(key, ui_conf):
    """
    Returns a schema node to configure the config 'key'
    This key should appear in the dict here above CONFIGURATION_KEYS
    """
    return colander.SchemaNode(
        colander.String(),
        title=ui_conf['title'],
        description=ui_conf.get('description'),
        missing=u"",
        name=key,
        widget=ui_conf.get('widget'),
    )


def get_config_schema(keys):
    """
    Returns a schema to configure Config objects

    :param list keys: The list of keys we want to configure (ui informations
    should be provided in the CONFIGURATION_KEYS dict

    :results: A colander Schema to configure the given keys
    :rtype: object colander Schema
    """
    schema = colander.Schema()
    mappings = {}
    for key in keys:
        ui_conf = CONFIGURATION_KEYS[key]
        node = get_config_key_schemanode(key, ui_conf)

        if "section" in ui_conf:  # This element should be shown in a mapping
            section_name = ui_conf['section']
            if section_name not in mappings:
                mappings[section_name] = mapping = colander.Schema(
                    title=section_name,
                    name=section_name,
                )
            else:
                mapping = mappings[section_name]
            mapping.add(node)
        else:
            schema.add(node)

    for mapping in mappings.values():
        schema.add(mapping)
    return schema


def build_config_appstruct(request, keys):
    """
    Build the configuration appstruct regarding the config keys we want to edit

    :param obj request: The pyramid request object (with a config attribute)
    :param list keys: the keys we want to edit
    :returns: A dict storing the configuration values adapted to a schema
    generated by get_config_schema
    """
    appstruct = {}
    for key in keys:
        value = request.config.get(key, "")
        if value:
            ui_conf = CONFIGURATION_KEYS[key]

            if "section" in ui_conf:
                appstruct.setdefault(ui_conf['section'], {})[key] = value
            else:
                appstruct[key] = value
    return appstruct


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
    compte_a_payer = colander.SchemaNode(
        colander.String(),
        missing="",
        title=u"Compte de Tva à payer",
        description=u"Utilisé dans les exports comptables des encaissements",
    )
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


def get_config_appstruct(request, config_dict, logo):
    """
        transform Config datas to ConfigSchema compatible appstruct
    """
    appstruct = {
        'site':     {'welcome': ''},
        'document': {
            'estimation': {
                'header': '',
                'footer': '',
            },
            'invoice': {
                'prefix': '',
                'header': '',
                'payment': '',
                'late': ''
            },
            'footertitle': '',
            'footercourse': '',
            'footercontent': '',
            'cgv': '',
        },
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
    dbdatas['coop_pdffootertitle'] = appstruct.get(
        'document', {}).get(
            'footertitle'
        )
    dbdatas['coop_pdffootercourse'] = appstruct.get(
        'document', {}).get(
            'footercourse')
    dbdatas['coop_pdffootertext'] = appstruct.get(
        'document', {}).get(
            'footercontent')
    dbdatas['coop_cgv'] = appstruct.get(
        'document', {}).get('cgv')

    dbdatas['coop_estimationheader'] = appstruct.get(
        'document', {}).get(
            'estimation', {}).get('header')
    dbdatas['coop_estimationfooter'] = appstruct.get(
        'document', {}).get(
            'estimation', {}).get('footer')

    dbdatas['invoiceprefix'] = appstruct.get(
        'document', {})\
        .get('invoice', {})\
        .get('prefix')
    dbdatas['coop_invoiceheader'] = appstruct.get(
        'document', {}).get(
            'invoice', {}).get('header')
    dbdatas['coop_invoicepayment'] = appstruct.get(
        'document', {}).get(
            'invoice', {}).get('payment')
    dbdatas['coop_invoicelate'] = appstruct.get(
        'document', {}).get(
            'invoice', {}).get('late')
    dbdatas['welcome'] = appstruct.get('site', {}).get(
        'welcome')

    dbdatas['attached_filetypes'] = json.dumps(
        appstruct.get('attached_filetypes', {}).get('types',  [])
    )
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


def get_sequence_model_admin(model, title=u"", excludes=()):
    """
    Return a schema for configuring sequence of models

        model

            The SQLAlchemy model to configure
    """
    node_schema = SQLAlchemySchemaNode(
        model,
        widget=deform.widget.MappingWidget(
            template=TEMPLATES_URL + "clean_mapping.pt",
        ),
        excludes=excludes,
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
                min_len=1,
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
