# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Accounting module related schemas
"""
import re
import datetime
import colander
import deform
import deform_extensions
from colanderalchemy import SQLAlchemySchemaNode
from sqlalchemy import distinct

from autonomie_base.models.base import DBSESSION
from autonomie.compute.parser import NumericStringParser
from autonomie.models.accounting.operations import AccountingOperation
from autonomie.models.accounting.treasury_measures import TreasuryMeasureGrid
from autonomie.models.accounting.income_statement_measures import (
    IncomeStatementMeasureGrid,
    IncomeStatementMeasureType,
    IncomeStatementMeasureTypeCategory,
)
from autonomie.models.company import Company
from autonomie import forms
from autonomie.forms.custom_types import CsvTuple
from autonomie.forms.lists import BaseListsSchema
from autonomie.forms.widgets import CleanMappingWidget
from autonomie.forms.fields import YearPeriodSchema


def get_upload_list_schema():
    """
    Build a schema for Accounting Operation upload listing
    """
    schema = BaseListsSchema().clone()
    del schema['search']

    schema.insert(
        0,
        colander.SchemaNode(
            colander.String(),
            name='filetype',
            widget=deform.widget.SelectWidget(
                values=(
                    ('all', u'Tous les types de fichier'),
                    ('general_ledger', u"Grand livre"),
                    ('analytical_balance', u"Balance analytique"),
                )
            ),
            default='all',
            missing=colander.drop,
        )
    )
    schema.insert(
        0,
        YearPeriodSchema(
            name='period',
            widget=CleanMappingWidget(),
            missing=colander.drop,
        )
    )
    return schema


@colander.deferred
def deferred_analytical_account_widget(node, kw):
    """
    Defer analytical widget
    """
    datas = DBSESSION().query(
        distinct(AccountingOperation.analytical_account)
    ).order_by(AccountingOperation.analytical_account).all()
    datas = zip(*datas)[0]
    values = zip(datas, datas)
    values.insert(0, ('', u'Filtrer par code analytique'))
    return deform.widget.Select2Widget(values=values)


@colander.deferred
def deferred_general_account_widget(node, kw):
    """
    Defer analytical widget
    """
    datas = DBSESSION().query(
        distinct(AccountingOperation.general_account)
    ).order_by(AccountingOperation.general_account).all()
    datas = zip(*datas)[0]
    values = zip(datas, datas)
    values.insert(0, ('', u'Filtrer par compte général'))
    return deform.widget.Select2Widget(values=values)


@colander.deferred
def deferred_company_id_widget(node, kw):
    """
    Defer the company id selection widget
    """
    datas = DBSESSION().query(
        distinct(AccountingOperation.company_id)
    ).all()
    datas = zip(*datas)[0]
    values = DBSESSION().query(Company.id, Company.name).all()
    values.insert(0, ('', u"Filtrer par entreprise"))
    return deform.widget.Select2Widget(values=values)


def get_operation_list_schema():
    """
    Build a schema listing operations
    """
    schema = BaseListsSchema().clone()
    del schema['search']
    schema.insert(
        0,
        colander.SchemaNode(
            colander.Boolean(),
            name='include_associated',
            title="",
            label=u"Inclure les opérations associées à une entreprise",
            default=True,
            missing=colander.drop,
        )
    )
    schema.insert(
        0,
        colander.SchemaNode(
            colander.String(),
            name='analytical_account',
            title="",
            widget=deferred_analytical_account_widget,
            missing=colander.drop,
        )
    )
    schema.insert(
        0,
        colander.SchemaNode(
            colander.String(),
            name='general_account',
            title="",
            widget=deferred_general_account_widget,
            missing=colander.drop,
        )
    )
    schema.insert(
        0,
        colander.SchemaNode(
            colander.Integer(),
            name='company_id',
            title="",
            widget=deferred_company_id_widget,
            missing=colander.drop
        )
    )

    return schema


def get_treasury_measures_list_schema():
    """
    Build the schema used to list treasury measures

    :returns: A form schema
    :rtype: colander.Schema
    """
    schema = BaseListsSchema().clone()
    del schema['search']

    def get_year_options(kw):
        return TreasuryMeasureGrid.get_years()

    node = forms.year_select_node(
        name='year',
        query_func=get_year_options,
        missing=-1,
        description=u"Année de dépôt"
    )

    schema.insert(0, node)
    return schema


def get_income_statement_measures_list_schema():
    """
    Build the schema used to list treasury measures

    :returns: A form schema
    :rtype: colander.Schema
    """
    schema = BaseListsSchema().clone()
    del schema['search']
    del schema['page']
    del schema['items_per_page']

    def get_year_options(kw):
        cid = kw['request'].context.get_company_id()
        years = IncomeStatementMeasureGrid.get_years(company_id=cid)
        current_year = datetime.date.today().year
        if current_year not in years:
            years.append(current_year)
        return years

    node = forms.year_select_node(
        name='year',
        query_func=get_year_options,
        title=u"Année"
    )

    schema.insert(0, node)
    return schema


@colander.deferred
def deferred_categories_widget(node, kw):
    query = DBSESSION().query(
        IncomeStatementMeasureTypeCategory.label,
        IncomeStatementMeasureTypeCategory.label,
    )
    choices = query.filter_by(active=True).all()
    return deform.widget.CheckboxChoiceWidget(values=choices)


@colander.deferred
def deferred_complexe_total_description(node, kw):
    categories = "".join(
        [i[0] for i in
        DBSESSION().query(
            IncomeStatementMeasureTypeCategory.label
        ).filter_by(active=True)
         ]
    )
    types = ",".join((
        i[0]
        for i in DBSESSION().query(
            IncomeStatementMeasureType.label
        ).filter_by(active=True)
    ))
    return u"""
Combiner plusieurs catégories et indicateurs au travers d'opérations
arithmétiques.
Les noms des variables (catégories ou indicateurs) doivent être encadrés de {}.
Exemple : {Salaires et Cotisations} + {Charges} / 100.
Liste des catégories : %s. Liste des indicateurs : %s""" % (categories, types)


@colander.deferred
def deferred_label_validator(node, kw):
    """
    Deffered label validator, check whether a type or a category has the same
    label
    """
    context = kw['request'].context

    category_query = DBSESSION().query(IncomeStatementMeasureTypeCategory.label)
    category_query.filter_by(active=True)

    if isinstance(context, IncomeStatementMeasureTypeCategory):
        category_query = category_query.filter(
            IncomeStatementMeasureTypeCategory.id != context.id
        )
    category_labels = [i[0] for i in category_query]

    type_query = DBSESSION().query(IncomeStatementMeasureType.label)
    type_query.filter_by(active=True)

    if isinstance(context, IncomeStatementMeasureType):
        type_query = type_query.filter(
            IncomeStatementMeasureType.id != context.id
        )
    type_labels = [i[0] for i in type_query]

    def label_validator(node, value):
        if ':' in value or '!' in value:
            raise colander.Invalid(
                u"Erreur de syntax (les caractères ':' et '!' sont interdits"
            )

        if value in category_labels:
            raise colander.Invalid(
                u"Une catégories porte déjà ce nom"
            )
        if value in type_labels:
            raise colander.Invalid(u"Un type d'indicateurs porte déjà ce nom")
    return label_validator


BRACES_REGEX = re.compile(r'\{([^}]+)\}\s?')


def complex_total_validator(node, value):
    """
    Validate the complex total syntax
    """
    if len(value) > 254:
        raise colander.Invalid(u"Ce champ est limité à 255 caractères")

    if value.count('{') != value.count('}'):
        raise colander.Invalid(u"Erreur de syntaxe")

    fields = BRACES_REGEX.findall(value)

    format_dict = dict((field, 1) for field in fields)
    try:
        temp = value.format(**format_dict)
    except Exception as err:
        raise colander.Invalid(u"Erreur de syntaxe : {0}".format(err.message))

    parser = NumericStringParser()
    try:
        temp = parser.eval(temp)
    except Exception as err:
        raise colander.Invalid(u"Erreur de syntaxe : {0}".format(err.message))


def get_admin_income_statement_measure_schema(total=False):
    """
    Build the schema for income statement measure type edit/add

    Total types are more complex and can be :

        * The sum of categories
        * A list of account prefix (like the common type of measure_types)
    """
    if total:
        schema = SQLAlchemySchemaNode(
            IncomeStatementMeasureType,
            includes=(
                "category_id",
                'label',
                "account_prefix",
                'is_total',
                'order',
            ),
        )
        schema['label'].validator = deferred_label_validator
        schema['is_total'].widget = deform.widget.HiddenWidget()
        schema.add_before(
            'account_prefix',
            colander.SchemaNode(
                colander.String(),
                name="total_type",
                title=u"Cet indicateur est il définit comme :",
                widget=deform_extensions.RadioChoiceToggleWidget(
                    values=(
                        (
                            "categories",
                            u"la somme des indicateurs de une ou plusieurs "
                            u"catégories ?",
                            "categories",
                        ),
                        (
                            "account_prefix",
                            u"un groupement d'écritures ?",
                            "account_prefix",
                        ),
                        (
                            "complex_total",
                            u"le résultat d'une formule arithmétique basée sur "
                            u"les catégories et les indicateurs ?",
                            "complex_total",
                        ),
                    )
                ),
                missing=colander.drop,
            )
        )
        schema['account_prefix'].missing = ""

        schema.add(
            colander.SchemaNode(
                colander.String(),
                name="complex_total",
                title=u"Combinaison complexe de catégories et d'indicateurs",
                description=deferred_complexe_total_description,
                validator=complex_total_validator,
                missing=""
            )
        )

        schema.add(
            colander.SchemaNode(
                CsvTuple(),
                name="categories",
                title=u"Somme des catégories",
                description=u"Représentera la somme des catégories "
                u"sélectionnées",
                widget=deferred_categories_widget,
            )
        )
    else:
        schema = SQLAlchemySchemaNode(
            IncomeStatementMeasureType,
            excludes=('is_total', "categories")
        )
        schema['label'].validator = deferred_label_validator
    return schema


def get_admin_income_statement_category_schema():
    """
    Build the schema for income statement measure type category edition
    """
    schema = SQLAlchemySchemaNode(
        IncomeStatementMeasureTypeCategory,
        includes=("label", "order")
    )
    schema['label'].validator = deferred_label_validator
    return schema
