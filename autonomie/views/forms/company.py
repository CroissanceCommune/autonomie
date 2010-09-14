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
    Company form schemas
"""
import os
import colander
import logging

from deform import FileData
from deform import widget

from autonomie.views.forms.widgets import deferred_edit_widget
from autonomie.views.forms.widgets import get_fileupload_widget
from autonomie.views.forms.validators import validate_image_mime
from autonomie.views.forms import main
from autonomie.utils.image import ImageResizer

log = logging.getLogger(__name__)
HEADER_PATH = "header"
LOGO_PATH = "logo"

HEADER_RESIZER = ImageResizer(4, 1)

def get_upload_options_from_request(request, directory):
    """
        Return the upload path and url from the request object
    """
    company = request.context
    rootpath = request.registry.settings.get('autonomie.assets', '/tmp')
    store_path = os.path.join(rootpath, company.get_path(), directory)
    store_url = os.path.join("/assets", company.get_path(), directory)
    return store_path, store_url

@colander.deferred
def deferred_edit_adminonly_widget(node, kw):
    """
        return a deferred adminonly edit widget
    """
    request = kw['request']
    if request.user.is_contractor():
        return deferred_edit_widget(node, dict(edit=True))
    else:
        return deferred_edit_widget(node, dict(edit=False))

@colander.deferred
def deferred_logo_widget(node, kw):
    """
        Return the logo upload widget
    """
    request = kw['request']
    path, url = get_upload_options_from_request(request, LOGO_PATH)
    return get_fileupload_widget(url, path, request.session)

@colander.deferred
def deferred_header_widget(node, kw):
    """
        Return the header upload widget
    """
    request = kw['request']
    path, url = get_upload_options_from_request(request, HEADER_PATH)
    return get_fileupload_widget(url, path, request.session,
                                    [HEADER_RESIZER.complete])


@colander.deferred
def deferred_default_contribution(node, kw):
    """
        Return the default contribution
    """
    request = kw['request']
    cae_contribution = request.config.get('contribution_cae')
    if cae_contribution is not None and cae_contribution.isdigit():
        return cae_contribution
    else:
        return None


def remove_admin_fields(schema, kw):
    """
        Remove admin only fields from the company schema
    """
    if kw['request'].user.is_contractor():
        del schema['RIB']
        del schema['IBAN']
        del schema['code_compta']
        del schema['contribution']


class CompanySchema(colander.MappingSchema):
    """
        Company add/edit form schema
    """
    name = colander.SchemaNode(
            colander.String(),
            widget=deferred_edit_adminonly_widget,
            title=u'Nom')
    goal = colander.SchemaNode(
            colander.String(),
            title=u'Activité')
    email = main.mail_node(missing=u'')
    phone = colander.SchemaNode(
            colander.String(),
            title=u'Téléphone',
            missing=u'')
    mobile = colander.SchemaNode(
            colander.String(),
            title=u'Téléphone portable',
            missing=u'')
    logo = colander.SchemaNode(
            FileData(),
            widget=deferred_logo_widget,
            title=u'Logo',
            validator=validate_image_mime,
            description=u"Charger un fichier de type image *.png *.jpeg \
*.jpg ...")
    header = colander.SchemaNode(
            FileData(),
            widget=deferred_header_widget,
            title=u'Entête des fichiers PDF',
            description=u"Charger un fichier de type image *.png *.jpeg \
*.jpg ... Le fichier est idéalement au format 20/4 (par exemple 1000px x \
200 px)",
            validator=validate_image_mime)
    # Fields specific to the treasury
    code_compta = colander.SchemaNode(
            colander.String(),
            title=u"Compte analytique",
            description=u"Compte analytique utilisé dans le logiciel de compta",
            missing="")
    contribution = colander.SchemaNode(
            colander.Integer(),
            widget=widget.TextInputWidget(
                input_append="%",
                css_class="span1"
                ),
            validator=colander.Range(min=0, max=100,
                min_err=u"Veuillez fournir un nombre supérieur à 0",
                max_err=u"Veuillez fournir un nombre inférieur à 100"),
            title=u"Contribution à la CAE",
            default=deferred_default_contribution,
            missing=deferred_default_contribution,
            description=u"Pourcentage que cette entreprise contribue à la CAE")
    RIB = colander.SchemaNode(
            colander.String(),
            title=u'RIB',
            missing=u'')
    IBAN = colander.SchemaNode(
            colander.String(),
            title=u'IBAN',
            missing=u'')


COMPANYSCHEMA = CompanySchema(after_bind=remove_admin_fields)
