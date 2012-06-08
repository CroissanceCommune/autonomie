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
import colander
import logging

from deform import widget

log = logging.getLogger(__name__)

class EstimationConfig(colander.MappingSchema):
    """
        Schema for estimation configuration
    """
    footer = colander.SchemaNode(colander.String(),
                            title=u"Informations sur l'acceptation des devis",
                            widget=widget.TextAreaWidget(cols=80, rows=2),
                            missing=u"")

class InvoiceConfig(colander.MappingSchema):
    """
        Schema for invoice configuration
    """
    payment = colander.SchemaNode(colander.String(),
                           title=u"Information de paiement pour les factures",
                           widget=widget.TextAreaWidget(cols=80, rows=2),
                           missing=u"")
    late = colander.SchemaNode(colander.String(),
                           title=u"Informations sur les délais de paiement",
                           widget=widget.TextAreaWidget(cols=80, rows=2),
                           missing=u"")

class DocumentConfig(colander.MappingSchema):
    """
        Schema for document (estimation/invoice ...) configuration
    """
    footertitle = colander.SchemaNode(colander.String(),
                                title=u"Titre du pied de page",
                                widget=widget.TextAreaWidget(cols=80, rows=2),
                                missing=u"")
    footercourse = colander.SchemaNode(colander.String(),
                                title=u"Pied de page des documents liées aux formations",
                                widget=widget.TextAreaWidget(cols=80, rows=2),
                                missing=u'')
    footercontent = colander.SchemaNode(colander.String(),
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
    pass


class MainConfig(colander.MappingSchema):
    """
        Schema for main site configuration
    """
    site = SiteConfig()
    document = DocumentConfig(title=u'Document (devis et factures)')

def get_config_appstruct(config_dict):
    """
        transform Config datas to ConfigSchema compatible appstruct
    """
    appstruct = {'site':{},
            'document':{'estimation':{'footer':None,},
                        'invoice':{'payment':None,
                                   'late':None},
                        'footertitle':None,
                        'footercourse':None,
                        'footercontent':None},
                }
    appstruct['document']['footertitle'] = config_dict.get('coop_pdffootertitle')
    appstruct['document']['footercourse'] = config_dict.get('coop_pdffootercourse')
    appstruct['document']['footercontent'] = config_dict.get('coop_pdffootertext')

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
    return dbdatas

def merge_dbdatas(dbdatas, appstruct):
    """
        Merge the datas returned by form validation and the original dbdatas
    """
    new_datas = get_config_dbdatas(appstruct)
    for datas in dbdatas:
        new_val = new_datas.get(datas.name)
        if new_val:
            datas.value = new_val
    return dbdatas
