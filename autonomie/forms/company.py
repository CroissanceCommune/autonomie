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
import colander
import logging
import deform

import deform_extensions
from deform import FileData

from autonomie.forms.validators import validate_image_mime
from autonomie import forms
from autonomie.forms import (
    files,
    lists,
)
from autonomie.utils.image import ImageResizer

log = logging.getLogger(__name__)

HEADER_RESIZER = ImageResizer(4, 1)


@colander.deferred
def deferred_edit_adminonly_widget(node, kw):
    """
        return a deferred adminonly edit widget
    """
    request = kw['request']
    if request.user.is_contractor():
        return deform_extensions.DisabledInput()
    else:
        return deform.widget.TextInputWidget()


@colander.deferred
def deferred_upload_header_widget(node, kw):
    request = kw['request']
    tmpstore = files.SessionDBFileUploadTempStore(
        request,
        filters=HEADER_RESIZER.complete
    )
    return files.CustomFileUploadWidget(
        tmpstore,
        template=forms.TEMPLATES_PATH + "fileupload.pt"
    )


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
        return colander.null


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
    user_id = forms.id_node()
    name = colander.SchemaNode(
            colander.String(),
            widget=deferred_edit_adminonly_widget,
            title=u'Nom')

    goal = colander.SchemaNode(
            colander.String(),
            title=u'Activité')

    email = forms.mail_node(missing=u'')

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
        widget=files.deferred_upload_widget,
        title="Choisir un logo",
        validator=validate_image_mime,
        missing=colander.drop,
        description=u"Charger un fichier de type image *.png *.jpeg \
*.jpg ...")

    header = colander.SchemaNode(
        FileData(),
        widget=deferred_upload_header_widget,
        title=u'Entête des fichiers PDF',
        validator=validate_image_mime,
        missing=colander.drop,
        description=u"Charger un fichier de type image *.png *.jpeg \
*.jpg ... Le fichier est idéalement au format 20/4 (par exemple 1000px x \
200 px)",
    )

    # Fields specific to the treasury
    code_compta = colander.SchemaNode(
            colander.String(),
            title=u"Compte analytique",
            description=u"Compte analytique utilisé dans le logiciel de \
comptabilité",
            missing="")

    contribution = colander.SchemaNode(
            colander.Integer(),
            widget=deform.widget.TextInputWidget(
                input_append="%",
                css_class="col-md-1"
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


def get_list_schema(company=False):
    """
    Return a schema for filtering companies list
    """
    schema = lists.BaseListsSchema().clone()
    schema.add(
        colander.SchemaNode(
        colander.String(),
        name='active',
        missing="Y",
        validator=colander.OneOf(('N', 'Y')),
        widget=deform.widget.HiddenWidget())
    )
    return schema
