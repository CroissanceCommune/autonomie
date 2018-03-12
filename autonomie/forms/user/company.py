# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Form schema used to managed relationship between a user and a company
"""
import deform
import colander

from autonomie.models.company import Company


def get_companies_choices():
    """
        Return companies choices for autocomplete
    """
    return [comp.name for comp in Company.query([Company.name]).all()]


@colander.deferred
def deferred_company_input(node, kw):
    """
        Deferred company autocomplete input widget
    """
    companies = get_companies_choices()
    wid = deform.widget.AutocompleteInputWidget(
        values=companies,
    )
    return wid


@colander.deferred
def deferred_company_validator(node, kw):
    """
    Check that the validated name is one of the original choices
    """
    return colander.OneOf(get_companies_choices())


class CompanySchema(colander.SequenceSchema):
    company = colander.SchemaNode(
        colander.String(),
        title=u"Nom de l'entreprise",
        widget=deferred_company_input,
        validator=deferred_company_validator
    )


def get_company_association_schema():
    """
    Return the schema used to associate a user to an existing company
    """
    schema = colander.Schema()
    schema.add(
        CompanySchema(
            name='companies',
            title=u"Entreprise(s)",
            widget=deform.widget.SequenceWidget(
                add_subitem_text_template=u"Ajouter une entreprise",
                min_len=1,
            ),
            description=u"Taper les premières lettres du nom \
d'une entreprise existante"
        )
    )
    return schema
