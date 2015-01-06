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
    TaskCompute,
    InvoiceCompute,
)
from autonomie.compute.sage import (
    double_lines,
    SageInvoice,
    SageFacturation,
    SageContribution,
    SageAssurance,
    SageCGScop,
    SageContributionOrganic,
    SageRGInterne,
    SageRGClient,
    InvoiceExport,
    SageExpenseMain,
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


class DummyInvoice(Dummy, InvoiceCompute):
    pass

def get_config():
    return {
            'code_journal': 'CODE_JOURNAL',
            'compte_cg_contribution':'CG_CONTRIB',
            'compte_rrr': 'CG_RRR',
            'compte_frais_annexes': 'CG_FA',
            'compte_cg_assurance': 'CG_ASSUR',
            'compte_cg_debiteur': 'CG_DEB',
            'compte_cgscop': 'CG_SCOP',
            'compte_cg_organic': "CG_ORGA",
            'compte_cg_debiteur_organic': "CG_DEB_ORGA",
            'compte_rg_externe': 'CG_RG_EXT',
            'compte_rg_interne': 'CG_RG_INT',
            'compte_cg_banque': 'BANK_CG',
            'compte_cg_tva_rrr': "CG_TVA_RRR",
            "code_tva_rrr": "CODE_TVA_RRR",
            'numero_analytique': 'NUM_ANA',
            'rg_coop': 'CG_RG_COOP',
            'taux_assurance': "5",
            'taux_cgscop': "5",
            'taux_rg_interne': "5",
            'taux_rg_client': "5",
            'taux_contribution_organic': "5",
            'contribution_cae': "10",
            'compte_cg_ndf': "CGNDF",
            'code_journal_ndf':"JOURNALNDF",
            }

@pytest.fixture
def def_tva():
    return MagicMock(
        name="tva1",
        value=1960,
        default=0,
        compte_cg="TVA0001",
        code='CTVA0001'
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
def invoice(def_tva, tva):

    p1 = MagicMock(name="product 1", compte_cg="P0001", tva=def_tva)
    p2 = MagicMock(name="product 2", compte_cg="P0002", tva=tva)
    line1 = DummyLine(
        cost=10000,
        quantity=1,
        tva=def_tva.value,
        product=p1,
        tva_object=def_tva
    )
    line2 = DummyLine(
        cost=10000,
        quantity=1,
        tva=def_tva.value,
        product=p1,
        tva_object=def_tva,
    )
    line3 = DummyLine(
        cost=10000,
        quantity=1,
        tva=tva.value,
        product=p2,
        tva_object=tva,
    )

    company = Dummy(name="company", code_compta='COMP_CG', contribution=None)
    customer = Dummy(name="customer", compte_tiers="CUSTOMER", compte_cg='CG_CUSTOMER')
    invoice = TaskCompute()
    invoice.default_tva = def_tva.value
    invoice.expenses_tva = def_tva.value
    invoice.taskDate = datetime.date(2013, 02, 02)
    invoice.customer = customer
    invoice.company = company
    invoice.officialNumber = "INV_001"
    invoice.lines = [line1, line2, line3]
    invoice.expenses_ht = 10000
    invoice.expenses = 10000
    return invoice


@pytest.fixture
def invoice_discount(def_tva, tva, invoice):
    discount1 = DummyLine(
        cost=10000,
        quantity=1,
        tva=def_tva.value,
        tva_object=def_tva
    )
    discount2 = DummyLine(
        cost=10000,
        quantity=1,
        tva=tva.value,
        tva_object=tva
    )
    invoice.discounts = [discount1, discount2]
    return invoice


@pytest.fixture
def sageinvoice(def_tva, invoice):
    return SageInvoice(
        invoice=invoice,
        config=get_config(),
        default_tva=def_tva,
    )

@pytest.fixture
def sageinvoice_discount(def_tva, invoice_discount):
    return SageInvoice(
        invoice=invoice_discount,
        config=get_config(),
        default_tva=def_tva
    )


def prepare(discount=False):
    tva1 = MagicMock(name="tva1", value=1960, default=0,
            compte_cg="TVA0001", code='CTVA0001')
    tva2 = MagicMock(
        name="tva2",
        value=700,
        default=0,
        compte_cg="TVA0002",
        code='CTVA0002'
    )

    p1 = MagicMock(name="product 1", compte_cg="P0001", tva=tva1)
    p2 = MagicMock(name="product 2", compte_cg="P0002", tva=tva2)

    line1 = DummyLine(cost=10000, quantity=1, tva=tva1.value, product=p1,
            tva_object=tva1)
    line2 = DummyLine(cost=10000, quantity=1, tva=tva1.value, product=p1,
            tva_object=tva1)
    line3 = DummyLine(cost=10000, quantity=1, tva=tva2.value, product=p2,
            tva_object=tva2)

    company = Dummy(name="company", code_compta='COMP_CG', contribution=None)
    customer = Dummy(name="customer", compte_tiers="CUSTOMER", compte_cg='CG_CUSTOMER')
    invoice = TaskCompute()
    invoice.default_tva = 1960
    invoice.expenses_tva = 1960
    invoice.taskDate = datetime.date(2013, 02, 02)
    invoice.customer = customer
    invoice.company = company
    invoice.officialNumber = "INV_001"
    invoice.lines = [line1, line2, line3]

    if discount:
        discount1 = DummyLine(cost=10000, quantity=1, tva=tva1.value,
                tva_object=tva1)
        discount2 = DummyLine(cost=10000, quantity=1, tva=tva2.value,
                tva_object=tva2)
        invoice.discounts = [discount1, discount2]

    invoice.expenses_ht = 10000
    invoice.expenses = 10000

    return ((tva1, tva2), (p1, p2), invoice)


def test_get_products(sageinvoice):
    sageinvoice.products['1'] = {'test_key':'test'}
    assert sageinvoice.get_product('1', 'dontcare', 'dontcare').has_key('test_key')
    assert len(sageinvoice.get_product('2', 'tva_compte_cg', 'tva_code').keys()) == 3

def test_populate_invoice_lines(sageinvoice):
    sageinvoice._populate_invoice_lines()
    sageinvoice._round_products()
    assert sageinvoice.products.keys() == ['P0001', 'P0002']
    assert sageinvoice.products['P0001']['ht'] == 20000
    assert sageinvoice.products['P0001']['tva'] == 3920
    assert sageinvoice.products['P0002']['ht'] == 10000
    assert sageinvoice.products['P0002']['tva'] == 700

def test_populate_discount_lines(sageinvoice_discount):
    sageinvoice_discount._populate_discounts()
    sageinvoice_discount._round_products()
    assert sageinvoice_discount.products.keys() == ['CG_RRR']
    assert sageinvoice_discount.products['CG_RRR']['code_tva'] == "CODE_TVA_RRR"
    assert sageinvoice_discount.products['CG_RRR']['compte_cg_tva'] == "CG_TVA_RRR"
    assert sageinvoice_discount.products['CG_RRR']['ht'] == 20000
    assert sageinvoice_discount.products['CG_RRR']['tva'] == 2660


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

def test_populate_expenses(sageinvoice):
    sageinvoice.expense_tva_compte_cg = "TVA0001"
    sageinvoice._populate_expenses()
    sageinvoice._round_products()
    assert sageinvoice.products.keys() == ['CG_FA']
    assert sageinvoice.products['CG_FA']['ht'] == 20000
    assert sageinvoice.products['CG_FA']['tva'] == 1960


class BaseBookEntryTest():
    factory = None

    def _test_product_book_entry(
            self,
            wrapped_invoice,
            method,
            exp_analytic_line,
            prod_cg='P0001'):
        """
        test a book_entry output (one of a product)
        """
        config = get_config()
        wrapped_invoice.populate()
        book_entry_factory = self.factory(config)
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

    def _test_invoice_book_entry(self, wrapped_invoice, method, exp_analytic_line):
        """
        test a book_entry output (one of a product)
        """
        config = get_config()
        wrapped_invoice.populate()
        book_entry_factory = self.factory(config)
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
    return {'type_': 'A', 'key': 'value', 'num_analytique':'NUM'}


def test_double_lines():
    res = list(double_lines(decoratorfunc)(None, None))
    assert res == [
        {'type_': 'G', 'key': 'value'},
        {'type_': 'A', 'key': 'value', 'num_analytique':'NUM'}
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

    def test_credit_totalht(self, sageinvoice):
        res = {'libelle': 'customer company',
            'compte_cg': 'P0001',
            'num_analytique': 'COMP_CG',
            'code_tva': 'CTVA0001',
            'credit': 20000}
        method = "credit_totalht"
        self._test_product_book_entry(sageinvoice, method, res)

    def test_credit_tva(self, sageinvoice):
        res = {'libelle': 'customer company',
            'compte_cg': 'TVA0001',
            'num_analytique': 'COMP_CG',
            'code_tva': 'CTVA0001',
            'credit': 3920}
        method = "credit_tva"
        self._test_product_book_entry(sageinvoice, method, res)

        # Ref bug #30


    def test_debit_ttc(self, sageinvoice):
        method = "debit_ttc"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CUSTOMER',
            'num_analytique': 'COMP_CG',
            'compte_tiers': 'CUSTOMER',
            'debit': 23920,
            'echeance': '040313'}
        self._test_product_book_entry(sageinvoice, method, res)


class TestSageContribution(BaseBookEntryTest):
    factory = SageContribution

    def test_debit_entreprise(self, sageinvoice):
        method = "debit_entreprise"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CONTRIB',
            'num_analytique': 'COMP_CG',
            'debit':2000}
        self._test_product_book_entry(sageinvoice, method, res)

    def test_credit_entreprise(self, sageinvoice):
        method = "credit_entreprise"
        res = {'libelle': 'customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'COMP_CG',
            'credit':2000}
        self._test_product_book_entry(sageinvoice, method, res)

    def test_debit_cae(self, sageinvoice):
        method = "debit_cae"
        res = {'libelle': 'customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'NUM_ANA',
            'debit':2000}
        self._test_product_book_entry(sageinvoice, method, res)

    def test_credit_cae(self, sageinvoice):
        method = "credit_cae"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CONTRIB',
            'num_analytique': 'NUM_ANA',
            'credit':2000}
        self._test_product_book_entry(sageinvoice, method, res)


class TestSageAssurance(BaseBookEntryTest):
    # Amount = 2000 0.05 * somme des ht des lignes + expense_ht
    factory = SageAssurance

    def test_debit_entreprise(self, sageinvoice):
        method = 'debit_entreprise'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_ASSUR',
                'num_analytique': 'COMP_CG',
                'debit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)

    def test_credit_entreprise(self, sageinvoice):
        method = 'credit_entreprise'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'BANK_CG',
                'num_analytique': 'COMP_CG',
                'credit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)

    def test_debit_cae(self, sageinvoice):
        method = 'debit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'BANK_CG',
                'num_analytique': 'NUM_ANA',
                'debit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)

    def test_credit_cae(self, sageinvoice):
        method = 'credit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_ASSUR',
                'num_analytique': 'NUM_ANA',
                'credit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)


class TestSageCGScop(BaseBookEntryTest):
    factory = SageCGScop

    def test_debit_entreprise(self, sageinvoice):
        method = 'debit_entreprise'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_SCOP',
                'num_analytique': 'COMP_CG',
                'debit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)

    def test_credit_entreprise(self, sageinvoice):
        method = 'credit_entreprise'
        res = {
                'libelle': 'customer company',
                'num_analytique': 'COMP_CG',
                'compte_cg': 'BANK_CG',
                'credit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)

    def test_debit_cae(self, sageinvoice):
        method = 'debit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'BANK_CG',
                'num_analytique': 'NUM_ANA',
                'debit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)

    def test_credit_cae(self, sageinvoice):
        method = 'credit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_DEB',
                'num_analytique': 'NUM_ANA',
                'credit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)


class TestSageContributionOrganic(BaseBookEntryTest):
    factory = SageContributionOrganic

    libelle = 'Contribution Organic customer company'

    def test_debit_entreprise(self, sageinvoice):
        method = 'debit_entreprise'
        res = {
                'libelle': self.libelle,
                'compte_cg': 'CG_ORGA',
                'num_analytique': 'COMP_CG',
                'debit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)

    def test_credit_entreprise(self, sageinvoice):
        method = 'credit_entreprise'
        res = {
                'libelle': self.libelle,
                'num_analytique': 'COMP_CG',
                'compte_cg': 'BANK_CG',
                'credit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)

    def test_debit_cae(self, sageinvoice):
        method = 'debit_cae'
        res = {
                'libelle': self.libelle,
                'compte_cg': 'BANK_CG',
                'num_analytique': 'NUM_ANA',
                'debit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)

    def test_credit_cae(self, sageinvoice):
        method = 'credit_cae'
        res = {
                'libelle': self.libelle,
                'compte_cg': 'CG_DEB_ORGA',
                'num_analytique': 'NUM_ANA',
                'credit': 2000,
                }
        self._test_invoice_book_entry(sageinvoice, method, res)


class TestSageRGInterne(BaseBookEntryTest):
    factory = SageRGInterne

    def test_debit_entreprise(self, sageinvoice):
        method = "debit_entreprise"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'CG_RG_INT',
            'num_analytique': 'COMP_CG',
            'debit':1196}
        self._test_product_book_entry(sageinvoice, method, res)

    def test_credit_entreprise(self, sageinvoice):
        method = "credit_entreprise"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'COMP_CG',
            'credit':1196}
        self._test_product_book_entry(sageinvoice, method, res)

    def test_debit_cae(self, sageinvoice):
        method = "debit_cae"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'NUM_ANA',
            'debit':1196}
        self._test_product_book_entry(sageinvoice, method, res)

    def test_credit_cae(self, sageinvoice):
        method = "credit_cae"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'CG_RG_INT',
            'num_analytique': 'NUM_ANA',
            'credit':1196}
        self._test_product_book_entry(sageinvoice, method, res)


class TestSageRGClient(BaseBookEntryTest):
    factory = SageRGClient

    def test_debit_entreprise(self, sageinvoice):
        method = 'debit_entreprise'
        res = {
                'libelle': 'RG customer company',
                'compte_cg': 'CG_RG_EXT',
                'num_analytique': 'COMP_CG',
                'echeance':'020214',
                'debit': 1196,
                }
        self._test_product_book_entry(sageinvoice, method, res)

    def test_credit_entreprise(self, sageinvoice):
        method = 'credit_entreprise'
        res = {
                'libelle': 'RG customer company',
                'num_analytique': 'COMP_CG',
                'compte_cg': 'CG_CUSTOMER',
                'compte_tiers': 'CUSTOMER',
                'echeance':'020214',
                'credit': 1196,
                }
        self._test_product_book_entry(sageinvoice, method, res)


class TestSageExport():
    def test_modules(self):
        config = {'sage_contribution':'1',
                'sage_assurance':'1',
                'sage_cgscop':'0'}
        exporter = InvoiceExport(config)
        assert len(exporter.modules) == 3
        sage_factories = [SageFacturation, SageContribution, SageAssurance]
        for fact in sage_factories:
            assert True in [isinstance(module, fact)
                for module in exporter.modules]


@pytest.mark.expense
class TestSageExpenseMain():
    """
    Main Expense export module testing
    """
    def get_factory(self):
        """
        Return an instance of the book entry factory we are testing
        """
        factory = SageExpenseMain(get_config())
        factory.set_expense(self.get_base_expense())
        return factory

    def get_base_expense(self):
        company = MagicMock(code_compta="COMP_ANA")
        user = MagicMock(
            firstname="firstname",
            lastname="lastname",
            compte_tiers="COMP_TIERS",
            )

        return MagicMock(
                company=company,
                user=user,
                month=5,
                year=2014,
                date=datetime.date.today(),
                )

    def get_type_obj(self, contrib=True):
        return MagicMock(
                code='ETYPE1',
                code_tva='CODETVA',
                compte_tva='COMPTETVA',
                contribution=contrib,
                )

    def test_base_entry(self):
        factory = self.get_factory()
        assert factory.libelle == "Firstname LASTNAME/frais 5 2014"
        assert factory.num_feuille == "ndf52014"
        assert factory.code_journal == "JOURNALNDF"

        base_entry = factory.get_base_entry()
        for i in ('code_journal', 'date', 'libelle', 'num_feuille', 'type_'):
            assert i in base_entry

    def test_credit(self):
        factory = self.get_factory()
        general, analytic = factory._credit(2500)
        assert analytic['type_'] == 'A'
        assert analytic['credit'] == 2500
        assert analytic['compte_cg'] == "CGNDF"
        assert analytic['num_analytique'] == "COMP_ANA"
        assert analytic['compte_tiers'] == "COMP_TIERS"

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()


    def test_debit_ht(self):
        tobj = self.get_type_obj()
        factory = self.get_factory()
        general, analytic = factory._debit_ht(tobj, 150)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "ETYPE1"
        assert analytic['num_analytique'] == 'COMP_ANA'
        assert analytic['code_tva'] == 'CODETVA'
        assert analytic['debit'] == 150

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()

    def test_debit_tva(self):
        tobj = self.get_type_obj()
        factory = self.get_factory()
        general, analytic = factory._debit_tva(tobj, 120)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "COMPTETVA"
        assert analytic['num_analytique'] == 'COMP_ANA'
        assert analytic['code_tva'] == 'CODETVA'
        assert analytic['debit'] == 120

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()

    def test_credit_entreprise(self):
        tobj = self.get_type_obj()
        factory = self.get_factory()
        general, analytic = factory._credit_entreprise(120)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "CG_CONTRIB"
        assert analytic['num_analytique'] == 'COMP_ANA'
        assert analytic['credit'] == 120

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()

    def test_debit_entreprise(self):
        tobj = self.get_type_obj()
        factory = self.get_factory()
        general, analytic = factory._debit_entreprise(120)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "BANK_CG"
        assert analytic['num_analytique'] == 'COMP_ANA'
        assert analytic['debit'] == 120

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()

    def test_credit_cae(self):
        tobj = self.get_type_obj()
        factory = self.get_factory()
        general, analytic = factory._credit_cae(120)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "BANK_CG"
        assert analytic['num_analytique'] == 'NUM_ANA'
        assert analytic['credit'] == 120

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()

    def test_debit_cae(self):
        tobj = self.get_type_obj()
        factory = self.get_factory()
        general, analytic = factory._debit_cae(120)

        assert analytic['type_'] == 'A'
        assert analytic['compte_cg'] == "CG_CONTRIB"
        assert analytic['num_analytique'] == 'NUM_ANA'
        assert analytic['debit'] == 120

        assert general['type_'] == 'G'
        assert 'num_analytique' not in general.keys()
