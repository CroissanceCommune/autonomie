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

from autonomie.models.company import CompanyActivity

from autonomie.forms.validators import validate_image_mime
from autonomie import forms
from autonomie.forms.custom_types import QuantityType
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
    if not request.has_permission('admin_company', request.context):
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
    return files.CustomFileUploadWidget(tmpstore)


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
    request = kw['request']
    if not request.has_permission("admin_treasury", request.context):
        del schema['RIB']
        del schema['IBAN']
        del schema['code_compta']
        del schema['contribution']


@colander.deferred
def deferred_company_datas_select(node, kw):
    values = CompanyActivity.query('id', 'label').all()
    values.insert(0, ('', "- Sélectionner un type d'activité"))
    return deform.widget.SelectWidget(
        values=values
    )


@colander.deferred
def deferred_company_datas_validator(node, kw):
    ids = [entry[0] for entry in CompanyActivity.query('id')]
    return colander.OneOf(ids)


class CompanyActivitySchema(colander.SequenceSchema):
    id = colander.SchemaNode(
        colander.Integer(),
        title=u"un domaine",
        widget=deferred_company_datas_select,
        validator=deferred_company_datas_validator,
    )


class CompanySchema(colander.MappingSchema):
    """
        Company add/edit form schema
    """
    user_id = forms.id_node()
    name = colander.SchemaNode(
        colander.String(),
        widget=deferred_edit_adminonly_widget,
        title=u'Nom'
    )

    goal = colander.SchemaNode(
        colander.String(),
        title=u"Descriptif de l'activité")

    activities = CompanyActivitySchema(
        title=u"Domaines d'activité",
        missing=colander.drop,
    )

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
            QuantityType(),
            widget=deform.widget.TextInputWidget(
                input_append="%",
                css_class="col-md-1"
                ),
            validator=colander.Range(
                min=0,
                max=100,
                min_err=u"Veuillez fournir un nombre supérieur à 0",
                max_err=u"Veuillez fournir un nombre inférieur à 100"),
            title=u"Contribution à la CAE",
            missing=colander.drop,
            description=u"Pourcentage que cette entreprise contribue à la CAE",
    )

    cgv = forms.textarea_node(
        title=u"Conditions générales complémentaires",
        richwidget=True,
        missing="",
    )

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
            colander.Boolean(),
            name='active',
            label=u"Inclure les entreprises désactivées",
        )
    )
    return schema
