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
        SageRGInterne,
        SageRGClient,
        SageExport,
        )

from autonomie.tests.base import BaseTestCase


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
            'contribution_cae': "10"
            }

def prepare(discount=False):
    tva1 = MagicMock(name="tva1", value=1960, default=0,
            compte_cg="TVA0001", code='CTVA0001')
    tva2 = MagicMock(name="tva2", value=700, default=0,
            compte_cg="TVA0002", code='CTVA0002')

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



class TestSageInvoice(BaseTestCase):
    """
        test Sage Invoice wrapper that group lines by products
    """
    def test_get_products(self):
        obj = SageInvoice(invoice=MagicMock())
        obj.products['1'] = {'test_key':'test'}
        self.assertTrue(
                obj.get_product('1', 'dontcare', 'dontcare').has_key('test_key'))
        self.assertEqual(len(obj.get_product('2', 'tva_compte_cg',
            'tva_code').keys()), 3)

    def test_populate_invoice_lines(self):
        tvas, products, invoice = prepare()
        wrapper = SageInvoice(invoice=invoice)
        wrapper._populate_invoice_lines()
        wrapper._round_products()
        self.assertEqual(wrapper.products.keys(), ['P0001', 'P0002'])
        self.assertEqual(wrapper.products['P0001']['ht'], 20000)
        self.assertEqual(wrapper.products['P0001']['tva'], 3920)
        self.assertEqual(wrapper.products['P0002']['ht'], 10000)
        self.assertEqual(wrapper.products['P0002']['tva'], 700)

    def test_populate_discount_lines(self):
        tvas, products, invoice = prepare(discount=True)
        wrapper = SageInvoice(invoice=invoice, compte_cgs=get_config())
        wrapper._populate_discounts()
        wrapper._round_products()
        self.assertEqual(wrapper.products.keys(), ['CG_RRR'])
        self.assertEqual(
                wrapper.products['CG_RRR']['code_tva'],
                "CODE_TVA_RRR")
        self.assertEqual(
                wrapper.products['CG_RRR']['compte_cg_tva'],
                "CG_TVA_RRR")
        self.assertEqual(wrapper.products['CG_RRR']['ht'], 20000)
        self.assertEqual(wrapper.products['CG_RRR']['tva'], 2660)

        # If one of compte_cg_tva_rrr or code_tva_rrr is not def
        # No entry should be returned
        config = get_config()
        config.pop("compte_cg_tva_rrr")
        wrapper = SageInvoice(invoice=invoice, compte_cgs=config)
        wrapper._populate_discounts()
        self.assertEqual(wrapper.products.keys(), [])

        config = get_config()
        config.pop("code_tva_rrr")
        wrapper = SageInvoice(invoice=invoice, compte_cgs=config)
        wrapper._populate_discounts()
        self.assertEqual(wrapper.products.keys(), [])



    def test_populate_expenses(self):
        tvas, products, invoice = prepare()
        wrapper = SageInvoice(invoice=invoice, compte_cgs=get_config())
        wrapper.expense_tva_compte_cg = "TVA0001"
        wrapper._populate_expenses()
        wrapper._round_products()
        self.assertEqual(wrapper.products.keys(), ['CG_FA'])
        self.assertEqual(wrapper.products['CG_FA']['ht'], 20000)
        self.assertEqual(wrapper.products['CG_FA']['tva'], 1960)

class BaseBookEntryTest(BaseTestCase):
    factory = None

    def _test_product_book_entry(
            self,
            method,
            exp_analytic_line,
            prod_cg='P0001'):
        """
        test a book_entry output (one of a product)
        """
        tvas, products, invoice = prepare()
        config = get_config()
        wrapped_invoice = SageInvoice(invoice=invoice, compte_cgs=config)
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

        self.assertEqual(general_line, exp_general_line)
        self.assertEqual(analytic_line, exp_analytic_line)

    def _test_invoice_book_entry(self, method, exp_analytic_line):
        """
        test a book_entry output (one of a product)
        """
        tvas, products, invoice = prepare()
        config = get_config()
        wrapped_invoice = SageInvoice(invoice=invoice, compte_cgs=config)
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

        self.assertEqual(general_line, exp_general_line)
        self.assertEqual(analytic_line, exp_analytic_line)


def decoratorfunc(a, b):
    return {'type_': 'A', 'key': 'value', 'num_analytique':'NUM'}


class Testmain(BaseTestCase):
    def test_double_lines(self):
        res = list(double_lines(decoratorfunc)(None, None))
        self.assertEqual(res, [
            {'type_': 'G', 'key': 'value'},
            {'type_': 'A', 'key': 'value', 'num_analytique':'NUM'}
            ])


class TestSageFacturation(BaseBookEntryTest):
    factory = SageFacturation

    def test_credit_totalht(self):
        res = {'libelle': 'customer company',
            'compte_cg': 'P0001',
            'num_analytique': 'COMP_CG',
            'code_tva': 'CTVA0001',
            'credit': 20000}
        method = "credit_totalht"
        self._test_product_book_entry(method, res)

    def test_credit_tva(self):
        res = {'libelle': 'customer company',
            'compte_cg': 'TVA0001',
            'num_analytique': 'COMP_CG',
            'code_tva': 'CTVA0001',
            'credit': 3920}
        method = "credit_tva"
        self._test_product_book_entry(method, res)

    def test_debit_ttc(self):
        method = "debit_ttc"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CUSTOMER',
            'num_analytique': 'COMP_CG',
            'compte_tiers': 'CUSTOMER',
            'debit': 23920,
            'echeance': '040313'}
        self._test_product_book_entry(method, res)


class TestSageContribution(BaseBookEntryTest):
    factory = SageContribution

    def test_debit_entreprise(self):
        method = "debit_entreprise"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CONTRIB',
            'num_analytique': 'COMP_CG',
            'debit':2000}
        self._test_product_book_entry(method, res)

    def test_credit_entreprise(self):
        method = "credit_entreprise"
        res = {'libelle': 'customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'COMP_CG',
            'credit':2000}
        self._test_product_book_entry(method, res)

    def test_debit_cae(self):
        method = "debit_cae"
        res = {'libelle': 'customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'NUM_ANA',
            'debit':2000}
        self._test_product_book_entry(method, res)

    def test_credit_cae(self):
        method = "credit_cae"
        res = {'libelle': 'customer company',
            'compte_cg': 'CG_CONTRIB',
            'num_analytique': 'NUM_ANA',
            'credit':2000}
        self._test_product_book_entry(method, res)


class TestSageAssurance(BaseBookEntryTest):
    # Amount = 2000 0.05 * somme des ht des lignes + expense_ht
    factory = SageAssurance

    def test_debit_entreprise(self):
        method = 'debit_entreprise'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_ASSUR',
                'num_analytique': 'COMP_CG',
                'debit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_credit_entreprise(self):
        method = 'credit_entreprise'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'BANK_CG',
                'num_analytique': 'COMP_CG',
                'credit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_debit_cae(self):
        method = 'debit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'BANK_CG',
                'num_analytique': 'NUM_ANA',
                'debit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_credit_cae(self):
        method = 'credit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_ASSUR',
                'num_analytique': 'NUM_ANA',
                'credit': 2000,
                }
        self._test_invoice_book_entry(method, res)


class TestSageCGScop(BaseBookEntryTest):
    factory = SageCGScop

    def test_debit_entreprise(self):
        method = 'debit_entreprise'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_SCOP',
                'num_analytique': 'COMP_CG',
                'debit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_credit_entreprise(self):
        method = 'credit_entreprise'
        res = {
                'libelle': 'customer company',
                'num_analytique': 'COMP_CG',
                'compte_cg': 'BANK_CG',
                'credit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_debit_cae(self):
        method = 'debit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'BANK_CG',
                'num_analytique': 'NUM_ANA',
                'debit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_credit_cae(self):
        method = 'credit_cae'
        res = {
                'libelle': 'customer company',
                'compte_cg': 'CG_DEB',
                'num_analytique': 'NUM_ANA',
                'credit': 2000,
                }
        self._test_invoice_book_entry(method, res)


class TestSageRGInterne(BaseBookEntryTest):
    factory = SageRGInterne

    def test_debit_entreprise(self):
        method = "debit_entreprise"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'CG_RG_INT',
            'num_analytique': 'COMP_CG',
            'debit':1196}
        self._test_product_book_entry(method, res)

    def test_credit_entreprise(self):
        method = "credit_entreprise"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'COMP_CG',
            'credit':1196}
        self._test_product_book_entry(method, res)

    def test_debit_cae(self):
        method = "debit_cae"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'BANK_CG',
            'num_analytique': 'NUM_ANA',
            'debit':1196}
        self._test_product_book_entry(method, res)

    def test_credit_cae(self):
        method = "credit_cae"
        res = {'libelle': 'RG COOP customer company',
            'compte_cg': 'CG_RG_INT',
            'num_analytique': 'NUM_ANA',
            'credit':1196}
        self._test_product_book_entry(method, res)


class TestSageRGClient(BaseBookEntryTest):
    factory = SageRGClient

    def test_debit_entreprise(self):
        method = 'debit_entreprise'
        res = {
                'libelle': 'RG customer company',
                'compte_cg': 'CG_RG_EXT',
                'num_analytique': 'COMP_CG',
                'echeance':'020214',
                'debit': 1196,
                }
        self._test_product_book_entry(method, res)

    def test_credit_entreprise(self):
        method = 'credit_entreprise'
        res = {
                'libelle': 'RG customer company',
                'num_analytique': 'COMP_CG',
                'compte_cg': 'CG_CUSTOMER',
                'compte_tiers': 'CUSTOMER',
                'echeance':'020214',
                'credit': 1196,
                }
        self._test_product_book_entry(method, res)


class TestSageExport(BaseTestCase):
    def test_modules(self):
        config = {'sage_contribution':'1',
                'sage_assurance':'1',
                'sage_cgscop':'0'}
        exporter = SageExport(config)
        self.assertEqual(len(exporter.modules), 3)
        sage_factories = [SageFacturation, SageContribution, SageAssurance]
        for fact in sage_factories:
            self.assertTrue(True in [isinstance(module, fact)
                for module in exporter.modules])
