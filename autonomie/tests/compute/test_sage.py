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
import pytest
import datetime
from mock import MagicMock

from autonomie.compute.task import (
    LineCompute,
    GroupCompute,
    TaskCompute,
    InvoiceCompute,
)
from autonomie.compute.sage import (
    double_lines,
    SageInvoice,
    SageFacturation,
    SageContribution,
    SageAssurance,
    SageRGInterne,
    SageRGClient,
    CustomBookEntryFactory,
    InvoiceExport,
    SageExpenseMain,
    SagePaymentMain,
    SagePaymentTva,
    SageExpensePaymentMain,
    SageExpensePaymentWaiver,
)


class Dummy(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DummyLine(Dummy, LineCompute):
    """
        Dummy line model
    """
    tva_object = None

    def get_tva(self):
        return self.tva_object


class DummyGroup(Dummy, GroupCompute):
    pass


class DummyInvoice(Dummy, InvoiceCompute):
    pass


@pytest.fixture
def app_config():
    return {
        'code_journal': 'CODE_JOURNAL',
        'compte_cg_contribution': 'CG_CONTRIB',
        'compte_rrr': 'CG_RRR',
        'compte_frais_annexes': 'CG_FA',
        'compte_rg_externe': 'CG_RG_EXT',
        'compte_rg_interne': 'CG_RG_INT',
        'compte_cg_banque': 'BANK_CG',
        'compte_cg_tva_rrr': "CG_TVA_RRR",
        "code_tva_rrr": "CODE_TVA_RRR",
        'numero_analytique': 'NUM_ANA',
        'rg_coop': 'CG_RG_COOP',
        'taux_rg_interne': "5",
        'taux_rg_client': "5",
        'contribution_cae': "10",
        'compte_cg_ndf': "CGNDF",
        'code_journal_ndf': "JOURNALNDF",
        'code_tva_ndf': "TVANDF",
        "compte_cg_waiver_ndf": "COMPTE_CG_WAIVER",
        'receipts_active_tva_module': True,
        'receipts_code_journal': "JOURNAL_RECEIPTS",
    }


@pytest.fixture
def config_request(pyramid_request, app_config, config):
    pyramid_request.config = app_config
    return pyramid_request


@pytest.fixture
def def_tva():
    return MagicMock(
        name="tva1",
        value=1960,
        default=0,
        compte_cg="TVA0001",
        compte_a_payer="TVAAPAYER0001",
        code='CTVA0001'
    )


@pytest.fixture
def tva_sans_code():
    return MagicMock(
        name="tva_sans_code",
        value=2000,
        default=0,
        compte_cg="TVA0001",
        compte_a_payer="TVAAPAYER0001",
        code=None,
    )


@pytest.fixture
def tva():
    return MagicMock(
        name="tva2",
        value=700,
        default=0,
        compte_cg="TVA0002",
        code='CTVA0002'
    )


@pytest.fixture
def tva10():
    return MagicMock(
        name="tva 10%",
        value=1000,
        default=0,
        compte_cg="TVA10",
        code='CTVA10'
    )


@pytest.fixture
def tva20():
    return MagicMock(
        name="tva 20%",
        value=2000,
        default=0,
        compte_cg="TVA20",
        code='CTVA20'
    )


@pytest.fixture
def invoice(def_tva, tva):

    p1 = MagicMock(name="product 1", compte_cg="P0001", tva=def_tva)
    p2 = MagicMock(name="product 2", compte_cg="P0002", tva=tva)
    line1 = DummyLine(
        cost=10000000,
        quantity=1,
        tva=def_tva.value,
        product=p1,
        tva_object=def_tva
    )
    line2 = DummyLine(
        cost=10000000,
        quantity=1,
        tva=def_tva.value,
        product=p1,
        tva_object=def_tva,
    )
    line3 = DummyLine(
        cost=10000000,
        quantity=1,
        tva=tva.value,
        product=p2,
        tva_object=tva,
    )

    group = DummyGroup(lines=(line1, line2, line3,))

    company = Dummy(name="company", code_compta='COMP_CG', contribution=None)
    customer = Dummy(name="customer", compte_tiers="CUSTOMER",
                     compte_cg='CG_CUSTOMER')
    invoice = TaskCompute()
    invoice.default_tva = def_tva.value
    invoice.expenses_tva = def_tva.value
    invoice.date = datetime.date(2013, 02, 02)
    invoice.customer = customer
    invoice.company = company
    invoice.official_number = "INV_001"
    invoice.line_groups = [group]
    invoice.all_lines = group.lines
    invoice.expenses_ht = 10000000
    invoice.expenses = 10000000
    return invoice


@pytest.fixture
def invoice_bug363(def_tva, tva10):
    prod = MagicMock(name="product 2", compte_cg="P0002", tva=tva10)
    lines = []

    for cost, qtity in (
        (15000000, 1),
        (2000000, 86),
        (-173010000, 1),
        (10000000, 1),
        (-201845000, 1),
        (4500000, 33),
        (1800000, 74),
        (3500000, 28),
    ):
        lines.append(
            DummyLine(
                cost=cost,
                quantity=qtity,
                tva=tva10.value,
                product=prod,
                tva_object=tva10
            )
        )

    group = DummyGroup(lines=lines)
    company = Dummy(name="company", code_compta='COMP_CG', contribution=None)
    customer = Dummy(name="customer", compte_tiers="CUSTOMER",
                     compte_cg='CG_CUSTOMER')
    invoice = TaskCompute()
    invoice.default_tva = def_tva.value
    invoice.expenses_tva = def_tva.value
    invoice.date = datetime.date(2013, 02, 02)
    invoice.customer = customer
    invoice.company = company
    invoice.official_number = "INV_001"
    invoice.line_groups = [group]
    invoice.all_lines = group.lines
    invoice.expenses_ht = 0
    invoice.expenses = 0
    return invoice


@pytest.fixture
def invoice_bug400(def_tva, tva20):
    prod = MagicMock(name="product 2", compte_cg="P0002", tva=tva20)
    lines = []

    for cost, qtity in (
        (22112500, 1),
    ):
        lines.append(
            DummyLine(
                cost=cost,
                quantity=qtity,
                tva=tva20.value,
                product=prod,
                tva_object=tva20
            )
        )

    group = DummyGroup(lines=lines)
    company = Dummy(name="company", code_compta='COMP_CG', contribution=None)
    customer = Dummy(name="customer", compte_tiers="CUSTOMER",
                     compte_cg='CG_CUSTOMER')
    invoice = TaskCompute()
    invoice.default_tva = def_tva.value
    invoice.expenses_tva = def_tva.value
    invoice.date = datetime.date(2013, 02, 02)
    invoice.customer = customer
    invoice.company = company
    invoice.official_number = "INV_001"
    invoice.line_groups = [group]
    invoice.all_lines = group.lines
    invoice.expenses_ht = 0
    invoice.expenses = 0
    return invoice


@pytest.fixture
def invoice_discount(def_tva, tva, invoice):
    discount1 = DummyLine(
        cost=10000000,
        quantity=1,
        tva=def_tva.value,
        tva_object=def_tva
    )
    discount2 = DummyLine(
        cost=10000000,
        quantity=1,
        tva=tva.value,
        tva_object=tva
    )
    invoice.discounts = [discount1, discount2]
    return invoice


@pytest.fixture
def sageinvoice(def_tva, invoice, app_config):
    return SageInvoice(
        invoice=invoice,
        config=app_config,
        default_tva=def_tva,
    )


@pytest.fixture
def sageinvoice_bug363(def_tva, invoice_bug363, app_config):
    return SageInvoice(
        invoice=invoice_bug363,
        config=app_config,
        default_tva=def_tva,
    )


@pytest.fixture
def sageinvoice_bug400(def_tva, invoice_bug400, app_config):
    return SageInvoice(
        invoice=invoice_bug400,
        config=app_config,
        default_tva=def_tva,
    )


@pytest.fixture
def sageinvoice_discount(def_tva, invoice_discount, app_config):
    return SageInvoice(
        invoice=invoice_discount,
        config=app_config,
        default_tva=def_tva
    )


@pytest.fixture
def bank():
    return Dummy(
        compte_cg=u"COMPTE_CG_BANK",
        code_journal="CODE_JOURNAL_BANK"
    )


@pytest.fixture
def payment(invoice, def_tva, bank):
    p = Dummy(
        remittance_amount=10000,
        amount=10000000,
        mode=u"chèque",
        date=datetime.date.today(),
        tva=def_tva,
        bank=bank,
        invoice=invoice,
    )
    return p


@pytest.fixture
def sagepayment(payment, config_request):
    factory = SagePaymentMain(None, config_request)
    factory.set_payment(payment)
    return factory


@pytest.fixture
def sagepayment_tva(payment, config_request):
    factory = SagePaymentTva(None, config_request)
    factory.set_payment(payment)
    return factory


@pytest.fixture
def expense():
    company = MagicMock(
        code_compta="COMP_ANA",
    )
    user = MagicMock(
        firstname="firstname",
        lastname="lastname",
        compte_tiers="COMP_TIERS",
        )

    return MagicMock(
        id=1254,
        company=company,
        user=user,
        month=5,
        year=2014,
        date=datetime.date.today(),
    )


@pytest.fixture
def expense_type():
    return MagicMock(
        code='ETYPE1',
        code_tva='CODETVA',
        compte_tva='COMPTETVA',
        contribution=True,
    )


@pytest.fixture
def expense_payment(expense, bank):
    p = Dummy(
        amount=10000000,
        mode=u"chèque",
        date=datetime.date.today(),
        expense=expense,
        bank=bank,
    )
    return p


@pytest.fixture
def sage_expense(config_request, expense):
    factory = SageExpenseMain(None, config_request)
    factory.set_expense(expense)
    return factory


@pytest.fixture
def sage_expense_payment(config_request, expense_payment):
    factory = SageExpensePaymentMain(None, config_request)
    factory.set_payment(expense_payment)
    return factory


@pytest.fixture
def sage_expense_payment_waiver(config_request, expense_payment):
    factory = SageExpensePaymentWaiver(None, config_request)
    factory.set_payment(expense_payment)
    return factory


def test_get_products(sageinvoice):
    sageinvoice.products['1'] = {'test_key': 'test'}
    assert "test_key" in sageinvoice.get_product('1', 'dontcare', 'dontcare', 20)
    assert len(
        sageinvoice.get_product('2', 'tva_compte_cg', 'tva_code', 20).keys()
    ) == 4


def test_populate_invoice_lines(sageinvoice):
    sageinvoice._populate_invoice_lines()
    sageinvoice._round_products()
    assert sageinvoice.products.keys() == ['P0001', 'P0002']
    assert sageinvoice.products['P0001']['ht'] == 20000000
    assert sageinvoice.products['P0001']['tva'] == 3920000
    assert sageinvoice.products['P0002']['ht'] == 10000000
    assert sageinvoice.products['P0002']['tva'] == 700000


def test_populate_discount_lines(sageinvoice_discount):
    sageinvoice_discount._populate_discounts()
    sageinvoice_discount._round_products()
    assert sageinvoice_discount.products.keys() == ['CG_RRR']
    assert sageinvoice_discount.products['CG_RRR']['code_tva'] == "CODE_TVA_RRR"
    assert sageinvoice_discount.products['CG_RRR']['compte_cg_tva'] == "CG_TVA_RRR"
    assert sageinvoice_discount.products['CG_RRR']['ht'] == 20000000
    assert sageinvoice_discount.products['CG_RRR']['tva'] == 2660000


def test_populate_discount_lines_without_compte_cg_tva(sageinvoice_discount):
    # If one compte_cg_tva_rrr is not def
    # No entry should be returned
    sageinvoice_discount.config.pop("compte_cg_tva_rrr")
    sageinvoice_discount._populate_discounts()
    assert sageinvoice_discount.products.keys() == []


def test_populate_discount_lines_without_code_tva(sageinvoice_discount):
    # If the code tva is not def, it should work
    sageinvoice_discount.config.pop("code_tva_rrr")
    sageinvoice_discount._populate_discounts()
    assert sageinvoice_discount.products.keys() != []


def test_round_products(sageinvoice_bug400):
    sageinvoice_bug400._populate_invoice_lines()
    sageinvoice_bug400._round_products()
    print sageinvoice_bug400.products
    assert sageinvoice_bug400.products.values()[0]['ht'] == 22113000


def test_populate_expenses(sageinvoice):
    sageinvoice.expense_tva_compte_cg = "TVA0001"
    sageinvoice._populate_expenses()
    sageinvoice._round_products()
    assert sageinvoice.products.keys() == ['CG_FA']
    assert sageinvoice.products['CG_FA']['ht'] == 20000000
    assert sageinvoice.products['CG_FA']['tva'] == 1960000


class BaseBookEntryTest():
    factory = None

    def build_factory(self, config_request):
        return self.factory(None, config_request)

    def _test_product_book_entry(
            self,
            config_request,
            wrapped_invoice,
            method,
            exp_analytic_line,
            prod_cg='P0001'):
        """
        test a book_entry output (one of a product)
        """
        wrapped_invoice.populate()
        book_entry_factory = self.build_factory(config_request)
        book_entry_factory.set_invoice(wrapped_invoice)
        product = wrapped_invoice.products[prod_cg]

        general_line, analytic_line = getattr(book_entry_factory, method)(product)

        exp_analytic_line['date'] = '020213'
        exp_analytic_line['num_facture'] = 'INV_001'
        exp_analytic_line['code_journal'] = 'CODE_JOURNAL'
        exp_general_line = exp_analytic_line.copy()
        exp_analytic_line['type_'] = 'A'
        exp_general_line['type_'] = 'G'
        exp_general_line.pop('num_analytique', '')

        assert general_line == exp_general_line
        assert analytic_line == exp_analytic_line

    def _test_invoice_book_entry(self, config_request, wrapped_invoice, method, exp_analytic_line):
        """
        test a book_entry output (one of a product)
        """
        wrapped_invoice.populate()
        book_entry_factory = self.build_factory(config_request)
        book_entry_factory.set_invoice(wrapped_invoice)

        general_line, analytic_line = getattr(book_entry_factory, method)()

        exp_analytic_line['date'] = '020213'
        exp_analytic_line['num_facture'] = 'INV_001'
        exp_analytic_line['code_journal'] = 'CODE_JOURNAL'
        exp_general_line = exp_analytic_line.copy()
        exp_analytic_line['type_'] = 'A'
        exp_general_line['type_'] = 'G'
        exp_general_line.pop('num_analytique', '')

        assert general_line == exp_general_line
        assert analytic_line == exp_analytic_line


def decoratorfunc(a, b):
    return {'type_': 'A', 'key': 'value', 'num_analytique': 'NUM'}


def test_double_lines():
    res = list(double_lines(decoratorfunc)(None, None))
    assert res == [
        {'type_': 'G', 'key': 'value'},
        {'type_': 'A', 'key': 'value', 'num_analytique': 'NUM'}
        ]


class TestSageFacturation(BaseBookEntryTest):
    factory = SageFacturation

    def test__has_tva_value(self):
        product = {'tva': 0.5}
        assert SageFacturation._has_tva_value(product)
        product = {'tva': 0.0}
        assert not SageFacturation._has_tva_value(product)
        product = {'tva': -0.5}
        assert SageFacturation._has_tva_value(product)

    def test_credit_totalht(self, sageinvoice, config_request):
        res = {
            'libelle': 'customer company',
            'compte_cg': 'P0001',
            'num_analytique': 'COMP_CG',
            'code_tva': 'CTVA0001',
            'credit': 20000000,
        }
        method = "credit_totalht"
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_credit_tva(self, sageinvoice, config_request):
        res = {'libelle': 'customer company',
            'compte_cg': 'TVA0001',
            'num_analytique': 'COMP_CG',
            'code_tva': 'CTVA0001',
            'credit': 3920000}
        method = "credit_tva"
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_debit_ttc(self, config_request, sageinvoice):
        method = "debit_ttc"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CUSTOMER',
            'num_analytique': 'COMP_CG',
            'compte_tiers': 'CUSTOMER',
            'debit': 23920000,
            'echeance': '040313'}
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_discount_ht(self, sageinvoice_discount, config_request):
        # REF #307 : https://github.com/CroissanceCommune/autonomie/issues/307
        method = "credit_totalht"
        res = {
            'libelle': "customer company",
            'compte_cg': 'CG_RRR',
            'num_analytique': 'COMP_CG',
            'code_tva': 'CODE_TVA_RRR',
            'debit': 20000000,
        }
        self._test_product_book_entry(
            config_request,
            sageinvoice_discount,
            method,
            res,
            'CG_RRR',
        )

    def test_discount_tva(self, sageinvoice_discount, config_request):
        # REF #307 : https://github.com/CroissanceCommune/autonomie/issues/307
        res = {
            'libelle': 'customer company',
            'compte_cg': 'CG_TVA_RRR',
            'num_analytique': 'COMP_CG',
            'code_tva': 'CODE_TVA_RRR',
            'debit': 1960000 + 700000 ,
        }
        method = "credit_tva"
        self._test_product_book_entry(
            config_request,
            sageinvoice_discount,
            method,
            res,
            'CG_RRR',
        )

    def test_discount_ttc(self, config_request, sageinvoice_discount):
        # REF #307 : https://github.com/CroissanceCommune/autonomie/issues/307
        method = "debit_ttc"
        res = {
            'libelle': 'customer company',
            'compte_cg': 'CG_CUSTOMER',
            'num_analytique': 'COMP_CG',
            'compte_tiers': 'CUSTOMER',
            'credit': 20000000 + 1960000 + 700000,
            'echeance': '040313',
        }
        self._test_product_book_entry(
            config_request,
            sageinvoice_discount,
            method,
            res,
            'CG_RRR',
        )

    def test_bug363(self, config_request, sageinvoice_bug363):
        res = {'libelle': 'customer company',
            'compte_cg': 'TVA10',
            'num_analytique': 'COMP_CG',
            'code_tva': 'CTVA10',
            'credit': 20185000}
        method = "credit_tva"
        self._test_product_book_entry(
            config_request,
            sageinvoice_bug363, method, res, "P0002")



class TestSageContribution(BaseBookEntryTest):
    factory = SageContribution

    def test_debit_entreprise(self, config_request, sageinvoice):
        method = "debit_entreprise"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CONTRIB',
            'num_analytique': 'COMP_CG',
            'debit':2000000}
        self._test_product_book_entry(
            config_request, sageinvoice, method, res)

    def test_credit_entreprise(self, config_request, sageinvoice):
        method = "credit_entreprise"
        res = {'libelle': 'customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'COMP_CG',
            'credit':2000000}
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_debit_cae(self, config_request, sageinvoice):
        method = "debit_cae"
        res = {'libelle': 'customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'NUM_ANA',
            'debit':2000000}
        self._test_product_book_entry(config_request,sageinvoice, method, res)

    def test_credit_cae(self, config_request, sageinvoice):
        method = "credit_cae"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CONTRIB',
            'num_analytique': 'NUM_ANA',
            'credit':2000000}
        self._test_product_book_entry(config_request,sageinvoice, method, res)

    def test_discount_line_inversion_debit_entr(self, config_request, sageinvoice_discount):
        # REF #333 : https://github.com/CroissanceCommune/autonomie/issues/333
        # Débit et crédit vont dans le sens inverse pour les remises (logique)
        method = "debit_entreprise"
        res = {'libelle': 'customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'COMP_CG',
            'debit': 2000000}
        self._test_product_book_entry(config_request,
            sageinvoice_discount,
            method,
            res,
            'CG_RRR',
        )

    def test_discount_line_inversion_credit_entr(self, config_request, sageinvoice_discount):
        # REF #333 : https://github.com/CroissanceCommune/autonomie/issues/333
        # Débit et crédit vont dans le sens inverse pour les remises (logique)
        method = "credit_entreprise"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CONTRIB',
            'num_analytique': 'COMP_CG',
            'credit':2000000}
        self._test_product_book_entry(config_request,
            sageinvoice_discount,
            method,
            res,
            'CG_RRR',
        )

    def test_discount_line_inversion_debit_cae(self, config_request, sageinvoice_discount):
        # REF #333 : https://github.com/CroissanceCommune/autonomie/issues/333
        # Débit et crédit vont dans le sens inverse pour les remises (logique)
        method = "debit_cae"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CONTRIB',
            'num_analytique': 'NUM_ANA',
            'debit':2000000}
        self._test_product_book_entry(config_request,
            sageinvoice_discount,
            method,
            res,
            'CG_RRR',
        )

    def test_discount_line_inversion_credit_cae(self, config_request, sageinvoice_discount):
        # REF #333 : https://github.com/CroissanceCommune/autonomie/issues/333
        # Débit et crédit vont dans le sens inverse pour les remises (logique)
        method = "credit_cae"
        res = {'libelle': 'customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'NUM_ANA',
            'credit':2000000}
        self._test_product_book_entry(config_request,
            sageinvoice_discount,
            method,
            res,
            'CG_RRR',
        )


class TestCustomAssurance(BaseBookEntryTest):
    # Amount = 2000 0.05 * somme des ht des lignes + expense_ht
    # Migrate the export module Assurance to a custom module
    def build_factory(self, config_request):
        return CustomBookEntryFactory(
            None,
            config_request,
            Dummy(
                compte_cg_debit='CG_ASSUR',
                compte_cg_credit='CG_ASSUR',
                percentage=5,
                label_template=u"{client.name} {entreprise.name}"
            )
        )



    def test_debit_entreprise(self, config_request, sageinvoice):
        method = 'debit_entreprise'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_ASSUR',
                'num_analytique': 'COMP_CG',
                'debit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_entreprise(self, config_request, sageinvoice):
        method = 'credit_entreprise'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'BANK_CG',
                'num_analytique': 'COMP_CG',
                'credit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_debit_cae(self, config_request, sageinvoice):
        method = 'debit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'BANK_CG',
                'num_analytique': 'NUM_ANA',
                'debit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_cae(self, config_request, sageinvoice):
        method = 'credit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_ASSUR',
                'num_analytique': 'NUM_ANA',
                'credit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)


class TestCustomCGScop(BaseBookEntryTest):
    # Migrate the export module CGScop to a custom module
    def build_factory(self, config_request):
        return CustomBookEntryFactory(
            None,
            config_request,
            Dummy(
                compte_cg_debit='CG_SCOP',
                compte_cg_credit='CG_DEB',
                percentage=5,
                label_template=u"{client.name} {entreprise.name}"
            )
        )


    def test_debit_entreprise(self, config_request, sageinvoice):
        method = 'debit_entreprise'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_SCOP',
                'num_analytique': 'COMP_CG',
                'debit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_entreprise(self, config_request, sageinvoice):
        method = 'credit_entreprise'
        res = {
                'libelle': 'customer company',
                'num_analytique': 'COMP_CG',
                'compte_cg': 'BANK_CG',
                'credit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_debit_cae(self, config_request, sageinvoice):
        method = 'debit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'BANK_CG',
                'num_analytique': 'NUM_ANA',
                'debit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_cae(self, config_request, sageinvoice):
        method = 'credit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_DEB',
                'num_analytique': 'NUM_ANA',
                'credit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)


class TestCustomBookEntryFactory(BaseBookEntryTest):
    # Replaced SageContributionOrganic
    libelle = 'Contribution Organic customer company'

    def build_factory(self, config_request):
        return CustomBookEntryFactory(
            None,
            config_request,
            Dummy(
                compte_cg_debit='CG_ORGA',
                compte_cg_credit='CG_DEB_ORGA',
                percentage=5,
                label_template=u"Contribution Organic {client.name} \
{entreprise.name}"
            )
        )


    def test_debit_entreprise(self, config_request, sageinvoice):
        method = 'debit_entreprise'
        res = {
                'libelle': self.libelle,
                'compte_cg': 'CG_ORGA',
                'num_analytique': 'COMP_CG',
                'debit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_entreprise(self, config_request, sageinvoice):
        method = 'credit_entreprise'
        res = {
                'libelle': self.libelle,
                'num_analytique': 'COMP_CG',
                'compte_cg': 'BANK_CG',
                'credit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_debit_cae(self, config_request, sageinvoice):
        method = 'debit_cae'
        res = {
                'libelle': self.libelle,
                'compte_cg': 'BANK_CG',
                'num_analytique': 'NUM_ANA',
                'debit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_cae(self, config_request, sageinvoice):
        method = 'credit_cae'
        res = {
                'libelle': self.libelle,
                'compte_cg': 'CG_DEB_ORGA',
                'num_analytique': 'NUM_ANA',
                'credit': 2000000,
                }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)


class TestSageRGInterne(BaseBookEntryTest):
    factory = SageRGInterne

    def test_debit_entreprise(self, config_request, sageinvoice):
        method = "debit_entreprise"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'CG_RG_INT',
            'num_analytique': 'COMP_CG',
            'debit':1196000}
        self._test_product_book_entry(config_request,sageinvoice, method, res)

    def test_credit_entreprise(self, config_request, sageinvoice):
        method = "credit_entreprise"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'COMP_CG',
            'credit':1196000}
        self._test_product_book_entry(config_request,sageinvoice, method, res)

    def test_debit_cae(self, config_request, sageinvoice):
        method = "debit_cae"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'NUM_ANA',
            'debit':1196000}
        self._test_product_book_entry(config_request,sageinvoice, method, res)

    def test_credit_cae(self, config_request, sageinvoice):
        method = "credit_cae"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'CG_RG_INT',
            'num_analytique': 'NUM_ANA',
            'credit':1196000}
        self._test_product_book_entry(config_request,sageinvoice, method, res)


class TestSageRGClient(BaseBookEntryTest):
    factory = SageRGClient

    def test_debit_entreprise(self, config_request, sageinvoice):
        method = 'debit_entreprise'
        res = {
                'libelle': 'RG customer company',
                'compte_cg': 'CG_RG_EXT',
                'num_analytique': 'COMP_CG',
                'echeance':'020214',
                'debit': 1196000,
                }
        self._test_product_book_entry(config_request,sageinvoice, method, res)

    def test_credit_entreprise(self, config_request, sageinvoice):
        method = 'credit_entreprise'
        res = {
                'libelle': 'RG customer company',
                'num_analytique': 'COMP_CG',
                'compte_cg': 'CG_CUSTOMER',
                'compte_tiers': 'CUSTOMER',
                'echeance':'020214',
                'credit': 1196000,
                }
        self._test_product_book_entry(config_request,sageinvoice, method, res)


class TestSageExport():
    def test_modules(self, config_request):
        config = {
            'sage_contribution':'1',
            'sage_assurance':'1',
            'sage_cgscop':'0'
        }
        config_request.config = config
        exporter = InvoiceExport(None, config_request)
        assert len(exporter.modules) == 3
        sage_factories = [SageFacturation, SageContribution, SageAssurance]
        for fact in sage_factories:
            assert True in [isinstance(module, fact)
                for module in exporter.modules]


@pytest.mark.payment
class TestSagePaymentMain():
    def test_base_entry(self, sagepayment):
        today = datetime.date.today()
        assert sagepayment.reference == "INV_001/10000"
        assert sagepayment.code_journal == "CODE_JOURNAL_BANK"
        assert sagepayment.date == today.strftime("%d%m%y")
        assert sagepayment.mode == u"chèque"
        assert sagepayment.libelle == u"company / Rgt customer"

    def test_credit_client(self, sagepayment):
        g_entry, entry = sagepayment.credit_client(10000000)
        assert entry['compte_cg'] == 'CG_CUSTOMER'
        assert entry['compte_tiers'] == 'CUSTOMER'
        assert entry['credit'] == 10000000

    def test_debit_banque(self, sagepayment):
        g_entry, entry = sagepayment.debit_banque(10000000)
        assert entry['compte_cg'] == "COMPTE_CG_BANK"
        assert entry['debit'] == 10000000


@pytest.mark.payment
class TestSagePaymentTva():
    def test_get_amount(self, sagepayment_tva, tva_sans_code, payment):
        payment.tva = tva_sans_code
        sagepayment_tva.set_payment(payment)
        amount = sagepayment_tva.get_amount()
        # tva inversée d'un paiement de 10000000 à 20%
        assert amount == 1666667

    def test_credit_tva(self, sagepayment_tva, tva_sans_code, payment):
        g_entry, entry = sagepayment_tva.credit_tva(10000000)
        assert entry['credit'] == 10000000
        assert entry['compte_cg'] == 'TVAAPAYER0001'
        assert entry['code_taxe'] == 'CTVA0001'

        # Test if there is no tva code
        payment.tva = tva_sans_code
        sagepayment_tva.set_payment(payment)
        g_entry, entry = sagepayment_tva.credit_tva(10000000)
        assert 'code_taxe' not in entry


    def test_debit_tva(self, sagepayment_tva):
        g_entry, entry = sagepayment_tva.debit_tva(10000000)
        assert entry['debit'] == 10000000
        assert entry['compte_cg'] == 'TVA0001'
        assert entry['code_taxe'] == 'CTVA0001'



@pytest.mark.expense
class TestSageExpenseMain():
    """
    Main Expense export module testing
    """
    def test_base_entry(self, sage_expense):
        assert sage_expense.libelle == "Firstname LASTNAME/frais 5 2014"
        assert sage_expense.num_feuille == "ndf52014"
        assert sage_expense.code_journal == "JOURNALNDF"

        base_entry = sage_expense.get_base_entry()
        for i in ('code_journal', 'date', 'libelle', 'num_feuille', 'type_'):
            assert i in base_entry

    def test_credit(self, sage_expense):
        general, analytic = sage_expense._credit(2500000)
        assert analytic['type_'] == 'A'
        assert analytic['credit'] == 2500000
        assert analytic['compte_cg'] == "CGNDF"
        assert analytic['num_analytique'] == "COMP_ANA"
        assert analytic['compte_tiers'] == "COMP_TIERS"

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()


    def test_debit_ht(self, sage_expense, expense_type):
        general, analytic = sage_expense._debit_ht(expense_type, 150000)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "ETYPE1"
        assert analytic['num_analytique'] == 'COMP_ANA'
        assert analytic['code_tva'] == 'CODETVA'
        assert analytic['debit'] == 150000

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()

    def test_debit_tva(self, sage_expense, expense_type):
        general, analytic = sage_expense._debit_tva(expense_type, 120000)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "COMPTETVA"
        assert analytic['num_analytique'] == 'COMP_ANA'
        assert analytic['code_tva'] == 'CODETVA'
        assert analytic['debit'] == 120000

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()

    def test_credit_entreprise(self, sage_expense):
        general, analytic = sage_expense._credit_entreprise(120000)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "CG_CONTRIB"
        assert analytic['num_analytique'] == 'COMP_ANA'
        assert analytic['credit'] == 120000

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()

    def test_debit_entreprise(self, sage_expense):
        general, analytic = sage_expense._debit_entreprise(120000)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "BANK_CG"
        assert analytic['num_analytique'] == 'COMP_ANA'
        assert analytic['debit'] == 120000

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()

    def test_credit_cae(self, sage_expense):
        general, analytic = sage_expense._credit_cae(120000)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "BANK_CG"
        assert analytic['num_analytique'] == 'NUM_ANA'
        assert analytic['credit'] == 120000

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()

    def test_debit_cae(self, sage_expense):
        general, analytic = sage_expense._debit_cae(120000)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "CG_CONTRIB"
        assert analytic['num_analytique'] == 'NUM_ANA'
        assert analytic['debit'] == 120000

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()


@pytest.mark.payment
class TestSageExpensePaymentMain():
    def test_base_entry(self, sage_expense_payment):
        today = datetime.date.today()
        assert sage_expense_payment.reference == "1254"
        assert sage_expense_payment.code_journal == "CODE_JOURNAL_BANK"
        assert sage_expense_payment.date == today.strftime("%d%m%y")
        assert sage_expense_payment.mode == u"chèque"
        libelle = u"LASTNAME / REMB FRAIS mai/2014"
        assert sage_expense_payment.libelle == libelle
        assert sage_expense_payment.code_taxe == "TVANDF"
        assert sage_expense_payment.num_analytique == "COMP_ANA"

    def test_credit_bank(self, sage_expense_payment):
        g_entry, entry = sage_expense_payment.credit_bank(10000000)
        assert entry['compte_cg'] == 'COMPTE_CG_BANK'
        assert entry.get('compte_tiers', '') == ''
        assert entry['credit'] == 10000000

    def test_debit_entrepreneur(self, sage_expense_payment):
        g_entry, entry = sage_expense_payment.debit_user(10000000)
        assert entry['compte_cg'] == "CGNDF"
        assert entry['compte_tiers'] == 'COMP_TIERS'
        assert entry['debit'] == 10000000


@pytest.mark.payment
class TestSageExpensePaymentWaiver():
    def test_code_journal(self, expense_payment, config_request):
        config_request.config['code_journal_waiver_ndf'] = 'JOURNAL_ABANDON'

        sage_expense_payment_waiver = SageExpensePaymentWaiver(None, config_request)
        sage_expense_payment_waiver.set_payment(expense_payment)
        assert sage_expense_payment_waiver.code_journal == "JOURNAL_ABANDON"

    def test_base_entry(self, sage_expense_payment_waiver):
        today = datetime.date.today()
        assert sage_expense_payment_waiver.reference == "1254"
        assert sage_expense_payment_waiver.code_journal == "JOURNALNDF"
        assert sage_expense_payment_waiver.date == today.strftime("%d%m%y")
        assert sage_expense_payment_waiver.mode == u"Abandon de créance"
        libelle = u"Abandon de créance LASTNAME mai/2014"
        assert sage_expense_payment_waiver.libelle == libelle
        assert sage_expense_payment_waiver.code_taxe == ""
        assert sage_expense_payment_waiver.num_analytique == "COMP_ANA"

    def test_credit_bank(self, sage_expense_payment_waiver):
        g_entry, entry = sage_expense_payment_waiver.credit_bank(10000000)
        assert entry['compte_cg'] == 'COMPTE_CG_WAIVER'
        assert entry.get('compte_tiers', '') == ''
        assert entry['credit'] == 10000000

    def test_debit_entrepreneur(self, sage_expense_payment_waiver):
        g_entry, entry = sage_expense_payment_waiver.debit_user(10000000)
        assert entry['compte_cg'] == "CGNDF"
        assert entry['compte_tiers'] == 'COMP_TIERS'
        assert entry['debit'] == 10000000
