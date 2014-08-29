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

from deform import widget as deform_widget
from deform import FileData

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.config import Config
from autonomie.views.forms import (
    main,
    flatten_appstruct,
    )
from autonomie.views.forms.validators import validate_image_mime
from autonomie.utils.image import ImageResizer
from autonomie.views.forms.main import get_fileupload_widget


from .custom_types import AmountType

log = logging.getLogger(__name__)


HEADER_RESIZER = ImageResizer(4, 1)


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

        return get_fileupload_widget(
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
    header = main.textarea_node(
        title=u"Cadre d'information spécifique (en entête des devis)",
        missing=u"")
    footer = main.textarea_node(
        title=u"Informations sur l'acceptation des devis",
        missing=u"")


class InvoiceConfig(colander.MappingSchema):
    """
        Schema for invoice configuration
    """
    prefix = colander.SchemaNode(
        colander.String(),
        title=u"Préfixer les numéros de facture",
        missing=u"")
    header = main.textarea_node(
        title=u"Cadre d'information spécifique (en entête des factures)",
        missing=u"")
    payment = main.textarea_node(
        title=u"Information de paiement pour les factures",
        missing=u"")
    late = main.textarea_node(
        title=u"Informations sur les délais de paiement",
        missing=u"")


class DocumentConfig(colander.MappingSchema):
    """
        Schema for document (estimation/invoice ...) configuration
    """
    cgv = main.textarea_node(
        title=u"Conditions générales de vente",
        description=u"Les conditions générales sont placées en dernière \
page des documents (devis/factures/avoirs)",
        missing=u'',
        richwidget=True)
    footertitle = main.textarea_node(
        title=u"Titre du pied de page",
        missing=u"")
    footercourse = main.textarea_node(
        title=u"Pied de page des documents liées aux formations",
        missing=u"")
    footercontent = main.textarea_node(
        title=u"Contenu du pied de page",
        missing=u"")

    estimation = EstimationConfig(title=u'Devis')
    invoice = InvoiceConfig(title=u"Factures")


class FileTypeConfig(colander.SequenceSchema):
    name = colander.SchemaNode(
        colander.String(),
        title=u"Type de document",
        description=u"Le libellé permet d'identifier plus facilement les \
documents attachés aux factures",
            )


class FileTypesConfig(colander.MappingSchema):
    """
        Configure file types that may be attached
    """
    types = FileTypeConfig(title=u"")


class SiteConfig(colander.MappingSchema):
    """
        Site configuration
        logos ...
    """
    logo = colander.SchemaNode(
        FileData(),
        widget=get_deferred_upload_widget('logo.png'),
        title=u'Logo du site',
        validator=validate_image_mime,
        default={"filename": "logo.png", "uid": "MAINLOGO"},
        )
    welcome = main.textarea_node(
        title=u"Texte d'accueil",
        richwidget=True,
        missing=u'')


class MainConfig(colander.MappingSchema):
    """
        Schema for main site configuration
    """
    site = SiteConfig()
    document = DocumentConfig(title=u'Document (devis et factures)')
    attached_filetypes = FileTypesConfig(title=u"Type des documents attachés")


class Product(colander.MappingSchema):
    """
        Form schema for a single product configuration
    """
    id = main.id_node()
    name = colander.SchemaNode(colander.String(), title=u"Libellé")
    compte_cg = colander.SchemaNode(colander.String(), title=u"Compte CG")


class ProductSequence(colander.SequenceSchema):
    product = Product(title=u"Compte produit")

class TvaItem(colander.MappingSchema):
    """
        Allows Tva configuration
    """
    id = main.id_node()
    name = colander.SchemaNode(
        colander.String(),
        title=u"Libellé du taux de TVA",
        css_class='span2')
    value = colander.SchemaNode(
        AmountType(),
        title=u"Montant",
        css_class='span2')
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
        widget=deform_widget.CheckboxWidget(true_val="1", false_val="0"))
    products = ProductSequence(
        title=u"",
        widget=deform_widget.SequenceWidget(orderable=False))


class TvaSequence(colander.SequenceSchema):
    tva = TvaItem(title=u"Taux de Tva")


class TvaConfig(colander.MappingSchema):
    tvas = TvaSequence(
        title=u"",
        missing=u'',
        widget=deform_widget.SequenceWidget(orderable=True))


class PaymentModeSequence(colander.SequenceSchema):
    """
        Single payment mode configuration scheme
    """
    label = colander.SchemaNode(colander.String(), title=u"Libellé")

class PaymentModeConfig(colander.MappingSchema):
    """
        Main configuration form model
    """
    paymentmodes = PaymentModeSequence(
        title=u"",
        missing=u"",
        widget=deform_widget.SequenceWidget(orderable=True))


class WorkUnitSequence(colander.SequenceSchema):
    """
        Single work untit configuration scheme
    """
    label = colander.SchemaNode(colander.String(), title=u"Libellé")

class WorkUnitConfig(colander.MappingSchema):
    """
        Main configuration form model
    """
    workunits = WorkUnitSequence(
        title=u"",
        missing=u"",
        widget=deform_widget.SequenceWidget(orderable=True))


class ExpenseConfig(colander.MappingSchema):
    """
        Schema for the configuration of different expense types
    """
    id = main.id_node()

    label = colander.SchemaNode(
        colander.String(),
        title=u"Libellé",
        validator=colander.Length(max=50))

    code = colander.SchemaNode(
        colander.String(),
        title=u"Code analytique",
        validator=colander.Length(max=15))

    code_tva = colander.SchemaNode(
        colander.String(),
        title=u"Code TVA",
        missing="",
        validator=colander.Length(max=15))

    compte_tva = colander.SchemaNode(
        colander.String(),
        title=u"Compte de TVA",
        missing="",
        description=u"Compte de TVA déductible",
        validator=colander.Length(max=15))

    contribution = colander.SchemaNode(
        colander.Boolean(),
        title=u"Contribution",
        description=u"Ce type de frais est-il intégré dans la contribution \
à la CAE?",
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
    expense = ExpenseConfig(title=u"")


class ExpensesKmConfig(colander.SequenceSchema):
    """
        The sequence Schema associated with the ExpenseKmConfig
    """
    expense = ExpenseKmConfig(title=u"")


class ExpensesTelConfig(colander.SequenceSchema):
    """
        The sequence Schema associated with the ExpenseTelConfig
    """
    expense = ExpenseTelConfig(title=u"")


class ExpenseTypesConfig(colander.MappingSchema):
    """
        Expense Configuration form schema
    """
    code_journal = colander.SchemaNode(
        colander.String(),
        title=u"Code journal",
        description=u"Le code journal pour les notes de frais",
        missing="",
        )
    compte_cg = colander.SchemaNode(
        colander.String(),
        title=u"Compte CG",
        description=u"Le compte général pour les notes de frais",
        missing="",
        )
    expenses = ExpensesConfig(title=u'Frais généraux')
    expenseskm = ExpensesKmConfig(title=u"Frais kilométriques")
    expensestel = ExpensesTelConfig(title=u"Frais téléphoniques")


class ActivityTypeConfig(colander.MappingSchema):
    """
        Schema for the configuration of different activity types
    """
    id = main.id_node()

    label = colander.SchemaNode(
        colander.String(),
        title=u"Libellé",
        validator=colander.Length(max=100)
        )


class ActivityTypesSeqConfig(colander.SequenceSchema):
    """
        The sequence Schema associated with the ActivityTypeConfig
    """
    activity_type = ActivityTypeConfig(title=u"Nature du rendez-vous")


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
    activity_mode = ActivityModeConfig(title=u"Mode d'entretien")


class ActivitySubActionConfig(colander.MappingSchema):
    id = main.id_node()

    label = colander.SchemaNode(
        colander.String(),
        title=u"Intitulé",
        validator=colander.Length(max=100)
        )


class ActivitySubActionSeq(colander.SequenceSchema):
    subaction = ActivitySubActionConfig(title=u"Sous-action")


class ActivityActionConfig(colander.Schema):
    id = main.id_node()
    label = colander.SchemaNode(
        colander.String(),
        title=u"Intitulé de l'action",
        validator=colander.Length(max=100)
        )
    children = ActivitySubActionSeq( title=u"Sous actions")


class ActivityActionSeq(colander.SequenceSchema):
    action = ActivityActionConfig(title=u"Action")


class MainActivityConfig(colander.MappingSchema):
    """
    Mapping schema for main configuration
    """
    header = colander.SchemaNode(
        FileData(),
        widget=get_deferred_upload_widget('accompagnement_header.png'),
        title=u'En-tête des sortie PDF',
        validator=validate_image_mime,
        default={
            "filename": "accompagnement_header.png",
            "uid": "ACCOMPAGNEMENT_HEADER",
            },
        )


class ActivityTypesConfig(colander.Schema):
    """
        The schema for activity types configuration
    """
    main = MainActivityConfig(title=u"")
    types = ActivityTypesSeqConfig(
        title=u"Configuration des natures de rendez-vous"
            )
    modes = ActivityModesSeqConfig(
        title=u"Configuration des modes d'entretien"
            )
    actions = ActivityActionSeq(
        title=u"Configuration des intitulés d'action"
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
    fields =(
    (
        'code_journal',
        u"Code journal",
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
        u"Compte CG correspondant à la contribution des entrepreneurs à la CAE"
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
        u"Compte CG Banque",
        "",
    ),

    (
        'compte_cg_assurance',
        u"Compte CG assurance",
        u"Requis pour le module d'écritures Assurance",
    ),
    (
        'compte_cgscop',
        u"Compte CGSCOP",
        u"Requis pour le module d'écritures CGSCOP",
    ),
    (
        'compte_cg_debiteur',
        u"Compte CG de débiteur",
        u"Requis pour le module d'écritures CGSCOP",
    ),
    (
        'compte_cg_organic',
        u"Compte CG Organic",
        u"Compte CG pour la contribution à l'Organic (requis pour le module \
d'écritures Contribution Organic)",
    ),
    (
        'compte_cg_debiteur_organic',
        u"Compte CG de débiteur Organic",
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
        u"(nombre entre 0 et 100) Requis pour le module d'écritures Assurance",
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
        u"(nombre entre 0 et 100) Requis pour le module d'écriture RG Client",
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
            name=key))


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
                u"",),
            )
    export_schema = SageExportConfig(
        title=u"Activation des modules d'export Sage",
        name='sage_export').clone()
    export_schema.add(
        colander.SchemaNode(
            colander.String(),
            widget=deform_widget.CheckboxWidget(
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
                widget=deform_widget.CheckboxWidget(true_val="1", false_val="0"),
                title=title,
                description=description,
                name=key)
        )
    schema.add(export_schema)

    return schema


CAECONFIG = build_cae_config_schema()


def get_config_appstruct(config_dict):
    """
        transform Config datas to ConfigSchema compatible appstruct
    """
    appstruct = {
        'site':     {'welcome': None},
        'document': {'estimation':  {
                                    'header': None,
                                    'footer': None,
                                    },
                     'invoice':     {
                                    'prefix': None,
                                    'header': None,
                                    'payment': None,
                                     'late': None},
                     'footertitle': None,
                     'footercourse': None,
                     'footercontent': None,
                     'cgv': None},
        "attached_filetypes": {}
    }
    appstruct['site']['welcome'] = config_dict.get('welcome')
    appstruct['document']['footertitle'] = config_dict.get(
                                                       'coop_pdffootertitle')
    appstruct['document']['footercourse'] = config_dict.get(
                                                      'coop_pdffootercourse')
    appstruct['document']['footercontent'] = config_dict.get(
                                                        'coop_pdffootertext')
    appstruct['document']['cgv'] = config_dict.get('coop_cgv')

    appstruct['document']['estimation']['header'] = config_dict.get(
                                                        'coop_estimationheader')
    appstruct['document']['estimation']['footer'] = config_dict.get(
                                                       'coop_estimationfooter')

    appstruct['document']['invoice']['prefix'] = config_dict.get(
                                                    'invoiceprefix')
    appstruct['document']['invoice']['header'] = config_dict.get(
                                                        'coop_invoiceheader')

    appstruct['document']['invoice']['payment'] = config_dict.get(
                                                        'coop_invoicepayment')
    appstruct['document']['invoice']['late'] = config_dict.get(
                                                        'coop_invoicelate')

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
    flat_appstruct = flatten_appstruct(appstruct)
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
    node_schema = SQLAlchemySchemaNode(model)
    node_schema.name = 'data'

    schema = colander.SchemaNode(colander.Mapping())
    schema.add(
        colander.SchemaNode(
            colander.Sequence(),
            node_schema,
            widget=deform_widget.SequenceWidget(min_len=1),
            title=title,
            name='datas')
    )
    return schema

