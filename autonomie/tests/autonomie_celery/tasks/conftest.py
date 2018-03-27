# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
import datetime


@pytest.fixture
def income_measure_type_categories(dbsession):
    from autonomie.models.accounting.income_statement_measures import (
        IncomeStatementMeasureTypeCategory,
    )
    result = []
    for i in (u"Produits", u"Achats"):
        cat = IncomeStatementMeasureTypeCategory(label=i)
        dbsession.add(cat)
        result.append(cat)
    dbsession.flush()
    return result


@pytest.fixture
def income_measure_types(dbsession, income_measure_type_categories):
    from autonomie.models.accounting.income_statement_measures import (
        IncomeStatementMeasureType,
    )
    types = []
    for (
        label, category_index, account_prefix, is_total, total_type
    ) in (
        ('Label 1', 0, u"701", False, ""),
        ('Label 2', 0, u"701,702", False, ""),
        ('Label 3', 1, u"601", False, ""),
        ('Total partiel autres achats', 1, u"6,-601", True, "account_prefix"),
        ('Total produits et achats', 1, u"Produits,Achats", True, "categories"),
        ('Ratio produits et achats', 1, u"{Achats} * 100 / {Produits}", True,
         "categories"),
    ):
        typ = IncomeStatementMeasureType(
            label=label,
            category_id=income_measure_type_categories[category_index].id,
            account_prefix=account_prefix,
            is_total=is_total,
            total_type=total_type,
        )
        dbsession.add(typ)
        typ.category = income_measure_type_categories[category_index]
        types.append(typ)
    return types


@pytest.fixture
def treasury_measure_types(dbsession):
    from autonomie.models.accounting.treasury_measures import (
        TreasuryMeasureType,
    )
    types = []
    for internal_id, start, label in (
        (1, '5', u"Trésorerie du jour",),
        (2, "42,-421,-425,43,44", u"Impôts, taxes et cotisations dues",),
        (3, "40", u"Fournisseurs à payer",),
        (5, "421", u"Salaires à payer",),
        (6, "41", u"Clients à encaisser"),
        (7, '425', u"Notes de dépenses à payer"),
        (9, "1,2,3", u"Comptes bilan non pris en compte"),
    ):
        typ = TreasuryMeasureType(
            internal_id=internal_id, account_prefix=start, label=label
            )
        dbsession.add(typ)
        types.append(typ)
    return types


@pytest.fixture
def analytical_upload(dbsession):
    from autonomie.models.accounting.operations import (
        AccountingOperationUpload
    )
    item = AccountingOperationUpload(
        md5sum="oooo",
        filetype="analytical_balance",
        date=datetime.date.today(),
    )
    dbsession.add(item)
    return item


@pytest.fixture
def analytical_operations(dbsession, analytical_upload, company):
    from autonomie.models.accounting.operations import (
        AccountingOperation,
    )
    operations = []
    for general, label, debit, credit in (
        ("50000", u"depot banque 1", 1000, 0),
        ("51000", u"depo banque 2", 1000, 0),
        ("42000", u"cotisation", 0, 1000),
        ("425000", u"dépenses", 0, 1000),
    ):
        op = AccountingOperation(
            analytical_account=company.code_compta,
            general_account=general,
            label=label,
            debit=debit,
            credit=credit,
            upload_id=analytical_upload.id,
            company_id=company.id,
        )
        dbsession.add(op)
        operations.append(op)
    return operations


@pytest.fixture
def general_upload(dbsession):
    from autonomie.models.accounting.operations import (
        AccountingOperationUpload
    )
    item = AccountingOperationUpload(
        md5sum="oooo",
        filetype="general_ledger",
        date=datetime.date.today(),
    )
    dbsession.add(item)
    return item


@pytest.fixture
def general_operations(dbsession, general_upload, company):
    from autonomie.models.accounting.operations import (
        AccountingOperation,
    )
    operations = []
    for month, general, label, debit, credit in (
        (1, "70100", u"", 1000, 0),
        (1, "70200", u"", 1000, 0),
        (1, "602", u"avoir", 0, 1000),
        (1, "601", u"achats", 0, 1000),
        (2, "70100", u"", 2000, 0),
        (2, "70200", u"", 2000, 0),
        (2, "602", u"avoir", 0, 2000),
        (2, "601", u"achats", 0, 2000),
    ):
        op = AccountingOperation(
            date=datetime.date(2017, month, 1),
            analytical_account=company.code_compta,
            general_account=general,
            label=label,
            debit=debit,
            credit=credit,
            upload_id=general_upload.id,
            company_id=company.id,
        )
        dbsession.add(op)
        operations.append(op)
    return operations
