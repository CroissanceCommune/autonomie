# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Accounting module related schemas
"""
import datetime
import colander
import deform
import deform_extensions
from colanderalchemy import SQLAlchemySchemaNode
from sqlalchemy import distinct

from autonomie_base.models.base import DBSESSION
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
        IncomeStatementMeasureTypeCategory.id,
        IncomeStatementMeasureTypeCategory.label,
    )
    choices = query.filter_by(active=True).all()
    return deform.widget.CheckboxChoiceWidget(values=choices)


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
                "categories",
                "account_prefix",
                'is_total'
            ),
        )
        schema['categories'].typ = CsvTuple()
        schema['categories'].widget = deferred_categories_widget
        schema['categories'].validator = colander.Length(min=1)
        schema['is_total'].widget = deform.widget.HiddenWidget()
        schema.add_before(
            'categories',
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
                    )
                ),
                missing=colander.drop,
            )
        )
        schema['account_prefix'].missing = ""
    else:
        schema = SQLAlchemySchemaNode(
            IncomeStatementMeasureType,
            excludes=('is_total', "categories")
        )
    return schema


def get_admin_income_statement_category_schema():
    """
    Build the schema for income statement measure type category edition
    """
    return SQLAlchemySchemaNode(
        IncomeStatementMeasureTypeCategory,
        includes=("label", "order")
    )
