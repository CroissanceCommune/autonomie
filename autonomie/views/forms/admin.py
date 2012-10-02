# -*- coding: utf-8 -*-
# * File Name : admin.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Form schemes for administration
"""
import os
import colander
import logging

from deform import widget
from deform import FileData

from autonomie.models.model import Config
from autonomie.views.forms.validators import validate_image_mime
from autonomie.utils.fileupload import FileTempStore


from .custom_types import AmountType

log = logging.getLogger(__name__)


@colander.deferred
def deferred_upload_widget(node, kw):
    """
        Returns a fileupload widget to allow logo upload
    """
    session = kw['session']
    root_path = kw['rootpath']
    root_url = kw['rooturl']
    store_url = os.path.join(root_url, "main")
    store_directory = os.path.join(root_path, "main")
    tmpstore = FileTempStore(session, store_directory, store_url, 'logo.png')
    return widget.FileUploadWidget(tmpstore,
            template="autonomie:deform_templates/fileupload.mako")


class EstimationConfig(colander.MappingSchema):
    """
        Schema for estimation configuration
    """
    footer = colander.SchemaNode(
        colander.String(),
        title=u"Informations sur l'acceptation des devis",
        widget=widget.TextAreaWidget(cols=80, rows=2),
        missing=u"")


class InvoiceConfig(colander.MappingSchema):
    """
        Schema for invoice configuration
    """
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


class TvaItem(colander.MappingSchema):
    """
        Allows Tva configuration
    """
    name = colander.SchemaNode(
        colander.String(),
        title=u"Libellé du taux de TVA",
        css_class='span2')
    value = colander.SchemaNode(
        AmountType(),
        title=u"Montant",
        css_class='span2')
    default = colander.SchemaNode(
        colander.Integer(),
        title=u"Valeur par défaut ?",
        widget=widget.CheckboxWidget(true_val="1", false_val="0"))


class TvaSequence(colander.SequenceSchema):
    tva = TvaItem(title=u"")


class TvaConfig(colander.MappingSchema):
    tvas = TvaSequence(title=u"", missing=u'')


def get_config_appstruct(config_dict):
    """
        transform Config datas to ConfigSchema compatible appstruct
    """
    appstruct = {
        'site':     {'welcome': None},
        'document': {'estimation':  {'footer': None, },
                     'invoice':     {'payment': None,
                                     'late': None},
                     'footertitle': None,
                     'footercourse': None,
                     'footercontent': None},
    }
    appstruct['site']['welcome'] = config_dict.get('welcome')
    appstruct['document']['footertitle'] = config_dict.get(
                                                       'coop_pdffootertitle')
    appstruct['document']['footercourse'] = config_dict.get(
                                                      'coop_pdffootercourse')
    appstruct['document']['footercontent'] = config_dict.get(
                                                        'coop_pdffootertext')

    appstruct['document']['estimation']['footer'] = config_dict.get(
                                                       'coop_estimationfooter')

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

    dbdatas['coop_estimationfooter'] = appstruct.get('document', {}).get(
                                                'estimation', {}).get('footer')

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


def merge_dbdatas(dbdatas, appstruct):
    """
        Merge the datas returned by form validation and the original dbdatas
    """
    new_datas = get_config_dbdatas(appstruct)
    for name, value in new_datas.items():
        dbdata = get_element_by_name(dbdatas, name)
        if not dbdata:
            # The key 'name' doesn't exist in the database, adding new one
            dbdata = Config(app=u"autonomie", name=name, value=value)
            dbdatas.append(dbdata)
        else:
            dbdata.value = value
    return dbdatas
