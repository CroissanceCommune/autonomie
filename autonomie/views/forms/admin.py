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

from deform import widget
from deform import FileData

from autonomie.models.config import Config
from autonomie.views.forms import flatten_appstruct
from autonomie.views.forms.validators import validate_image_mime
from autonomie.utils.fileupload import FileTempStore


from .custom_types import AmountType

log = logging.getLogger(__name__)


@colander.deferred
def deferred_upload_widget(node, kw):
    """
        Returns a fileupload widget to allow logo upload
    """
    request = kw['request']
    session = request.session
    root_path = request.registry.settings.get('autonomie.assets')
    root_url = "/assets/"
    store_url = os.path.join(root_url, "main")
    store_directory = os.path.join(root_path, "main")
    tmpstore = FileTempStore(session, store_directory, store_url, 'logo.png')
    return widget.FileUploadWidget(tmpstore,
            template="autonomie:deform_templates/fileupload.mako")


class EstimationConfig(colander.MappingSchema):
    """
        Schema for estimation configuration
    """
    header = colander.SchemaNode(
            colander.String(),
            title=u"Cadre d'information spécifique (en entête des devis)",
            widget=widget.TextAreaWidget(cols=80, rows=2),
            missing=u'')
    footer = colander.SchemaNode(
        colander.String(),
        title=u"Informations sur l'acceptation des devis",
        widget=widget.TextAreaWidget(cols=80, rows=2),
        missing=u"")


class InvoiceConfig(colander.MappingSchema):
    """
        Schema for invoice configuration
    """
    prefix = colander.SchemaNode(colander.String(),
            title=u"Préfixer les numéros de facture",
            missing=u"")
    header = colander.SchemaNode(
            colander.String(),
            title=u"Cadre d'information spécifique (en entête des factures)",
            widget=widget.TextAreaWidget(cols=80, rows=2),
            missing=u'')
    payment = colander.SchemaNode(
        colander.String(),
        title=u"Information de paiement pour les factures",
        widget=widget.TextAreaWidget(cols=80, rows=2),
        missing=u"")
    late = colander.SchemaNode(
        colander.String(),
        title=u"Informations sur les délais de paiement",
        widget=widget.TextAreaWidget(cols=80, rows=2),
        missing=u"")


class DocumentConfig(colander.MappingSchema):
    """
        Schema for document (estimation/invoice ...) configuration
    """
    cgv = colander.SchemaNode(
            colander.String(),
            title=u"Conditions générales de vente",
            widget=widget.RichTextWidget(cols=80, rows=2, theme="advanced"),
            description=u"Les conditions générales sont placées en dernière \
page des documents (devis/factures/avoirs)",
            missing=u'')
    footertitle = colander.SchemaNode(
        colander.String(),
        title=u"Titre du pied de page",
        widget=widget.TextAreaWidget(cols=80, rows=2),
        missing=u"")
    footercourse = colander.SchemaNode(
        colander.String(),
        title=u"Pied de page des documents liées aux formations",
        widget=widget.TextAreaWidget(cols=80, rows=2),
        missing=u'')
    footercontent = colander.SchemaNode(
        colander.String(),
        title=u"Contenu du pied de page",
        widget=widget.TextAreaWidget(cols=80, rows=2),
        missing=u'')

    estimation = EstimationConfig(title=u'Devis')
    invoice = InvoiceConfig(title=u"Factures")


class SiteConfig(colander.MappingSchema):
    """
        Site configuration
        logos ...
    """
    logo = colander.SchemaNode(FileData(),
                widget=deferred_upload_widget,
                title=u'Logo du site',
                validator=validate_image_mime,
                default={"filename": "logo.png", "uid": "MAINLOGO"})
    welcome = colander.SchemaNode(
        colander.String(),
        title=u"Texte d'accueil",
        widget=widget.RichTextWidget(cols=80, rows=2, theme="advanced"),
        missing=u'')

class MainConfig(colander.MappingSchema):
    """
        Schema for main site configuration
    """
    site = SiteConfig()
    document = DocumentConfig(title=u'Document (devis et factures)')


class Product(colander.MappingSchema):
    """
        Form schema for a single product configuration
    """
    id = colander.SchemaNode(colander.Integer(),
            widget=widget.HiddenWidget(),
            default=None,
            missing=None)
    name = colander.SchemaNode(colander.String(), title=u"Libellé")
    compte_cg = colander.SchemaNode(colander.String(),
                                    title=u"Compte CG")


class ProductSequence(colander.SequenceSchema):
    product = Product(title=u"Compte produit")

class TvaItem(colander.MappingSchema):
    """
        Allows Tva configuration
    """
    id = colander.SchemaNode(colander.Integer(),
            widget=widget.HiddenWidget(),
            default=0,
            missing=0)
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
        widget=widget.CheckboxWidget(true_val="1", false_val="0"))
    products = ProductSequence(title=u"",
            widget=widget.SequenceWidget(orderable=False))


class TvaSequence(colander.SequenceSchema):
    tva = TvaItem(title=u"Taux de Tva")


class TvaConfig(colander.MappingSchema):
    tvas = TvaSequence(title=u"", missing=u'',
            widget=widget.SequenceWidget(orderable=True))


class PaymentModeSequence(colander.SequenceSchema):
    """
        Single payment mode configuration scheme
    """
    label = colander.SchemaNode(colander.String(), title=u"Libellé")

class PaymentModeConfig(colander.MappingSchema):
    """
        Main configuration form model
    """
    paymentmodes = PaymentModeSequence(title=u"", missing=u"",
            widget=widget.SequenceWidget(orderable=True))


class WorkUnitSequence(colander.SequenceSchema):
    """
        Single work untit configuration scheme
    """
    label = colander.SchemaNode(colander.String(), title=u"Libellé")

class WorkUnitConfig(colander.MappingSchema):
    """
        Main configuration form model
    """
    workunits = WorkUnitSequence(title=u"", missing=u"",
            widget=widget.SequenceWidget(orderable=True))


class ExpenseConfig(colander.MappingSchema):
    """
        Schema for the configuration of different expense types
    """
    id = colander.SchemaNode(colander.Integer(),
            widget=widget.HiddenWidget(),
            default=None,
            missing=None)
    label = colander.SchemaNode(colander.String(), title=u"Libellé",
            validator=colander.Length(max=50))
    code = colander.SchemaNode(colander.String(), title=u"Code analytique",
            validator=colander.Length(max=15))

class ExpenseKmConfig(ExpenseConfig):
    """
        Schema for the configuration of vehicle related expenses
    """
    amount = colander.SchemaNode(colander.Float(),
            title=u"Tarif", description=u"Tarif au km")


class ExpenseTelConfig(ExpenseConfig):
    """
        Schema for telefonic expenses
    """
    percentage = colander.SchemaNode(colander.Integer(),
                                title=u"Pourcentage remboursé",
                                validator=colander.Range(1, 100))
    initialize = colander.SchemaNode(colander.Boolean(),
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
    expenses = ExpensesConfig(title=u'Frais généraux')
    expenseskm = ExpensesKmConfig(title=u"Frais kilométriques")
    expensestel = ExpensesTelConfig(title=u"Frais téléphoniques")


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
        schema.add(colander.SchemaNode(
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
    export_schema.add(colander.SchemaNode(
        colander.String(),
        widget=widget.CheckboxWidget(
            template='autonomie:deform_templates/checkbox_readonly.pt',
            ),
        title=u"Module facturation",
        description=u"activé par défaut",
        name="sage_facturation_not_used",
        ))
    for key, title, description in export_modules:
        export_schema.add(colander.SchemaNode(
            colander.String(),
            widget=widget.CheckboxWidget(true_val="1", false_val="0"),
            title=title,
            description=description,
            name=key))
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
    return appstruct



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
            dbdata = Config(app=u"autonomie", name=name, value=value)
            dbdatas.append(dbdata)
        else:
            dbdata.value = value
    return dbdatas
